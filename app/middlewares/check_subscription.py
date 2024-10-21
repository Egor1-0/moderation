from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from app.database.queries import get_channels

class CheckSubscription(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        channels = await get_channels()
        
        for channel in channels:
            try:
                is_subscribed = await event.bot.get_chat_member('-100' + channel.tg_id, event.from_user.id)
                
                if is_subscribed.status == 'left':
                    await event.answer(f'Вы не подписались на канал {channel.link}')
                    return None
            except Exception as exception:
                print(exception)

        return await handler(event, data)