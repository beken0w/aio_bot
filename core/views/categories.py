from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from aiogram import Bot, Router, F
from aiogram.filters import Text

from core.states.category_state import CategoryState
from core.keyboards.inline import approve_category_kb
from core.database.db_category import Category
from core.database.db_task import Task

obj = Category()
router_cat = Router()
task = Task()


@router_cat.message(Text('➕ Новая категория'))
async def category_create(message: Message, state: FSMContext):
    await state.update_data(user_id=message.from_user.id)
    await message.answer("Введите название Категории ⬇️")
    await state.set_state(CategoryState.GET_TITLE)


@router_cat.message(CategoryState.GET_TITLE)
async def category_create_finish(message: Message, state: FSMContext):
    await state.update_data(new_title=message.text)
    context_data = await state.get_data()
    obj.create_category(context_data)
    await state.clear()

    text = obj.get_category(context_data)[0]
    await message.answer(text="📂 " + str(text[2]),
                         reply_markup=approve_category_kb(str(text[0])))


@router_cat.message(Text('🗂️ Мои категории'))
async def show_catogories(message: Message, bot: Bot):
    user_id = message.from_user.id
    result = obj.get_all_categories(user_id)
    if result:
        for i in range(len(result)):
            kb = approve_category_kb(result[i][0])
            await message.answer(text="📂 " + result[i][2], reply_markup=kb)
    else:
        sticker = "CAACAgIAAxkBAAEJiEhknb2jxsbNGXKMX"\
                  "JcKSowK2dGg1gACSxYAArVkIEitLhBSiib0gS8E"
        await bot.send_sticker(chat_id=message.chat.id, sticker=sticker)
        await message.answer(text="Вы еще не создали категории =(")


@router_cat.callback_query(F.data.startswith("/delete_ctgr"))
async def delete_category(call: CallbackQuery):
    await call.answer()

    ctgr_id = call.data.split()[1]
    user_id = call.from_user.id
    message_id = call.message.message_id
    title = obj.is_exist(user_id, ctgr_id)
    if title:
        obj.delete_category(user_id, ctgr_id)
        await call.message.edit_text(inline_message_id=message_id,
                                     text=f"Категория {title[0]} удалена")
    else:
        await call.message.edit_text(
            inline_message_id=message_id,
            text="Упс, такой категории не существует")
    call.answer()


@router_cat.callback_query(F.data.startswith("/change_ctgr"))
async def category_change(call: CallbackQuery, state: FSMContext):
    await call.answer()

    ctgr_id = call.data.split()[1]
    user_id = call.from_user.id
    message_id = call.message.message_id
    await state.update_data(mess_id=message_id)
    await state.update_data(user_id=call.from_user.id)

    title = obj.is_exist(user_id, ctgr_id)

    if title:
        await call.message.answer(
            f"Текущее название: {title[0]}\n"
            f"{'-'*70}\n"
            "Введите новое название Категории ⬇️")
        await state.update_data(old_title=title)
        await state.set_state(CategoryState.CHANGE_TITLE)
    else:
        await call.message.answer("Такой категории больше нет")
        await state.clear()


@router_cat.message(CategoryState.CHANGE_TITLE)
async def category_change_finish(message: Message, state: FSMContext):
    await state.update_data(new_title=message.text)
    context_data = await state.get_data()
    obj.update_title(context_data)
    task.update_category(context_data)
    await state.clear()

    text = obj.get_category(context_data)[0]
    await message.answer(text="📂 " + str(text[2]),
                         reply_markup=approve_category_kb(str(text[0])))
