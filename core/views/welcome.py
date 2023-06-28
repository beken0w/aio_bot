import os
from aiogram.types import Message
from aiogram import Bot
from dotenv import load_dotenv

from core.keyboards.reply import permanent_kb


load_dotenv()

MY_TG_ID = os.getenv("MY_TG_ID")


async def start_bot(bot: Bot):
    await bot.send_message(MY_TG_ID, "Бот запущен")


async def stop_bot(bot: Bot):
    await bot.send_message(MY_TG_ID, "Бот остановлен")


async def welcome(message: Message, bot: Bot):
    await message.answer(f"Привет, {message.from_user.first_name}",
                         reply_markup=permanent_kb())
