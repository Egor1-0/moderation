from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.keyboard.shop_kb import products
from app.state.shop import BuySponsor

shop_router = Router()


@shop_router.callback_query(F.data == 'shop')
async def shop(call: CallbackQuery):
    await call.answer()
    await call.message.answer('ПОШЕЛ НАХУЙ', reply_markup=products)


@shop_router.callback_query(F.data == 'sponsor')
async def sponsor(call: CallbackQuery, state: FSMContext):
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

"""
покупка спонсорства: цена, колво - подписок (0.4 доллара 1 подписка) 



"""