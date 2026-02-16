# ============================================================
# Fake In-Memory Database
# ============================================================
# In a real app this would be replaced with SQLAlchemy / Tortoise
# sessions and actual database models.
# For teaching purposes, plain Python dicts work perfectly.
# ============================================================

from typing import Any

# ── Users ─────────────────────────────────────────────────
users_db: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "name": "Alice Rahman",
        "email": "alice@example.com",
        "age": 28,
    },
    2: {
        "id": 2,
        "name": "Bob Hossain",
        "email": "bob@example.com",
        "age": 34,
    },
    3: {
        "id": 3,
        "name": "Charlie Dev",
        "email": "charlie@example.com",
        "age": 22,
    },
}

# ── Orders ────────────────────────────────────────────────
orders_db: dict[int, dict[str, Any]] = {
    1: {
        "id": 1,
        "user_id": 1,
        "item": "Laptop",
        "quantity": 1,
        "total": 999.99,
    },
    2: {
        "id": 2,
        "user_id": 1,
        "item": "Mouse",
        "quantity": 2,
        "total": 49.98,
    },
    3: {
        "id": 3,
        "user_id": 2,
        "item": "Keyboard",
        "quantity": 1,
        "total": 89.99,
    },
}
