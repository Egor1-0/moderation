from aiogram import Router, F
from aiogram.types import CallbackQuery

from app.database.queries import get_user, get_finance, get_ref_data
from app.keyboard.user_kb import profile, finance_kb, back_profils

from config import LINK


user_profile = Router()

@user_profile.callback_query(F.data == 'back_profiles')
@user_profile.callback_query(F.data == 'back_profile')
@user_profile.callback_query(F.data == 'back_profile_user')
@user_profile.callback_query(F.data == 'profile_user')
async def user_profiles(call: CallbackQuery):
    await call.answer()
    user = await get_user(call.from_user.id)
    finance = await get_finance(call.from_user.id)
    # Динамическое форматирование профиля
    status_display = user.status.value  # Используем значение Enum (например, "Новичок")
    
    subscription_user = (
       "нет подписки" if user.subscription is None 
        else user.subscription.strftime('%d.%m.%Y')
    )

    profile_text = (
        f"<b>📖 Личный профиль</b> \n\n"
        f"<b>🔓 Информация:</b>\n"
        f"<b>┣🆔 Мой ID: <code>{user.tg_id}</code></b>\n"
        f"<b>┣💳 Баланс: <code>{finance.balance:.2f} 💲</code></b>\n"
        f"<b>┣🗓 Подписка : <code>{subscription_user}</code></b>\n"
        f"<b>┗🏆 Статус: <code>{status_display}</code></b>\n\n"
        f"<b>❔Winxart team</b>"
    )
    await call.message.edit_caption(caption=profile_text, reply_markup=profile)
    

@user_profile.callback_query(F.data == 'my_finance')
async def get_my_finance(call: CallbackQuery):
    await call.answer()
    finance = await get_finance(call.from_user.id)
    await call.message.edit_caption(caption=(
        f"💸 Мои финансы \n\n"
        f"💳 Информация : \n"
        f"<b>┣💵 Баланс: <code>{finance.balance}</code>💲</b>\n"
        f"<b>┣💰 Всего выводов: <code>{finance.total_findings}</code>💲</b>\n"
        f"<b>┣💸 Всего заработано в тиме: <code>{finance.total_earned}</code>💲</b>\n"
        f"<b>┗🪪 Адрес кошелка: <code>{finance.adress_wallet}</code></b>"), reply_markup=finance_kb
    )
    

@user_profile.callback_query(F.data == 'refferals_programm')
async def user_profiles(call: CallbackQuery):
    await call.answer()
    ref_data = await get_ref_data(call.from_user.id) 
    await call.message.edit_caption(caption=(f'<b>💸 Ваша ссылка для приглашение в тиму:  {LINK}?start={hex(call.from_user.id)} \n\n </b>'
                                 f'<b>📊 Статистика ваших приглашение: </b>\n<b> ┣Всего приглашено: <code>{ref_data.invited}</code></b>'
                                 f'\n <b>┗Всего заработано с помощью реф ссылки: <code>{ref_data.total_summ_invited}</code></b>'), disable_web_page_preview=True, reply_markup=back_profils)