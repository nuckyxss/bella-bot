import os
import logging
from typing import Dict, Any
from dotenv import load_dotenv
import httpx
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# API URLs
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Create FastAPI app
app = FastAPI()

# System prompt for the model
SYSTEM_PROMPT = """Jesteś seksowną, uwodzicielską kobietą, która flirtuje odważnie i zmysłowo. 
Twoje odpowiedzi są pełne napięcia, subtelnie NSFW i erotyczne, ale z klasą."""

class TelegramUpdate(BaseModel):
    update_id: int
    message: Dict[str, Any] = None
    edited_message: Dict[str, Any] = None

@app.get("/")
async def root():
    return {"status": "Bot is running"}

@app.get("/ping")
async def ping():
    return {"status": "OK"}

@app.post("/webhook")
async def telegram_webhook(update: TelegramUpdate):
    try:
        # Extract message details
        if update.message is None:
            # Skip updates without messages
            return {"status": "ok"}
        
        chat_id = update.message.get("chat", {}).get("id")
        message_text = update.message.get("text", "")
        
        if not message_text:
            # Skip messages without text
            return {"status": "ok"}
        
        logger.info(f"Received message from chat {chat_id}: {message_text}")
        
        # Get response from LLM
        llm_response = await get_llm_response(message_text)
        
        # Send response back to user
        await send_telegram_message(chat_id, llm_response)
        
        return {"status": "ok"}
    
    except Exception as e:
        logger.error(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def get_llm_response(message_text: str) -> str:
    """Get response from LLM using OpenRouter API"""
    try:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://your-site.com",  # Replace with your site
            "X-Title": "Telegram Bot"
        }
        
        payload = {
            "model": "nousresearch/deephermes-3-llama-3-8b-preview:free",
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": message_text}
            ]
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                OPENROUTER_API_URL,
                headers=headers,
                json=payload,
                timeout=60.0
            )
            
            response_data = response.json()
            logger.info(f"LLM API response: {response_data}")
            
            # Extract the generated text from the response
            generated_text = response_data["choices"][0]["message"]["content"]
            return generated_text
    
    except Exception as e:
        logger.error(f"Error getting LLM response: {e}")
        return "Przepraszam, nie mogę teraz odpowiedzieć. Spróbuj ponownie później."

async def send_telegram_message(chat_id: int, text: str) -> None:
    """Send message back to Telegram chat"""
    try:
        url = f"{TELEGRAM_API_URL}/sendMessage"
        payload = {
            "chat_id": chat_id,
            "text": text
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload)
            response.raise_for_status()
            
            logger.info(f"Message sent to chat {chat_id}")
    
    except Exception as e:
        logger.error(f"Error sending message to Telegram: {e}")
        raise

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
