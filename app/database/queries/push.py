from sqlalchemy import select

from app.database.models import User, Finance
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
