"""Tests for Pydantic v2 validation patterns."""

from __future__ import annotations

from typing import Annotated, Any

import pytest

pydantic = pytest.importorskip("pydantic")

from pydantic import Field, TypeAdapter, ValidationError  # noqa: E402

from concepts.validation import (  # noqa: E402
    Address,
    Circle,
    Rectangle,
    User,
    deserialize_user,
    serialize_user,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _valid_address() -> dict[str, str]:
    return {
        "street": "123 Main St",
        "city": "Springfield",
        "state": "IL",
        "zip_code": "62704",
    }


def _valid_user(**overrides: Any) -> dict[str, Any]:
    base: dict[str, Any] = {
        "name": "Alice",
        "email": "alice@example.com",
        "age": 30,
        "address": _valid_address(),
        "tags": [],
    }
    base.update(overrides)
    return base


# ---------------------------------------------------------------------------
# User creation
# ---------------------------------------------------------------------------


class TestUserCreation:
    def test_valid_user(self) -> None:
        user = User(**_valid_user())
        assert user.name == "Alice"
        assert user.age == 30

    def test_invalid_email_no_at(self) -> None:
        with pytest.raises(ValidationError, match="email"):
            User(**_valid_user(email="not-an-email"))

    def test_age_below_zero(self) -> None:
        with pytest.raises(ValidationError):
            User(**_valid_user(age=-1))

    def test_age_above_150(self) -> None:
        with pytest.raises(ValidationError):
            User(**_valid_user(age=200))


# ---------------------------------------------------------------------------
# Nested Address validation
# ---------------------------------------------------------------------------


class TestAddress:
    def test_valid_address(self) -> None:
        addr = Address(**_valid_address())
        assert addr.city == "Springfield"

    def test_state_too_long(self) -> None:
        with pytest.raises(ValidationError):
            Address(street="1 Elm", city="X", state="Illinois", zip_code="62704")

    def test_bad_zip(self) -> None:
        with pytest.raises(ValidationError):
            Address(street="1 Elm", city="X", state="IL", zip_code="abc")


# ---------------------------------------------------------------------------
# Model validator (cross-field)
# ---------------------------------------------------------------------------


class TestModelValidator:
    def test_under_18_admin_rejected(self) -> None:
        with pytest.raises(ValidationError, match="under 18"):
            User(**_valid_user(age=16, tags=["admin"]))

    def test_under_18_non_admin_ok(self) -> None:
        user = User(**_valid_user(age=16, tags=["reader"]))
        assert user.age == 16

    def test_adult_admin_ok(self) -> None:
        user = User(**_valid_user(age=25, tags=["admin"]))
        assert "admin" in user.tags


# ---------------------------------------------------------------------------
# Discriminated union: Shape
# ---------------------------------------------------------------------------

Shape = Annotated[Circle | Rectangle, Field(discriminator="shape_type")]
ShapeAdapter: TypeAdapter[Circle | Rectangle] = TypeAdapter(Shape)


class TestDiscriminatedUnion:
    def test_circle(self) -> None:
        shape = ShapeAdapter.validate_python({"shape_type": "circle", "radius": 5.0})
        assert isinstance(shape, Circle)
        assert shape.radius == 5.0

    def test_rectangle(self) -> None:
        shape = ShapeAdapter.validate_python(
            {"shape_type": "rectangle", "width": 3.0, "height": 4.0}
        )
        assert isinstance(shape, Rectangle)
        assert shape.width == 3.0

    def test_invalid_discriminator(self) -> None:
        with pytest.raises(ValidationError):
            ShapeAdapter.validate_python({"shape_type": "triangle", "side": 1.0})


# ---------------------------------------------------------------------------
# Serialization round-trip
# ---------------------------------------------------------------------------


class TestSerialization:
    def test_roundtrip(self) -> None:
        original = User(**_valid_user())
        dumped = serialize_user(original)
        recovered = deserialize_user(dumped)
        assert recovered.name == original.name
        assert recovered.email == original.email
        assert recovered.age == original.age

    def test_deserialize_bad_data(self) -> None:
        with pytest.raises(ValidationError):
            deserialize_user({"name": "Bob"})
