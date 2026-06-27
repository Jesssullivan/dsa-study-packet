"""Modern Flask 3.x patterns — app factory, blueprints, middleware.

This module demonstrates idiomatic Flask for building JSON APIs:
    1. Application factory  — ``create_app()`` builds a fresh app each time,
       making tests reproducible and avoiding global state.
    2. Blueprints           — ``api_bp`` groups related routes under /api.
    3. Error handlers       — custom ``ValidationError`` + 404 both return JSON.
    4. Middleware            — before/after request hooks for logging & headers.

Real-world relevance:
    Many backend services expose REST or GraphQL APIs. Understanding Flask's
    request lifecycle helps with debugging, testing, and extending any
    WSGI-based Python service.

References:
    https://flask.palletsprojects.com/en/stable/patterns/appfactories/
    https://flask.palletsprojects.com/en/stable/blueprints/
    https://flask.palletsprojects.com/en/stable/testing/
"""

import uuid
from dataclasses import dataclass
from typing import Any

from flask import Blueprint, Flask, Response, jsonify, request


# ---------------------------------------------------------------------------
# Domain models (plain dataclasses — no ORM needed for demo)
# ---------------------------------------------------------------------------
@dataclass
class Item:
    """A catalog item with an integer id, a name, and a price."""

    id: int
    name: str
    price: float


@dataclass
class ItemCreate:
    """Payload for creating a new Item (no id yet)."""

    name: str
    price: float


# ---------------------------------------------------------------------------
# In-memory store — seeded with a few items for convenience
# ---------------------------------------------------------------------------

_items: dict[int, Item] = {
    1: Item(id=1, name="Widget", price=9.99),
    2: Item(id=2, name="Gadget", price=24.50),
    3: Item(id=3, name="Doohickey", price=4.75),
}

# Auto-increment counter for new item IDs.
_next_id: int = 4


def _reset_store() -> None:
    """Reset in-memory store to initial state (used in tests)."""
    global _next_id
    _items.clear()
    _items.update(
        {
            1: Item(id=1, name="Widget", price=9.99),
            2: Item(id=2, name="Gadget", price=24.50),
            3: Item(id=3, name="Doohickey", price=4.75),
        }
    )
    _next_id = 4


# ---------------------------------------------------------------------------
# Custom error
# ---------------------------------------------------------------------------
class ValidationError(Exception):
    """Raised when request data fails validation.

    Carries a human-readable *message* and an HTTP *status_code* (default 400).
    The app-level error handler converts this to a JSON response.
    """

    def __init__(self, message: str, status_code: int = 400) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code


# ---------------------------------------------------------------------------
# Blueprint — all API routes live here
# ---------------------------------------------------------------------------
# Blueprints let you organize routes into logical groups.  Each blueprint
# can have its own url_prefix, error handlers, and template folder.
# The main app registers blueprints at startup.
# ---------------------------------------------------------------------------

api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/health")
def health() -> tuple[Response, int]:
    """Simple health-check endpoint."""
    return jsonify({"status": "healthy"}), 200


@api_bp.route("/items")
def list_items() -> tuple[Response, int]:
    """Return all items as a JSON list."""
    items_list = [
        {"id": item.id, "name": item.name, "price": item.price}
        for item in _items.values()
    ]
    return jsonify(items_list), 200


@api_bp.route("/items/<int:item_id>")
def get_item(item_id: int) -> tuple[Response, int]:
    """Return a single item or 404."""
    item = _items.get(item_id)
    if item is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": item.id, "name": item.name, "price": item.price}), 200


@api_bp.route("/items", methods=["POST"])
def create_item() -> tuple[Response, int]:
    """Create an item from the JSON request body.

    Expects ``{"name": "...", "price": ...}``.  Returns 201 on success.
    """
    global _next_id

    body: Any = request.get_json(silent=True)
    if body is None:
        raise ValidationError("request body must be JSON")

    name = body.get("name")
    price = body.get("price")

    if not name or not isinstance(name, str):
        raise ValidationError("'name' is required and must be a string")
    if price is None or not isinstance(price, (int, float)):
        raise ValidationError("'price' is required and must be a number")

    new_item = Item(id=_next_id, name=name, price=float(price))
    _items[_next_id] = new_item
    _next_id += 1

    return (
        jsonify({"id": new_item.id, "name": new_item.name, "price": new_item.price}),
        201,
    )


# ---------------------------------------------------------------------------
# Before / after request hooks (middleware)
# ---------------------------------------------------------------------------
# ``before_request`` runs before the view function — great for auth checks,
# request logging, or injecting context.
# ``after_request`` runs after the view — perfect for adding headers.
# ---------------------------------------------------------------------------
@api_bp.before_request
def log_request() -> None:
    """Log every incoming request's method and path."""
    from flask import current_app

    current_app.logger.debug("%s %s", request.method, request.path)


@api_bp.after_request
def add_request_id(response: Response) -> Response:
    """Attach a unique X-Request-ID header to every response."""
    response.headers["X-Request-ID"] = str(uuid.uuid4())
    return response


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------
# The factory pattern avoids module-level ``app = Flask(__name__)``.
# Benefits:
#   - Tests can create isolated app instances.
#   - Multiple configurations (dev, staging, prod) can coexist.
#   - Circular-import issues around ``app`` are eliminated.
# ---------------------------------------------------------------------------
def create_app(testing: bool = False) -> Flask:
    """Build and configure the Flask application.

    When *testing* is True the app runs in testing mode and the in-memory
    store is reset to a known state.
    """
    app = Flask(__name__)
    app.testing = testing

    if testing:
        _reset_store()

    # --- Register the API blueprint ---
    app.register_blueprint(api_bp)

    # --- Error handlers (registered on the app, not the blueprint) ---
    @app.errorhandler(ValidationError)
    def handle_validation_error(exc: ValidationError) -> tuple[Response, int]:
        return jsonify({"error": exc.message}), exc.status_code

    @app.errorhandler(404)
    def handle_not_found(_exc: Exception) -> tuple[Response, int]:
        return jsonify({"error": "not found"}), 404

    return app
