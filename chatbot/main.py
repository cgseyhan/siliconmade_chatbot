from chatbot.llama import LlamaChatbot
from chatbot.openai import chat_with_openai
from utils.mysql_logger import log_interaction as log_mysql, save_lead, init_db
from integrations.airtable_integration import log_interaction as log_airtable
from utils.lead_extractor import extract_lead_info
from utils.sentiment_analyzer import analyze_sentiment_and_intent
import threading

# Initialize database
init_db()

from chatbot.prompts import get_system_prompt
from data_ingestion.rag_helper import get_knowledge_context

# Load system prompt
SYSTEM_PROMPT = get_system_prompt("sales")

def background_logs(user_input: str, response: str, model_name: str, sentiment: str = "Neutral", intent: str = "Other", messages: list = None):
    """
    Runs logging and Lead extraction operations in the background (thread).
    """
    # 1. Normal logging
    try:
        log_mysql(user_input, response, model_name, sentiment, intent)
    except Exception as e:
        print(f"DEBUG: SQLite log error -> {e}")

    try:
        log_airtable(user_input, response, model_name)
    except Exception as e:
        print(f"DEBUG: Airtable log error -> {e}")

    # 2. Lead extraction (if message history is available)
    if messages:
        try:
            lead_data = extract_lead_info(messages)
            # If at least one contact detail (name, email, or phone) is extracted, save it
            if lead_data.get("name") or lead_data.get("email") or lead_data.get("phone"):
                save_lead(
                    name=lead_data.get("name"),
                    email=lead_data.get("email"),
                    phone=lead_data.get("phone"),
                    product=lead_data.get("product") or lead_data.get("course"),
                    notes=f"Model: {model_name}"
                )
        except Exception as e:
            print(f"Background Lead Error: {e}")

def run_chatbot(model_name: str, messages: list, image_b64: str = None) -> str:
    """
    Processes the conversation history based on the selected model and returns the response.
    """
    # 1. Retrieve user message and fetch RAG context
    user_input = messages[-1]["content"] if messages else ""
    context = get_knowledge_context(user_input)

    # 2. Append context to the system message or start of history
    enriched_messages = messages.copy()
    
    if context:
        rag_prompt = f"\n\nKNOWLEDGE BASE CONTEXT:\n{context}\n\nPlease answer based strictly on the information above."
        if enriched_messages and enriched_messages[0]["role"] == "system":
            enriched_messages[0] = {
                "role": "system", 
                "content": enriched_messages[0]["content"] + rag_prompt
            }
        else:
            enriched_messages.insert(0, {"role": "system", "content": SYSTEM_PROMPT + rag_prompt})

    # 3. Process with model
    sentiment, intent = "Neutral", "Other"
    if model_name == "ChatGPT-4o":
        ai_res = chat_with_openai(enriched_messages, image_b64=image_b64)
        response = ai_res.get("answer", "An error occurred.")
        sentiment = ai_res.get("sentiment", "Neutral")
        intent = ai_res.get("intent", "Other")
    elif model_name == "LLaMA":
        response = LlamaChatbot().chat(enriched_messages)
    else:
        raise ValueError(f"Unknown model: {model_name}")

    # 4. Dispatch logging tasks to background thread
    log_thread = threading.Thread(
        target=background_logs, 
        args=(user_input, response, model_name, sentiment, intent, messages)
    )
    log_thread.start()
            
    return response