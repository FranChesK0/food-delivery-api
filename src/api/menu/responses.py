from pydantic import BaseModel

from schemas import CategorySchema, MenuItemSchema


class Item(BaseModel):
    category: CategorySchema
    items: list[MenuItemSchema]


class Menu(BaseModel):
    restaurant_id: int
    items: list[Item]
