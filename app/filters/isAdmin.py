from aiogram.filters import BaseFilter

from app.database.queries import get_user

class IsAdmin(BaseFilter):
    async def __call__(self, message):

        user = await get_user(message.from_user.id)

        return user.is_admin