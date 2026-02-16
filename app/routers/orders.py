# ============================================================
# Orders Router
# ============================================================
# Demonstrates:
#   - APIRouter with prefix and tags
#   - Full CRUD for Orders resource
#   - Cross-resource validation (user must exist before creating order)
#   - Depends() for pagination
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.fake_db import orders_db, users_db
from app.dependencies import pagination_params
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.utils.helpers import next_id

router = APIRouter(
    prefix="/orders",
    tags=["Orders"],
)


# ──────────────────────────────────────────────────────────
# GET /orders — list all orders with pagination
# ──────────────────────────────────────────────────────────
@router.get("/", response_model=list[OrderOut], summary="List all orders")
async def list_orders(pagination: dict = Depends(pagination_params)):
    orders = list(orders_db.values())
    skip   = pagination["skip"]
    limit  = pagination["limit"]
    return orders[skip: skip + limit]


# ──────────────────────────────────────────────────────────
# GET /orders/{order_id}
# ──────────────────────────────────────────────────────────
@router.get("/{order_id}", response_model=OrderOut, summary="Get an order by ID")
async def get_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order {order_id} not found",
        )
    return orders_db[order_id]


# ──────────────────────────────────────────────────────────
# GET /orders/user/{user_id} — all orders for a specific user
# ──────────────────────────────────────────────────────────
@router.get(
    "/user/{user_id}",
    response_model=list[OrderOut],
    summary="Get all orders for a user",
)
async def get_orders_by_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    return [o for o in orders_db.values() if o["user_id"] == user_id]


# ──────────────────────────────────────────────────────────
# POST /orders — create a new order
# Cross-resource check: user_id must exist
# ──────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=OrderOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new order",
)
async def create_order(order: OrderCreate):
    # Validate that the referenced user actually exists
    if order.user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {order.user_id} not found — cannot create order",
        )
    new_id = next_id(orders_db)
    new_order = {"id": new_id, **order.model_dump()}
    orders_db[new_id] = new_order
    return new_order


# ──────────────────────────────────────────────────────────
# PUT /orders/{order_id} — full update
# ──────────────────────────────────────────────────────────
@router.put("/{order_id}", response_model=OrderOut, summary="Fully update an order")
async def replace_order(order_id: int, order: OrderCreate):
    if order_id not in orders_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    if order.user_id not in users_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {order.user_id} not found")
    orders_db[order_id] = {"id": order_id, **order.model_dump()}
    return orders_db[order_id]


# ──────────────────────────────────────────────────────────
# PATCH /orders/{order_id} — partial update
# ──────────────────────────────────────────────────────────
@router.patch("/{order_id}", response_model=OrderOut, summary="Partially update an order")
async def update_order(order_id: int, order: OrderUpdate):
    if order_id not in orders_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    update_data = order.model_dump(exclude_unset=True)
    orders_db[order_id].update(update_data)
    return orders_db[order_id]


# ──────────────────────────────────────────────────────────
# DELETE /orders/{order_id}
# ──────────────────────────────────────────────────────────
@router.delete(
    "/{order_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete an order",
)
async def delete_order(order_id: int):
    if order_id not in orders_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")
    del orders_db[order_id]
    return {"message": f"Order {order_id} deleted successfully"}
