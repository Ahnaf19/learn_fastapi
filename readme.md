# learn_fastapi — Intern Teaching Kit

A structured, runnable teaching kit for learning FastAPI from scratch.
Aligned with the **"Get Faster with FastAPI"** guide (see `docs/`).

---

## Quick Start

This project uses **[uv](https://docs.astral.sh/uv/)** for dependency and environment management.

```bash
# Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install all dependencies and create .venv automatically
uv sync

# Run any numbered teaching file (from project root)
uv run uvicorn learn.01_hello_world:app --reload

# Run the structured demo app
uv run uvicorn app.main:app --reload

# Run all tests
uv run pytest tests/ -v
```

Then open **http://127.0.0.1:8000/docs** for interactive Swagger UI.

> The `.venv` is created and managed by `uv` — do not create it manually.

---

## Starter Kit Learning Path

Step through the numbered files in `learn/` in order. Each builds on the previous.
All commands run from the **project root**.

| File | Concept | Run Command |
|------|---------|-------------|
| `learn/01_hello_world.py` | FastAPI app, first endpoint, auto docs (`/docs`, `/redoc`) | `uv run uvicorn learn.01_hello_world:app --reload` |
| `learn/02_path_params.py` | Path parameters, `Path()` validation, `HTTPException` | `uv run uvicorn learn.02_path_params:app --reload` |
| `learn/03_query_params.py` | Query parameters, `Query()`, `Optional`, filters + pagination | `uv run uvicorn learn.03_query_params:app --reload` |
| `learn/04_request_body.py` | Pydantic `BaseModel`, POST/PUT/PATCH, `model_dump()`, `exclude_unset` | `uv run uvicorn learn.04_request_body:app --reload` |
| `learn/05_pydantic_field.py` | `Field()` constraints, `EmailStr`, nested models, Swagger examples | `uv run uvicorn learn.05_pydantic_field:app --reload` |
| `learn/06_response_status.py` | `response_model`, status codes, Create/Update/Out schema pattern | `uv run uvicorn learn.06_response_status:app --reload` |
| `learn/07_crud_all_in_one.py` | Full CRUD — all best practices combined in one file | `uv run uvicorn learn.07_crud_all_in_one:app --reload` |

---

## Structured App Demo (`app/`)

A modular, production-style FastAPI application with **Users** and **Orders** CRUD.

```bash
uv run uvicorn app.main:app --reload
```

### What it demonstrates

| Concept | Where |
|---------|-------|
| `APIRouter` with `prefix` + `tags` | `app/routers/users.py`, `app/routers/orders.py` |
| `include_router` to compose the app | `app/main.py` |
| `Depends()` for pagination | `app/dependencies.py` → used in both routers |
| `Depends()` for get-or-404 | `app/dependencies.py` → `get_user_or_404` |
| Separate `schemas/` directory | `app/schemas/user.py`, `app/schemas/order.py` |
| `Field()` constraints + `EmailStr` | `app/schemas/user.py` |
| In-memory fake DB | `app/db/fake_db.py` |
| Cross-resource validation | `app/routers/orders.py` (user must exist) |
| Full CRUD with proper status codes | Both routers |

### App structure

```
app/
├── __init__.py
├── main.py               # FastAPI instance + include_router
├── dependencies.py       # Shared Depends(): pagination, get_user_or_404
├── db/
│   └── fake_db.py        # In-memory dicts (users_db, orders_db)
├── schemas/
│   ├── user.py           # UserCreate, UserUpdate, UserOut
│   └── order.py          # OrderCreate, OrderUpdate, OrderOut
├── routers/
│   ├── users.py          # /users  — full CRUD
│   └── orders.py         # /orders — full CRUD
└── utils/
    └── helpers.py        # next_id() helper
```

---

## Tests

```bash
uv run pytest tests/ -v
```

| File | Tests |
|------|-------|
| `tests/test_myapi.py` | Original student API (reference) |
| `tests/test_app.py`   | Structured app — Users + Orders full coverage |

---

## uv Cheatsheet

| Task | Command |
|------|---------|
| Install / sync all deps | `uv sync` |
| Run tests | `uv run pytest tests/ -v` |
| Run the demo app | `uv run uvicorn app.main:app --reload` |
| Run a teaching file | `uv run uvicorn learn.01_hello_world:app --reload` |
| Add a dependency | `uv add <package>` |
| Add a dev dependency | `uv add --dev <package>` |
| Remove a dependency | `uv remove <package>` |
| Show installed packages | `uv pip list` |

---

## Reference

- `pyproject.toml` — project manifest and dependency declaration (uv)
- `uv.lock` — exact lockfile for reproducible installs
- `myapi.py` — original student CRUD (kept as reference)
- `docs/Fast API_ Beginner to Intermediate Guide.pdf` — the companion guide
- FastAPI official docs: https://fastapi.tiangolo.com

---

## Road to Glory — What's Next?

After the Starter Kit, explore these advanced topics:

- **Get Modular** — `APIRouter`, bigger app structure (done in `app/`)
- **DB Connection** — SQLAlchemy / Tortoise ORM (`app/db/db_session.py`)
- **Dependencies** — auth, DB sessions, rate limiting (see `app/dependencies.py`)
- **Middleware** — CORS, logging, timing
- **Security** — OAuth2, JWT, `passlib`
- **Lifespan Events** — startup/shutdown hooks
- **Background Tasks** — `BackgroundTasks`
- **Custom Exception Handling** — global exception handlers
- **Testing & CI** — `pytest` + GitHub Actions

> GOAT of all resources: [FastAPI Official Documentation](https://fastapi.tiangolo.com)
