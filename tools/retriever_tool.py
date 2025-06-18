# tools/retriever_tool.py
from langchain_core.tools import tool
from core.vectorstore import retriever


@tool
def answer_leave_policy_question(query: str) -> str:
    """Use this tool to answer ANY question about the Leave Policy Template document. This is the ONLY way to access information from the document. Always use this tool for document-related questions, no matter how simple or complex."""
    print(f"Executing answer_leave_policy_question tool with query: '{query}'")
    docs = retriever.invoke(query)

    if not docs:
        return "I found no relevant information in the Leave Policy Template document."

    results = []
    for doc in docs:
        source_info = f"Source (Page {doc.metadata.get('page', 'N/A')})"
        results.append(f"Result from {source_info}:\n{doc.page_content}")

    return "\n\n---\n\n".join(results)
