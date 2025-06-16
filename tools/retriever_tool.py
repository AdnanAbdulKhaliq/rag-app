# tools/retriever_tool.py
from langchain_core.tools import tool
from core.vectorstore import retriever


@tool
def retriever_tool(query: str) -> str:
    """This tool searches and returns the information from the Leave Policy Template document."""
    print(f"Executing retriever tool with query: '{query}'")
    docs = retriever.invoke(query)

    if not docs:
        return "I found no relevant information in the Leave Policy Template document."

    results = []
    for doc in docs:
        source_info = f"Source (Page {doc.metadata.get('page', 'N/A')})"
        results.append(f"Result from {source_info}:\n{doc.page_content}")

    return "\n\n---\n\n".join(results)
