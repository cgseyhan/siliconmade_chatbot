from pyairtable import Table
import os

def log_interaction(user_input: str, response: str, model: str):
    """
    Logs the conversation interaction directly into Airtable if configured.
    """
    try:
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        table_name = os.getenv("AIRTABLE_TABLE_NAME", "chat_logs")

        # Skip logging if Airtable credentials are not fully configured
        if not api_key or not base_id:
            return

        table = Table(api_key, base_id, table_name)

        record = {
            "model": model,
            "user_input": user_input,
            "bot_response": response
        }

        table.create(record)
        print(f"DEBUG: Airtable record successfully added -> {model}")
    except Exception as e:
        print(f"ERROR: Airtable logging failed -> {e}")
