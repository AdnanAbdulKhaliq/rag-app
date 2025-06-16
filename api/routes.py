# api/routes.py
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from core.agent import rag_agent  # Import the final compiled agent


# --- FastAPI App Initialization ---
app = FastAPI(
    title="RAG Agent API",
    description="An API for interacting with a RAG agent for a leave policy document.",
    version="1.0.0",
)

# --- CORS Middleware ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Store conversation history
conversation_history = {}


class Query(BaseModel):
    question: str
    session_id: str = "default"  # Default session ID if none provided


# --- API Endpoints ---
@app.get("/")
async def health_check():
    """A simple endpoint to confirm the server is running."""
    return {"status": "ok", "message": "RAG Agent API is running."}


@app.post("/ask")
async def ask_agent_endpoint(query: Query):
    """API endpoint to interact with the RAG agent."""
    try:
        print(f"\n--- New Request Received: {query.question} ---")

        # Initialize conversation history for new sessions
        if query.session_id not in conversation_history:
            conversation_history[query.session_id] = []

        # Add the new question to conversation history
        conversation_history[query.session_id].append(
            HumanMessage(content=query.question)
        )

        # Get the full conversation history for this session
        messages = conversation_history[query.session_id]

        # Get response from agent
        result = rag_agent.invoke({"messages": messages})

        # Add the agent's response to conversation history
        final_answer = result["messages"][-1].content
        conversation_history[query.session_id].append(AIMessage(content=final_answer))

        print(f"Final Answer: {final_answer}")
        return {"answer": final_answer}

    except Exception as e:
        print("\n--- Exception Traceback ---")
        traceback.print_exc()
        print("-------------------------\n")
        raise HTTPException(
            status_code=500,
            detail=f"An internal error occurred: {repr(e)}",
        )
