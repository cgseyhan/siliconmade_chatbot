import streamlit as st
import sqlite3
import pandas as pd
import os
import plotly.express as px
from dotenv import load_dotenv
from utils.mysql_logger import init_db

load_dotenv()
init_db()

# ---- Page Config ----
st.set_page_config(
    page_title="Siliconmade Admin Dashboard",
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

st.title("📊 Siliconmade Chatbot Intelligence Dashboard")
st.markdown("Veri analitiği ve aday müşteri takibi için merkezi yönetim paneli.")

try:
    conn = get_db_connection()
    
    # --- 0. KPI Metrics ---
    total_chats = pd.read_sql("SELECT COUNT(*) FROM chat_logs", conn).iloc[0,0]
    total_leads = pd.read_sql("SELECT COUNT(*) FROM leads", conn).iloc[0,0]
    positive_ratio = 0
    try:
        pos_chats = pd.read_sql("SELECT COUNT(*) FROM chat_logs WHERE sentiment='Pozitif'", conn).iloc[0,0]
        if total_chats > 0:
            positive_ratio = (pos_chats / total_chats) * 100
    except: pass

    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Toplam Etkileşim", total_chats)
    with m2: st.metric("Toplanan Lead Sayısı", total_leads)
    with m3: st.metric("Pozitif Memnuniyet", f"%{positive_ratio:.1f}")

    st.write("---")

    # --- 1. Aday Müşteriler (Leads) ---
    st.subheader("🎯 Aday Müşteri Havuzu")
    leads_df = pd.read_sql("SELECT * FROM leads ORDER BY timestamp DESC", conn)
    if not leads_df.empty:
        st.dataframe(leads_df, use_container_width=True, hide_index=True)
        
        # Download Leads CSV
        csv = leads_df.to_csv(index=False).encode('utf-8-sig')
        st.download_button("Leads CSV İndir", csv, "leads.csv", "text/csv")
    else:
        st.info("Henüz aday müşteri kaydı bulunmuyor.")

    st.write("---")

    # --- 2. Analitik Grafikler ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("📈 Duygu Durum Dağılımı")
        sent_df = pd.read_sql("SELECT sentiment, COUNT(*) as count FROM chat_logs GROUP BY sentiment", conn)
        if not sent_df.empty:
            fig = px.pie(sent_df, values='count', names='sentiment', 
                         color='sentiment',
                         color_discrete_map={'Pozitif':'#00d2ff','Nötr':'#3a7bd5','Negatif':'#e74c3c'},
                         hole=0.4)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("🎯 Kullanıcı Niyet Analizi")
        intent_df = pd.read_sql("SELECT intent, COUNT(*) as count FROM chat_logs GROUP BY intent", conn)
        if not intent_df.empty:
            fig2 = px.bar(intent_df, x='intent', y='count', color='intent',
                          color_discrete_sequence=px.colors.sequential.Blues_r)
            fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
            st.plotly_chart(fig2, use_container_width=True)

    st.write("---")

    # --- 3. Trafik Analizi ---
    st.subheader("📅 Mesaj Trafiği")
    traffic_df = pd.read_sql("SELECT DATE(timestamp) as date, COUNT(*) as count FROM chat_logs GROUP BY date", conn)
    if not traffic_df.empty:
        fig3 = px.line(traffic_df, x='date', y='count', markers=True, line_shape='spline')
        fig3.update_traces(line_color='#00d2ff')
        fig3.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
        st.plotly_chart(fig3, use_container_width=True)

    st.write("---")

    # --- 4. Tüm Loglar ---
    st.subheader("💬 Detaylı Sohbet Logları")
    logs_df = pd.read_sql("SELECT timestamp, model, user_input, response, sentiment, intent FROM chat_logs ORDER BY timestamp DESC LIMIT 100", conn)
    st.dataframe(logs_df, use_container_width=True, hide_index=True)

    conn.close()

except Exception as e:
    st.error(f"Hata: {e}")
