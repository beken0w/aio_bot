import os
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from aiogram import Bot

from core.states.task_state import TaskState
from core.keyboards.inline import done_delete_kb
from core.database.db_task import Task

obj = Task()


async def take_id(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer("Введите заголовок задачи ⬇️")
    await state.set_state(TaskState.GET_TITLE)


async def take_title(message: Message, state: FSMContext):
    await message.answer("Введите описание задачи ⬇️")
    await state.set_state(TaskState.GET_DESCRIPTION)
    await state.update_data(title=message.text)


async def take_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    context_data = await state.get_data()
    obj.create_task(context_data)
    await state.clear()

    user_id = message.from_user.id
    ids, statuses, result = obj.get_task(user_id)
    kb = done_delete_kb(ids[0], statuses[0])
    await message.answer(text=result[0], reply_markup=kb)


async def show_tasks(message: Message):
    user_id = message.from_user.id
    ids, statuses, result = obj.get_tasks(user_id)
    if ids:
        for i in range(len(ids)):
            kb = done_delete_kb(ids[i], status=statuses[i])
            await message.answer(text=result[i], reply_markup=kb)
