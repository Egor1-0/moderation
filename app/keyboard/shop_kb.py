from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


products = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Спонсорство 🎉', callback_data='sponsor'), InlineKeyboardButton(text='Подписка 📅', callback_data='subscribe')],
    [InlineKeyboardButton(text='🔚 Назад', callback_data='back_shop')],
])


async def subs_prod():
    kb = InlineKeyboardBuilder()
    kb.button(text='📆 Неделя', callback_data='edit_week-price')
    kb.button(text='📆 Месяц', callback_data='edit_month-price')
    kb.button(text='📆 Год', callback_data='edit_year-price')
    kb.button(text='🔙 Назад', callback_data='back_menu_subs')
    kb.adjust(1)
    return kb.as_markup()


buy_sponsors = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Оплатит', callback_data='buy_sponsor')]
])