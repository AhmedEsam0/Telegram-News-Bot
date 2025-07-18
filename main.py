from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from telegram import Bot
from dotenv import load_dotenv
import os

# تحميل المتغيرات من .env
load_dotenv()

# إنشاء تطبيق FastAPI
app = FastAPI()

# إعداد CORS للسماح بالاتصال من أي مكان
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ممكن تخليها ["https://your-frontend.com"] لو عايز تأمنها
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# جلب متغيرات البيئة
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# تأكد إن التوكن موجود
if not BOT_TOKEN or not CHANNEL_ID:
    raise Exception("❌ BOT_TOKEN أو CHANNEL_ID مش متسجلين في Environment Variables")

# تهيئة البوت
bot = Bot(token=BOT_TOKEN)

# راوت لاختبار التشغيل
@app.get("/")
def root():
    return {"message": "✅ Bot is running!"}

# راوت للنشر من خلال POST
@app.post("/execute")
async def execute(request: Request):
    try:
        data = await request.json()
        message = data.get("message")

        if not message:
            return {"status": "❌ no message found in request"}

        # إرسال الرسالة
        bot.send_message(chat_id=CHANNEL_ID, text=message)
        return {"status": "✅ message sent", "text": message}

    except Exception as e:
        return {"status": "❌ failed", "error": str(e)}
