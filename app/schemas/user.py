from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    """Fields required to create a new user."""
    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="User's full name",
        examples=["Alice Rahman"],
    )
    email: EmailStr = Field(
        ...,
        description="Valid email address",
        examples=["alice@example.com"],
    )
    age: int = Field(
        ...,
        gt=0,
        lt=120,
        description="Age (1–119)",
        examples=[28],
    )


class UserUpdate(BaseModel):
    """All fields optional — send only what you want to change."""
    name: Optional[str]  = Field(None, min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    age: Optional[int]   = Field(None, gt=0, lt=120)


class UserOut(BaseModel):
    """Fields returned to the client."""
    id: int
    name: str
    email: str
    age: int
