# ============================================================
# Shared Dependencies — used with FastAPI's Depends()
# ============================================================
# Depends() lets you declare reusable logic (pagination,
# authentication, DB sessions, etc.) that FastAPI injects
# automatically into route handlers.
# ============================================================

from fastapi import HTTPException, Query, status

from app.db.fake_db import users_db


# ──────────────────────────────────────────────────────────
# Pagination dependency
# ──────────────────────────────────────────────────────────
# Usage in a router:
#   async def list_items(pagination: dict = Depends(pagination_params)):
#       skip  = pagination["skip"]
#       limit = pagination["limit"]
# ──────────────────────────────────────────────────────────
def pagination_params(
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max records to return (1–100)"),
) -> dict:
    return {"skip": skip, "limit": limit}


# ──────────────────────────────────────────────────────────
# get_user_or_404 dependency
# ──────────────────────────────────────────────────────────
# Usage in a router:
#   async def get_user(user: dict = Depends(get_user_or_404)):
#       return user
#
# The user_id is read from the path parameter automatically.
# ──────────────────────────────────────────────────────────
def get_user_or_404(user_id: int) -> dict:
    """Shared dependency — raises 404 if the user does not exist."""
    if user_id not in users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found",
        )
    return users_db[user_id]
