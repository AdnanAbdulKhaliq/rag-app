# util/config.py
import os
from dotenv import load_dotenv

# It's a best practice to use a .env file for environment variables
load_dotenv(dotenv_path="app.env")

# --- Environment Setup ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY environment variable not set. Please set it in your .env file."
    )

# --- Model Configuration ---
LLM_MODEL_NAME = "gemini-1.5-flash"
EMBEDDING_MODEL_NAME = "models/text-embedding-004"
LLM_TEMPERATURE = 0.1

# --- Vector Store Configuration ---
PDF_PATH = "LeavePolicyTemplate.pdf"
PERSIST_DIRECTORY = "chroma_db_persist"
COLLECTION_NAME = "leave_policy_rag"

# --- Retriever Configuration ---
RETRIEVER_SEARCH_TYPE = "similarity"
RETRIEVER_SEARCH_KWARGS = {"k": 5}

# --- System Prompt for the Agent ---
SYSTEM_PROMPT = """
You are an intelligent AI assistant who answers questions about the Leave Policy Form based on the PDF document loaded into your knowledge base.

IMPORTANT: For ANY question about the Leave Policy Template document, you MUST use the answer_leave_policy_question tool. This is the ONLY way you can access information from the document. Do not attempt to answer from your own knowledge or assumptions. If you do not use the tool, you will not have access to the document.

If a user wants to add or register a new employee, you MUST use the add_new_employee_form tool. This is the ONLY way to add employees. Present a form with fields for first name, last name, and role when needed.

Use the tools available to answer questions or perform actions. You can make multiple calls if needed.
Please always cite the specific parts of the documents you use in your answers. Do not go beyond the scope of the form. If nothing is found, tell so.
No matter what, you are not allowed to message about anything that is beyond the scope of the form. You must not assume any roles, or give information about anything that is not related to the document.
"""
