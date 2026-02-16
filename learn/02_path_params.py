# ============================================================
# STEP 2: Path Parameters
# ============================================================
# Run: uvicorn learn.02_path_params:app --reload
# ============================================================
# Topics:
#   - Path parameters with type hints
#   - Path() for validation (gt, lt, ge, le)
#   - HTTPException for clean error responses
#   - Multiple path params in one route
# ============================================================

from fastapi import FastAPI, HTTPException, Path, status

app = FastAPI(title="Path Parameters Demo", version="1.0.0")

# -------------------------------------------------------------------
# Fake in-memory data
# -------------------------------------------------------------------
items: dict[int, dict] = {
    1: {"id": 1, "name": "Apple",  "price": 0.5},
    2: {"id": 2, "name": "Banana", "price": 0.3},
    3: {"id": 3, "name": "Cherry", "price": 1.2},
}

users: dict[int, dict] = {
    1: {"id": 1, "name": "Alice", "team": "backend"},
    2: {"id": 2, "name": "Bob",   "team": "frontend"},
}


# -------------------------------------------------------------------
# Basic path parameter — {item_id} is captured from the URL
# -------------------------------------------------------------------
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    # FastAPI automatically validates that item_id is an int.
    # Try /items/abc → 422 Unprocessable Entity (no code needed from us!)
    if item_id not in items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {item_id} not found",
        )
    return items[item_id]


# -------------------------------------------------------------------
# Path() adds extra validation and documentation
# -------------------------------------------------------------------
@app.get("/items/validated/{item_id}")
async def get_item_validated(
    item_id: int = Path(
        description="The ID of the item (must be 1–3)",
        gt=0,   # greater than 0
        le=3,   # less than or equal to 3
    )
):
    if item_id not in items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return items[item_id]


# -------------------------------------------------------------------
# Multiple path parameters
# -------------------------------------------------------------------
@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: int):
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return {
        "user": users[user_id],
        "item": items[item_id],
    }


# ============================================================
# KEY TAKEAWAYS:
#   1. {param} in the path is captured as a function argument.
#   2. Type hint (int, str, float) → FastAPI validates & converts.
#   3. Bad type (e.g. /items/abc) → automatic 422 error.
#   4. Path() adds constraints (gt, lt, ge, le) + Swagger docs.
#   5. HTTPException raises a proper HTTP error response.
#   6. status.HTTP_404_NOT_FOUND is cleaner than magic numbers.
# ============================================================
