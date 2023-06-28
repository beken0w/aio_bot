from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.keyboard_button import KeyboardButton


def permanent_kb():
    btns = [
        [KeyboardButton(text="Создать задачу"),
         KeyboardButton(text="Список задач")],
    ]
    kb = ReplyKeyboardMarkup(keyboard=btns, resize_keyboard=True)
    return kb
