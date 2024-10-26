from sqlalchemy import select

from app.database.models import User, Finance, Channel, Price, Account, BaseChat, Slot
from app.database.session import async_session

async def push_prices() -> None:
    async with async_session() as session:
        price = await session.scalar(select(Price).where(Price.id == 1))
        if not price:
            session.add(Price())
            await session.commit()

async def push_user(tg_id: int, inviter: int = None) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id, inviter=inviter)
            session.add(new_user)
            await session.flush()
            
            session.add(Account(user_id=new_user.id))
            session.add(Finance(user_id=new_user.id))
            await session.commit()


async def push_channel(tg_id: str, link: str) -> None:
    async with async_session() as session:
        channel = await session.scalar(select(Channel).where(Channel.tg_id == tg_id))

        if not channel:
            session.add(Channel(tg_id=tg_id, link=link))
            await session.commit()
            
            
async def save_chat_base(tg_id: str, name_base: str, chat_link: str) -> None:
    async with async_session() as session:
        
        new_base_chat = BaseChat(user_id=tg_id, name_base=name_base, chat_link=chat_link)
        session.add(new_base_chat)
        
        await session.commit()
        
        
async def add_tastk(tg_id: int, name_task: str, name_base: str, text_sms: str, flow: int, interval: int):
    async with async_session() as session:
        
        new_task = Slot(user_id=tg_id, name_slot=name_task, chat_base=name_base, text_sms=text_sms, flow=flow, interval=interval)
        session.add(new_task)
        
        await session.commit()
        
    