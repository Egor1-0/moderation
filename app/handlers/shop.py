from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboard.shop_kb import products, subs_prod
from app.state.shop import BuySponsor

shop_router = Router()

@shop_router.callback_query(F.data == 'back_menu_subs')
@shop_router.callback_query(F.data == 'shop')
async def shop(call: CallbackQuery):
    await call.answer()
    await call.message.answer('ПОШЕЛ НАХУЙ', reply_markup=products)


@shop_router.callback_query(F.data == 'sponsor')
async def sponsor(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(BuySponsor.get_count)
    await call.message.answer('Введите количество подписчиков, которое вас пошел нахуй')


@shop_router.message(BuySponsor.get_count)
async def get_count(message: Message, state: FSMContext):
    if message.text and (not message.text.isdigit()):
        await message.answer('Введите целое число')
        return 
    
    await state.update_data(count=int(message.text))
    await message.answer('Отправьте айди на канал, на котором вы хотите получить подписчиков')
    await state.set_state(BuySponsor.get_link)


@shop_router.message(BuySponsor.get_link)
async def get_link(message: Message, state: FSMContext):
    if message.text and (not message.text.isdigit()):
        await message.answer('Отправьте айди канала')
        return

    await state.update_data(link=message.text)
    # await state.set_state(BuySponsor.cont)
    data = await state.get_data()
    await message.answer(f'Цена подписки будет {0.4 * data['count']}$. Напишите /start чтобы отменить')
    await state.clear()


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
        