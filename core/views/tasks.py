from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram import Bot, Router
from aiogram import F

from core.states.task_state import TaskState
from core.database.db_task import Task
from core.database.db_category import Category
from core.keyboards.inline import done_delete_kb, choose_category_kb


obj = Task()
router_task = Router()
cat = Category()


@router_task.message(Text('📌 Создать задачу'))
async def task_create(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)
    context = {'user_id': user_id, 'new_title': 'Основная'}
    if not cat.get_category(context):
        cat.create_category(context)
    titles = [title[2] for title in cat.get_all_categories(user_id)]
    kb = choose_category_kb(titles)
    await message.answer("Выберите категорию задачи ⬇️",
                         reply_markup=kb)
    await state.set_state(TaskState.GET_CATEGORY)


@router_task.callback_query(TaskState.GET_CATEGORY)
async def task_create_category(call: CallbackQuery, state: FSMContext):
    await call.answer()
    if call.data == '/create_ctgr':
        await call.message.answer("Введите название Категории ⬇️")
        await state.set_state(TaskState.CREATE_CATEGORY)
        return
    await call.message.edit_text(
        f"Выбрана категория: {call.data.replace('/choose_ctgr ', '')}")
    await state.update_data(category=call.data.replace('/choose_ctgr ', ''))
    await call.message.answer("Введите заголовок задачи ⬇️")
    await state.set_state(TaskState.GET_TITLE)


@router_task.message(TaskState.CREATE_CATEGORY)
async def task_create_category_finish(message: Message, state: FSMContext):
    await state.update_data(new_title=message.text)
    context_data = await state.get_data()
    cat.create_category(context_data)
    await state.clear()
    await task_create(message, state)


@router_task.message(TaskState.GET_TITLE)
async def task_create_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)
    await message.answer("Введите описание задачи ⬇️")
    await state.set_state(TaskState.GET_DESCRIPTION)


@router_task.message(TaskState.GET_DESCRIPTION)
async def task_create_desc(message: Message, state: FSMContext):
    await state.update_data(desc=message.text)
    context_data = await state.get_data()
    obj.create_task(context_data)
    await state.clear()

    user_id = message.from_user.id
    ids, statuses, result = obj.get_task(user_id)
    kb = done_delete_kb(ids[0], statuses[0])
    await message.answer(text=result[0], reply_markup=kb)


@router_task.message(Text('🗄️ Список задач'))
async def show_tasks(message: Message, state: FSMContext):
    user_id = message.from_user.id
    ids, statuses, result = obj.get_tasks(user_id)
    if ids:
        for i in range(len(ids)):
            kb = done_delete_kb(ids[i], status=statuses[i])
            await message.answer(text=result[i], reply_markup=kb)
            await state.clear()
    else:
        await message.answer(text="Список задач пуст")


@router_task.message(Text('📂 Задачи по категориям'))
async def show_tasks_by_category(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id)

    titles = [title[2] for title in cat.get_all_categories(user_id)]
    kb = choose_category_kb(titles, True)
    await message.answer("Выберите категорию задачи ⬇️",
                         reply_markup=kb)
    await state.set_state(TaskState.GET_TASKS_BY_CATEGORY)


@router_task.callback_query(TaskState.GET_TASKS_BY_CATEGORY)
async def show_tasks_by_category_finish(call: CallbackQuery,
                                        state: FSMContext):
    await call.answer()
    await call.message.delete()
    await state.update_data(category=call.data.replace('/choose_ctgr ', ''))
    context_data = await state.get_data()

    ids, statuses, result = obj.get_tasks_by_category(context_data)
    if ids:
        for i in range(len(ids)):
            kb = done_delete_kb(ids[i], status=statuses[i])
            await call.message.answer(text=result[i], reply_markup=kb)
    else:
        await call.message.answer(
            text=f"Список категории '{context_data['category']}' пуст")
    await state.clear()


@router_task.callback_query(F.data.startswith("/done_task"))
async def done_task(call: CallbackQuery, state: FSMContext):
    await call.answer()

    task_id = call.data.split()[1]
    user_id = call.from_user.id
    message_id = call.message.message_id

    if obj.is_exist(user_id, task_id) == (1,) and\
       obj.check_status(user_id, task_id) != (1,):
        obj.update_status(user_id, task_id)
        updated_text = call.message.text.replace(
            '💼 Не выполнена', '✅ Выполнена')
        kb = done_delete_kb(task_id, status=1)
        await call.message.edit_text(inline_message_id=message_id,
                                     text=updated_text)
        await call.message.edit_reply_markup(message_id,
                                             reply_markup=kb)

    elif obj.check_status(user_id, task_id) == (1,):
        updated_text = call.message.text.replace(
            '💼 Не выполнена', '✅ Выполнена')
        kb = done_delete_kb(task_id, status=1)
        await call.message.edit_text(inline_message_id=message_id,
                                     text=updated_text)
        await call.message.edit_reply_markup(message_id,
                                             reply_markup=kb)

    else:
        await call.message.edit_text(
            inline_message_id=message_id,
            text=f"Упс, задача {task_id} была ранее удалена")
    await state.clear()


@router_task.callback_query(F.data.startswith("/delete_task"))
async def delete_task(call: CallbackQuery, state: FSMContext):
    await call.answer()

    task_id = call.data.split()[1]
    user_id = call.from_user.id
    message_id = call.message.message_id

    if obj.is_exist(user_id, task_id) == (1,):
        await call.message.edit_text(inline_message_id=message_id,
                                     text="Задача удалена")
        obj.delete_task(user_id, task_id)
    else:
        await call.message.edit_text(
            inline_message_id=message_id,
            text="Упс, задача была ранее удалена")
    await state.clear()
