# Gerekli kütüphaneler
import os                                                                      # Ortam değişkenlerini ve dosya yollarını kullanmak için
from chatbot.llama import LlamaChatbot                                         # LLaMA tabanlı yerel chatbot sınıfı
from chatbot.openai import chat_with_openai                                    # OpenAI tabanlı chatbot fonksiyonu
from utils.json_logger import log_interaction                                  # JSON dosyasına kaydetme fonksiyonu
from utils.mysql_logger import log_interaction as log_mysql                    # MySQL veritabanına kaydetme fonksiyonu
from integrations.airtable_integration import log_interaction as log_airtable  # Airtable'a kaydetme fonksiyonu

# Sabit sistem promptu
SYSTEM_PROMPT = "Sen bilgili, yardımsever ve nazik bir yapay zeka satış asistanısın."

# Chatbot'u çalıştıran fonksiyon
def run_chatbot(model_name: str, user_input: str) -> str:                           # Seçilen modele göre kullanıcı girdisini işleyip yanıt döndüren fonksiyon
    if model_name == "LLaMA":                                                       # Eğer LLaMA modeli seçildiyse
        model_path = os.getenv("LLAMA_MODEL_PATH", "models/aya-23-8B-Q4_K_M.gguf")  # Model yolunu ortam değişkeninden veya varsayılan yoldan al
        chatbot = LlamaChatbot(model_path)                                          # LLaMA chatbot örneğini oluştur
        response = chatbot.chat(SYSTEM_PROMPT, user_input)                          # Kullanıcı girdisine yanıt üret
    elif model_name == "ChatGPT-4o":                                                # Eğer ChatGPT-4o modeli seçildiyse
        response = chat_with_openai(SYSTEM_PROMPT, user_input)                      # OpenAI modelinden yanıt al

    # Yanıtı kaydet
    log_interaction(user_input, response, model_name) # JSON dosyasına kaydet
    log_mysql(user_input, response, model_name)       # MySQL veritabanına kaydet
    log_airtable(user_input, response, model_name)    # Airtable'a kaydet
    return response                                   # Kullanıcıya yanıtı döndür
