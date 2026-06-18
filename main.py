print("Telegram AI Assistant ishga tushdi!")
import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8859863032:AAG4pj0ybaGJdblqiIc_DF6rtOLiLpcrvV4")
GEMINI_API_KEY = os.getenv("AQ.Ab8RN6IKYgL7Z5U9G-p-Wh2yVZSUqrX0uELosmkKYoZvuTZnjQ")

print("===================================")
print("Telegram AI Assistant")
print("Bot Token:", BOT_TOKEN)
print("Gemini API:", GEMINI_API_KEY)
print("Bot ishga tushdi!")
print("===================================")
