from datetime import timedelta

from fastapi import APIRouter

from schemas import OrderSchema, OrderStatus, OrderAddSchema
from scheduler import update_status
from repository import SessionDep, OrderRepository

router = APIRouter(prefix="/order", tags=["Orders"])


@router.post("", summary="Create a new order")
async def create_order(order: OrderAddSchema, session: SessionDep) -> OrderSchema:
    order = await OrderRepository.add_one(order, session)
    update_status(
        order.id, OrderStatus.COOKING, timedelta(seconds=10).total_seconds(), session
    )
    update_status(
        order.id, OrderStatus.DELIVERING, timedelta(minutes=20).total_seconds(), session
    )
    update_status(
        order.id, OrderStatus.DELIVERED, timedelta(minutes=50).total_seconds(), session
    )
    return order


@router.get("/{order_id}", summary="Get order info")
async def get_order(order_id: int, session: SessionDep) -> OrderSchema:
    return await OrderRepository.find(order_id, session)
