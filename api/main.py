from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Proje kök dizinini Python yoluna ekle (chatbot modülünü bulabilmesi için)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.main import run_chatbot

app = FastAPI(title="Siliconmade Chatbot API", version="1.0.0")

# CORS Ayarları (Her yerden erişime izin veriyoruz)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# İstek Modelleri
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "ChatGPT-4o"
    messages: List[Message]
    image_b64: Optional[str] = None

@app.get("/")
def home():
    return {"status": "online", "message": "Siliconmade Chatbot API is running."}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Mesajları sözlük listesine çevir
        formatted_messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        # Chatbotu çalıştır
        response = run_chatbot(
            model_name=request.model,
            messages=formatted_messages,
            image_b64=request.image_b64
        )
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
