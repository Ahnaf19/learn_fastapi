# ============================================================
# STEP 3: Query Parameters
# ============================================================
# Run: uvicorn learn.03_query_params:app --reload
# ============================================================
# Topics:
#   - Simple query params with defaults
#   - Optional query params
#   - Query() for validation + documentation
#   - Combining path params and query params
# ============================================================

from typing import Optional

from fastapi import FastAPI, HTTPException, Path, Query, status

app = FastAPI(title="Query Parameters Demo", version="1.0.0")

# -------------------------------------------------------------------
# Fake in-memory data
# -------------------------------------------------------------------
fake_users: list[dict] = [
    {"id": 1, "name": "Alice",   "age": 28, "active": True,  "team": "backend"},
    {"id": 2, "name": "Bob",     "age": 34, "active": False, "team": "frontend"},
    {"id": 3, "name": "Charlie", "age": 22, "active": True,  "team": "backend"},
    {"id": 4, "name": "Diana",   "age": 30, "active": True,  "team": "devops"},
    {"id": 5, "name": "Eve",     "age": 25, "active": False, "team": "frontend"},
]


# -------------------------------------------------------------------
# Query params with defaults
# Try: /users
#      /users?skip=1&limit=2
# -------------------------------------------------------------------
@app.get("/users")
async def list_users(
    skip: int = 0,    # default = 0 (first item)
    limit: int = 10,  # default = 10
):
    return fake_users[skip: skip + limit]


# -------------------------------------------------------------------
# Query() adds validation + documentation
# Try: /users/filtered?skip=0&limit=3&active=true&team=backend
# -------------------------------------------------------------------
@app.get("/users/filtered")
async def list_users_filtered(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Max items to return (1–100)"),
    active: Optional[bool] = Query(None, description="Filter by active status"),
    team: Optional[str] = Query(None, description="Filter by team name"),
):
    result = fake_users

    if active is not None:
        result = [u for u in result if u["active"] == active]
    if team is not None:
        result = [u for u in result if u["team"] == team]

    return result[skip: skip + limit]


# -------------------------------------------------------------------
# Combining path param + query params
# Try: /users/1?include_team=true
# -------------------------------------------------------------------
@app.get("/users/{user_id}")
async def get_user(
    user_id: int = Path(description="User ID", gt=0),
    include_team: bool = Query(False, description="Include team info in response"),
):
    user = next((u for u in fake_users if u["id"] == user_id), None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found",
        )
    if not include_team:
        # Return a copy without the 'team' field
        return {k: v for k, v in user.items() if k != "team"}
    return user


# -------------------------------------------------------------------
# Required query param (no default = required)
# Try: /search?q=alice
# -------------------------------------------------------------------
@app.get("/search")
async def search_users(
    q: str = Query(description="Search term (matches name)"),
):
    results = [u for u in fake_users if q.lower() in u["name"].lower()]
    return {"query": q, "results": results, "count": len(results)}


# ============================================================
# KEY TAKEAWAYS:
#   1. Function params without path placeholders = query params.
#   2. Default value → optional query param.
#   3. No default → required query param.
#   4. Query() gives constraints (ge, le) + Swagger description.
#   5. Optional[str] = Query(None) → truly optional param.
#   6. Mix path + query params freely in one function.
# ============================================================
