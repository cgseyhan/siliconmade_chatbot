from chatbot.llama import LlamaChatbot
from chatbot.openai import chat_with_openai
from utils.mysql_logger import log_interaction as log_mysql, save_lead, init_db
from integrations.airtable_integration import log_interaction as log_airtable
from utils.lead_extractor import extract_lead_info
from utils.sentiment_analyzer import analyze_sentiment_and_intent
import threading

# Veritabanını başlat
init_db()

from chatbot.prompts import get_system_prompt
from data_ingestion.rag_helper import get_knowledge_context

# Varsayılan sistem mesajını merkezden alıyoruz
SYSTEM_PROMPT = get_system_prompt("sales")

def background_logs(user_input: str, response: str, model_name: str, sentiment: str = "Nötr", intent: str = "Diğer", messages: list = None):
    """
    Loglama ve Lead çıkarma işlemlerini arka planda (thread) çalıştırır.
    """
    # 1. Normal loglama
    try:
        log_mysql(user_input, response, model_name, sentiment, intent)
    except Exception as e:
        print(f"DEBUG: SQLite Log hatası -> {e}")

    try:
        log_airtable(user_input, response, model_name)
    except Exception as e:
        print(f"DEBUG: Airtable Log hatası -> {e}")

    # 2. Lead çıkarma (Eğer mesaj geçmişi varsa)
    if messages:
        try:
            lead_data = extract_lead_info(messages)
            # Eğer en azından bir bilgi (isim, mail veya telefon) bulunduysa kaydet
            if lead_data.get("name") or lead_data.get("email") or lead_data.get("phone"):
                save_lead(
                    name=lead_data.get("name"),
                    email=lead_data.get("email"),
                    phone=lead_data.get("phone"),
                    course=lead_data.get("course"),
                    notes=f"Model: {model_name}"
                )
        except Exception as e:
            print(f"Background Lead Error: {e}")

def run_chatbot(model_name: str, messages: list, image_b64: str = None) -> str:
    """
    Seçilen modele göre tüm mesaj geçmişini işler ve yanıtı döndürür.
    """
    # 1. Son kullanıcı mesajını al ve context bul
    user_input = messages[-1]["content"] if messages else ""
    context = get_knowledge_context(user_input)

    # 2. Mesaj listesinin başına (veya sistem mesajına) context ekle
    enriched_messages = messages.copy()
    
    if context:
        rag_prompt = f"\n\nBİLGİ BANKASI VERİSİ:\n{context}\n\nLütfen yukarıdaki bilgilere dayanarak cevap ver."
        if enriched_messages and enriched_messages[0]["role"] == "system":
            enriched_messages[0] = {
                "role": "system", 
                "content": enriched_messages[0]["content"] + rag_prompt
            }
        else:
            enriched_messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT + rag_prompt})

    # 3. Modeli çalıştır
    sentiment, intent = "Nötr", "Diğer"
    if model_name == "ChatGPT-4o":
        ai_res = chat_with_openai(enriched_messages, image_b64=image_b64)
        response = ai_res.get("answer", "Hata oluştu.")
        sentiment = ai_res.get("sentiment", "Nötr")
        intent = ai_res.get("intent", "Diğer")
    elif model_name == "LLaMA":
        response = LlamaChatbot().chat(enriched_messages)
    else:
        raise ValueError(f"Bilinmeyen model: {model_name}")

    # 4. Loglama işlemlerini arka plana at
    log_thread = threading.Thread(
        target=background_logs, 
        args=(user_input, response, model_name, sentiment, intent, messages)
    )
    log_thread.start()
            
    return response