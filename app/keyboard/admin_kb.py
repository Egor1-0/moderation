from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆔 Поиск пользователя', callback_data='search_user')]
])