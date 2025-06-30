from typing import List, Any, TypeVar, Generic, Type, Optional, Dict
from pydantic import BaseModel
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.future import select
from sqlalchemy import update as sqlalchemy_update, delete as sqlalchemy_delete, func
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from bot.dao.database import Base

# Объявляем типовой параметр T с ограничением, что это наследник Base
T = TypeVar("T", bound=Base)


class BaseDAO(Generic[T]):
    model: type[T]

    @classmethod
    async def get_all(cls, session: AsyncSession):
        query = select(cls.model)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_by_id(cls, session: AsyncSession, id_: int):
        logger.info(f"Поиск {cls.model.__name__} c ID: {id_}")
        try:
            query = select(cls.model).filter_by(id=id_)
            result = await session.execute(query)
            record = result.scalar_one_or_none()
            if record:
                logger.info(f"Запись с ID {id_} найдена.")
            else:
                logger.info(f"Запись с ID {id_} не найдена.")
            return record
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при поиске записи с ID {id_}: {e}")
            raise

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        result = cls.model(**kwargs)
        session.add(result)
        try:
            await session.flush()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return result

    @classmethod
    async def update(cls, session: AsyncSession, id_: int, **kwargs):
        query = sqlalchemy_update(cls.model).where(cls.model.id == id_).values(**kwargs).execution_options(synchronize_session="fetch")
        result = await session.execute(query)
        try:
            await session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            raise e

    @classmethod
    async def delete(cls, session: AsyncSession, id_: int):
        query = sqlalchemy_delete(cls.model).where(cls.model.id == id_).execution_options(synchronize_session="fetch")
        result = await session.execute(query)
        try:
            await session.flush()
            return result.rowcount
        except SQLAlchemyError as e:
            await session.rollback()
            raise e


