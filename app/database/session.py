from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database.queries.push import push_prices
from app.database.models import *
from app.database.base import Base
from config import URL

engine = create_async_engine(URL)

async_session = async_sessionmaker(engine)


async def create_session():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
        await push_prices()

