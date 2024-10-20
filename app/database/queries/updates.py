from sqlalchemy import update

from app.database.models import Finance
from app.database.session import async_session


async def increase_balance(user_id: int, amount: float) -> None:
    async with async_session() as session:
        await session.execute(update(Finance)
                              .where(Finance.user_id == user_id)
                              .values(balance=Finance.balance + amount))
        await session.commit()