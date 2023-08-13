from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from aiogram.types.inline_keyboard_button import InlineKeyboardButton


def done_delete_kb(id=None, status=0):
    buttons = [
        [
            InlineKeyboardButton(text="Удалить задачу",
                                 callback_data=f"/delete_task {id}"),
        ],
    ]
    if not status:
        buttons[0].append(
            InlineKeyboardButton(text="Выполнить задачу",
                                 callback_data=f"/done_task {id}"))
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def approve_category_kb(id):
    buttons = [
        [
            InlineKeyboardButton(text="Изменить название",
                                 callback_data=f"/change_ctgr {id}"),
            InlineKeyboardButton(text="Удалить",
                                 callback_data=f"/delete_ctgr {id}"),
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def choose_category_kb(titles, show=None):
    if show is None:
        buttons = [[InlineKeyboardButton(
                    text="➕ добавить",
                    callback_data="/create_ctgr")]]
    else:
        buttons = []
    for title in titles:
        buttons.append(
            [InlineKeyboardButton(
                text=title,
                callback_data=f"/choose_ctgr {title}")])
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
