from pydantic import BaseModel, ConfigDict


class RestaurantAddSchema(BaseModel):
    """
    Restaurant add schema.

    Attributes:
        title (str): Restaurant title
        address (str): Restaurant address
    """

    title: str
    address: str

    model_config = ConfigDict(from_attributes=True)


class RestaurantSchema(RestaurantAddSchema):
    """
    Restaurant schema.

    Attributes:
        id (int): Restaurant id
        title (str): Restaurant title
        address (str): Restaurant address
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
