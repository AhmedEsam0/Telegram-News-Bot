from fastapi import FastAPI, Request
import telegram
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

bot = telegram.Bot(token=os.getenv("BOT_TOKEN"))

@app.get("/")
def root():
    return {"message": "Bot is running!"}

@app.post("/execute")
async def execute(request: Request):
    data = await request.json()
    msg = data.get("message")
    if msg:
        bot.send_message(chat_id=os.getenv("CHANNEL_ID"), text=msg)
        return {"status": "sent"}
    return {"status": "no message"}