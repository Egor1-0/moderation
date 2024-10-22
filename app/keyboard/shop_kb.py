from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.queries import get_products

products = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Спонсорство', callback_data='sponsor')],
    [InlineKeyboardButton(text='Подписка', callback_data='subscribe')],
])


async def subs_prod():
    kb = InlineKeyboardBuilder()
    prods = await get_products()
    for prod in prods:
        kb.button(text=prod.name, callback_data=f'buy_{prod.id}')
    kb.adjust(2)
    kb.button(text='🔙 Назад', callback_data='back_menu_subs')
    return kb.as_markup()