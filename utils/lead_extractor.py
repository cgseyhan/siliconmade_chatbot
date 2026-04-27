import json
import os
from openai import OpenAI

def extract_lead_info(messages: list) -> dict:
    """
    Konuşma geçmişini analiz ederek isim, e-posta ve telefon bilgilerini JSON olarak döndürür.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    # Sadece son birkaç mesajı analiz etmek yeterli olabilir
    conversation_text = ""
    for m in messages[-4:]:
        conversation_text += f"{m['role']}: {m['content']}\n"

    system_prompt = """
    Sen bir veri ayıklayıcısısın. Aşağıdaki konuşmadan eğer varsa şu bilgileri ayıkla:
    - name (İsim Soyisim)
    - email (E-posta)
    - phone (Telefon)
    - course (İlgilenilen kurs)

    Eğer bilgi yoksa null bırak. Yanıtı SADECE saf JSON formatında ver.
    Örnek: {"name": "Ahmet Yılmaz", "email": "ahmet@mail.com", "phone": "0555...", "course": "Java"}
    """

    try:
        response = client.chat.completions.create(
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
