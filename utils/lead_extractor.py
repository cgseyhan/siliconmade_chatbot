import json
import os
from openai import OpenAI

_lead_client = None

def get_lead_client():
    global _lead_client
    if _lead_client is None:
        key = os.getenv("OPENAI_API_KEY") or "dummy"
        _lead_client = OpenAI(api_key=key)
    return _lead_client

def extract_lead_info(messages: list) -> dict:
    """
    Analyzes the conversation history to extract name, email, and phone info as JSON.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or key == "dummy":
        return {}

    # Analyzing the last few messages is usually sufficient
    conversation_text = ""
    for m in messages[-4:]:
        conversation_text += f"{m['role']}: {m['content']}\n"

    system_prompt = """
    You are a data extractor. Extract the following details from the conversation if available:
    - name (Full Name)
    - email (Email address)
    - phone (Phone number)
    - product (Product/service/topic of interest)

    If any information is not present, set it to null. Respond ONLY in pure JSON format.
    Example: {"name": "John Doe", "email": "john@mail.com", "phone": "+1234...", "product": "ERP Solution"}
    """

    try:
        response = get_lead_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": conversation_text}
            ],
            response_format={ "type": "json_object" }
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Lead extraction error: {e}")
        return {}
