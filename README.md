# 🚀 Enterprise Brand AI Sales Assistant (Next-Gen RAG & Analytics)

Herhangi bir marka veya işletme için kolayca özelleştirilebilen; anlamsal arama (RAG) yeteneğine sahip, duygu ve niyet analizi yapabilen, dinamik arayüz üzerinden özelleştirilebilir profesyonel bir **Yapay Zeka Satış Asistanı** ekosistemidir.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20API-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI%2FUX-FF4B4B.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Storage-orange.svg)

---

## 🌟 Öne Çıkan Özellikler

### 🧠 Markaya Özel Anlamsal Bellek (RAG - Retrieval Augmented Generation)
Arayüz üzerinden yükleyeceğiniz her türlü bilgi bankası (.txt, .md) dosyasını otomatik olarak **ChromaDB** vektör veritabanına indeksler ve asistanınızın anında marka uzmanına dönüşmesini sağlar.

### 📝 Dinamik Sistem Promptu Özelleştirme
Asistanın karakterini, dil tonunu, kırmızı çizgilerini ve satış stratejilerini kod yazmadan doğrudan arayüz üzerindeki **Marka Özelleştirme** panelinden değiştirebilirsiniz.

### 📊 Akıllı Analitik & Dashboard
*   **Duygu Analizi:** Kullanıcının mutlu mu, kızgın mı yoksa nötr mü olduğunu anlık olarak tespit eder.
*   **Niyet Analizi:** Kullanıcının sadece bilgi mi almak istediğini yoksa satın almaya hazır bir "Lead" mi olduğunu anlar.
*   **Yönetim Paneli:** Plotly tabanlı grafiklerle müşteri segmentasyonu ve trafik analizi sunar.

### ⚡ Çok Kanallı Mimari (FastAPI)
Sadece bir web arayüzü değil, aynı zamanda bir API servisidir. Bu sayede asistanı mobil uygulamalara, WordPress sitelerine veya kurumsal sistemlere kolayca entegre edebilirsiniz.

### 🎨 Premium UI/UX
*   **Glassmorphism Tasarım:** Modern, yarı saydam ve estetik kullanıcı arayüzü.
*   **Multimodal Desteği:** Resim analizi yapabilir (Örn: Bir sertifikayı veya broşürü yorumlayabilir).
*   **Sesli Sohbet:** OpenAI Whisper ve TTS (Text-to-Speech) entegrasyonu ile konuşarak iletişim kurma.

---

## 🏗️ Proje Yapısı

```text
📁 chatbotforbrands
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
git clone https://github.com/cgseyhan/chatbotforbrands.git
cd chatbotforbrands
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
Asistanınız; rakipler hakkında konuşmamak, resmi fiyat politikasının dışına çıkmamak, uydurma bilgi vermemek ve etik dışı konularda yorum yapmamak üzere korumalı kurallar barındırır.

---

## 📝 Geliştirici Notu
Bu proje, modern yapay zeka tekniklerini (RAG, Sentiment Analysis, Agentic Flow) kurumsal bir satış ve müşteri ilişkileri senaryosuna entegre etmek amacıyla geliştirilmiş profesyonel bir altyapıdır.

---

**Geliştirici:** [cgseyhan]  
**Lisans:** MIT
