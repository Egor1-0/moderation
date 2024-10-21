from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, CommandObject


soft_handlers = Router()


@soft_handlers.callback_query(F.data == 'soft_panels')
async def my_soft(call: CallbackQuery):
    await call.message.edit_text(
        f'<b>♨️ Софт - Winxart Team </b>\n\n'
        f'<b>🆔 Мой ID: </b>'
        f'<b>💹 Подписка: </b>'
        f'<b>💳 Баланс </b>'
    )