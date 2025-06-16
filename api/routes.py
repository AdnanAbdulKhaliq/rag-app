# api/routes.py
import traceback
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain_core.messages import HumanMessage
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


class Query(BaseModel):
    question: str


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
        messages = [HumanMessage(content=query.question)]
        result = rag_agent.invoke({"messages": messages})

        final_answer = result["messages"][-1].content
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
