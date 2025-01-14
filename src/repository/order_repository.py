from loguru import logger
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import OrderSchema, OrderStatus, OrderAddSchema

from .models import Order


class OrderRepository:
    @classmethod
    @logger.catch
    async def add_one(cls, order: OrderAddSchema, session: AsyncSession) -> OrderSchema:
        logger.debug(f"Adding {order}")
        order_dict = order.model_dump()
        order_orm = Order(**order_dict)
        session.add(order_orm)

        await session.flush()
        await session.commit()

        logger.info(f"Added {order}")
        return OrderSchema.model_validate(order_orm)

    @classmethod
    @logger.catch
    async def find(cls, id: int, session: AsyncSession) -> OrderSchema:
        logger.debug(f"Finding order {id}")
        order_orm = await session.execute(select(Order).where(Order.id == id))
        order = order_orm.scalars().one_or_none()
        if order is None:
            raise ValueError(f"Order {id} not found")

        logger.info(f"Found order {id}")
        return OrderSchema.model_validate(order)

    @classmethod
    @logger.catch
    async def update_status(
        cls, id: int, status: OrderStatus, session: AsyncSession
    ) -> OrderSchema:
        logger.debug(f"Updating order {id} status to {status}")
        order_orm = await session.execute(select(Order).where(Order.id == id))
        order = order_orm.scalars().one_or_none()
        if order is None:
            raise ValueError(f"Order {id} not found")

        order.status = status

        await session.flush()
        await session.commit()

        logger.info(f"Updated order {id} status to {status}")
        return OrderSchema.model_validate(order)
