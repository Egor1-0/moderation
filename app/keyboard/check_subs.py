from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.database.queries import get_channels

async def check_subs_kb():
    kb = InlineKeyboardBuilder()
    channels = await get_channels()
    i = 1
    for channel in channels:
        kb.button(text=f'Спонсор {i}', url=channel.link)
        i += 1
    kb.button(text='Проверить подписку', callback_data='check_sub')
    kb.adjust(2)
    return kb.as_markup()