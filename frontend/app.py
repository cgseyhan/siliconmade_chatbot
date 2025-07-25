# Gerekli kütüphaneler
import streamlit as st                       # Streamlit arayüzü
from chatbot.llama import LlamaChatbot       # LLaMA tabanlı yerel model
from chatbot.openai import chat_with_openai  # OpenAI tabanlı model fonksiyonu
import os                                    # Ortam değişkenleri ve dosya yolları

# Tüm modeller için ortak kullanılacak sistem promptu
SYSTEM_PROMPT = "Sen bilgili, yardımsever ve nazik bir yapay zeka satış asistanısın."

# Model seçimi için bir açılır menü
MODEL_TYPE = st.sidebar.selectbox("Model Seçimi", ["LLaMA", "ChatGPT-4o"])

# Uygulama başlığı
st.title("Chatbot")

# Kullanıcıdan metin girdisi alınır
user_input = st.text_input("Kullanıcı Girdisi")

# "Gönder" butonuna basıldığında işlem başlar
if st.button("Gönder"):
    # Seçilen model LLaMA ise
    if MODEL_TYPE == "LLaMA":
        # Ortam değişkeninden model yolu alınır, tanımlı değilse varsayılan yol kullanılır
        model_path = os.getenv("LLAMA_MODEL_PATH", "models/aya-23-8B-Q4_K_M.gguf")
        # LlamaChatbot sınıfı ile model örneği oluşturulur
        chatbot = LlamaChatbot(model_path)
        # Kullanıcı girdisiyle modelden yanıt alınır
        response = chatbot.chat(SYSTEM_PROMPT, user_input)
    else:
        # OpenAI tabanlı modelden yanıt alınır
        response = chat_with_openai(SYSTEM_PROMPT, user_input)

    st.markdown("**Yanıt:**")
    st.success(response)