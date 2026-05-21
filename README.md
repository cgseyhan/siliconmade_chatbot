# 🚀 Enterprise Brand AI Sales Assistant (Next-Gen RAG & Analytics)

An enterprise-grade, customizable **AI Sales Assistant Ecosystem** designed to empower any brand or business. Equipped with Semantic Search (RAG), real-time sentiment and intent analysis, dynamic role customization, and an advanced administrative dashboard, this solution seamlessly converts user interactions into structured, actionable business intelligence.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-Modern%20API-009688.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-UI%2FUX-FF4B4B.svg)
![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4o-412991.svg)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector%20Storage-orange.svg)
![SQLite](https://img.shields.io/badge/SQLite-Data%20Storage-003B57.svg)

---

## 🌟 Key Features

### 🧠 Brand-Specific Semantic Memory (RAG)
Instantly uploads and indexes any knowledge base files (`.txt`, `.md`) directly via the administration panel into a local **ChromaDB** vector database. The chatbot dynamically retrieves context for user queries to deliver highly accurate, domain-specific responses.

### 📝 Dynamic System Prompt Customization
Tailor the assistant's character, brand guidelines, tone of voice, boundaries, and sales strategy instantly. Admin changes to the system prompt take effect immediately without requiring code edits or application restarts.

### 📊 Real-Time Analytics & Dashboard
*   **Sentiment Analysis:** Instantly classifies user feedback and reactions (`Positive`, `Neutral`, `Negative`) to assess customer satisfaction.
*   **Intent Recognition:** Automatically determines whether a user is seeking basic `Information`, ready to `Purchase`, requesting `Support`, filing a `Complaint`, or doing `Other` tasks.
*   **KPI Metrics & Visualizations:** The Plotly-powered executive dashboard tracks total interactions, lead count, positive satisfaction ratio, and message traffic trends over time.

### ⚡ Multi-Channel System (FastAPI Backend)
Includes a modern, high-performance **FastAPI** web service. The core business logic can be instantly accessed by external services, making it easy to embed the chatbot into mobile apps, corporate websites, WordPress portals, or custom CRM solutions.

### 🎨 Premium UI/UX & Multimodal Support
*   **Glassmorphism Theme:** A sleek, beautiful, dark user interface with smooth animations and responsive components.
*   **Multimodal Capabilities:** Supports image uploads and analyzes files (e.g. brochures, screenshots, certificates) in real time using GPT-4o.
*   **Voice Integration:** Converse naturally using built-in high-fidelity audio recording, powered by OpenAI Whisper (STT) and dynamic speech generation (TTS).

---

## 🏗️ System Architecture

```text
📁 chatbotforbrands
├── 📁 api              # FastAPI Backend Server (API Core Gateway)
├── 📁 chatbot          # Core AI Modules (OpenAI & LLaMA Integration, Prompts, Memory)
├── 📁 chroma_db        # ChromaDB Vector Database (Semantic Knowledge Memory)
├── 📁 data_ingestion   # RAG Helpers & Default Brand Knowledge Base files
├── 📁 frontend         # Streamlit Web Interfaces (User App & Admin Dashboard)
├── 📁 utils            # Utility Modules (SQLite Logging, Lead Extractor, Sentiment Analyzer, Vector Store)
├── 📁 widget           # Embeddable HTML/CSS/JS Widget for corporate websites
├── 📄 run_api.py       # API Launcher Script
├── 📄 run_app.py       # Customer Chatbot Web App Launcher
└── 📄 run_admin.py     # Admin Dashboard Launcher
```

### 💾 Relational Database Schema (SQLite: `chatbot.db`)

The system automatically manages application states, analytics, and leads using three core tables in SQLite:

#### 1. `chat_logs` (Conversation History & Analytics Data)
Stores granular details of every user message and AI response for audit trails and Plotly metrics:
*   `id` (INTEGER, Primary Key): Unique log identifier.
*   `timestamp` (DATETIME): Time of the interaction.
*   `model` (TEXT): The AI model utilized (`ChatGPT-4o` or `LLaMA`).
*   `user_input` (TEXT): Raw input message from the user.
*   `response` (TEXT): The generated response from the assistant.
*   `sentiment` (TEXT): Categorized sentiment (`Positive`, `Neutral`, `Negative`).
*   `intent` (TEXT): Categorized user intent (`Information`, `Purchase`, `Support`, `Complaint`, `Other`).

#### 2. `leads` (Customer Acquisition Pool)
Aggregates customer contacts parsed and extracted automatically from conversation transcripts in the background:
*   `id` (INTEGER, Primary Key): Unique lead identifier.
*   `timestamp` (DATETIME): Creation time.
*   `name` (TEXT): Customer name.
*   `email` (TEXT): Email address.
*   `phone` (TEXT): Telephone number.
*   `product_interest` (TEXT): Identified product, course, or service interest.
*   `notes` (TEXT): Contextual remarks (e.g., model used, conversation highlights).

#### 3. `settings` (Dynamic Configuration)
Maintains system variables persistently:
*   `key` (TEXT, Primary Key): Configuration variable name (e.g., `selected_model`, `custom_system_prompt`).
*   `value` (TEXT): Value mapping.

---

## 🛠️ Setup & Local Execution

### 1. Prerequisites & Environment Setup
Clone the repository and initialize a local Python virtual environment:
```bash
git clone https://github.com/cgseyhan/chatbotforbrands.git
cd chatbotforbrands

# Create and activate virtual environment
python -m venv .venv
# On macOS/Linux:
source .venv/bin/activate
# On Windows:
.venv\Scripts\activate

# Install all dependencies
pip install -r requirements.txt
```

### 2. Configuration
Create a `.env` file in the root directory and populate your API credentials:
```env
OPENAI_API_KEY=sk-...
OPENROUTER_API_KEY=...
# Optional OpenRouter variables
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
OPENROUTER_SITE_URL=http://localhost
OPENROUTER_APP_NAME=BrandChatbot
```

> [!TIP]
> The application includes smart fallbacks. If `OPENAI_API_KEY` is not present, it will run gracefully, providing intuitive visual warnings in the UI instead of raising unhandled 401 exceptions.

### 3. Launching the Services
To run the complete ecosystem locally, start the three core scripts in separate terminals:

#### FastAPI Backend Server
Launches the lightweight gateway for external integrations:
```bash
python run_api.py
```
*Access home API status at: [http://localhost:8000](http://localhost:8000)*

#### Customer-Facing Web App
Launches the customer-facing interface:
```bash
python run_app.py
```

#### Administration Dashboard
Launches the data analytics, RAG indexing, and prompt management panel:
```bash
python run_admin.py
```

---

## 🛡️ Guardrails & Operational Constraints

The assistant operates under strict rules defined in the prompt guidelines to protect brand reputation:
*   **Competitor Immunity:** Never compares itself with competitor brands. If prompted, it responds gracefully: *"We focus on our own quality and customer satisfaction."*
*   **Price Integrity:** Refuses to issue customized or unofficial discount promises. Instead, it invites users to leave contact information to check active campaign options.
*   **Scope Limitation:** Automatically avoids discussions on unethical, political, or highly controversial subjects.
*   **Accuracy Control:** If the search context does not contain sufficient details to answer a question, it avoids hallucination and states: *"I can refer you to our expert on this matter."*

---

## 📝 Developer Notes

This codebase serves as a blueprint for implementing state-of-the-art AI interactions (RAG, Speech-to-Text, Multimodal Analysis) in corporate environments. 

**Developer:** cgseyhan  
**License:** MIT
