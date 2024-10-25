from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext

from app.keyboard.start_kb import start
from app.database.queries import push_user
from app.filters import IsExist

start_router = Router()


@start_router.message(CommandStart(), ~IsExist())
async def cmd_start(message: Message, command: CommandObject, state: FSMContext):
    await state.clear()
    await push_user(message.from_user.id, int(command.args, 16) if command.args else None)
    # if not await get_user(message.from_user.id):

    #     inviter = int(command.args, 16) if command.args else None

    #     if inviter and inviter != message.from_user.id:
    #         await increase_balance_and_invites(inviter, 0.4)


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