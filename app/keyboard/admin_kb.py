from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆔 Поиск пользователя', callback_data='search_user')],
    [InlineKeyboardButton(text='🆔 Добавить канал', callback_data='add_channel')],
    [InlineKeyboardButton(text='🆔 Рассылка юзерам', callback_data='mass_send')],
    [InlineKeyboardButton(text='🆔 Добавить админа', callback_data='add_admin')],
    [InlineKeyboardButton(text='🆔 Изменить цену', callback_data='edit_price')],
])