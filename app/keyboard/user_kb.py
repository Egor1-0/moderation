from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

profile = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='💸 Финансы', callback_data='my_finance')],
    [InlineKeyboardButton(text='📢 Рефералка', callback_data='refferals_programm'), InlineKeyboardButton(text='🗂 Аккаунты', callback_data='accounts_panels')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back_menu')],
])


finance_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='📥 Пополнить', callback_data='replenish_balance'), 
     InlineKeyboardButton(text='📤 Вывести', callback_data='withdraw_balance')],
    [InlineKeyboardButton(text='💳 Добавить адрес', callback_data='add_adress')], 
    [InlineKeyboardButton(text='🔙 Назад', callback_data='back_profile')]
])
