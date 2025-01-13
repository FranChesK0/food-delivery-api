from pydantic import BaseModel, ConfigDict


class ScheduleAddSchema(BaseModel):
    """
    Schedule add schema.

    Attributes:
        restaurant_id (int): Restaurant id
        start (str): Schedule start time
        end (str): Schedule end time
    """

    restaurant_id: int
    start: str
    end: str

    model_config = ConfigDict(from_attributes=True)


class ScheduleSchema(BaseModel):
    """
    Schedule schema.

    Attributes:
        id (int): Schedule id
        restaurant_id (int): Restaurant id
        start (str): Schedule start time
        end (str): Schedule end time
    """

    id: int

    model_config = ConfigDict(from_attributes=True)
