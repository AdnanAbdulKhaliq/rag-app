# core/llm.py
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from util.config import (
    GOOGLE_API_KEY,
    LLM_MODEL_NAME,
    EMBEDDING_MODEL_NAME,
    LLM_TEMPERATURE,
)


try:
    # Initialize the LLM for chat generation
    llm = ChatGoogleGenerativeAI(
        model=LLM_MODEL_NAME,
        google_api_key=GOOGLE_API_KEY,
        temperature=LLM_TEMPERATURE,
        convert_system_message_to_human=True,  # Often helps with tool use
    )

    # Initialize the embeddings model
    embeddings = GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL_NAME, google_api_key=GOOGLE_API_KEY
    )
    print("LLM and Embeddings models initialized successfully.")
except Exception as e:
    print(f"Error initializing Google AI models: {e}")
    raise
