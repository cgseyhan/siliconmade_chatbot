from chatbot.llama import LlamaChatbot
from chatbot.openai import chat_with_openai
from utils.json_logger import log_interaction
from utils.mysql_logger import log_interaction as log_mysql
from integrations.airtable_integration import log_interaction as log_airtable

SYSTEM_PROMPT = "Sen bilgili, yardımsever ve nazik bir yapay zeka satış asistanısın."

def run_chatbot(model_name: str, user_input: str) -> str:
    if model_name == "LLaMA":  # OpenRouter tabanlı LLaMA
        response = LlamaChatbot().chat(SYSTEM_PROMPT, user_input)
    elif model_name == "ChatGPT-4o":
        response = chat_with_openai(SYSTEM_PROMPT, user_input)
    else:
        raise ValueError(f"Bilinmeyen model: {model_name}")

    # logları sessizce dene
    for fn in (log_interaction, log_mysql, log_airtable):
        try:
            fn(user_input, response, model_name)
        except Exception:
            pass
    return response