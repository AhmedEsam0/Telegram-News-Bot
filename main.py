from fastapi import FastAPI, Request
from telegram import Bot
from dotenv import load_dotenv
import os

# تحميل المتغيرات من .env
load_dotenv()

app = FastAPI()

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = Bot(token=BOT_TOKEN)

@app.get("/")
def root():
    return {"message": "Bot is running!"}

# المسار الأساسي اللي بتستخدمه بنفسك
@app.post("/execute")
async def execute(request: Request):
    data = await request.json()
    message = data.get("message")
    if message:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        return {"status": "sent"}
    return {"status": "no message"}

# ✅ المسار اللي أنا (ChatGPT) هستخدمه
@app.post("/chatgpt-control")
async def chatgpt_control(request: Request):
    data = await request.json()
    message = data.get("message")
    
    if not message:
        return {"status": "no message"}

    try:
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        return {"status": "sent from ChatGPT"}
    except Exception as e:
        return {"status": "failed", "error": str(e)}
