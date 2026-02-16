from typing import Optional

from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    """Fields required to create a new order."""
    user_id: int = Field(..., gt=0, description="ID of the user placing the order")
    item: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Item name",
        examples=["Laptop"],
    )
    quantity: int = Field(
        ...,
        gt=0,
        description="Quantity ordered (must be > 0)",
        examples=[1],
    )
    total: float = Field(
        ...,
        gt=0,
        description="Total price in USD (must be > 0)",
        examples=[999.99],
    )


class OrderUpdate(BaseModel):
    """All fields optional — send only what you want to change."""
    item: Optional[str]     = Field(None, min_length=1, max_length=100)
    quantity: Optional[int]  = Field(None, gt=0)
    total: Optional[float]   = Field(None, gt=0)


class OrderOut(BaseModel):
    """Fields returned to the client."""
    id: int
    user_id: int
    item: str
    quantity: int
    total: float
