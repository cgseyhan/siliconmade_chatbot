# 🚀 Siliconmade AI Sales Assistant (Next-Gen RAG & Analytics)

Siliconmade Academy için geliştirilmiş, potansiyel öğrencilere rehberlik eden, anlamsal arama (RAG) yeteneğine sahip, duygu ve niyet analizi yapabilen profesyonel bir **Yapay Zeka Satış Asistanı** ekosistemidir.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20API-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI%2FUX-FF4B4B.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Storage-orange.svg)

---

## 🌟 Öne Çıkan Özellikler

### 🧠 Anlamsal Bellek (RAG - Retrieval Augmented Generation)
Bot, sadece önceden tanımlanmış metinlere bakmaz. **ChromaDB** vektör veritabanını kullanarak Siliconmade bilgi bankasında anlamsal arama yapar ve en doğru bilgiyi saniyeler içinde bulur.

### 📊 Akıllı Analitik & Dashboard
*   **Duygu Analizi:** Kullanıcının mutlu mu, kızgın mı yoksa nötr mü olduğunu anlık olarak tespit eder.
*   **Niyet Analizi:** Kullanıcının sadece bilgi mi almak istediğini yoksa satın almaya hazır bir "Lead" mi olduğunu anlar.
*   **Yönetim Paneli:** Plotly tabanlı grafiklerle müşteri segmentasyonu ve trafik analizi sunar.

### ⚡ Çok Kanallı Mimari (FastAPI)
Sadece bir web arayüzü değil, aynı zamanda bir API servisidir. Bu sayede botu mobil uygulamalara, WordPress sitelerine veya kurumsal sistemlere kolayca entegre edebilirsiniz.

### 🎨 Premium UI/UX
*   **Glassmorphism Tasarım:** Modern, yarı saydam ve estetik kullanıcı arayüzü.
*   **Multimodal Desteği:** Resim analizi yapabilir (Örn: Bir sertifikayı veya broşürü yorumlayabilir).
*   **Sesli Sohbet:** OpenAI Whisper ve TTS (Text-to-Speech) entegrasyonu ile konuşarak iletişim kurma.

---

## 🏗️ Proje Yapısı

```text
📁 siliconmade_chatbot
├── 📁 api              # FastAPI Backend (Santral)
├── 📁 chatbot          # Ana Mantık (OpenAI & LLaMA Entegrasyonları)
├── 📁 chroma_db        # Vektör Veritabanı (Hafıza)
├── 📁 data_ingestion   # Bilgi Bankası ve RAG Hazırlık Araçları
├── 📁 frontend         # Streamlit Arayüzleri (App & Admin Dashboard)
├── 📁 utils            # Yardımcı Araçlar (Loglama, Lead Çıkarma, Analiz)
├── 📁 widget           # Web Siteleri İçin Gömülebilir Widget
└── 📄 run_api.py       # API Sunucusunu Başlatıcı
```

---

## 🛠️ Kurulum ve Çalıştırma

### 1. Hazırlık
```bash
git clone https://github.com/cgseyhan/siliconmade_chatbot.git
cd siliconmade_chatbot
python -m venv .venv
source .venv/bin/activate # Windows için: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Yapılandırma
`.env` dosyanıza API anahtarlarınızı ekleyin:
```env
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=...
```

### 3. Çalıştırma
Proje üç ana katmandan oluşur:

*   **API Sunucusu:** `python run_api.py` (Port 8000)
*   **Kullanıcı Arayüzü:** `streamlit run run_app.py`
*   **Yönetim Paneli:** `streamlit run run_admin.py`

---

## 🛡️ Güvenlik ve Guardrails
Botumuz, rakip kurumlar hakkında konuşmamak, resmi fiyat listesi dışına çıkmamak ve tıbbi/etik dışı konularda yorum yapmamak üzere özel olarak eğitilmiştir.

---

## 📝 Geliştirici Notu
Bu proje, modern yapay zeka tekniklerini (RAG, Sentiment Analysis, Agentic Flow) kurumsal bir satış senaryosuna entegre etmek amacıyla Siliconmade Academy staj süreci kapsamında geliştirilmiştir.

---

**Geliştirici:** [cgseyhan]  
**Lisans:** MIT
