from aiogram import Bot
from aiogram.types import CallbackQuery
from core.database.db_task import Task
from core.keyboards.inline import done_delete_kb

obj = Task()


async def done_task(call: CallbackQuery):
    task_id = call.data.split()[1]
    user_id = call.from_user.id
    message_id = call.message.message_id
    updated_text = call.message.text.replace('💼 Не выполнена', '✅ Выполнена')
    kb = done_delete_kb(task_id, status=1)
    await call.message.edit_text(inline_message_id=message_id,
                                 text=updated_text)
    await call.message.edit_reply_markup(message_id,
                                         reply_markup=kb)
    obj.update_status(user_id, task_id)


async def delete_task(call: CallbackQuery):
    task_id = call.data.split()[1]
    user_id = call.from_user.id
    message_id = call.message.message_id
    await call.message.edit_text(inline_message_id=message_id,
                                 text=f"Задача {task_id} удалена")
    obj.delete_task(user_id, task_id)
