from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from app.keyboard.start_kb import start, start_user, menu_start, back_start
from app.database.queries import push_user, get_statistic, increase_balance_and_invites, get_user
from app.filters import IsExist

from config import PHOTO

start_handler = Router()


# @start_handler.callback_query(F.data == 'check_sub')
# async def check_sub(call: CallbackQuery):
#     await call.answer()

#     await call.message.answer('Вы подписались на канал')



@start_handler.message(CommandStart(), ~IsExist())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    if not await get_user(message.from_user.id):

        inviter = int(command.args, 16) if command.args else None

        if inviter and inviter != message.from_user.id:
            await increase_balance_and_invites(inviter, 0.4)


    await message.answer(
    "<b>🚀 Добро пожаловать в мир арбитража трафика!</b>\n\n"
    "Здесь вы сможете превратить поток трафика в стабильный доход, даже если только начинаете. "
    "Мы шаг за шагом проведем вас через все этапы: "
    "<i>от выбора лучших офферов и запуска кампаний до анализа результатов и масштабирования.</i> 📊\n\n"
    "<b>✨ Что вас ждет:</b>\n"
    "• Пошаговые инструкции и проверенные стратегии;\n"
    "• Поддержка на всех этапах и индивидуальные консультации;\n"
    "• Доступ к эксклюзивным офферам и бонусам от партнеров.\n\n"
    "<b>💸 Выплаты и бонусы:</b>\n"
    "Каждая успешная кампания принесет вам доход. Мы гарантируем прозрачные условия и "
    "своевременные выплаты. 🔥\n\n"
    "<b>Готовы начать путь к успеху?</b> Присоединяйтесь к нам прямо сейчас и сделайте "
    "первые шаги к стабильному заработку!", reply_markup=start
)


@start_handler.message(CommandStart())
async def cmd_start(message: Message):    
    photo = PHOTO
    await message.answer_photo(
        photo=photo, caption="<b>🌊 Панель управление:</b>", reply_markup=menu_start
    )


@start_handler.callback_query(F.data == 'start_traffic')
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

@start_handler.callback_query(F.data == 'check_sub')
@start_handler.callback_query(F.data == 'start_work')
async def menu(call: CallbackQuery):
    await call.answer()
    
    photo = PHOTO
    await call.message.answer_photo(
        photo=photo, caption="<b>🌊 Панель управления:</b>", reply_markup=menu_start
    )
    

@start_handler.callback_query(F.data == 'statistic')
async def statistic_viewing(call: CallbackQuery):
    await call.answer()
    statistic_all = await get_statistic()

    await call.message.edit_caption(caption=(
        f"<b>📊 Статистика </b>\n"
        f"<b>┣Всего пользователей: </b> <code>{statistic_all.total_users}</code>\n"
        f"<b>┣За сегодня: </b> <code>{statistic_all.day_users}</code>\n"
        f"<b>┗Выплачено: </b> <code>{statistic_all.withdrawal}</code>"), reply_markup=back_start)


@start_handler.callback_query(F.data == 'back_starts')
@start_handler.callback_query(F.data == 'back_shop')
@start_handler.callback_query(F.data == 'back_menu')
async def menu(call: CallbackQuery):
    await call.answer()
    
    photo = PHOTO
    await call.message.edit_caption(
        photo=photo, caption="<b>🌊 Панель управление:</b>", reply_markup=menu_start
    )
    
