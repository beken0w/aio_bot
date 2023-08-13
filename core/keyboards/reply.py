from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


def permanent_kb():
    btns = [
        [
            KeyboardButton(text="📌 Создать задачу"),
            KeyboardButton(text="➕ Новая категория")
        ],
        [
            KeyboardButton(text="🗄️ Список задач"),
            KeyboardButton(text="🗂️ Мои категории")
        ],
        [
            KeyboardButton(text="📂 Задачи по категориям")
        ]
    ]
    kb = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)
    return kb
