from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

from app.keyboard.shop_kb import products, subs_prod, buy_sponsors
from app.state.shop import BuySponsor
from app.database.queries import push_channel


shop_router = Router()

@shop_router.callback_query(F.data == 'back_menu_subs')
@shop_router.callback_query(F.data == 'shop')
async def shop(call: CallbackQuery):
    await call.answer()
    await call.message.edit_caption(caption='<b>🛍 Winxart Маркет </b>', reply_markup=products)
    
    
async def shopv2(call: CallbackQuery):
    await call.answer()
    await call.message.answer_photo(photo=FSInputFile('app/img/img_1.png'), caption='<b>🛍 Winxart Маркет </b>', reply_markup=products)


@shop_router.callback_query(F.data == 'sponsor')
async def sponsor(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(BuySponsor.get_count)
    await call.message.answer('<b>👥 Введите количество подписчиков </b>')


@shop_router.message(BuySponsor.get_count)
async def get_count(message: Message, state: FSMContext):
    if message.text and (not message.text.isdigit()):
        await message.answer('<b>⚠️ Введите целое число!</b>')
        return 
    
    await state.update_data(count=int(message.text))
    await message.answer('🆔 Введите ID канала')
    await state.set_state(BuySponsor.get_id)


@shop_router.message(BuySponsor.get_id)
async def get_id_channels(message: Message, state: FSMContext):
    if message.text and (not message.text.isdigit()):
        await message.answer('⚠️ Введите ID канала ')
        return

    await state.update_data(get_id=message.text)
    await state.set_state(BuySponsor.get_link)
    await message.answer('<b>🔗 Введите ссылку на канал</b>')
    
  
@shop_router.message(BuySponsor.get_link)
async def add_chennels_sponsor(message: Message, state: FSMContext):
    await state.update_data(get_link=message.text)
    data = await state.get_data()
    await message.answer(f'Цена подписки будет {0.4 * data['count']}💲', reply_markup=buy_sponsors)
    
@shop_router.callback_query(F.data == 'buy_sponsor')
async def buy_order(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await push_channel(data['get_id'], data['get_link'])
    await call.message.answer('<b>Канал успешно добавлен</b>')
    await state.clear()
    await shopv2(call)


@shop_router.callback_query(F.data == 'subscribe')
async def subscribe(call: CallbackQuery):
    await call.answer()
    await call.message.answer('ПОШЕЛ НАХУЙ SUBS', reply_markup=await subs_prod())


@shop_router.callback_query(F.data.startswith('edit_'))
async def edit(call: CallbackQuery):
    await call.answer()
    match call.data.split('_')[1]:
        case 'week-price':
            pass
        case 'link':
            pass
        