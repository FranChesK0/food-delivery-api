from pydantic import BaseModel, ConfigDict


class CategoryAddSchema(BaseModel):
    """
    Category add schema.

    Attributes:
        name (str): Category name
    """

    name: str

    model_config = ConfigDict(from_attributes=True)


class CategorySchema(CategoryAddSchema):
    """
    Category schema.

    Attributes:
        id (int): Category id
        name (str): Category name
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
