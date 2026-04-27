import os
import streamlit as st
import base64
from audio_recorder_streamlit import audio_recorder
from chatbot.main import run_chatbot
from chatbot.speech import transcribe_audio_openai, synthesize_tts_openai
from chatbot.prompts import get_system_prompt
from chatbot.memory import ChatMemory

# ---- Sayfa Ayarları ----
st.set_page_config(
    page_title="Siliconmade AI Assistant",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---- Premium CSS (Glassmorphism & Dark Theme) ----
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
        color: #E0E0E0;
    }

    .stApp {
        background: radial-gradient(circle at top right, #1a1a2e, #16213e, #0f3460);
    }

    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: rgba(15, 52, 96, 0.8) !important;
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }

    /* Message Bubbles */
    .message-row {
        display: flex;
        width: 100%;
        margin-bottom: 1.5rem;
    }

    .user-row { justify-content: flex-end; }
    .bot-row { justify-content: flex-start; }

    .bubble {
        max-width: 75%;
        padding: 1rem 1.5rem;
        border-radius: 1.5rem;
        font-size: 1rem;
        line-height: 1.6;
        position: relative;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .user-bubble {
        background: linear-gradient(135deg, #00d2ff 0%, #3a7bd5 100%);
        color: white;
        border-bottom-right-radius: 0.2rem;
    }

    .bot-bubble {
        background: rgba(255, 255, 255, 0.05);
        color: #f0f0f0;
        border: 1px solid rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(5px);
        border-bottom-left-radius: 0.2rem;
    }

    .avatar {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        margin: 0 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.75rem;
        flex-shrink: 0;
    }

    .user-avatar { background: #3a7bd5; color: white; order: 2; }
    .bot-avatar { background: #0f3460; border: 1px solid #00d2ff; color: #00d2ff; order: 1; }

    /* Input Area Styling */
    .stTextInput input {
        background-color: rgba(255,255,255,0.05) !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        color: white !important;
        border-radius: 12px !important;
        padding: 12px 15px !important;
    }

    .stButton button {
        background: linear-gradient(90deg, #00d2ff 0%, #3a7bd5 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        height: 45px;
    }

    .stButton button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0, 210, 255, 0.4);
    }

    /* Hide Streamlit components */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ---- Sidebar Content ----
with st.sidebar:
    st.image("https://siliconmade.com/wp-content/uploads/2023/11/logo.png", width=200)
    st.markdown("### 🤖 Asistan Ayarları")
    MODEL_TYPE = st.selectbox("Model Seçimi", ["ChatGPT-4o", "LLaMA"], index=0)
    
    st.write("---")
    st.markdown("""
    **Hızlı Linkler:**
    - [🌐 Web Sitemiz](https://siliconmade.com)
    - [📚 Kurslarımız](https://siliconmade.com/kurslar)
    - [📞 İletişim](https://siliconmade.com/iletisim)
    """)
    
    st.write("---")
    if st.button("Sohbeti Sıfırla"):
        st.session_state.messages = [{"role": "system", "content": get_system_prompt("sales")}]
        st.session_state.user_text = ""
        st.rerun()

# ---- Session State ----
if "session_id" not in st.session_state:
    st.session_state.session_id = "user_1"

memory = ChatMemory(st.session_state.session_id)

if "messages" not in st.session_state:
    saved_messages = memory.get_history()
    if not saved_messages:
        st.session_state.messages = [{"role": "system", "content": get_system_prompt("sales")}]
        memory.save_message("system", get_system_prompt("sales"))
    else:
        st.session_state.messages = saved_messages

# ---- Ana Arayüz ----
st.title("Siliconmade AI Sales Assistant")
st.caption("Geleceğin yazılımcıları için akıllı rehber.")

# Chat history container
chat_placeholder = st.container()

with chat_placeholder:
    for msg in st.session_state.messages:
        if msg["role"] == "system": continue
        
        if msg["role"] == "user":
            st.markdown(f"""
            <div class="message-row user-row">
                <div class="bubble user-bubble">{msg['content']}</div>
                <div class="avatar user-avatar">SİZ</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message-row bot-row">
                <div class="avatar bot-avatar">AI</div>
                <div class="bubble bot-bubble">{msg['content']}</div>
            </div>
            """, unsafe_allow_html=True)

# Girdi alanı (Fixed-ish bottom)
st.markdown("<br><br>", unsafe_allow_html=True)
col_input, col_mic, col_btn = st.columns([6, 1, 1.2])

with col_input:
    user_input = st.text_input("", placeholder="Mesajınızı buraya yazın...", key="user_text", label_visibility="collapsed")

with col_mic:
    audio_bytes = audio_recorder(
        text="",
        recording_color="#e74c3c",
        neutral_color="#3a7bd5",
        icon_size="2x"
    )

with col_btn:
    send_btn = st.button("GÖNDER", use_container_width=True)

with st.expander("📁 Medya Yükle (Resim Analizi)"):
    uploaded_file = st.file_uploader("Bir görsel seçin", type=["jpg", "jpeg", "png"])

# ---- Logic ----
if send_btn or audio_bytes:
    input_text = user_input.strip() if user_input.strip() else None
    image_b64 = None

    if uploaded_file:
        image_b64 = base64.b64encode(uploaded_file.read()).decode("utf-8")

    if not input_text and audio_bytes:
        try:
            with st.spinner("Sesiniz işleniyor..."):
                input_text = transcribe_audio_openai(audio_bytes, "recorded.wav")
        except Exception as e:
            st.error(f"STT Hatası: {e}")

    if input_text:
        st.session_state.messages.append({"role": "user", "content": input_text})
        memory.save_message("user", input_text)
        
        try:
            with st.spinner("AI Yanıt veriyor..."):
                reply = run_chatbot(MODEL_TYPE, st.session_state.messages, image_b64=image_b64)
            
            if reply:
                st.session_state.messages.append({"role": "assistant", "content": reply})
                memory.save_message("assistant", reply)
                
                # Auto-play TTS
                try:
                    tts_path = synthesize_tts_openai(reply, voice="alloy")
                    with open(tts_path, "rb") as f:
                        audio_data = f.read()
                    st.audio(audio_data, format="audio/mp3", autoplay=True)
                    if os.path.exists(tts_path): os.remove(tts_path)
                except: pass
                
                st.rerun()
        except Exception as e:
            st.error(f"Sistem Hatası: {e}")