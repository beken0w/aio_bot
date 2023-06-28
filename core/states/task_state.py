from aiogram.fsm.state import StatesGroup, State


class TaskState(StatesGroup):
    GET_TITLE = State()
    GET_DESCRIPTION = State()
