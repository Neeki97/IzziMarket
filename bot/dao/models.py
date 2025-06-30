from typing import List, Optional
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, ForeignKey, Float, String, Enum as SQLEnum
from bot.dao.database import Base
from enum import Enum


class ProductStatus(str, Enum):
    available = 'available'
    out_of_stock = 'out of stock'
    archvied = 'archived'


class OrderStatus(str, Enum):
    pending = 'pending'
    paid = 'paid'
    cancelled = 'cancelled'


class TransactionStatus(str, Enum):
    pending = "pending"
    success = "success"
    failed = "failed"


class User(Base):
    __tablename__ = 'users'

    chat_id: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    phone: Mapped[int] = mapped_column(BigInteger, unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(30), nullable=True)
    last_name: Mapped[str] = mapped_column(String, nullable=True)

    orders: Mapped[List['Order']] = relationship(back_populates='user', cascade='all, delete-orphan')


class Product(Base):
    __tablename__ = 'products'

    name: Mapped[str]
    description: Mapped[str] = mapped_column(String)
    price: Mapped[Float] = mapped_column(Float, nullable=False)
    stock: Mapped[int] = mapped_column(ge=0)
    status: Mapped[ProductStatus] = mapped_column(SQLEnum(ProductStatus), default=ProductStatus.available)

    purchases: Mapped[List['Purchase']] = relationship(back_populates='product', cascade="all, delete-orphan")


class Purchase(Base):
    __tablename__ = 'purchases'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey('products.id'), nullable=False)
    quantity: Mapped[int] = mapped_column(ge=0)
    unit_price: Mapped[float] = mapped_column(ge=0)

    order: Mapped['Order'] = relationship(back_populates='purchases')
    product: Mapped['Product'] = relationship(back_populates='purchases')


class Order(Base):
    __tablename__ = 'orders'

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    total_price: Mapped[float] = mapped_column(ge=0)
    status: Mapped[OrderStatus] = mapped_column(SQLEnum(OrderStatus), default=OrderStatus.pending)

    user: Mapped["User"] = relationship(back_populates="orders")
    purchases: Mapped[List["Purchase"]] = relationship(back_populates="order", cascade="all, delete-orphan")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="order", cascade="all, delete-orphan")


class Payment(Base):
    __tablename__ = "payments"

    name: Mapped[str]
    description: Mapped[Optional[str]]
    is_active: Mapped[bool] = mapped_column(default=True)

    transactions: Mapped[List['Transaction']] = relationship(back_populates='payment', cascade='all, delete-orphan')


class Transaction(Base):
    __tablename__ = 'transactions'

    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=False)
    payment_id: Mapped[int] = mapped_column(ForeignKey('payments.id'), nullable=False)
    amount: Mapped[float] = mapped_column(ge=0)
    status: Mapped[TransactionStatus] = mapped_column(SQLEnum(TransactionStatus), default=TransactionStatus.pending)

    order: Mapped['Order'] = relationship(back_populates='transactions')
    payment: Mapped['Payment'] = relationship(back_populates='transactions')
