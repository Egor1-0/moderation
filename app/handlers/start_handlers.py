from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject

from app.keyboard.start_kb import start, start_user, menu_start

from app.database.queries import push_user, get_statistic, increase_balance, get_user

start_handler = Router()


@start_handler.message(CommandStart())
async def cmd_start(message: Message, command: CommandObject):

    if not await get_user(message.from_user.id):
        await push_user(message.from_user.id, message.from_user.full_name)

        inviter = int(command.args, 16) if command.args else None

        if inviter and inviter != message.from_user.id:
            await increase_balance(inviter, 0.4)

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


@start_handler.callback_query(F.data == 'start_work')
async def menu(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        f"<b>💻 Winxart team </b>\n\n"
        f"<b>📚 Информация :</b>\n"
        f"<b>┣Всего пользователей : </b>\n"
        f"<b>┣За сегодня:</b>\n"
        f"<b>┗Пришло по вашей ссылки:</b>\n\n"
        f"<b>🔒 Панель управление Winxart team </b>", reply_markup=menu_start
    )
    

@start_handler.callback_query(F.data == 'statistic')
async def statistic_viewing(call: CallbackQuery):
    await call.answer()
    statistic_all = await get_statistic()

    await call.message.answer(
        f"📊 Статистика \n"
        f"<b>┣Всего пользователей: </b> <i>{statistic_all.total_users}</i>\n"
        f"<b>┣За сегодня: </b> <i>{statistic_all.day_users}</i>\n"
        f"<b>┗Выплачено: </b> <i>{statistic_all.withdrawal}</i>"
    )

@start_handler.callback_query(F.data == 'back_menu')
async def menu(call: CallbackQuery):
    await call.answer()
    await call.message.edit_text(
        f"<b>💻 Winxart team </b>\n\n"
        f"<b>📚 Информация :</b>\n"
        f"<b>┣Всего пользователей : </b>\n"
        f"<b>┣За сегодня:</b>\n"
        f"<b>┗Пришло по вашей ссылки:</b>\n\n"
        f"<b>🔒 Панель управление Winxart team </b>", reply_markup=menu_start
    )