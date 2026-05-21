from utils.vector_store import query_vector_db

def get_knowledge_context(query: str) -> str:
    """
    Performs a semantic search using the vector database (ChromaDB).
    """
    try:
        context = query_vector_db(query)
        return context
    except Exception as e:
        print(f"RAG Error: {e}")
        return ""
