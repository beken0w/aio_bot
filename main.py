import os
import logging

from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Text

from core.views.welcome import welcome, start_bot, stop_bot
from core.views.categories import router_cat
from core.views.tasks import router_task


load_dotenv()


# Настройка логгов
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    encoding='utf-8',
    filemode='w',
    format='%(asctime)s | %(levelname)s | %(name)s | %(message)s',
    datefmt=r'| %H:%M | %d.%m.%Y')
logger = logging.getLogger(__name__)


async def start():
    bot = Bot(os.getenv("TOKEN"))
    dp = Dispatcher()

    # при запуске и остановке выводит сообщение админу
    # dp.startup.register(start_bot)
    # dp.shutdown.register(stop_bot)

    # регистируем вьюшкиs
    dp.message.register(welcome, Text('/start'))
    dp.include_routers(router_task, router_cat)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        logger.info("Токен успешно получен. Запускаю бота")
        await dp.start_polling(bot)

    finally:
        await bot.session.close()
        logger.info("Бот остановлен")


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("Программа остановлена пользователем.")
