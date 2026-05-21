import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# Load .env file with its absolute path
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), ".env")
load_dotenv(env_path)

client = None

def get_sentiment_client():
    global client
    if client is None:
        key = os.getenv("OPENAI_API_KEY") or "dummy"
        client = OpenAI(api_key=key)
    return client

def analyze_sentiment_and_intent(user_input: str):
    """
    Analyzes the user's message to extract sentiment and intent.
    """
    try:
        # Check if API key is set
        key = os.getenv("OPENAI_API_KEY")
        if not key or key == "dummy":
            return "Neutral", "Other"

        prompt = f"""
        Analyze the following user message and respond ONLY in JSON format.
        Format: {{"sentiment": "Positive/Neutral/Negative", "intent": "Information/Purchase/Support/Complaint/Other"}}

        Message: "{user_input}"
        """

        response = get_sentiment_client().chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "You are a data analyst assistant. Respond ONLY in the requested JSON format."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )

        analysis = json.loads(response.choices[0].message.content)
        return analysis.get("sentiment", "Neutral"), analysis.get("intent", "Other")
    except Exception as e:
        print(f"Sentiment Analysis Error: {e}")
        return "Neutral", "Other"
