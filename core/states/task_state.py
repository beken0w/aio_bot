from aiogram.fsm.state import StatesGroup, State


class TaskState(StatesGroup):
    CREATE_CATEGORY = State()
    GET_CATEGORY = State()
    GET_TITLE = State()
    GET_DESCRIPTION = State()
    GET_TASKS_BY_CATEGORY = State()
