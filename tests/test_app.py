"""
Tests for the structured app/ (app/main.py).

Covers:
    - Users CRUD (list, get, create, update, delete, 404 cases)
    - Orders CRUD (list, get, create, update, delete, 404 cases)
    - Cross-resource validation (order referencing non-existent user)

Run: pytest tests/test_app.py -v
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.db import fake_db

client = TestClient(app)


# ──────────────────────────────────────────────────────────
# Fixtures — reset DB state between tests so tests don't
# affect each other (important for mutable in-memory state)
# ──────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_db():
    """Reset the in-memory databases to a known state before each test."""
    fake_db.users_db.clear()
    fake_db.users_db.update({
        1: {"id": 1, "name": "Alice Rahman",  "email": "alice@example.com", "age": 28},
        2: {"id": 2, "name": "Bob Hossain",   "email": "bob@example.com",   "age": 34},
        3: {"id": 3, "name": "Charlie Dev",   "email": "charlie@example.com","age": 22},
    })

    fake_db.orders_db.clear()
    fake_db.orders_db.update({
        1: {"id": 1, "user_id": 1, "item": "Laptop",   "quantity": 1, "total": 999.99},
        2: {"id": 2, "user_id": 1, "item": "Mouse",    "quantity": 2, "total": 49.98},
        3: {"id": 3, "user_id": 2, "item": "Keyboard", "quantity": 1, "total": 89.99},
    })


# ══════════════════════════════════════════════════════════
# ROOT
# ══════════════════════════════════════════════════════════

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


# ══════════════════════════════════════════════════════════
# USERS
# ══════════════════════════════════════════════════════════

class TestListUsers:
    def test_list_users_default(self):
        response = client.get("/users/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 3

    def test_list_users_with_pagination(self):
        response = client.get("/users/?skip=1&limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_list_users_skip_all(self):
        response = client.get("/users/?skip=100")
        assert response.status_code == 200
        assert response.json() == []


class TestGetUser:
    def test_get_existing_user(self):
        response = client.get("/users/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["name"] == "Alice Rahman"
        assert data["email"] == "alice@example.com"

    def test_get_nonexistent_user(self):
        response = client.get("/users/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestCreateUser:
    def test_create_user_success(self):
        payload = {"name": "Diana Dev", "email": "diana@example.com", "age": 25}
        response = client.post("/users/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Diana Dev"
        assert data["email"] == "diana@example.com"
        assert "id" in data

    def test_create_user_invalid_email(self):
        payload = {"name": "BadUser", "email": "not-an-email", "age": 25}
        response = client.post("/users/", json=payload)
        assert response.status_code == 422

    def test_create_user_invalid_age(self):
        payload = {"name": "OldUser", "email": "old@example.com", "age": 200}
        response = client.post("/users/", json=payload)
        assert response.status_code == 422

    def test_create_user_name_too_short(self):
        payload = {"name": "X", "email": "x@example.com", "age": 25}
        response = client.post("/users/", json=payload)
        assert response.status_code == 422

    def test_create_user_missing_required_field(self):
        payload = {"name": "NoEmail"}
        response = client.post("/users/", json=payload)
        assert response.status_code == 422


class TestUpdateUser:
    def test_full_update_user(self):
        payload = {"name": "Alice Updated", "email": "alice_new@example.com", "age": 29}
        response = client.put("/users/1", json=payload)
        assert response.status_code == 200
        assert response.json()["name"] == "Alice Updated"
        assert response.json()["age"] == 29

    def test_partial_update_user(self):
        response = client.patch("/users/1", json={"age": 30})
        assert response.status_code == 200
        data = response.json()
        assert data["age"] == 30
        assert data["name"] == "Alice Rahman"  # unchanged

    def test_update_nonexistent_user(self):
        response = client.put("/users/999", json={"name": "Ghost", "email": "g@g.com", "age": 20})
        assert response.status_code == 404


class TestDeleteUser:
    def test_delete_existing_user(self):
        response = client.delete("/users/1")
        assert response.status_code == 200
        # Verify it's gone
        assert client.get("/users/1").status_code == 404

    def test_delete_nonexistent_user(self):
        response = client.delete("/users/999")
        assert response.status_code == 404


# ══════════════════════════════════════════════════════════
# ORDERS
# ══════════════════════════════════════════════════════════

class TestListOrders:
    def test_list_orders_default(self):
        response = client.get("/orders/")
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_list_orders_pagination(self):
        response = client.get("/orders/?limit=2")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGetOrder:
    def test_get_existing_order(self):
        response = client.get("/orders/1")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert data["item"] == "Laptop"

    def test_get_nonexistent_order(self):
        response = client.get("/orders/999")
        assert response.status_code == 404

    def test_get_orders_by_user(self):
        response = client.get("/orders/user/1")
        assert response.status_code == 200
        orders = response.json()
        assert len(orders) == 2
        assert all(o["user_id"] == 1 for o in orders)

    def test_get_orders_by_nonexistent_user(self):
        response = client.get("/orders/user/999")
        assert response.status_code == 404


class TestCreateOrder:
    def test_create_order_success(self):
        payload = {"user_id": 1, "item": "Monitor", "quantity": 1, "total": 299.99}
        response = client.post("/orders/", json=payload)
        assert response.status_code == 201
        data = response.json()
        assert data["item"] == "Monitor"
        assert data["user_id"] == 1

    def test_create_order_nonexistent_user(self):
        """Cross-resource validation: user must exist."""
        payload = {"user_id": 999, "item": "Widget", "quantity": 1, "total": 9.99}
        response = client.post("/orders/", json=payload)
        assert response.status_code == 404

    def test_create_order_invalid_quantity(self):
        payload = {"user_id": 1, "item": "Widget", "quantity": 0, "total": 9.99}
        response = client.post("/orders/", json=payload)
        assert response.status_code == 422

    def test_create_order_invalid_total(self):
        payload = {"user_id": 1, "item": "Widget", "quantity": 1, "total": -5.0}
        response = client.post("/orders/", json=payload)
        assert response.status_code == 422


class TestUpdateOrder:
    def test_partial_update_order(self):
        response = client.patch("/orders/1", json={"quantity": 3, "total": 2999.97})
        assert response.status_code == 200
        data = response.json()
        assert data["quantity"] == 3
        assert data["item"] == "Laptop"  # unchanged

    def test_update_nonexistent_order(self):
        response = client.patch("/orders/999", json={"quantity": 1})
        assert response.status_code == 404


class TestDeleteOrder:
    def test_delete_existing_order(self):
        response = client.delete("/orders/1")
        assert response.status_code == 200
        assert client.get("/orders/1").status_code == 404

    def test_delete_nonexistent_order(self):
        response = client.delete("/orders/999")
        assert response.status_code == 404
