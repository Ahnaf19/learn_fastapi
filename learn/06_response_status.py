# ============================================================
# STEP 6: Response Model & Status Codes
# ============================================================
# Run: uvicorn learn.06_response_status:app --reload
# ============================================================
# Topics:
#   - response_model — controls what the client sees
#   - Separate Create vs Out schemas (never expose internals)
#   - status_code on the decorator
#   - status module (HTTP_200_OK, HTTP_201_CREATED, etc.)
#   - HTTPException with proper status codes
# ============================================================

from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(title="Response Model & Status Codes Demo", version="1.0.0")


# -------------------------------------------------------------------
# Schema separation pattern:
#   *Create  — what the client sends (input)
#   *Update  — partial update (all optional)
#   *Out     — what we return (output, never expose secrets)
# -------------------------------------------------------------------
class ProductCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0, description="Price must be > 0")
    category: str = Field(..., description="Product category")


class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0)
    category: Optional[str] = None


class ProductOut(BaseModel):
    id: int
    name: str
    price: float
    category: str
    # Notice: no _internal_cost or _supplier — those are hidden from clients


# -------------------------------------------------------------------
# In-memory store (has internal fields the client should NOT see)
# -------------------------------------------------------------------
products: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Widget",
        "price": 9.99,
        "category": "hardware",
        "_internal_cost": 3.50,   # supplier cost — should never leak
        "_supplier": "ACME Corp", # internal — should never leak
    }
}
_next_id = 2


# -------------------------------------------------------------------
# response_model=ProductOut strips _internal_* fields automatically
# -------------------------------------------------------------------
@app.get(
    "/products/{product_id}",
    response_model=ProductOut,                    # ← only ProductOut fields returned
    status_code=status.HTTP_200_OK,
    summary="Get a product by ID",
)
async def get_product(product_id: int):
    if product_id not in products:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found",
        )
    return products[product_id]  # _internal fields are stripped by response_model


@app.get(
    "/products",
    response_model=list[ProductOut],
    summary="List all products",
)
async def list_products():
    return list(products.values())


# -------------------------------------------------------------------
# 201 Created on successful POST
# -------------------------------------------------------------------
@app.post(
    "/products",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,   # ← 201, not 200
    summary="Create a new product",
)
async def create_product(product: ProductCreate):
    global _next_id
    new_product = {
        "id": _next_id,
        **product.model_dump(),
        "_internal_cost": 0.0,   # stored internally but never returned
        "_supplier": "TBD",
    }
    products[_next_id] = new_product
    _next_id += 1
    return new_product  # response_model hides the _ fields


# -------------------------------------------------------------------
# PUT — full update
# -------------------------------------------------------------------
@app.put("/products/{product_id}", response_model=ProductOut)
async def update_product(product_id: int, product: ProductCreate):
    if product_id not in products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    # Preserve internal fields, update the rest
    products[product_id].update(product.model_dump())
    return products[product_id]


# -------------------------------------------------------------------
# 204 No Content — nothing to return after delete
# -------------------------------------------------------------------
@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
)
async def delete_product(product_id: int):
    if product_id not in products:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    del products[product_id]
    # 204 → return nothing (None)


# ============================================================
# KEY TAKEAWAYS:
#   1. response_model= on the decorator defines the output shape.
#   2. Any extra fields in the returned dict are silently stripped.
#   3. This prevents accidental data leakage (passwords, secrets).
#   4. Use separate *Create, *Update, *Out schemas — common pattern.
#   5. status_code= on the decorator sets the HTTP response code.
#   6. Use status.HTTP_XXX constants — readable and IDE-complete.
#   7. 201 → resource created; 204 → success but nothing to return.
# ============================================================
