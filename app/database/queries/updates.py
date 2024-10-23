from sqlalchemy import update

from app.database.models import Finance, User, Price
from app.database.session import async_session


async def increase_balance_and_invites(user_id: int, amount: float) -> None:
    async with async_session() as session:
        await session.execute(update(Finance)
                              .where(Finance.user_id == user_id)
                              .values(balance=Finance.balance + amount, 
                                      total_summ_invited=Finance.total_summ_invited + amount, 
                                      total_earned=Finance.total_earned + amount))
        
        await session.execute(update(User)
                              .where(User.tg_id == user_id)
                              .values(invited=User.invited + 1))

        await session.commit()


async def become_admin(user_id: int) -> None:
    async with async_session() as session:
        await session.execute(update(User)
                              .where(User.tg_id == user_id)
                              .values(is_admin=True))

        await session.commit()


async def update_price(price: float, name: str) -> None:
    async with async_session() as session:
        await session.execute(update(Price)
                              .where(Price.id == 1)
                              .values({name: price}))

        await session.commit()
        
        
async def update_balance(user_id: int, amount: float) -> None:
    async with async_session() as session:
        await session.execute(update(Finance)
                              .where(Finance.user_id == user_id)
                              .values(balance=Finance.balance + amount))
        
        await session.commit()
        
