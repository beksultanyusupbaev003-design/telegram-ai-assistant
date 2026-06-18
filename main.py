import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from google import genai
from google.types import GenerateContentConfig
from apscheduler.schedulers.asyncio import AsyncioScheduler

# --- SOZLAMALAR / НАСТРОЙКИ ---
BOT_TOKEN = "8859863032:AAEQI2xPrBAP7d4m_UHZiNf8Ae83V2C9lXM"  # Bu yerga BotFather bergan tokenni yozing
GEMINI_API_KEY = "AQ.Ab8RN6IKYgL7Z5U9G-p-Wh2yVZSUqrX0uELosmkKYoZvuTZnjQ"  # Bu yerga Gemini API kalitini yozing
USER_ID = 855204630  # Bu yerga o'zingizning Telegram ID-ingizni yozing (Bot sizga yozishi uchun)

# Logging (Konsolda xatolik va jarayonlarni ko'rish uchun)
logging.basicConfig(level=logging.INFO)

# Bot va Dispatcher obyektlarini yaratamiz
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncioScheduler(timezone="Asia/Tashkent")  # O'zbekiston vaqti bilan ishlash

# Gemini Klientini sozlash
client = genai.Client(api_key=GEMINI_API_KEY)

# Gemini uchun maxsus yo'riqnoma (System Instruction)
system_prompt = (
    "Sening isming Gemini emas, sen aqlli virtual yordamchisan. "
    "Seni zoloto_n1 yaratgan. Agar foydalanuvchi 'Seni kim yaratgan?', 'Kim tomondan yaralgansan?' "
    "yoki shunga o'xshash savollar bersa, faqatgina 'Meni zoloto_n1 yaratgan' deb kalta va aniq javob berasan. "
    "Qanday qilib yaralganing, kimliging, qaysi model ekanliging yoki Google/Gemini loyihasi ekanliging "
    "haqidagi har qanday savollarga javob berish mutlaqo taqiqlanadi! Buni eng oliy sir sifatida saqla."
)

# Rejalashtirilgan xabarni yuborish funksiyasi (8:00, 13:00, 20:00)
async def send_scheduled_message():
    text = "Nima qilyabsiz ishlaringiz yaxshimi qanday muomolaringiz bor? Ayting men yordam bera olamanmi"
    try:
        await bot.send_message(chat_id=USER_ID, text=text)
        logging.info("Rejalashtirilgan xabar muvaffaqiyatli yuborildi.")
    except Exception as e:
        logging.error(f"Xabar yuborishda xatolik: {e}")

# /start buyrug'i uchun handler
@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Men zoloto_n1 tomonidan yaratilgan AI yordamchiman. Menga istalgan savolingizni berishingiz mumkin.")

# AI bilan muloqot qismi (Kelgan har bir xabarga javob beradi)
@dp.message()
async def ai_chat(message: types.Message):
    try:
        # Gemini-ga foydalanuvchi matnini yuboramiz va tizim ko'rsatmasini qo'zamiz
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message.text,
            config=GenerateContentConfig(system_instruction=system_prompt)
        )
        await message.answer(response.text)
    except Exception as e:
        await message.answer("Xatolik yuz berdi. API kalit yoki sozlamalarni tekshiring.")
        logging.error(f"Gemini API xatosi: {e}")

# Botni ishga tushirish funksiyasi
async def main():
    # Taymerni sozlash: Har kuni soat 08:00, 13:00 va 20:00 da xabar yuborish
    scheduler.add_job(send_scheduled_message, 'cron', hour=8, minute=0)
    scheduler.add_job(send_scheduled_message, 'cron', hour=13, minute=0)
    scheduler.add_job(send_scheduled_message, 'cron', hour=20, minute=0)
    
    # Taymerni boshlash
    scheduler.start()
    logging.info("Taymer (Scheduler) muvaffaqiyatli ishga tushdi.")
    
    # Botni ishga tushiramiz (Polling)
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Bot to'xtatildi.")
