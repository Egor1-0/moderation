from sqlalchemy import update

from app.database.models import Finance, User, Price, Account
from app.database.session import async_session
from app.database.queries.requests import get_user


async def increase_balance_and_invites(user_id: int, amount: float) -> None:
    async with async_session() as session:
        user = await get_user(user_id)
        inviter = await get_user(user.inviter)
        await session.execute(update(Finance)
                              .where(Finance.user_id == inviter.id)
                              .values(balance=Finance.balance + amount, 
                                      total_summ_invited=Finance.total_summ_invited + amount, 
                                      total_earned=Finance.total_earned + amount))
        
        await session.execute(update(User)
                              .where(User.tg_id == inviter.tg_id)
                              .values(invited=User.invited + 1))
        
        await session.execute(update(Finance)
                                .where(Finance.user_id == user.id)
                                .values(balance=Finance.balance + amount
                            ))

        await session.execute(update(User)
                            .where(User.tg_id == user_id)
                            .values(active = True)
                            )

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
        user = await get_user(user_id)
        await session.execute(update(Finance)
                              .where(Finance.user_id == user.id)
                              .values(balance=Finance.balance + amount))
        
        await session.commit()
        

async def save_session(user_id: int, session_name: str, phone: str):
    async with async_session() as session:
        await session.execute(update(Account)
                              .where(Account.user_id == user_id)
                              .values(session_name=session_name, phone=phone))
        
        await session.commit()
            