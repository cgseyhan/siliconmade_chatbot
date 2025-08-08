import os
import streamlit as st
from audio_recorder_streamlit import audio_recorder  # tek mikrofon butonu

from chatbot.main import run_chatbot
from chatbot.speech import transcribe_audio_openai, synthesize_tts_openai

# ---- Sayfa ayarları (ikon/başlık/düzen) ----
st.set_page_config(
    page_title="Chatbot",
    page_icon="➡️",   # veya "⏩"
    layout="wide"
)

# ---- Kenar çubuğu: sadece iki seçenek ----
MODEL_TYPE = st.sidebar.selectbox("Model Seçimi", ["LLaMA", "ChatGPT-4o"])
if MODEL_TYPE == "LLaMA":
    st.sidebar.caption(
        f"Aktif LLaMA modeli: `{os.getenv('OPENROUTER_LLAMA_MODEL', 'meta-llama/llama-3.3-70b-instruct:free')}`"
    )

# ---- Basit ve sıkı layout ----
st.markdown("""
<style>
  .block-container { padding-top: 1.2rem; padding-bottom: 2rem; max-width: 980px; }
  .bubble { background: rgba(46,160,67,.12); border:1px solid rgba(125,125,125,.25);
            padding:.9rem 1rem; border-radius:.75rem; }
</style>
""", unsafe_allow_html=True)

st.write("💬 Metin yazarak ya da 🎤 mikrofonla soru sorabilirsin.")

# ---- Girdi alanları ----
user_input = st.text_input("Metin Gir:", placeholder="Herhangi bir şey sor")

st.caption("Veya mikrofon ile konuş (basılı tut, bırakınca biter):")
audio_bytes = audio_recorder(pause_threshold=0.8)

if audio_bytes:
    st.audio(audio_bytes, format="audio/wav")

# ---- Gönder ----
if st.button("Gönder"):
    input_text = user_input.strip() if user_input.strip() else None

    if not input_text and audio_bytes:
        try:
            transcript = transcribe_audio_openai(audio_bytes, "recorded.wav")
            with st.expander("Ses çözümlemesi (STT)", expanded=False):
                st.write(transcript)
            input_text = transcript
        except Exception as e:
            st.error(f"STT hata: {e}")

    if not input_text:
        st.warning("Lütfen metin gir veya kısa bir ses kaydı yap.")
    else:
        # Chatbot yanıtı
        reply = None
        try:
            reply = run_chatbot(MODEL_TYPE, input_text)
        except Exception as e:
            st.error(f"Chatbot hatası: {e}")

        if reply:
            st.markdown("**Yanıt:**")
            st.markdown(f"<div class='bubble'>{reply}</div>", unsafe_allow_html=True)

            # TTS
            try:
                tts_path = synthesize_tts_openai(reply, voice="alloy")
                st.caption("Yanıt (Ses):")
                with open(tts_path, "rb") as f:
                    st.audio(f.read(), format="audio/mp3")
            except Exception as e:
                st.error(f"TTS hata: {e}")