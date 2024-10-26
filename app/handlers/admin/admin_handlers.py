from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from app.database.queries import (push_channel, get_user,
                                  get_finance, get_users,
                                  become_admin, update_price, 
                                  update_balance, push_subscription, 
                                  update_admin)
from app.filters import IsAdmin
from app.state.admin_states import AddChannel, FindUser, MassSend, AddAdmin, UpdatePrice
from app.keyboard.admin_kb import (admin_panel_kb, subs_prod_price,
                                   admin_search_kb, subs_give, admin_user)

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
            await state.update_data(find_user=user.tg_id)
            await message.answer(
                f'<b>🆔 ID: </b> <code>{user.tg_id}</code>\n'
                f'<b>💰 Баланс: </b> <code>{finance.balance}</code>\n'
                f'<b>👥 Пригласил: </b><code>{user.invited}</code>\n'
                f'<b>💸 Всего заработано:</b> <code>{finance.total_earned}</code>\n'
                f'<b>💳 Адрес кошелка: <code>{finance.adress_wallet}</code> </b>', reply_markup=admin_search_kb
            )
        else:
            await message.answer('Пользователь не найден')
            await state.clear()
    else:
        await message.answer('Отправьте айди пользователя')

@admin_router.callback_query(F.data == 'replenish_user')
async def replenish_user_id(call: CallbackQuery, state: FSMContext):
    await state.set_state(FindUser.amount_money)
    await call.message.edit_text('<b>Введите сумму 💸</b>')
    


@admin_router.message(FindUser.amount_money)
async def add_money_user(message: Message, state: FSMContext):
    user_id = await state.get_data()
    if message.text.isdigit():
        await update_balance(user_id['find_user'], message.text)
        await message.answer('<b>Сумма успешно пополнено ✅</b>')
        await admin_panel(message)
        state.clear()
    else:
        await message.answer('<b>Введите сумму 💸</b>')
        
    
@admin_router.callback_query(F.data == 'send_message_user')
async def send_message_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(FindUser.text_send)
    await call.message.answer('<b>💬 Введите свое сообщений </b>')
    
    
@admin_router.message(FindUser.text_send)
async def sens_sms_user(message: Message, state: FSMContext):
    user_id = await state.get_data()
    user = user_id['find_user']
    try:
        await message.copy_to(user)
    except:
        pass
    await message.answer('<b>✅ Сообщение отправлено </b>')
    await state.clear()
    
    
@admin_router.callback_query(F.data == 'mass_send')
async def mass_send(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(MassSend.get_mes)
    await call.message.answer('<b>💬 Введите свое сообщений</b>')


@admin_router.message(MassSend.get_mes)
async def get_mes(message: Message, state: FSMContext):
    users = await get_users()
    for user in users:
        try:
            await message.copy_to(user.tg_id)
        except:
            pass
    await message.answer('<b>✅ Сообщение отправлено</b>')
    await state.clear()
    

@admin_router.callback_query(F.data == 'add_channel')
async def add_channel(call: CallbackQuery, state: FSMContext):
    await state.set_state(AddChannel.add_channel_id)
    await call.message.answer('<b>🆔 Введите ID канала</b>')


@admin_router.message(AddChannel.add_channel_id)
async def add_channel_id(message: Message, state: FSMContext):
    if message.text.isdigit():
        await state.update_data(tg_id=message.text)
        await state.set_state(AddChannel.add_channel_link)
        await message.answer('<b>🔗 Введите ссылку на канал</b>')
    else:
        await message.answer('<b>🆔 Введите ID канала</b>')


@admin_router.message(AddChannel.add_channel_link)
async def add_channel_link(message: Message, state: FSMContext):
    await state.update_data(link=message.text)

    data = await state.get_data()
    await push_channel(data['tg_id'], data['link'])
    await message.answer('<b>✅ Канал добавлен</b>')
    await state.clear()


@admin_router.callback_query(F.data == 'edit_price')
async def edit_price(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(UpdatePrice.name_price)
    await call.message.answer('<b>🔍 Выберите раздел где хотите сменить цену </b>', reply_markup=subs_prod_price())


@admin_router.callback_query(UpdatePrice.name_price)
async def edit_price_name(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.update_data(name=call.data.split('-')[1])
    await state.set_state(UpdatePrice.price)
    await call.message.answer('<b>✏️ Введите цену </b>')


@admin_router.message(UpdatePrice.price)
async def edit_price(message: Message, state: FSMContext):
    try:
        price = float(message.text)
    except:
        await message.answer('<b>⚠️ Отправьте целое число</b>')
        return
    data = await state.get_data()
    await update_price(price, data['name'])
    await message.answer('✅ Цена обновлена')
    await state.clear()
    
    
@admin_router.callback_query(F.data == 'give_subscription')
async def give_subscription_user(call: CallbackQuery, state: FSMContext):
    await state.set_state(FindUser.subscription)
    await call.message.answer("<b>📆 Выберите срок подписки </b>", reply_markup=await subs_give())
    
    
@admin_router.callback_query(FindUser.subscription)
async def give_subscription_users(call: CallbackQuery, state: FSMContext):
    await state.update_data(subscription=call.data.split('-')[1])
    data = await state.get_data()
    match call.data.split('_')[1]:
        case 'week-price':
            await call.message.answer('<b>🎁 Подписка оформлена </b>')
            await push_subscription(data['find_user'], 7)
            await admin_panel(call.message)
            await state.clear()
        case 'month-price':
            await call.message.answer('<b>🎁 Подписка оформлена </b>')
            await push_subscription(data['find_user'], 30)
            await admin_panel(call.message)
            await state.clear()
        case 'year-price':
            await call.message.answer('<b>🎁 Подписка оформлена </b>')
            await push_subscription(data['find_user'], 365)
            await admin_panel(call.message)
            await state.clear()
            
            
@admin_router.callback_query(F.data == 'do_user_admin')
async def admin_users(call: CallbackQuery, state: FSMContext):
    await call.message.answer('<b>Выберите действие </b>', reply_markup=admin_user)
   
@admin_router.callback_query(F.data == 'add_admin_users')
async def add_admins(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await update_admin(data['find_user'], True)
    await call.message.answer('<b>⭐️ пользователь теперь админ </b>')
    await state.clear()

@admin_router.callback_query(F.data == 'del_admin_users')
async def add_admins(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await update_admin(data['find_user'], False)
    await call.message.answer('<b>⭐️ пользователь снять с админки </b>')
    await state.clear()

    


    