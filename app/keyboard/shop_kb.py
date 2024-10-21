from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


products = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Спонсорство', callback_data='sponsor')],
    [InlineKeyboardButton(text='Подписка', callback_data='subscribe')],
])