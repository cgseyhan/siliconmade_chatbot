import os
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from dotenv import load_dotenv

# .env dosyasını yükle
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), ".env")
load_dotenv(env_path)

# Ayarlar
DB_DIR = os.path.join(os.path.dirname(current_dir), "chroma_db")
KNOWLEDGE_FILE = os.path.join(os.path.dirname(current_dir), "data_ingestion", "knowledge_base.txt")

# Embedding modelini başlat
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def initialize_vector_db():
    """
    Metin dosyasını okur, parçalar ve vektör veritabanını oluşturur/günceller.
    """
    if not os.path.exists(KNOWLEDGE_FILE):
        print(f"HATA: Bilgi bankası dosyası bulunamadı: {KNOWLEDGE_FILE}")
        return None

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    # Metni anlamlı parçalara böl (1000 karakterlik, 200 karakter çakışmalı)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    docs = text_splitter.create_documents([text])

    # ChromaDB oluştur
    vector_db = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print(f"DEBUG: Vektör veritabanı başarıyla oluşturuldu/güncellendi. ({len(docs)} parça)")
    return vector_db

def get_vector_db():
    """
    Mevcut vektör veritabanına bağlanır.
    """
    if not os.path.exists(DB_DIR):
        return initialize_vector_db()
    
    return Chroma(persist_directory=DB_DIR, embedding_function=embeddings)

def query_vector_db(query: str, k: int = 3):
    """
    Verilen soruya en yakın bilgileri (context) getirir.
    """
    db = get_vector_db()
    if not db:
        return ""
    
    results = db.similarity_search(query, k=k)
    context = "\n\n".join([doc.page_content for doc in results])
    return context

if __name__ == "__main__":
    # Test için çalıştır
    initialize_vector_db()
    print("Test araması (Java):")
    print(query_vector_db("Java kursu içeriği nedir?"))
