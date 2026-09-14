import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8953500993:AAHKA7GxIb_bowItU8QxlyqffXhVFMoIEuo")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1004450031548"))
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "0").split(",")))
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://winners-academy.netlify.app")
DB_PATH = os.getenv("DB_PATH", "winners_academy.db")

PHONE_NUMBER = "+998 55 510 98 98"
MANAGER_USERNAME = "@WinnersManager"
TELEGRAM_CHANNEL = "https://t.me/Winners_AcademyUz"
INSTAGRAM = "https://www.instagram.com/winners_academyuz"
YOUTUBE = "https://www.youtube.com/@winnersacademyuz"
WEBSITE = "https://winnersacademy.uz"
