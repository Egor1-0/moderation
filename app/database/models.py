from datetime import datetime
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, String, Float, Enum

from sqlalchemy.orm import Mapped, mapped_column
from app.database.base import Base

from enum import Enum


class Statistic:
    total_users:int
    day_users: int
    withdrawal: float

    def __init__(self, total_users, day_user, paid):
        self.total_users = total_users
        self.day_users = day_user
        self.withdrawal = paid

class Status(str, Enum):
    newbie = "Новичок"
    advanced = "Продвинутый"
    professional = "Профессионал"
    master = "Мастер"


class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    name: Mapped[str] = mapped_column(String(35), nullable=True)
    notification: Mapped[bool] = mapped_column(Boolean, default=True)
    status: Mapped[Status] = mapped_column(default=Status.newbie)
    registered_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)


class Finance(Base):
    __tablename__ = 'finance'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey(User.id))
    balance: Mapped[float] = mapped_column(Float, default=0.00)
    total_findings: Mapped[float] = mapped_column(Float, default=0.00)
    total_earned: Mapped[float] = mapped_column(Float, default=0.00)
    total_withdrawal: Mapped[float] = mapped_column(Float, default=0.00)
    adress_wallet: Mapped[str] = mapped_column(String(255), default='Адрес не указан')


class Channel(Base):
    __tablename__ = 'channels'

    id: Mapped[int] = mapped_column(primary_key=True)
    link: Mapped[str] = mapped_column()
    tg_id: Mapped[str] = mapped_column()