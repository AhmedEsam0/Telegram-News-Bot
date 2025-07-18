from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from telegram import Bot
import os

# تحميل متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# إنشاء البوت
bot = Bot(token=BOT_TOKEN)

# إنشاء تطبيق FastAPI
app = FastAPI()

# عرض ملف index.html من مجلد static
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def home():
    return FileResponse("static/index.html")

@app.post("/chatgpt-control")
async def post_message(request: Request):
    try:
        data = await request.json()
        message = data.get("message")
        if message:
            bot.send_message(chat_id=CHANNEL_ID, text=message)
            return {"status": "✅ sent"}
        else:
            return JSONResponse(status_code=400, content={"status": "❌", "error": "No message provided"})
    except Exception as e:
        return JSONResponse(status_code=500, content={"status": "❌", "error": str(e)})
