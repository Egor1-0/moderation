from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart

from app.keyboard.start_kb import start_user, menu_start, back_start
from app.database.queries import get_statistic, increase_balance_and_invites, get_user, get_price

menu_handler = Router()





@menu_handler.message(CommandStart())
async def cmd_start(message: Message):    
    photo = "https://i.imgur.com/Jcn6mjE.png"
    await message.answer_photo(
        photo=photo, caption="<b>🌊 Панель управление:</b>", reply_markup=menu_start
    )


@menu_handler.callback_query(F.data == 'start_traffic')
async def start_one(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        "<b>Хотите начать зарабатывать прямо сейчас?</b>\n\n"
        "Нажмите на кнопку <i>«Генерация ссылки»</i>, и бот создаст вашу уникальную ссылку. "
        "С ее помощью вы сможете привлекать трафик и зарабатывать на каждой конверсии! 💸\n\n"
        "Чем больше переходов по вашей ссылке — тем выше ваш доход. Вся аналитика будет доступна в личном кабинете, а выплаты — в удобное для вас время. 🚀\n\n"
        "Начните прямо сейчас и откройте для себя новые возможности заработка!", reply_markup=start_user
    )

# @start_handler.message(F.photo)
# async def get_photo_id(message: Message):
#     # Берём самое большое фото (последнее в списке)
#     file_id = message.photo[-1].file_id

#     # Отправляем пользователю file_id
#     await message.answer(f"ID вашего фото: {file_id}")

@menu_handler.callback_query(F.data == 'check_sub')
@menu_handler.callback_query(F.data == 'start_work')
async def menu(call: CallbackQuery):
    await call.answer()
    
    photo = "https://i.imgur.com/Jcn6mjE.png"
    await call.message.answer_photo(
        photo=photo, caption="<b>🌊 Панель управления:</b>", reply_markup=menu_start
    )
    

@menu_handler.callback_query(F.data == 'statistic')
async def statistic_viewing(call: CallbackQuery):
    await call.answer()
    statistic_all = await get_statistic()

    await call.message.edit_caption(caption=(
        f"<b>📊 Статистика </b>\n"
        f"<b>┣Всего пользователей: </b> <code>{statistic_all.total_users}</code>\n"
        f"<b>┣За сегодня: </b> <code>{statistic_all.day_users}</code>\n"
        f"<b>┗Выплачено: </b> <code>{statistic_all.withdrawal}</code>"), reply_markup=back_start)


@menu_handler.callback_query(F.data == 'top_users')
async def top_users(call: CallbackQuery):
    await call.answer()


@menu_handler.callback_query(F.data == 'back_menu')
async def menu(call: CallbackQuery):
    await call.answer()
    
    photo = "https://i.imgur.com/Jcn6mjE.png"
    await call.message.edit_caption(
        photo=photo, caption="<b>🌊 Панель управление:</b>", reply_markup=menu_start
    )


@menu_handler.callback_query(F.data == 'bonus')
async def bonus(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    price = await get_price()
    if not user.active and user.inviter:
        await increase_balance_and_invites(call.from_user.id, price.price_ref, price.price_bonus)
        await call.message.answer(f'<b>🎁 Вы получили бонус в размере {price.price_bonus}$</b>')
    else:
        await call.message.answer('<b>❗️ Вы уже получали бонус / Вы не приглащены не кем</b>')