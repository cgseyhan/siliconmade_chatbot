from utils.vector_store import query_vector_db

def get_knowledge_context(query: str) -> str:
    """
    Vektör veritabanı kullanarak (ChromaDB) anlamsal arama yapar.
    """
    try:
        context = query_vector_db(query)
        return context
    except Exception as e:
        print(f"RAG Error: {e}")
        return ""
