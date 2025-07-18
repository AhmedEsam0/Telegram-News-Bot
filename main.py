from fastapi import FastAPI, Request
from telegram import Bot
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# Get bot token and channel ID from environment
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Initialize the Telegram bot
bot = Bot(token=BOT_TOKEN)

@app.get("/")
def root():
    return {"message": "Bot is running ✅"}

@app.post("/execute")
async def execute(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        print(f"Execute endpoint message: {message}")
        if message:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            return {"status": "sent"}
        return {"status": "no message provided"}
    except Exception as e:
        print(f"Error in /execute: {e}")
        return {"status": "error", "detail": str(e)}

@app.post("/chatgpt-control")
async def control_from_chatgpt(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        print(f"Message received from ChatGPT: {message}")
        if message:
            bot.send_message(chat_id=CHANNEL_ID, text=message + "\n\n(sent from ChatGPT)")
            return {"status": "sent from ChatGPT"}
        return {"status": "no message provided"}
    except Exception as e:
        print(f"Error in /chatgpt-control: {e}")
        return {"status": "error", "detail": str(e)}
