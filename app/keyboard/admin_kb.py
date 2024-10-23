from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


admin_panel_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🆔 Поиск пользователя', callback_data='search_user')],
    [InlineKeyboardButton(text='📢 Спонсоры', callback_data='add_channel')],
    [InlineKeyboardButton(text='💬 Рассылка юзерам', callback_data='mass_send')],
    [InlineKeyboardButton(text='✏️ Изменить цены', callback_data='edit_price')],
])

admin_search_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💳 Пополнить баланс ', callback_data='replenish_user'), InlineKeyboardButton(text='❌ Удалить пользователя', callback_data='delete_user')],
    [InlineKeyboardButton(text='🎁 Подарить подписку', callback_data='give_subscription'), InlineKeyboardButton(text='⭐️ Сделать админом', callback_data='do_user_admin')],
    [InlineKeyboardButton(text='💬 Написать сообщение', callback_data='send_message_user')]
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