# ============================================================
# STEP 5: Pydantic Field() — Constraints & Richer Docs
# ============================================================
# Run: uvicorn learn.05_pydantic_field:app --reload
# ============================================================
# Topics:
#   - Field() for value constraints (min_length, max_length, gt, lt)
#   - Field() for Swagger documentation (description, examples)
#   - EmailStr for email validation
#   - Nested Pydantic models
#   - model_config with json_schema_extra for Swagger examples
# ============================================================

from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

app = FastAPI(title="Pydantic Field Demo", version="1.0.0")


# -------------------------------------------------------------------
# Nested model — used inside UserCreate
# -------------------------------------------------------------------
class Address(BaseModel):
    street: str = Field(..., min_length=3, description="Street address")
    city: str   = Field(..., min_length=2, description="City name")
    country: str = Field("BD", description="Country code (default: BD)")


# -------------------------------------------------------------------
# Full model with Field() constraints
# -------------------------------------------------------------------
class UserCreate(BaseModel):
    name: str = Field(
        ...,                       # ... means required
        min_length=2,
        max_length=50,
        description="User's full name",
    )
    email: EmailStr = Field(..., description="Valid email address")
    age: int = Field(
        ...,
        gt=0,    # greater than 0
        lt=120,  # less than 120
        description="Age (1–119)",
    )
    bio: Optional[str] = Field(
        None,
        max_length=300,
        description="Short bio (optional, max 300 chars)",
    )
    address: Optional[Address] = Field(None, description="User address (optional)")

    # Adds an example in Swagger UI "Try it out"
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Alice Rahman",
                    "email": "alice@example.com",
                    "age": 28,
                    "bio": "Backend developer who loves FastAPI.",
                    "address": {"street": "123 Main St", "city": "Dhaka"},
                }
            ]
        }
    }


class UserOut(BaseModel):
    id: int
    name: str
    email: str
    age: int
    bio: Optional[str] = None
    address: Optional[Address] = None


# -------------------------------------------------------------------
# In-memory store
# -------------------------------------------------------------------
users: dict[int, UserOut] = {}
_next_id = 1


# -------------------------------------------------------------------
# POST — Field validation fires automatically
# Try sending: age=200 → 422 error
#              email="not-an-email" → 422 error
#              name="A" (too short) → 422 error
# -------------------------------------------------------------------
@app.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    global _next_id
    new_user = UserOut(id=_next_id, **user.model_dump())
    users[_next_id] = new_user
    _next_id += 1
    return new_user


@app.get("/users", response_model=list[UserOut])
async def list_users():
    return list(users.values())


@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]


# ============================================================
# KEY TAKEAWAYS:
#   1. Field(...) = required. Field(default) = optional.
#   2. min_length / max_length → string constraints.
#   3. gt / lt / ge / le → numeric constraints.
#   4. EmailStr validates email format (needs pydantic[email]).
#   5. Nested models: just use another BaseModel as a type.
#   6. json_schema_extra → adds example in Swagger UI.
#   7. All constraints are checked before your function runs.
# ============================================================
