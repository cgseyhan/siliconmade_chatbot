# Chatbot Satış Asistanı (GPT-4o & LLaMA)

Bu proje, **OpenAI GPT-4o** ve **yerel LLaMA modeli** ile çalışan, **Streamlit tabanlı** bir chatbot arayüzü sunar. Kullanıcı girişleri otomatik olarak **MySQL veritabanına** ve **Airtable bulut platformuna** kaydedilir.

```
📁 siliconmade_chatbot
├── chatbot
│ ├── chatbot_logic.py                    
│ ├── llama.py 
│ ├── main.py 
│ ├── memory.py 
│ ├── openai.py 
│ ├── prompts.py 
│
├── config
│ ├── config.yaml 
│ ├── secrets.json 
│
├── data_ingestion 
│
├── database
│
├── frontend
│ ├── app.py 
│ ├── ui_components.py 
│
├── integrations
│ ├── airtable_integration.py 
│
├── models 
│
├── utils
│ ├── helpers.py 
│ ├── json_logger.py
│ ├── log_analyzer.py 
│ ├── mysql_logger.py 
│
├── widget
│ ├── chatbot_widget.css 
│ ├── chatbot_widget.html 
│ ├── chatbot_widget.js 
│
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── run_app.py
└── run.py
```
---
## Özellikler

- GPT-4o (OpenAI) ile Türkçe yazılı ve sesli sohbet
- LLaMA (yerel) ile offline yazılı ve sesli sohbet deneyimi
- MySQL veritabanına sohbet kayıtları
- Airtable'a bulut senkronizasyonu
- JSON sohbet kayıtları

---

## Kurulum

### 1. Depoyu klonlayın:

```bash
git clone https://github.com/cgseyhan/siliconmade_chatbot
cd siliconmade_chatbot
```

### 2. Sanal ortam oluşturun ve etkinleştirin:

```bash
python -m venv .venv
```
Windows: 
```bash
.venv\Scripts\activate
```
macOS/Linux: 
```bash
source .venv/bin/activate
```

### 3. Gereksinimleri Yükleyin:

```bash
pip install -r requirements.txt
```

---

## .env Dosyası
Proje dizinine `.env` dosyası oluşturun ve aşağıdaki içerikle doldurun:

```bash
OPENAI_API_KEY="sk-"

MYSQL_HOST="localhost"
MYSQL_USER="root"
MYSQL_PASSWORD="password"
MYSQL_DATABASE="chatbot_db"

AIRTABLE_API_KEY="pat..."
AIRTABLE_BASE_ID="app..."
AIRTABLE_TABLE_NAME="chat_logs"
```

## Uygulamayı Başlatma
GPT-4o versiyonu:
```bash
streamlit run gpt.py
```
LLaMA versiyonu:
```bash
streamlit run llama.py
```
---

## Gereken Kütüphaneler

Hepsi `requirements.txt` dosyasında listelenmiştir.

---

## Uyarılar

- LLaMA için `.gguf` model dosyası `models/` klasöründe olmalıdır. [Hugging Face](https://huggingface.co/models?library=gguf&sort=trending&search=llama) üzerinden istediğiniz modeli indirip `models/` klasörüne kopyalamanız yeterli olacaktır.
- `.gitignore` dosyasına `chatbot.db`, `*.mp3`, `models/`, `.env` gibi büyük veya hassas dosyaları ekleyin.
- API anahtarlarınızı asla açık olarak paylaşmayın.

---

## Geliştirici Notu
Bu proje, [Siliconmade Academy](https://www.siliconmadeacademy.com/lead/?c=03-00092-20250503&gad_source=1&gad_campaignid=20731985909&gbraid=0AAAAABfTe3vGSw8oDAKaH2-h5W3AtBkvu&gclid=CjwKCAjw3_PCBhA2EiwAkH_j4uQdM2WmWLP6onaujAH4SkzhN9i9Frencb2NfS2M99VT7x_fHYsxbhoC3H0QAvD_BwE) staj süreci kapsamında bireysel bir proje olarak geliştirilmiştir.
