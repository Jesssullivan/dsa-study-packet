"""Tests for modern Flask API patterns."""

from typing import Any

import pytest

pytest.importorskip("flask")

from concepts.modern_flask import create_app


@pytest.fixture
def client() -> Any:
    """Create a test client from a fresh app instance."""
    app = create_app(testing=True)
    return app.test_client()


class TestHealth:
    def test_health_returns_200(self, client: Any) -> None:
        resp = client.get("/api/health")
        assert resp.status_code == 200
        assert resp.get_json() == {"status": "healthy"}


class TestListItems:
    def test_returns_list(self, client: Any) -> None:
        resp = client.get("/api/items")
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, list)
        assert len(data) == 3  # seeded items


class TestGetItem:
    def test_existing_item(self, client: Any) -> None:
        resp = client.get("/api/items/1")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["name"] == "Widget"

    def test_missing_item_returns_404(self, client: Any) -> None:
        resp = client.get("/api/items/999")
        assert resp.status_code == 404
        data = resp.get_json()
        assert data["error"] == "not found"


class TestCreateItem:
    def test_create_success(self, client: Any) -> None:
        resp = client.post(
            "/api/items",
            json={"name": "Sprocket", "price": 12.99},
        )
        assert resp.status_code == 201
        data = resp.get_json()
        assert data["name"] == "Sprocket"
        assert data["price"] == 12.99
        assert "id" in data

    def test_missing_name_returns_400(self, client: Any) -> None:
        resp = client.post("/api/items", json={"price": 5.0})
        assert resp.status_code == 400
        assert "name" in resp.get_json()["error"].lower()

    def test_missing_price_returns_400(self, client: Any) -> None:
        resp = client.post("/api/items", json={"name": "Thingy"})
        assert resp.status_code == 400
        assert "price" in resp.get_json()["error"].lower()


class TestMiddleware:
    def test_x_request_id_present(self, client: Any) -> None:
        resp = client.get("/api/health")
        assert "X-Request-ID" in resp.headers
        # Should be a valid UUID4 (36 chars with dashes).
        assert len(resp.headers["X-Request-ID"]) == 36
