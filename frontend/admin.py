import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px
from dotenv import load_dotenv
from utils.mysql_logger import init_db, set_setting, get_setting
from chatbot.prompts import get_system_prompt

load_dotenv()
init_db()

# ---- Page Config ----
st.set_page_config(
    page_title="Brand AI Admin Dashboard",
    page_icon="📊",
    layout="wide"
)

# ---- Dark Theme CSS ----
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        padding: 15px;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    h1, h2, h3 {
        color: #00d2ff !important;
    }
</style>
""", unsafe_allow_html=True)

def get_db_connection():
    return sqlite3.connect("chatbot.db")

# ---- Sidebar (Brand Customization & RAG Settings) ----
with st.sidebar:
    st.markdown("<h2 style='text-align: center; color: #00d2ff; margin-bottom: 20px;'>🤖 BrandAI Admin</h2>", unsafe_allow_html=True)
    st.markdown("### ⚙️ Assistant Settings")
    
    # Model selection
    db_model = get_setting("selected_model", "ChatGPT-4o")
    model_index = 0 if db_model == "ChatGPT-4o" else 1
    selected_model = st.selectbox("Model Selection", ["ChatGPT-4o", "LLaMA"], index=model_index)
    if selected_model != db_model:
        set_setting("selected_model", selected_model)
        st.toast(f"Model updated to {selected_model}!", icon="🤖")

    st.write("---")
    st.markdown("### 🔧 Brand Customization")

    # 1. Custom System Prompt
    db_prompt = get_setting("custom_system_prompt", get_system_prompt("sales"))
    custom_prompt = st.text_area(
        "System Prompt (Assistant Role)",
        value=db_prompt,
        height=180,
        help="Customize the assistant's character, language, and tasks here."
    )
    if custom_prompt != db_prompt:
        set_setting("custom_system_prompt", custom_prompt)
        st.toast("System prompt updated!", icon="📝")

    # 2. RAG File Upload
    st.markdown("#### 📁 Knowledge Base (RAG)")
    rag_file = st.file_uploader(
        "Upload New Knowledge Base",
        type=["txt", "md"],
        help="Upload a text file (.txt or .md) containing custom knowledge for the assistant."
    )
    if rag_file is not None:
        try:
            file_content = rag_file.read().decode("utf-8")
            from utils.vector_store import reindex_from_text, KNOWLEDGE_FILE
            
            with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
                f.write(file_content)
                
            with st.spinner("Indexing Knowledge Base..."):
                reindex_from_text(file_content)
            st.success("Knowledge Base indexed successfully!", icon="✅")
        except Exception as e:
            st.error(f"Indexing error: {e}")

st.title("📊 Brand AI Chatbot Intelligence Dashboard")
st.markdown("Centralized management panel for data analytics and lead tracking.")

try:
    conn = get_db_connection()
    
    # --- 0. KPI Metrics ---
    total_chats = pd.read_sql("SELECT COUNT(*) FROM chat_logs", conn).iloc[0,0]
    total_leads = pd.read_sql("SELECT COUNT(*) FROM leads", conn).iloc[0,0]
    positive_ratio = 0
    try:
        # Support both 'Positive' (new English) and 'Pozitif' (old Turkish logs if any)
        pos_chats = pd.read_sql("SELECT COUNT(*) FROM chat_logs WHERE sentiment IN ('Positive', 'Pozitif')", conn).iloc[0,0]
        if total_chats > 0:
            positive_ratio = (pos_chats / total_chats) * 100
    except: pass

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Total Interactions", total_chats)
    with m2: st.metric("Collected Leads", total_leads)
    with m3: st.metric("Positive Satisfaction", f"{positive_ratio:.1f}%")

    st.write("---")

    # --- 1. Leads Pool ---
    st.subheader("🎯 Lead Pool")
    leads_df = pd.read_sql("SELECT * FROM leads ORDER BY timestamp DESC", conn)
    if not leads_df.empty:
        # Rename columns to be elegant and localized
        rename_dict = {
            "id": "ID",
            "timestamp": "Date",
            "name": "Customer Name",
            "email": "Email",
            "phone": "Phone",
            "product_interest": "Product/Service of Interest",
            "notes": "Notes"
        }
        display_df = leads_df.rename(columns=rename_dict)
        st.dataframe(display_df, use_container_width=True, hide_index=True)
        
        # Download Leads CSV
        csv = display_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Download Lead List as CSV", csv, "leads.csv", "text/csv")
    else:
        st.info("No lead records found yet.")

    st.write("---")

    # --- 2. Analytics Charts ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Sentiment Distribution")
        sent_df = pd.read_sql("SELECT sentiment, COUNT(*) as count FROM chat_logs GROUP BY sentiment", conn)
        if not sent_df.empty:
            # Map sentiments (handling both English and potential old Turkish logs)
            sent_df['sentiment'] = sent_df['sentiment'].replace({
                'Pozitif': 'Positive',
                'Nötr': 'Neutral',
                'Negatif': 'Negative'
            })
            # Re-aggregate in case replacement caused duplicates
            sent_df = sent_df.groupby('sentiment').sum().reset_index()
            
            fig = px.pie(sent_df, values='count', names='sentiment', 
                         color='sentiment',
                         color_discrete_map={
                             'Positive': '#00d2ff',
                             'Neutral': '#3a7bd5',
                             'Negative': '#e74c3c'
                         },
                         hole=0.4)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 User Intent Analysis")
        intent_df = pd.read_sql("SELECT intent, COUNT(*) as count FROM chat_logs GROUP BY intent", conn)
        if not intent_df.empty:
            # Map intents (handling potential Turkish logs)
            intent_df['intent'] = intent_df['intent'].replace({
                'Bilgi': 'Information',
                'Satın Alma': 'Purchase',
                'Destek': 'Support',
                'Şikayet': 'Complaint',
                'Diğer': 'Other'
            })
            # Re-aggregate
            intent_df = intent_df.groupby('intent').sum().reset_index()
            
            fig2 = px.bar(intent_df, x='intent', y='count', color='intent',
                          color_discrete_sequence=px.colors.sequential.Blues_r)
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig2, use_container_width=True)

    st.write("---")

    # --- 3. Traffic Analysis ---
    st.subheader("📅 Message Traffic")
    traffic_df = pd.read_sql("SELECT DATE(timestamp) as date, COUNT(*) as count FROM chat_logs GROUP BY date", conn)
    if not traffic_df.empty:
        fig3 = px.line(traffic_df, x='date', y='count', markers=True, line_shape='spline')
        fig3.update_traces(line_color='#00d2ff')
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig3, use_container_width=True)

    st.write("---")

    # --- 4. Detailed Logs ---
    st.subheader("💬 Detailed Chat Logs")
    logs_df = pd.read_sql("SELECT timestamp, model, user_input, response, sentiment, intent FROM chat_logs ORDER BY timestamp DESC LIMIT 100", conn)
    
    # Map column headers to be user-friendly in English
    rename_logs = {
        "timestamp": "Timestamp",
        "model": "Model",
        "user_input": "User Message",
        "response": "AI Response",
        "sentiment": "Sentiment",
        "intent": "Intent"
    }
    display_logs_df = logs_df.rename(columns=rename_logs)
    st.dataframe(display_logs_df, use_container_width=True, hide_index=True)

    conn.close()

except Exception as e:
    st.error(f"Error: {e}")
