import logging
import logging.handlers
import datetime


class CustomFormatter(logging.Formatter):
    def formatTime(self, record):
        dt = datetime.datetime.fromtimestamp(record.created)
        time_part = dt.strftime('%H:%M')
        date_part = dt.strftime('%d.%m.%y')
        return f"{time_part} / {date_part}"


logging.basicConfig(
    filename='main.log',
    level=logging.INFO,
    encoding='utf-8',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger("=>")
logger.setLevel(logging.DEBUG)

# Создаем обработчик, который записывает в файл
handler = logging.FileHandler('app.log', encoding='utf-8')

# Создаем форматер и устанавливаем его для обработчика
formatter = CustomFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Добавляем обработчик в логгер
logger.addHandler(handler)
