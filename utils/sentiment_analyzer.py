import os
import json
from openai import OpenAI
from dotenv import load_dotenv

# .env dosyasını tam yol ile yükle
current_dir = os.path.dirname(os.path.abspath(__file__))
env_path = os.path.join(os.path.dirname(current_dir), ".env")
load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print(f"WARNING: Sentiment Analyzer için OPENAI_API_KEY bulunamadı! Yol: {env_path}")

client = OpenAI(api_key=api_key)

def analyze_sentiment_and_intent(user_input: str):
    """
    Kullanıcı mesajını analiz eder: Duygu ve Niyet çıkarır.
    """
    try:
        prompt = f"""
        Aşağıdaki kullanıcı mesajını analiz et ve sadece JSON formatında yanıt ver.
        Format: {{"sentiment": "Pozitif/Nötr/Negatif", "intent": "Bilgi/Satın Alma/Destek/Şikayet/Diğer"}}

        Mesaj: "{user_input}"
        """

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "system", "content": "Sen bir veri analisti asistanısın. Sadece istenen JSON formatında cevap verirsin."},
                      {"role": "user", "content": prompt}],
            response_format={ "type": "json_object" }
        )

        analysis = json.loads(response.choices[0].message.content)
        return analysis.get("sentiment", "Nötr"), analysis.get("intent", "Diğer")
    except Exception as e:
        print(f"Sentiment Analysis Error: {e}")
        return "Nötr", "Diğer"
