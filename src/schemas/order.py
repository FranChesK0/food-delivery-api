from pydantic import BaseModel, ConfigDict

from .database_types import OrderStatus


class OrderAddSchema(BaseModel):
    """
    Order add schema.

    Attributes:
        restaurant_id (int): Restaurant id
        items (list[int]): List of menu item ids
        address (str): User address
        comment (str): User comment
    """

    restaurant_id: int
    items: list[int]
    address: str
    comment: str = ""

    model_config = ConfigDict(from_attributes=True)


class OrderSchema(OrderAddSchema):
    """
    Order schema.

    Attributes:
        id (int): Order id
        status (OrderStatus): Order status
        restaurant_id (int): Restaurant id
        items (list[int]): List of menu item ids
        address (str): User address
        comment (str): User comment
    """

    id: int
    status: OrderStatus

    model_config = ConfigDict(from_attributes=True)
