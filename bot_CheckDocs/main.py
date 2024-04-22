import asyncio
import os

from aiogram import Bot, Dispatcher, types
from aiogram.client.bot import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())

from handlers import user_private
from common.bot_cmds_list import private

# ALLOWED_UPDATES = ["message", "edited_message"]

bot = Bot(token=os.getenv("BOT_TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_router(
    user_private.user_private_router
)  # Бот обрабатывает только личные сообщения от пользователя.


async def start():
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_my_commands(
            commands=private, scope=types.BotCommandScopeAllPrivateChats()
        )
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    print("Бот запущен")
    asyncio.run(start())
