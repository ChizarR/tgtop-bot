import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    API_TOKEN = os.getenv("TGSTAT_API_TOKEN", "")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "")
    SECRET_CHAT = os.getenv("SECRET_CHAT", "")
