# ============================================================
# App Entry Point
# ============================================================
# Run: uvicorn app.main:app --reload
# Docs: http://127.0.0.1:8000/docs
# ============================================================
# This is where the FastAPI instance is created and all
# routers are registered (included) into the app.
# ============================================================

from fastapi import FastAPI

from app.routers import orders, users

app = FastAPI(
    title="Demo API — Users & Orders",
    description=(
        "A modular FastAPI demo with Users and Orders CRUD.\n\n"
        "Shows: APIRouter, Depends, schemas/, db/, routers/ separation."
    ),
    version="1.0.0",
)

# ------------------------------------------------------------------
# include_router() key parameters:
#
#   prefix           — prepend a path to every route in the router
#                      (overrides the router's own prefix if set)
#   tags             — group name shown in Swagger UI
#                      (overrides/extends the router's own tags)
#   dependencies     — Depends() applied to EVERY route in the router
#                      e.g. dependencies=[Depends(verify_token)]
#   responses        — extra response codes documented for ALL routes
#                      e.g. {401: {"description": "Unauthorized"}}
#   include_in_schema — False = router still works but hidden from /docs
#                       useful for internal/admin routes
#   deprecated       — True = marks every route as deprecated in /docs
# ------------------------------------------------------------------

app.include_router(
    users.router,
    # prefix="/users",          # already set in the router itself
    # tags=["Users"],           # already set in the router itself
    # dependencies=[],          # e.g. [Depends(verify_token)] for auth on all user routes
    responses={404: {"description": "User not found"}},
    include_in_schema=True,     # flip to False to hide from /docs entirely
    # deprecated=False,         # flip to True to mark all routes deprecated
)

app.include_router(
    orders.router,
    responses={404: {"description": "Order or user not found"}},
    include_in_schema=True,
)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Demo API is running",
        "docs": "/docs",
        "redoc": "/redoc",
    }
