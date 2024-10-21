from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.queries import get_user, get_finance
from app.keyboard.user_kb import profile, finance_kb
from config import LINK


user_profile = Router()


@user_profile.callback_query(F.data == 'profile_user')
async def user_profiles(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    finance = await get_finance(call.from_user.id)
    # Динамическое форматирование профиля
    notification_status = "Включено ✅" if user.notification else "Выключено ❌"
    status_display = user.status.value  # Используем значение Enum (например, "Новичок")

    profile_text = (
        f"<b>📖 Личный профиль</b> \n\n"
        f"<b>🔓 Информация:</b>\n"
        f"<b>┣🆔 Мой ID: <code>{user.tg_id}</code></b>\n"
        f"<b>┣✏️ Имя: {user.name or 'Не указано'}</b>\n"
        f"<b>┣💳 Баланс: <code>{finance.balance:.2f} 💲</code></b>\n"
        f"<b>┣🔔 Уведомление: {notification_status}</b>\n"
        f"<b>┗⚜️ Статус: {status_display}</b>\n\n"
        f"<b>❔Winxart team</b>"
    )
    await call.message.edit_text(profile_text, reply_markup=profile)
    

@user_profile.callback_query(F.data == 'my_finance')
async def get_my_finance(call: CallbackQuery):
    await call.answer()
    finance = await get_finance(call.from_user.id)
    await call.message.edit_text(
        f"💸 Мои финансы \n\n"
        f"💳 Информация : \n"
        f"<b>┣💵 Баланс: <code>{finance.balance}</code>💲</b>\n"
        f"<b>┣💰 Всего выводов: <code>{finance.total_findings}</code>💲</b>\n"
        f"<b>┣💸 Всего заработано в тиме: <code>{finance.total_earned}</code>💲</b>\n"
        f"<b>┗🪪 Адрес кошелка: {finance.adress_wallet}</b>", reply_markup=finance_kb
    )
    

@user_profile.callback_query(F.data == 'back_profile')
async def user_profiles(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    finance = await get_finance(call.from_user.id)
    notification_status = "Включено ✅" if user.notification else "Выключено ❌"
    status_display = user.status.value  # Используем значение Enum (например, "Новичок")

    profile_text = (
        f"<b>📖 Личный профиль</b> \n\n"
        f"<b>🔓 Информация:</b>\n"
        f"<b>┣🆔 Мой ID: <code>{user.tg_id}</code></b>\n"
        f"<b>┣✏️ Имя: {user.name or 'Не указано'}</b>\n"
        f"<b>┣💳 Баланс: <code>{finance.balance:.2f} 💲</code></b>\n"
        f"<b>┣🔔 Уведомление: {notification_status}</b>\n"
        f"<b>┗⚜️ Статус: {status_display}</b>\n\n"
        f"<b>❔Winxart team</b>"
    )
    await call.message.edit_text(profile_text, reply_markup=profile)
    

@user_profile.callback_query(F.data == 'refferals_programm')
async def user_profiles(call: CallbackQuery):
    await call.answer()
    await call.message.answer(f'Ваша ссылка: {LINK}?start={hex(call.from_user.id)}')