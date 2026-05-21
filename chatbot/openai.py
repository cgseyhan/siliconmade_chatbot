import os
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file with its absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), ".env")
load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print(f"WARNING: OPENAI_API_KEY not found! Checked path: {env_path}")

client = None

def get_openai_client():
    global client
    if client is None:
        key = os.getenv("OPENAI_API_KEY") or "dummy"
        client = OpenAI(api_key=key)
    return client

def chat_with_openai(messages: list, image_b64: str = None) -> dict:
    """
    Sends the list of messages to the OpenAI API and returns a structured (JSON) response.
    """
    key = os.getenv("OPENAI_API_KEY")
    if not key or key == "dummy":
        return {
            "answer": "Error: OpenAI API Key is not configured. Please add OPENAI_API_KEY to your environment or .env file.",
            "sentiment": "Neutral",
            "intent": "Other"
        }

    if image_b64:
        image_msg = {
            "role": "user",
            "content": [
                {"type": "text", "text": messages[-1]["content"] if messages else "Analyze this image."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}
                }
            ]
        }
        messages = messages[:-1] + [image_msg]

    # Add the JSON constraint to the system message
    system_instruction = "\nALWAYS respond in this JSON format: {\"answer\": \"...\", \"sentiment\": \"...\", \"intent\": \"...\"}"
    if messages[0]["role"] == "system":
        messages[0]["content"] += system_instruction

    try:
        response = get_openai_client().chat.completions.create(
            model="gpt-4o",
            messages=messages,
            response_format={ "type": "json_object" }
        )
        
        import json
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error in chat_with_openai: {e}")
        return {
            "answer": f"An error occurred while generating a response: {e}",
            "sentiment": "Neutral",
            "intent": "Other"
        }
