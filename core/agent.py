# core/agent.py
from typing import TypedDict, Annotated, Sequence
from operator import add as add_messages
from langgraph.graph import StateGraph, END
from langchain_core.messages import BaseMessage, SystemMessage, ToolMessage
from core.llm import llm
from tools import all_tools  # <-- Scalable import of all tools
from util.config import SYSTEM_PROMPT


# --- Agent State and Graph Definition ---
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


# Bind the tools to the LLM
llm_with_tools = llm.bind_tools(all_tools)
tools_dict = {t.name: t for t in all_tools}


# --- Agent Nodes ---
def call_llm(state: AgentState) -> AgentState:
    """Function to call the LLM with the current state."""
    print("Calling LLM...")
    # Add the system prompt only if it's the first message
    messages = [SystemMessage(content=SYSTEM_PROMPT)] + list(state["messages"])
    response = llm_with_tools.invoke(messages)
    print(f"LLM Response: {response.content}")
    if hasattr(response, "tool_calls"):
        print(f"Tool calls: {response.tool_calls}")
    return {"messages": [response]}


def take_action(state: AgentState) -> AgentState:
    """Execute tool calls from the LLM's response."""
    print("Taking action (executing tools)...")
    tool_calls = state["messages"][-1].tool_calls
    results = []
    for t in tool_calls:
        print(f"Tool call detected: name={t['name']}, args={t['args']}")
        if t["name"] not in tools_dict:
            result = "Incorrect Tool Name, Please Retry and Select tool from List of Available tools."
        else:
            print(f"Executing tool: {t['name']} with args: {t['args']}")
            result = tools_dict[t["name"]].invoke(t["args"])

        results.append(
            ToolMessage(tool_call_id=t["id"], name=t["name"], content=str(result))
        )
    print("Tools Execution Complete. Returning results to LLM.")
    return {"messages": results}


def should_continue(state: AgentState) -> str:
    """Check if the last message contains tool calls."""
    last_message = state["messages"][-1]
    return (
        "retriever_agent"
        if hasattr(last_message, "tool_calls") and last_message.tool_calls
        else END
    )


# --- Graph Construction ---
graph = StateGraph(AgentState)
graph.add_node("llm", call_llm)
graph.add_node("retriever_agent", take_action)
graph.add_conditional_edges(
    "llm", should_continue, {"retriever_agent": "retriever_agent", END: END}
)
graph.add_edge("retriever_agent", "llm")
graph.set_entry_point("llm")

rag_agent = graph.compile()
print("RAG Agent compiled and ready.")
