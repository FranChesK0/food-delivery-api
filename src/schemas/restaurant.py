from pydantic import BaseModel, ConfigDict


class RestaurantAddSchema(BaseModel):
    """
    Restaurant add schema.

    Attributes:
        title (str): Restaurant title
        address (str): Restaurant address
        cuisines (list[str]): List of cuisines
    """

    title: str
    address: str
    cuisines: list[str]

    model_config = ConfigDict(from_attributes=True)


class RestaurantSchema(RestaurantAddSchema):
    """
    Restaurant schema.

    Attributes:
        id (int): Restaurant id
        title (str): Restaurant title
        address (str): Restaurant address
        cuisines (list[str]): List of cuisines
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
