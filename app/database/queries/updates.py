from sqlalchemy import update

from app.database.models import Finance, User, Price, Account
from app.database.session import async_session
from app.database.queries.requests import get_user
from datetime import datetime, timedelta


async def increase_balance_and_invites(user_id: int, price_ref: float, price_bonus: float) -> None:
    async with async_session() as session:
        user = await get_user(user_id)
        inviter = await get_user(user.inviter)
        await session.execute(update(Finance)
                              .where(Finance.user_id == inviter.id)
                              .values(balance=Finance.balance + price_ref, 
                                      total_summ_invited=Finance.total_summ_invited + price_ref, 
                                      total_earned=Finance.total_earned + price_ref))
        
        await session.execute(update(User)
                              .where(User.tg_id == inviter.tg_id)
                              .values(invited=User.invited + 1))
        
        await session.execute(update(Finance)
                                .where(Finance.user_id == user.id)
                                .values(balance=Finance.balance + price_bonus
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
        
async def update_balance_users(user_id: int, amount: float) -> None:
    async with async_session() as session:
        user = await get_user(user_id)
        await session.execute(update(Finance)
                              .where(Finance.user_id == user.id)
                              .values(balance=Finance.balance - amount))
        
        await session.commit()

async def save_session(user_id: int, session_name: str, phone: str):
    async with async_session() as session:
        await session.execute(update(Account)
                              .where(Account.user_id == user_id)
                              .values(session_name=session_name, phone=phone))
        
        await session.commit()
            
            
async def push_subscription(user_id: int, term_days: int):
    expiration_date = datetime.now() + timedelta(days=term_days)  # Рассчитываем срок подписки

    async with async_session() as session:
        await session.execute(
            update(User)
            .where(User.tg_id == user_id)
            .values(subscription=expiration_date)  # Записываем дату окончания
        )
        await session.commit()
        

async def update_admin(user_id: int, meaning: bool):
    async with async_session() as session:
        await session.execute(
            update(User).where(User.tg_id == user_id)
            .values(is_admin=meaning)
        )
        await session.commit()
    
    
    