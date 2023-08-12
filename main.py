import os
import logging
import datetime

from dotenv import load_dotenv
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command

from core.views.welcome import welcome, start_bot, stop_bot
from core.views import tasks
from core.states.task_state import TaskState
from core.views.callback import done_task, delete_task


load_dotenv()


# Настройка логгов
logging.basicConfig(level=logging.INFO,
                    filename='log_file.log',
                    filemode='a')


async def start():
    bot = Bot(os.getenv("TOKEN"))
    dp = Dispatcher()

    # при запуске и остановке выводит сообщение админу
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # регистируем вьюшки
    # Получае данные для создания задачи
    dp.callback_query.register(done_task, F.data.startswith("/done"))
    dp.callback_query.register(delete_task, F.data.startswith("/delete"))
    dp.message.register(tasks.show_tasks, F.text == 'Список задач')
    dp.message.register(tasks.take_id, F.text == 'Создать задачу')
    dp.message.register(tasks.take_title, TaskState.GET_TITLE)
    dp.message.register(tasks.take_desc, TaskState.GET_DESCRIPTION)

    dp.message.register(welcome, CommandStart)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
        date_time = datetime.datetime.now().replace(microsecond=0)
        logging.info(f"\n{'='*30}[ {date_time} ]{'='*30}\n")
        logging.info("Токен успешно получен. Запускаю бота")

    finally:
        await bot.session.close()
        logging.info("Бот остановлен")


if __name__ == '__main__':
    try:
        asyncio.run(start())
    except KeyboardInterrupt:
        print("Программа остановлена пользователем.")
