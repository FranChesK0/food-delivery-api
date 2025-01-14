from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from schemas import OrderStatus

from .database import Model


class Restaurant(Model):
    """
    Restaurant table model.

    Attributes:
        id (int): Restaurant id.
        title (str): Title of the restaurant.
        address (str): Address of the restaurant.
        cuisines (List[str]): List of cuisines served at the restaurant.
    """

    _repr_columns_number = 3

    title: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    address: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)
    cuisines: Mapped[list[str]] = mapped_column(JSON)


class Schedule(Model):
    """
    Restaurant schedule table model.

    Attributes:
        id (int): Schedule id.
        restaurant_id (int): Restaurant id.
        start (str): Schedule start time.
        end (str): Schedule end time.
    """

    _repr_columns_number = 5

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"), nullable=True
    )
    start: Mapped[str] = mapped_column(nullable=False)
    end: Mapped[str] = mapped_column(nullable=False)


class Category(Model):
    """
    Category table model.

    Attributes:
        id (int): Category id.
        name (str): Category name.
    """

    _repr_columns_number = 2

    name: Mapped[str] = mapped_column(unique=True, index=True, nullable=False)


class MenuItem(Model):
    """
    Menu item table model.

    Attributes:
        id (int): Menu item id.
        restaurant_id (int): Restaurant id.
        category_id (int): Category id.
        name (str): Menu item name.
        price (float): Menu item price.
        description (str): Menu item description.
    """

    _repr_columns_number = 5

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"), nullable=False
    )
    category_id: Mapped[int] = mapped_column(ForeignKey("categorys.id"), nullable=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[float] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)


class Order(Model):
    """
    Order table model.

    Attributes:
        id (int): Order id.
        restaurant_id (int): Restaurant id.
        items (List[int]): List of menu item ids.
        address (str): User address.
        comment (str): User comment.
        status (OrderStatus): Order status.
    """

    restaurant_id: Mapped[int] = mapped_column(
        ForeignKey("restaurants.id"), nullable=False
    )
    items: Mapped[list[int]] = mapped_column(JSON)
    address: Mapped[str] = mapped_column(nullable=False)
    comment: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[OrderStatus] = mapped_column(nullable=False)
