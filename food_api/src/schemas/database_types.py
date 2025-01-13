from enum import StrEnum


class OrderStatus(StrEnum):
    CREATING = "creating"
    COOKING = "cooking"
    DELIVERING = "delivering"
    DELIVERED = "delivered"
