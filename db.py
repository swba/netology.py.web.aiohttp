from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

import config

engine = create_async_engine(config.DB_URL)
SessionMaker = async_sessionmaker(bind=engine, expire_on_commit=False)


async def drop_tables(model_class: type[DeclarativeBase]) -> None:
    async with engine.begin() as conn:
        await conn.run_sync(model_class.metadata.drop_all)

async def create_tables(model_class: type[DeclarativeBase]):
    async with engine.begin() as conn:
        await conn.run_sync(model_class.metadata.create_all)

async def close():
    await engine.dispose()
