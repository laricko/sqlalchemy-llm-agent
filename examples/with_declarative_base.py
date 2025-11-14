from __future__ import annotations

import os
from datetime import datetime
from typing import List

from sqlalchemy import (
    Boolean,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    create_engine,
    inspect,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship

from sqlalchemy_llm_agent import SqlalchemyAgent, SqlalchemyAgentConfig


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    name: Mapped[str] = mapped_column(String(100))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    orders: Mapped[List["Order"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, email={self.email!r})"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(String(500), nullable=True)
    price: Mapped[float] = mapped_column(Float)
    in_stock: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    items: Mapped[List["OrderItem"]] = relationship(back_populates="product")

    def __repr__(self) -> str:
        return f"Product(id={self.id!r}, name={self.name!r})"


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str] = mapped_column(String(50))
    total_amount: Mapped[float] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)

    user: Mapped["User"] = relationship(back_populates="orders")
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )
    payment: Mapped["Payment | None"] = relationship(
        back_populates="order",
        uselist=False,
    )

    def __repr__(self) -> str:
        return f"Order(id={self.id!r}, user_id={self.user_id!r}, total={self.total_amount!r})"


class OrderItem(Base):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)

    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="items")

    def __repr__(self) -> str:
        return (
            f"OrderItem(id={self.id!r}, order_id={self.order_id!r}, "
            f"product_id={self.product_id!r}, qty={self.quantity!r})"
        )


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), unique=True)
    amount: Mapped[float] = mapped_column(Float)
    provider: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(50))
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    order: Mapped["Order"] = relationship(back_populates="payment")

    def __repr__(self) -> str:
        return f"Payment(id={self.id!r}, order_id={self.order_id!r}, amount={self.amount!r})"


def populate_test_data(engine) -> None:
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        # Users
        user1 = User(
            email="alice@example.com",
            name="Alice",
        )
        user2 = User(
            email="bob@example.com",
            name="Bob",
        )

        # Products
        products = [
            Product(
                name="Wireless Mouse",
                description="Ergonomic 2.4GHz wireless mouse",
                price=19.99,
                in_stock=100,
            ),
            Product(
                name="Mechanical Keyboard",
                description="RGB mechanical keyboard with blue switches",
                price=79.99,
                in_stock=50,
            ),
            Product(
                name="USB-C Hub",
                description="7-in-1 USB-C hub for laptops",
                price=39.99,
                in_stock=80,
            ),
            Product(
                name="27\" 4K Monitor",
                description="Ultra HD IPS monitor",
                price=299.99,
                in_stock=20,
            ),
            Product(
                name="Noise Cancelling Headphones",
                description="Over-ear wireless headphones",
                price=149.99,
                in_stock=35,
            ),
            Product(
                name="Laptop Stand",
                description="Adjustable aluminum laptop stand",
                price=29.99,
                in_stock=60,
            ),
            Product(
                name="External SSD 1TB",
                description="Portable NVMe SSD",
                price=129.99,
                in_stock=40,
            ),
            Product(
                name="Webcam 1080p",
                description="Full HD webcam with microphone",
                price=49.99,
                in_stock=70,
            ),
            Product(
                name="Desk Lamp",
                description="LED desk lamp with brightness control",
                price=24.99,
                in_stock=90,
            ),
            Product(
                name="Gaming Chair",
                description="Ergonomic gaming chair with lumbar support",
                price=199.99,
                in_stock=15,
            ),
        ]

        # Orders
        order1 = Order(
            user=user1,
            status="pending",
            total_amount=0.0,  # will adjust after items
        )
        order2 = Order(
            user=user1,
            status="paid",
            total_amount=0.0,
        )
        order3 = Order(
            user=user2,
            status="paid",
            total_amount=0.0,
        )
        order4 = Order(
            user=user2,
            status="shipped",
            total_amount=0.0,
        )

        # Order items (and compute totals)
        def add_item(order: Order, product: Product, quantity: int) -> OrderItem:
            item = OrderItem(
                order=order,
                product=product,
                quantity=quantity,
                unit_price=product.price,
            )
            order.total_amount += product.price * quantity
            return item

        order_items = [
            add_item(order1, products[0], 2),  # 2x Wireless Mouse
            add_item(order1, products[1], 1),  # 1x Keyboard
            add_item(order2, products[3], 1),  # 1x Monitor
            add_item(order2, products[4], 1),  # 1x Headphones
            add_item(order3, products[6], 1),  # 1x SSD
            add_item(order3, products[2], 2),  # 2x USB-C Hub
            add_item(order4, products[9], 1),  # 1x Gaming Chair
            add_item(order4, products[5], 1),  # 1x Laptop Stand
        ]

        # Payments
        payment1 = Payment(
            order=order2,
            amount=order2.total_amount,
            provider="Stripe",
            status="completed",
            paid_at=datetime.now(),
        )
        payment2 = Payment(
            order=order3,
            amount=order3.total_amount,
            provider="PayPal",
            status="completed",
            paid_at=datetime.now(),
        )
        payment3 = Payment(
            order=order4,
            amount=order4.total_amount,
            provider="Stripe",
            status="pending",
            paid_at=None,
        )

        session.add_all(
            [
                user1,
                user2,
                *products,
                order1,
                order2,
                order3,
                order4,
                *order_items,
                payment1,
                payment2,
                payment3,
            ]
        )
        session.commit()


if __name__ == "__main__":
    engine = create_engine("sqlite:///playground.db", echo=True)
    inspector = inspect(engine)
    populate_test_data(engine)

    sqlalchemy_llm_agent_config = SqlalchemyAgentConfig(
        api_key=os.environ["openai_api_key"],
        tables=["*"],
        inspector=inspector,
        engine=engine,
    )
    agent = SqlalchemyAgent(config=sqlalchemy_llm_agent_config)
    res = agent.query("give me success payments")
    print(res)
