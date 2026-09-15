import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "8953500993:AAHKA7GxIb_bowItU8QxlyqffXhVFMoIEuo")
CHANNEL_ID = int(os.getenv("CHANNEL_ID", "-1004450031548"))
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS", "8415020146").split(",")))
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://aliy-cyber.github.io/winners-academy-bot/")
DB_PATH = os.getenv("DB_PATH", "winners_academy.db")

PHONE_NUMBER = "+998 55 510 98 98"
MANAGER_USERNAME = "@WinnersManager"
MANAGER_URL = "https://t.me/WinnersManager"
TELEGRAM_CHANNEL = "https://t.me/Winners_AcademyUz"
INSTAGRAM = "https://www.instagram.com/winners_academyuz/?__pwa=1"
YOUTUBE = "https://www.youtube.com/@winnersacademyuz"
WEBSITE = "https://winnersacademy.uz/#rec1119205156"

