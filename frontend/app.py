import streamlit as st
from chatbot.main import run_chatbot

SYSTEM_PROMPT = "Sen bilgili, yardımsever ve nazik bir yapay zeka satış asistanısın."
MODEL_TYPE = st.sidebar.selectbox("Model Seçimi", ["LLaMA", "ChatGPT-4o"])

st.title("Chatbot")
user_input = st.text_input("Ne üzerinde çalışıyorsun?", placeholder="Herhangi bir şey sor")

if st.button("Gönder"):
    if user_input.strip():
        response = run_chatbot(MODEL_TYPE, user_input)
        st.markdown("**Yanıt:**")
        st.success(response)
    else:
        st.warning("Lütfen bir metin giriniz.")