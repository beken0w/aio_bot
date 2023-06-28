from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


def done_delete_kb(id=None, status=0):
    buttons = [
        [
            InlineKeyboardButton(text="Удалить задачу",
                                 callback_data=f"/delete {id}"),
        ],
    ]
    if not status:
        buttons[0].append(
            InlineKeyboardButton(text="Выполнить задачу",
                                 callback_data=f"/done {id}"))
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
