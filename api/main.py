from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
import sys

# Add project root directory to Python path (so chatbot module can be found)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from chatbot.main import run_chatbot

app = FastAPI(title="Brand Chatbot API", version="1.0.0")

# CORS Settings (allowing access from everywhere)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Models
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str = "ChatGPT-4o"
    messages: List[Message]
    image_b64: Optional[str] = None

@app.get("/")
def home():
    return {"status": "online", "message": "Brand Chatbot API is running."}

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    try:
        # Convert messages to a list of dicts
        formatted_messages = [{"role": m.role, "content": m.content} for m in request.messages]
        
        # Run the chatbot
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
