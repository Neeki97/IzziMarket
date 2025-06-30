from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from bot.dao.base import BaseDAO
from bot.dao.models import Product, User, Purchase, Order, Transaction, Payment, OrderStatus, ProductStatus


class ProductDAO(BaseDAO):
    model = Product

    @classmethod
    async def get_by_status(cls, session: AsyncSession):
        query = select(cls.model).where(cls.model.status == ProductStatus.available)
        result = await session.execute(query)
        return result.scalars().all()


class PurchaseDAO(BaseDAO):
    model = Purchase

    @classmethod
    async def get_by_order_id(cls, session: AsyncSession, order_id: int):
        query = select(cls.model).where(cls.model.order_id == order_id)
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_total_sum_by_order_id(cls, session: AsyncSession, order_id: int):
        unit_price = cls.model.unit_price
        qty = cls.model.quantity
        query = select(func.sum(unit_price * qty)).where(cls.model.order_id == order_id)
        result = await session.execute(query)
        total = result.scalars().one_or_none()
        return total

    @classmethod
    async def delete_by_order_id(cls, session: AsyncSession, order_id: int):
        query = select(cls.model).where(cls.model.order_id == order_id)
        await session.execute(query)
        await session.flush()


class UserDAO(BaseDAO):
    model = User


class OrderDAO(BaseDAO):
    model = Order

    @classmethod
    async def get_pending_order_by_user(cls, session: AsyncSession, user_id: int):
        query = select(cls.model).where(cls.model.user_id == user_id, cls.model.status == OrderStatus.pending)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def get_all_orders_by_paid(cls, sesion: AsyncSession):
        query = select(cls.model).where(cls.model.status == OrderStatus.paid)
        result = await sesion.execute(query)
        return result.scalars().all()


class PaymentDAO(BaseDAO):
    model = Payment


class TransactionDAO(BaseDAO):
    model = Transaction

    @classmethod
    async def get_by_order_id(cls, session: AsyncSession, order_id: int):
        query = select(cls.model).where(cls.model.order_id == order_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()