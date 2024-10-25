from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚀 Начать! ', callback_data = 'start_traffic')]
])

start_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💸 Приступаю к работе!', callback_data='start_work')]
])


menu_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🛍 Магазин', callback_data='shop'), InlineKeyboardButton(text='💻 Профиль', callback_data='profile_user')],
    [InlineKeyboardButton(text='🍯 Winxart pass', callback_data='winxart_pass'), InlineKeyboardButton(text='📊 Статистика', callback_data='statistic')],
    [InlineKeyboardButton(text='🎁 Получить', callback_data='bonus')]  
])

back_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back_starts')]
])