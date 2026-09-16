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



import os
from aiohttp import web

async def handle_health_check(request):
    return web.Response(text="Winners Academy Bot is alive and running 24/7!")


async def start_web_server():
    port_str = os.getenv("PORT")
    if port_str:
        port = int(port_str)
        app = web.Application()
        app.router.add_get("/", handle_health_check)
        app.router.add_get("/health", handle_health_check)
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        logger.info(f"Health-check web server started on port {port}")


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

    await start_web_server()

    logger.info("Winners Academy Bot ishga tushmoqda...")
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())

