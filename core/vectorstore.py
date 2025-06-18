# core/vectorstore.py
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from core.llm import embeddings
from util.config import (
    PERSIST_DIRECTORY,
    COLLECTION_NAME,
    PDF_PATH,
    RETRIEVER_SEARCH_TYPE,
    RETRIEVER_SEARCH_KWARGS,
)


def get_retriever():
    """
    Creates or loads a Chroma vector store and returns a retriever.
    """
    db_is_ready = (
        os.path.exists(PERSIST_DIRECTORY) and len(os.listdir(PERSIST_DIRECTORY)) > 0
    )

    if db_is_ready:
        print(f"Loading existing ChromaDB vector store from '{PERSIST_DIRECTORY}'!")
        vectorstore = Chroma(
            persist_directory=PERSIST_DIRECTORY,
            embedding_function=embeddings,
            collection_name=COLLECTION_NAME,
        )
    else:
        print(
            f"Database not found. Creating new ChromaDB vector store in '{PERSIST_DIRECTORY}'..."
        )
        if not os.path.exists(PDF_PATH):
            raise FileNotFoundError(f"The PDF file was not found at path: {PDF_PATH}")

        try:
            loader = PyPDFLoader(PDF_PATH)
            pages = loader.load()
            print(f"PDF loaded with {len(pages)} pages.")
            for i, page in enumerate(pages[:3]):
                print(f"Page {i+1} content preview: {page.page_content[:300]}")
        except Exception as e:
            print(f"Error loading PDF: {e}")
            raise

        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200
        )
        pages_split = text_splitter.split_documents(pages)

        vectorstore = Chroma.from_documents(
            documents=pages_split,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY,
            collection_name=COLLECTION_NAME,
        )
        print("Database creation complete.")

    print("Vector store is ready.")
    return vectorstore.as_retriever(
        search_type=RETRIEVER_SEARCH_TYPE,
        search_kwargs=RETRIEVER_SEARCH_KWARGS,
    )


# Initialize the retriever when the module is loaded
retriever = get_retriever()
