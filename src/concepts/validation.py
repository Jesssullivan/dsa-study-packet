"""Pydantic v2 schema validation — with inline Zod (TypeScript) comparisons.

Covers:
    1. BaseModel with field constraints and custom validators.
    2. Nested models and model-level cross-field validation.
    3. Discriminated unions for polymorphic data.
    4. Serialization / deserialization helpers.

Why validation matters at API boundaries:
    Static type checkers (mypy, pyright) verify structure at *development*
    time, but they cannot guard against bad data arriving at *runtime* over
    the network.  Pydantic fills that gap — it validates values, coerces
    types, and produces clear error messages, all with minimal boilerplate.

Pydantic v2 vs v1:
    v2 rewrote the core in Rust (``pydantic-core``), yielding 5--50x
    speedups.  The API shifted: ``model_validate`` replaces ``parse_obj``,
    ``model_dump`` replaces ``.dict()``, and ``model_config`` (a class var)
    replaces the inner ``Config`` class.

References:
    https://docs.pydantic.dev/latest/
    https://zod.dev/  (TypeScript counterpart — see inline comparisons)
"""

from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field, ValidationError, field_validator, model_validator

# ---------------------------------------------------------------------------
# Nested model: Address
# ---------------------------------------------------------------------------
# Zod (TypeScript) equivalent for comparison:
#   AddressSchema = z.object with fields street (z.string min 1),
#   city (z.string min 1), state (z.string length 2),
#   zip_code (z.string regex for 5 digits).
# ---------------------------------------------------------------------------


class Address(BaseModel):
    """A US-style mailing address."""

    street: str = Field(min_length=1)
    city: str = Field(min_length=1)
    state: str = Field(min_length=2, max_length=2)
    zip_code: str = Field(pattern=r"^\d{5}$")


# ---------------------------------------------------------------------------
# Main model: User
# ---------------------------------------------------------------------------
# Zod (TypeScript) equivalent for comparison:
#   UserSchema = z.object with fields name (z.string), email (z.string.email),
#   age (z.number min 0 max 150), address (AddressSchema),
#   tags (z.array of z.string, default empty).
# ---------------------------------------------------------------------------


class User(BaseModel):
    """A user account with nested address and optional tags."""

    name: str
    # We skip EmailStr to avoid the extra ``email-validator`` dependency.
    # Instead, a field_validator does a minimal "@" check.
    email: str
    age: int = Field(ge=0, le=150)
    address: Address
    tags: list[str] = Field(default_factory=list)

    # --- Field-level validator ---
    # Pydantic v2 field validators receive the value *after* core
    # validation (type coercion) but *before* model validators.
    @field_validator("email")
    @classmethod
    def email_must_contain_at(cls, v: str) -> str:
        """Ensure the email contains an '@' character."""
        if "@" not in v:
            msg = "email must contain '@'"
            raise ValueError(msg)
        return v

    # --- Model-level (cross-field) validator ---
    # Runs after all field validators.  ``mode="after"`` means `self`
    # is a fully-constructed User instance.
    @model_validator(mode="after")
    def check_admin_age(self) -> User:
        """Reject users under 18 who carry the 'admin' tag."""
        if self.age < 18 and "admin" in self.tags:
            msg = "users under 18 cannot be admins"
            raise ValueError(msg)
        return self


# ---------------------------------------------------------------------------
# Discriminated union: Shape
# ---------------------------------------------------------------------------
# Discriminated unions let you parse polymorphic JSON into the correct
# model based on a literal field (the "discriminator").  This is much
# faster than trying each model in sequence.
#
# Zod (TypeScript) equivalent for comparison:
#   CircleSchema = z.object with shape_type (z.literal "circle"),
#     radius (z.number positive).
#   RectangleSchema = z.object with shape_type (z.literal "rectangle"),
#     width (z.number positive), height (z.number positive).
#   ShapeSchema = z.discriminatedUnion on "shape_type" with
#     CircleSchema and RectangleSchema.
# ---------------------------------------------------------------------------


class Circle(BaseModel):
    """A circle, identified by ``shape_type = "circle"``."""

    shape_type: Literal["circle"]
    radius: float = Field(gt=0)


class Rectangle(BaseModel):
    """A rectangle, identified by ``shape_type = "rectangle"``."""

    shape_type: Literal["rectangle"]
    width: float = Field(gt=0)
    height: float = Field(gt=0)


# ``Annotated`` + ``Field(discriminator=...)`` tells Pydantic which
# literal field to inspect when deciding which branch to parse.
Shape = Annotated[Circle | Rectangle, Field(discriminator="shape_type")]


# ---------------------------------------------------------------------------
# Serialization helpers
# ---------------------------------------------------------------------------
# ``model_dump()`` converts a model instance to a plain dict.
# ``model_validate()`` creates a model from a dict, running all validators.
# Together they give you a safe serialize/deserialize round-trip.
# ---------------------------------------------------------------------------


def serialize_user(user: User) -> dict[str, object]:
    """Convert a User to a plain dict (JSON-safe)."""
    return user.model_dump()


def deserialize_user(data: dict[str, object]) -> User:
    """Parse and validate *data* into a User instance.

    Raises ``pydantic.ValidationError`` on bad input.
    """
    return User.model_validate(data)


# Re-export ValidationError so test code can import it from here.
__all__ = [
    "Address",
    "Circle",
    "Rectangle",
    "Shape",
    "User",
    "ValidationError",
    "deserialize_user",
    "serialize_user",
]
