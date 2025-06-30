from datetime import datetime
from bot.config import database_url
from sqlalchemy import func, TIMESTAMP, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession


# Создание асинхронного движка для подключения к БД
engine = create_async_engine(url=database_url)

# Создание фабрики сессий
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Базовый класс для моделей
class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        attrs = ", ".join(
            f"{key}={getattr(self, key)!r}" for key in self.__mapper__.c.keys()
        )
        return f"<{self.__class__.__name__}({attrs})>"


# отключил, так как буду использовать мидлвары (позже удалить)
# def connection(method):
#     async def wrapper(*args, **kwargs):
#         async with async_session_maker() as session:
#             try:
#                 return await method(*args, session=session, **kwargs)
#             except Exception as e:
#                 await session.rollback()
#                 raise e
#     return wrapper
