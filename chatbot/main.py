# Gerekli kütüphaneler
import os                                    # Ortam değişkenlerini ve dosya yollarını kullanmak için
from chatbot.llama import LlamaChatbot       # LLaMA tabanlı yerel chatbot sınıfı
from chatbot.openai import chat_with_openai  # OpenAI tabanlı chatbot fonksiyonu

# Sabit sistem promptu — her iki model için ortak başlangıç mesajı
SYSTEM_PROMPT = "Sen bilgili, yardımsever ve nazik bir yapay zeka satış asistanısın."

# Chatbot'u çalıştıran fonksiyon
def run_chatbot(model_name: str, user_input: str) -> str:

    # Eğer model adı "LLaMA" ise yerel modelle cevap üret
    if model_name == "LLaMA":

        # Ortam değişkeninden model yolu alınır, tanımlı değilse varsayılan model yolu kullanılır
        model_path = os.getenv("LLAMA_MODEL_PATH", "models/aya-23-8B-Q4_K_M.gguf")

        # LlamaChatbot örneği oluşturulur
        chatbot = LlamaChatbot(model_path)

        # Kullanıcının girdisine karşılık modelin yanıtı döndürülür
        return chatbot.chat(SYSTEM_PROMPT, user_input)

    # Eğer model adı ChatGPT-4o ise OpenAI API'ı kullanılarak cevap üretilir
    elif model_name == "ChatGPT-4o":
        return chat_with_openai(SYSTEM_PROMPT, user_input)