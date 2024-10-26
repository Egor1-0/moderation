from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.queries import get_user

start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🚀 Начать! ', callback_data = 'start_traffic')]
])

start_user = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💸 Приступаю к работе!', callback_data='start_work')]
])


async def menu_start(user_id):
    kb = InlineKeyboardBuilder() 
    kb.button(text='🛍 Магазин', callback_data='shop')
    kb.button(text='💻 Профиль', callback_data='profile_user')
    kb.button(text='🎁 Получить', callback_data='bonus')
    kb.button(text='📊 Статистика', callback_data='statistic')
    user = await get_user(user_id)
    if user.is_admin:
        kb.button(text='🔐 Админ панель', callback_data='panels')
    kb.adjust(2)
    return kb.as_markup()
#     InlineKeyboardMarkup(inline_keyboard=[
#     [InlineKeyboardButton(text='🛍 Магазин', callback_data='shop'), InlineKeyboardButton(text='💻 Профиль', callback_data='profile_user')],
#     [InlineKeyboardButton(text='🎁 Получить', callback_data='bonus'), InlineKeyboardButton(text='📊 Статистика', callback_data='statistic')],
# ])

back_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Топ пользователей', callback_data='top_users')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back_menu')]
])