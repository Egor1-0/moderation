from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚀 Начать! ', callback_data = 'start_traffic')]
])

start_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💸 Приступаю к работе!', callback_data='start_work')]
])


menu_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛍 Магазин', callback_data='shop'), InlineKeyboardButton(text='💻 Профиль', callback_data='profile_user')],
    [InlineKeyboardButton(text='🎁 Получить', callback_data='bonus'), InlineKeyboardButton(text='📊 Статистика', callback_data='statistic')],
])

back_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Топ пользователей', callback_data='top_users')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back_menu')]
])