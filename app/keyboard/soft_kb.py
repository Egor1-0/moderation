from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


soft_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='🗂 Создать задачу', callback_data='create_task'), InlineKeyboardButton(text='💻 Аккаунты ', callback_data='my_accounts')],
    [InlineKeyboardButton(text='🔍 Мои задачи', callback_data='static_task'), InlineKeyboardButton(text='🗄 База чатов', callback_data='my_base')],
    [InlineKeyboardButton(text='🔙 Назад', callback_data='profile_user')]
])



def generate_account_kb(account_count: int) -> InlineKeyboardMarkup:
    """Генерирует клавиатуру с помощью Builder в зависимости от количества аккаунтов."""
    builder = InlineKeyboardBuilder()

    if account_count >= 1:
        builder.button(text='❌ Удалить аккаунт', callback_data='delete_account')
        builder.button(text='🔙 Назад', callback_data='back_profile_acc')
    else:
        builder.button(text='➕ Добавить аккаунт', callback_data='add_account')
        builder.button(text='🔙 Назад', callback_data='back_profile_acc')

    return builder.adjust(1).as_markup()



soft_start = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='✅ Начать рассылку', callback_data='start_task')]
])