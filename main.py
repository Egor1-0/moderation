import logging
import asyncio

from aiogram import Dispatcher, Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from config import TOKEN
from app.database.session import create_session
from app.handlers import handlers_
from app.middlewares.check_subscription import CheckSubscription


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()

    await create_session()

    dp.message.middleware(CheckSubscription())
    dp.callback_query.middleware(CheckSubscription())

    dp.include_routers(handlers_)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass

