import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import TOKEN
from app.database.session import create_session
from app.database.queries import push_prices
from app.middlewares.check_ban import CheckBan
from app.handlers import handlers_
from app.handlers.start_handlers import start_router


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    await create_session()
    await push_prices()

    dp.include_routers(start_router, handlers_)   

    dp.update.middleware(CheckBan())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    


