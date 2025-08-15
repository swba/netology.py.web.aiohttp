from datetime import datetime
from typing import List

from sqlalchemy import String, DateTime, ForeignKey
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class BaseModel(DeclarativeBase, AsyncAttrs):
    id: Mapped[int] = mapped_column(primary_key=True)

    def __eq__(self, other):
        return self.id == other.id

    def dict(self) -> dict:
        return {'id': self.id}


class User(BaseModel):
    __tablename__ = 'user'

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False)
    password: Mapped[str] = mapped_column(
        String(200),
        nullable=False)
    email: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        index=True,
        nullable=False)
    ads: Mapped[List['Advertisement']] = relationship(
        back_populates='owner',
        cascade = 'all, delete-orphan')

    def dict(self):
        return super().dict() | {
            'username': self.username,
            'email': self.email
        }


class Advertisement(BaseModel):
    __tablename__ = 'advertisement'

    title: Mapped[str] = mapped_column(
        String(100),
        nullable=False)
    description: Mapped[str] = mapped_column(
        String(100),
        nullable=False)
    created: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.now)
    owner_id: Mapped[int] = mapped_column(
        ForeignKey('user.id'),
        nullable=False)
    owner: Mapped['User'] = relationship(
        back_populates='ads',
        lazy='joined')

    def dict(self):
        return super().dict() | {
            'title': self.title,
            'description': self.description,
            'created': self.created.isoformat(),
            'owner': self.owner.dict(),
        }
