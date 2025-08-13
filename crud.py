from typing import TypeVar

from sqlalchemy import select, ColumnElement
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

import db
from models import BaseModel

T = TypeVar('T', bound=BaseModel)


async def get(model_cls: type[T], value: int, key: str = 'id') -> T | None:
    field: ColumnElement = getattr(model_cls, key)
    stmt = select(model_cls).where(field == value)
    async with db.SessionMaker() as session: # type: AsyncSession
        result = await session.execute(stmt)
        try:
            return result.scalars().one()
        except NoResultFound:
            return None

async def save(instance: T):
    async with db.SessionMaker() as session: # type: AsyncSession
        async with session.begin():
            session.add(instance)

async def delete(instance: T):
    async with db.SessionMaker() as session: # type: AsyncSession
        await session.delete(instance)
        await session.commit()
