from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from app.database.queries import get_channels, push_user
from app.keyboard.check_subs import check_subs_kb


class CheckSubscription(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        channels = await get_channels()
        message = event if isinstance(event, Message) else None 

        callback = event if isinstance(event, CallbackQuery) else None 

        if message:
            await push_user(message.from_user.id)
            for channel in channels:
                try:
                    is_subscribed = await event.bot.get_chat_member('-100' + channel.tg_id, message.from_user.id)
                    
                    if is_subscribed.status == 'left':
                        await message.answer(f'Подпишитесь на все каналы спонсоры', reply_markup=await check_subs_kb())
                        return None
                except Exception as exception:
                    # return None
                    print(exception, event)

            return await handler(event, data)

        elif callback:
            for channel in channels:
                await push_user(callback.from_user.id)
                try:
                    is_subscribed = await event.bot.get_chat_member('-100' + channel.tg_id, callback.from_user.id)
                    
                    if is_subscribed.status == 'left':
                        await callback.message.answer(f'Подпишитесь на все каналы спонсоры', reply_markup=await check_subs_kb())
                        return None
                except Exception as exception:
                    # return None
                    print(exception, event)

            return await handler(event, data)