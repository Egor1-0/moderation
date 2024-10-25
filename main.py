import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import TOKEN
from app.database.session import create_session
from app.database.queries import push_prices, get_top_users
from app.handlers import handlers_
from app.handlers.start_handlers import start_router


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    # users = await get_top_users()
    # for i in users:
    #     pass
    await create_session()
    await push_prices()

    dp.include_routers(start_router, handlers_)   

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    


