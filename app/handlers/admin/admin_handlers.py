from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from app.database.queries import push_channel, get_user, get_finance, get_users, become_admin, update_price
from app.filters import IsAdmin
from app.state.admin_states import AddChannel, FindUser, MassSend, AddAdmin, UpdatePrice
from app.keyboard.admin_kb import admin_panel_kb, subs_prod_price

admin_router = Router()

admin_router.message.filter(IsAdmin())
admin_router.callback_query.filter(IsAdmin())

@admin_router.message(Command('panels'))
async def admin_panel(message: Message):
    await message.answer('<b>🗃 Админ панель Winxart Team </b>', reply_markup=admin_panel_kb)


@admin_router.callback_query(F.data == 'search_user')
async def search_user(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(FindUser.find_user)
    await call.message.answer('Отправьте айди пользователя')


@admin_router.message(FindUser.find_user)
async def find_user(message: Message, state: FSMContext):
    if message.text.isdigit():
        user = await get_user(int(message.text))
        finance = await get_finance(int(message.text))
        if user and finance:
            await message.answer(
                f'<b>🆔 ID: </b> {user.tg_id}\n'
                f'<b>👤 Имя: </b> {user.name}\n'
                f'<b>💰 Баланс: </b> {finance.balance}\n'
                f'пришфвыаждовжп: {user.invited}\n'
                f'allasdf: {finance.total_earned}\n'
            )
            await state.clear()
        else:
            await message.answer('Пользователь не найден')
            await state.clear()
    else:
        await message.answer('Отправьте айди пользователя')


@admin_router.callback_query(F.data == 'mass_send')
async def mass_send(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(MassSend.get_mes)
    await call.message.answer('Отправьте сообщение, которое должно быть разослано')


@admin_router.message(MassSend.get_mes)
async def get_mes(message: Message, state: FSMContext):
    users = await get_users()
    for user in users:
        try:
            await message.copy_to(user.tg_id)
        except:
            pass
    await message.answer('Сообщение разослано')
    await state.clear()


@admin_router.callback_query(F.data == 'add_admin')
async def add_admin(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(AddAdmin.add_admin_id)
    await call.message.answer('Отправьте айди пользователя')


@admin_router.message(AddAdmin.add_admin_id)
async def add_admin_id(message: Message, state: FSMContext):
    if message.text.isdigit():
        if await get_user(int(message.text)):
            await become_admin(int(message.text))
            await message.answer('Админ добавлен')
            await state.clear()
        else:
            await message.answer('Пользователь не найден')
            await state.clear()
    else:
        await message.answer('Отправьте айди пользователя')


    

@admin_router.callback_query(Command('add_channel'))
async def add_channel(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddChannel.add_channel_id)
    await call.message.answer('Отправьте айди канала')


@admin_router.message(AddChannel.add_channel_id)
async def add_channel_id(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(tg_id=message.text)
        await state.set_state(AddChannel.add_channel_link)
        await message.answer('Отправьте ссылку на канал')
    else:
        await message.answer('Отпрвьте айди канала')


@admin_router.message(AddChannel.add_channel_link)
async def add_channel_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)

    data = await state.get_data()
    await push_channel(data['tg_id'], data['link'])
    await message.answer('Канал добавлен')
    await state.clear()


@admin_router.callback_query(F.data == 'edit_price')
async def edit_price(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(UpdatePrice.name_price)
    await call.message.answer('Выьериту цену которую хотите изменить', reply_markup=subs_prod_price())


@admin_router.callback_query(UpdatePrice.name_price)
async def edit_price_name(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(name=call.data.split('-')[1])
    await state.set_state(UpdatePrice.price)
    await call.message.answer('Отправьте цену')


@admin_router.message(UpdatePrice.price)
async def edit_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except:
        await message.answer('Отправьте целое число')
        return
    data = await state.get_data()
    await update_price(price, data['name'])
    await message.answer('Цена изменена')
    await state.clear()