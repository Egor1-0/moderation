# from typing import Callable, Dict, Any, Awaitable
# from aiogram import BaseMiddleware
# from aiogram.types import TelegramObject, Message, CallbackQuery

# from app.database.queries import get_user


# # class CheckBan(BaseMiddleware):
# #     async def __call__(
# #         self,
# #         handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
# #         event: TelegramObject,
# #         data: Dict[str, Any]
# #     ) -> Any:
        
# #         update = event.message or event.callback_query or None

# #         if not update:
# #             return

# #         user = await get_user(update.from_user.id)

# #         if not user.banned:
# #             return await handler(event, data)
# #         else:
# #             if isinstance(update, Message):
# #                 await update.answer('Вы забанены')
# #             elif isinstance(update, CallbackQuery):
# #                 await update.answer('')
# #                 await update.message.answer('Вы забанены')