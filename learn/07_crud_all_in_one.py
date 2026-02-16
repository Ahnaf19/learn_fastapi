# ============================================================
# STEP 7: Full CRUD — Everything Combined in One File
# ============================================================
# Run: uvicorn learn.07_crud_all_in_one:app --reload
# ============================================================
# This is the "polished all-in-one" file — everything from
# steps 1–6 applied together to a single resource (Products).
#
# Concepts demonstrated:
#   - FastAPI app with metadata
#   - Pydantic schemas: Create / Update / Out separation
#   - Field() with constraints + descriptions
#   - response_model to control output shape
#   - Proper HTTP status codes (200, 201, 204, 404, 400)
#   - Full CRUD: GET all, GET one, POST, PUT, PATCH, DELETE
#   - exclude_unset=True for partial updates
#   - HTTPException with status module
# ============================================================

from typing import Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

app = FastAPI(
    title="Products CRUD API",
    description="Full CRUD demo — all best practices in one file.",
    version="1.0.0",
)


# ──────────────────────────────────────────────
# Pydantic Schemas
# ──────────────────────────────────────────────

class ProductCreate(BaseModel):
    """Schema for creating a new product. All fields required."""
    name: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Product name",
        examples=["Wireless Mouse"],
    )
    price: float = Field(
        ...,
        gt=0,
        description="Price in USD (must be > 0)",
        examples=[29.99],
    )
    category: str = Field(
        ...,
        min_length=1,
        max_length=50,
        description="Product category",
        examples=["Electronics"],
    )
    in_stock: bool = Field(True, description="Is the product currently in stock?")
    description: Optional[str] = Field(
        None,
        max_length=500,
        description="Optional product description",
    )


class ProductUpdate(BaseModel):
    """Schema for partial updates. All fields optional."""
    name: Optional[str]        = Field(None, min_length=1, max_length=100)
    price: Optional[float]     = Field(None, gt=0)
    category: Optional[str]    = Field(None, min_length=1, max_length=50)
    in_stock: Optional[bool]   = None
    description: Optional[str] = Field(None, max_length=500)


class ProductOut(BaseModel):
    """Schema returned to clients. Defines exactly what they see."""
    id: int
    name: str
    price: float
    category: str
    in_stock: bool
    description: Optional[str] = None


# ──────────────────────────────────────────────
# In-memory "Database"
# ──────────────────────────────────────────────

products_db: dict[int, dict] = {
    1: {
        "id": 1,
        "name": "Wireless Mouse",
        "price": 29.99,
        "category": "Electronics",
        "in_stock": True,
        "description": "Ergonomic wireless mouse with long battery life.",
    },
    2: {
        "id": 2,
        "name": "Mechanical Keyboard",
        "price": 89.99,
        "category": "Electronics",
        "in_stock": True,
        "description": None,
    },
}
_next_id = 3


# ──────────────────────────────────────────────
# Helper
# ──────────────────────────────────────────────

def _get_or_404(product_id: int) -> dict:
    """Return product dict or raise a clean 404."""
    if product_id not in products_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with id {product_id} not found",
        )
    return products_db[product_id]


# ──────────────────────────────────────────────
# Endpoints
# ──────────────────────────────────────────────

@app.get(
    "/products",
    response_model=list[ProductOut],
    summary="List all products",
    tags=["Products"],
)
async def list_products():
    """Return all products."""
    return list(products_db.values())


@app.get(
    "/products/{product_id}",
    response_model=ProductOut,
    summary="Get a product by ID",
    tags=["Products"],
)
async def get_product(product_id: int):
    """Return a single product by its ID."""
    return _get_or_404(product_id)


@app.post(
    "/products",
    response_model=ProductOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new product",
    tags=["Products"],
)
async def create_product(product: ProductCreate):
    """Create and store a new product."""
    global _next_id
    new_product = {"id": _next_id, **product.model_dump()}
    products_db[_next_id] = new_product
    _next_id += 1
    return new_product


@app.put(
    "/products/{product_id}",
    response_model=ProductOut,
    summary="Fully replace a product",
    tags=["Products"],
)
async def replace_product(product_id: int, product: ProductCreate):
    """Replace all fields of a product (full update)."""
    _get_or_404(product_id)  # raises 404 if missing
    products_db[product_id] = {"id": product_id, **product.model_dump()}
    return products_db[product_id]


@app.patch(
    "/products/{product_id}",
    response_model=ProductOut,
    summary="Partially update a product",
    tags=["Products"],
)
async def update_product(product_id: int, product: ProductUpdate):
    """Update only the fields provided (partial update)."""
    _get_or_404(product_id)
    # exclude_unset=True → only include fields the client actually sent
    update_data = product.model_dump(exclude_unset=True)
    products_db[product_id].update(update_data)
    return products_db[product_id]


@app.delete(
    "/products/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a product",
    tags=["Products"],
)
async def delete_product(product_id: int):
    """Delete a product by ID. Returns 204 No Content on success."""
    _get_or_404(product_id)
    del products_db[product_id]


# ============================================================
# KEY TAKEAWAYS (full summary):
#   1. Three schemas per resource: Create / Update / Out.
#   2. Field() gives constraints + Swagger docs in one place.
#   3. response_model= hides anything not in the Out schema.
#   4. Status codes: 200 GET/PUT/PATCH, 201 POST, 204 DELETE.
#   5. HTTPException(status_code=..., detail=...) for errors.
#   6. exclude_unset=True enables clean partial updates.
#   7. tags=[...] groups endpoints in Swagger UI.
#   8. A small helper (_get_or_404) keeps route handlers clean.
# ============================================================
