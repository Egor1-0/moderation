from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from app.database.queries import push_channel
from app.filters import IsAdmin
from app.state.admin_states import AddingFunctions

admin_router = Router()

admin_router.message.filter(IsAdmin())

@admin_router.message(Command('add_channel'))
async def add_channel(message: Message, state: FSMContext):
    await state.set_state(AddingFunctions.add_channel_id)
    await message.answer('Отправьте айди канала')


@admin_router.message(AddingFunctions.add_channel_id)
async def add_channel_id(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(tg_id=message.text)
        await state.set_state(AddingFunctions.add_channel_link)
        await message.answer('Отправьте ссылку на канал')
    else:
        await message.answer('Отпрвьте айди канала')


@admin_router.message(AddingFunctions.add_channel_link)
async def add_channel_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)

    data = await state.get_data()
    await push_channel(data['tg_id'], data['link'])
    await message.answer('Канал добавлен')
    await state.clear()