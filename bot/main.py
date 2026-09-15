import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import MenuButtonWebApp, WebAppInfo, BotCommand

from bot.config import BOT_TOKEN, WEBAPP_URL
from bot.database import init_db
from bot.handlers import start, courses, branches, contacts, quiz, register, admin

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup(bot: Bot):
    await init_db()
    logger.info("Database initialized.")
    # Pastdagi doimiy WebApp tugmasi
    await bot.set_chat_menu_button(
        menu_button=MenuButtonWebApp(
            text="\U0001f3c6 Winners Academy",
            web_app=WebAppInfo(url=WEBAPP_URL),
        )
    )
    await bot.set_my_commands([
        BotCommand(command="start", description="Bosh sahifa"),
        BotCommand(command="admin", description="Admin panel"),
    ])

    from bot.config import CHANNEL_ID
    try:
        chat = await bot.get_chat(CHANNEL_ID)
        logger.info(f"✅ Kanal muvaffaqiyatli topildi: '{chat.title}' (ID: {CHANNEL_ID})")
    except Exception as e:
        logger.warning(f"⚠️ Kanalga ({CHANNEL_ID}) ulanib bo'lmadi: {e}. Bot kanalga ADMIN qilib qo'shilganini tekshiring!")



async def main():
    bot = Bot(
        token=BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(
        admin.router,
        start.router,
        courses.router,
        branches.router,
        contacts.router,
        quiz.router,
        register.router,
    )
    dp.startup.register(on_startup)
    logger.info("Winners Academy Bot ishga tushmoqda...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
