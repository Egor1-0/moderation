from datetime import datetime, timedelta

from sqlalchemy import select, func
from app.database.session import async_session

from app.database.models import User, Finance, Statistic, Channel, Ref, Account, Price, BaseChat
    

async def get_users():
    async with async_session() as session:
        result = await session.scalars(select(User))
        return result

async def get_user(user_id: int):
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == user_id))
        return result

async def get_statistic():
    async with async_session() as session:
        count_users = await session.scalar(select(func.count(User.id))
                                           .select_from(User))
        
        day_users = await session.scalar(select(func.count(User.id))
                                         .select_from(User)
                                         .where(User.registered_at >= datetime.now() - timedelta(days=1)))
        
        paid = await session.scalar(select(func.sum(Finance.total_findings))
                                    .select_from(Finance))

        return Statistic(
            count_users,
            day_users,
            paid
        )

async def get_finance(user_id: int):
    async with async_session() as session:
        # Получаем объект Finance по user_id
        user = await get_user(user_id)
        result = await session.scalar(select(Finance).where(Finance.user_id == user.id))

        # Если записи нет, создаём новую
        if result is None:
            result = Finance(user_id=user_id)
            session.add(result)
            await session.commit()

        return result

async def get_channels():
    async with async_session() as session:
        result = await session.scalars(select(Channel))
        return result

async def get_ref_data(user_id: int):
    async with async_session() as session:
        user = await get_user(user_id)
        result = Ref(await session.scalar(select(User.invited).where(User.tg_id == user_id)),
                     await session.scalar(select(Finance.total_summ_invited).where(Finance.user_id == user.id))
                     )
        return result
    
async def get_my_account(user_id: int):
    async with async_session() as session:
        result = await session.scalar(select(Account).where(Account.user_id == user_id))
        
    return result

async def get_price():
    async with async_session() as session:
        result = await session.scalar(select(Price))
    return result  

async def get_top_users():
    async with async_session() as session:
        result = await session.scalars(select(User).join(Finance))
        print(result)
    return result


async def get_my_bases(user_id: int):
    async with async_session() as sesison:
        result = await sesison.scalar(select(BaseChat).where(BaseChat.user_id == user_id))
        
    return result