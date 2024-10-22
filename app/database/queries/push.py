from sqlalchemy import select

from app.database.models import User, Finance, Channel, Invite_link
from app.database.session import async_session


async def push_user(tg_id: int, name: str) -> None:
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            new_user = User(tg_id=tg_id, name=name)
            session.add(new_user)
            await session.flush()

            session.add(Finance(user_id=tg_id))
            await session.commit()


async def push_channel(tg_id: str, link: str) -> None:
    async with async_session() as session:
        channel = await session.scalar(select(Channel).where(Channel.tg_id == tg_id))

        if not channel:
            session.add(Channel(tg_id=tg_id, link=link))
            await session.commit()
            
            
# async def update_static_link(tg_id: int, user: int, earned: int):
#     async with async_session() as session:
#         updates_static = await session.scalar(select(Invite_link).where(Invite_link.user_id == tg_id))
        