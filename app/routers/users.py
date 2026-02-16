# ============================================================
# Users Router
# ============================================================
# Demonstrates:
#   - APIRouter with prefix and tags
#   - Full CRUD: GET list, GET one, POST, PUT, PATCH, DELETE
#   - response_model + status codes
#   - Depends() for pagination and get_or_404
# ============================================================

from fastapi import APIRouter, Depends, HTTPException, status

from app.db.fake_db import users_db
from app.dependencies import get_user_or_404, pagination_params
from app.schemas.user import UserCreate, UserOut, UserUpdate
from app.utils.helpers import next_id

# APIRouter groups related endpoints under a common prefix.
# All routes here will be prefixed with /users.
router = APIRouter(
    prefix="/users",
    tags=["Users"],  # groups endpoints in Swagger UI
)


# ──────────────────────────────────────────────────────────
# GET /users — list with pagination via Depends()
# ──────────────────────────────────────────────────────────
@router.get("/", response_model=list[UserOut], summary="List all users")
async def list_users(pagination: dict = Depends(pagination_params)):
    """
    Returns a paginated list of users.
    Use `skip` and `limit` query params to paginate.
    """
    users = list(users_db.values())
    skip  = pagination["skip"]
    limit = pagination["limit"]
    return users[skip: skip + limit]


# ──────────────────────────────────────────────────────────
# GET /users/{user_id} — get one via Depends(get_user_or_404)
# ──────────────────────────────────────────────────────────
@router.get("/{user_id}", response_model=UserOut, summary="Get a user by ID")
async def get_user(user: dict = Depends(get_user_or_404)):
    """
    Returns a single user.
    The get_user_or_404 dependency automatically raises 404
    if the user_id does not exist — no boilerplate needed here.
    """
    return user


# ──────────────────────────────────────────────────────────
# POST /users — create a new user
# ──────────────────────────────────────────────────────────
@router.post(
    "/",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new user",
)
async def create_user(user: UserCreate):
    new_id = next_id(users_db)
    new_user = {"id": new_id, **user.model_dump()}
    users_db[new_id] = new_user
    return new_user


# ──────────────────────────────────────────────────────────
# PUT /users/{user_id} — full update (replace all fields)
# ──────────────────────────────────────────────────────────
@router.put("/{user_id}", response_model=UserOut, summary="Fully update a user")
async def replace_user(user_id: int, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    users_db[user_id] = {"id": user_id, **user.model_dump()}
    return users_db[user_id]


# ──────────────────────────────────────────────────────────
# PATCH /users/{user_id} — partial update
# ──────────────────────────────────────────────────────────
@router.patch("/{user_id}", response_model=UserOut, summary="Partially update a user")
async def update_user(user_id: int, user: UserUpdate):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    update_data = user.model_dump(exclude_unset=True)
    users_db[user_id].update(update_data)
    return users_db[user_id]


# ──────────────────────────────────────────────────────────
# DELETE /users/{user_id} — delete a user
# ──────────────────────────────────────────────────────────
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    summary="Delete a user",
)
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    del users_db[user_id]
    return {"message": f"User {user_id} deleted successfully"}
