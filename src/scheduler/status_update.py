import asyncio
import threading

from sqlalchemy.ext.asyncio import AsyncSession

from schemas import OrderStatus
from repository import OrderRepository


def update_status(
    id: int, status: OrderStatus, delay: float, session: AsyncSession
) -> None:
    def task() -> None:
        try:
            asyncio.run(OrderRepository.update_status(id, status, session))
        except RuntimeError:
            asyncio.get_event_loop().create_task(
                OrderRepository.update_status(id, status, session)
            )

    threading.Timer(interval=delay, function=task).start()
