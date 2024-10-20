from datetime import datetime, timedelta

from sqlalchemy import select, func
from app.database.session import async_session

from app.database.models import User, Finance, Statistic
    
    
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
        
        paid = await session.scalar(select(func.sum(Finance.total_withdrawal))
                                    .select_from(Finance))


        return Statistic(
            count_users,
            day_users,
            paid
        )


async def get_finance(user_id: int):
    async with async_session() as session:
        # Получаем объект Finance по user_id
        result = await session.scalar(select(Finance).where(Finance.user_id == user_id))

        # Если записи нет, создаём новую
        if result is None:
            result = Finance(user_id=user_id)
            session.add(result)
            await session.commit()

        return result