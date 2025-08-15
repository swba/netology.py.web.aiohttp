from typing import TypeVar

from sqlalchemy import select, ColumnElement
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from models import BaseModel

T = TypeVar('T', bound=BaseModel)


class Crud:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get(self, model_cls: type[T], value: int, key: str = 'id') -> T | None:
        field: ColumnElement = getattr(model_cls, key)
        stmt = select(model_cls).where(field == value)
        try:
            result = await self.session.execute(stmt)
            return result.scalars().one()
        except NoResultFound:
            return None

    async def save(self, instance: T):
        try:
            self.session.add(instance)
            await self.session.commit()
        except IntegrityError:
            await self.session.rollback()
            raise

    async def delete(self, instance: T):
        await self.session.delete(instance)
        await self.session.commit()
