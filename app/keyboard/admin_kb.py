from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆔 Поиск пользователя', callback_data='search_user')],
    [InlineKeyboardButton(text='🆔 Добавить канал', callback_data='add_channel')],
    [InlineKeyboardButton(text='🆔 Рассылка юзерам', callback_data='mass_send')],
    [InlineKeyboardButton(text='🆔 Добавить админа', callback_data='add_admin')],
    [InlineKeyboardButton(text='🆔 Изменить цену', callback_data='edit_price')],
])


def subs_prod_price():
    kb = InlineKeyboardBuilder()
    kb.button(text='Неделя', callback_data='edit-price_week')
    kb.button(text='Месяц', callback_data='edit-price_month')
    kb.button(text='Год', callback_data='edit-price_year')
    kb.button(text='Реферальное вознаграждение', callback_data='edit-price_ref')
    kb.button(text='Спонсор', callback_data='edit-price_sponsor')
    kb.button(text='наазд', callback_data='back-menu_subs')
    kb.adjust(2)
    return kb.as_markup()