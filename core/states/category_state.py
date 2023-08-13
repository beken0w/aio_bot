from aiogram.fsm.state import StatesGroup, State


class CategoryState(StatesGroup):
    CREATE = State()
    CHANGE_TITLE = State()
    GET_TITLE = State()
