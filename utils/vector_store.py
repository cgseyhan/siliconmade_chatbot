import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# Load .env file
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), ".env")
load_dotenv(env_path)

# Settings
DB_DIR = os.path.join(os.path.dirname(current_dir), "chroma_db")
KNOWLEDGE_FILE = os.path.join(os.path.dirname(current_dir), "data_ingestion", "knowledge_base.txt")

# Lazy load embeddings
_embeddings = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        key = os.getenv("OPENAI_API_KEY") or "dummy"
        _embeddings = OpenAIEmbeddings(model="text-embedding-3-small", openai_api_key=key)
    return _embeddings

def is_api_key_valid():
    """
    Checks if the OpenAI API Key is set and is not the placeholder dummy key.
    """
    key = os.getenv("OPENAI_API_KEY")
    return bool(key and key.strip() and key != "dummy")

def initialize_vector_db():
    """
    Reads the knowledge base file, chunks it, and builds/updates the vector database.
    """
    if not is_api_key_valid():
        print("WARNING: OPENAI_API_KEY is not set or invalid. Skipping vector database initialization.")
        return None

    if not os.path.exists(KNOWLEDGE_FILE):
        print(f"ERROR: Knowledge base file not found: {KNOWLEDGE_FILE}")
        return None

    try:
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            text = f.read()

        # Split text into meaningful chunks (1000 characters chunk size with 200 overlap)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.create_documents([text])

        # Create ChromaDB
        vector_db = Chroma.from_documents(
            documents=docs,
            embedding=get_embeddings(),
            persist_directory=DB_DIR
        )
        print(f"DEBUG: Vector database successfully created/updated. ({len(docs)} chunks)")
        return vector_db
    except Exception as e:
        print(f"ERROR: Failed to initialize vector database: {e}")
        return None

def reindex_from_text(text: str):
    """
    Splits the provided metin chunk, resets, and rebuilds the vector database.
    """
    if not is_api_key_valid():
        print("WARNING: OPENAI_API_KEY is not set or invalid. Skipping reindexing.")
        return None

    try:
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        docs = text_splitter.create_documents([text])

        import shutil
        if os.path.exists(DB_DIR):
            try:
                shutil.rmtree(DB_DIR)
            except Exception as e:
                print(f"DEBUG: Could not delete old database: {e}")

        vector_db = Chroma.from_documents(
            documents=docs,
            embedding=get_embeddings(),
            persist_directory=DB_DIR
        )
        print(f"DEBUG: Vector database reindexed with dynamic text. ({len(docs)} chunks)")
        return vector_db
    except Exception as e:
        print(f"ERROR: Failed to reindex vector database: {e}")
        return None

def get_vector_db():
    """
    Connects to the existing vector database.
    """
    if not is_api_key_valid():
        return None

    if not os.path.exists(DB_DIR):
        return initialize_vector_db()
    
    try:
        return Chroma(persist_directory=DB_DIR, embedding_function=get_embeddings())
    except Exception as e:
        print(f"ERROR: Failed to load vector database: {e}")
        return None

def query_vector_db(query: str, k: int = 3):
    """
    Retrieves the closest context to the given query.
    """
    if not is_api_key_valid():
        print("WARNING: OPENAI_API_KEY is not set or invalid. Skipping vector search.")
        return ""

    db = get_vector_db()
    if not db:
        return ""
    
    try:
        results = db.similarity_search(query, k=k)
        context = "\n\n".join([doc.page_content for doc in results])
        return context
    except Exception as e:
        print(f"WARNING: Vector search failed: {e}")
        return ""

if __name__ == "__main__":
    # Test execution
    if is_api_key_valid():
        initialize_vector_db()
        print("Test search (Java):")
        print(query_vector_db("What is the content of the Java course?"))
    else:
        print("Skipping tests as OPENAI_API_KEY is not configured.")
