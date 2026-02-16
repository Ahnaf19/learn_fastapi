# ============================================================
# STEP 4: Request Body with Pydantic BaseModel
# ============================================================
# Run: uvicorn learn.04_request_body:app --reload
# ============================================================
# Topics:
#   - Pydantic BaseModel for request body
#   - POST / PUT with body
#   - Automatic validation (wrong type, missing field → 422)
#   - model_dump() to convert to dict
#   - Optional fields with defaults
# ============================================================

from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

app = FastAPI(title="Request Body Demo", version="1.0.0")

# -------------------------------------------------------------------
# Pydantic model defines the shape of the request body.
# FastAPI reads this from the JSON body of the request.
# -------------------------------------------------------------------
class ItemCreate(BaseModel):
    name: str               # required
    price: float            # required
    in_stock: bool = True   # optional — has a default
    description: Optional[str] = None  # optional — can be None


class ItemUpdate(BaseModel):
    # For updates we make everything optional so callers
    # only need to send what they want to change.
    name: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
    description: Optional[str] = None


# -------------------------------------------------------------------
# In-memory store
# -------------------------------------------------------------------
items: dict[int, dict] = {}
_next_id = 1


# -------------------------------------------------------------------
# POST — create a new item
# Body example:
#   { "name": "Widget", "price": 9.99, "description": "A small widget" }
# -------------------------------------------------------------------
@app.post("/items", status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate):
    global _next_id
    new_item = {"id": _next_id, **item.model_dump()}
    items[_next_id] = new_item
    _next_id += 1
    return new_item


# -------------------------------------------------------------------
# GET all items
# -------------------------------------------------------------------
@app.get("/items")
async def list_items():
    return list(items.values())


# -------------------------------------------------------------------
# GET one item
# -------------------------------------------------------------------
@app.get("/items/{item_id}")
async def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]


# -------------------------------------------------------------------
# PUT — full update (replace all fields)
# -------------------------------------------------------------------
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemCreate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id] = {"id": item_id, **item.model_dump()}
    return items[item_id]


# -------------------------------------------------------------------
# PATCH-style update — only update fields that are sent
# -------------------------------------------------------------------
@app.patch("/items/{item_id}")
async def partial_update_item(item_id: int, item: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    # exclude_unset=True → only fields the client explicitly sent
    update_data = item.model_dump(exclude_unset=True)
    items[item_id].update(update_data)
    return items[item_id]


# -------------------------------------------------------------------
# DELETE
# -------------------------------------------------------------------
@app.delete("/items/{item_id}", status_code=status.HTTP_200_OK)
async def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
    return {"message": f"Item {item_id} deleted"}


# ============================================================
# KEY TAKEAWAYS:
#   1. class MyModel(BaseModel) defines the request body shape.
#   2. FastAPI reads JSON body → validates → injects as Python object.
#   3. Missing required field or wrong type → automatic 422 error.
#   4. model_dump() converts the Pydantic object to a plain dict.
#   5. model_dump(exclude_unset=True) → only fields client sent.
#   6. Optional[str] = None → field is not required in the body.
# ============================================================
