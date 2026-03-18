"""Modern Python type-system demonstrations (3.12 - 3.14).

Each section below showcases one typing feature with full inline
commentary.  Together they cover the practical subset of Python's type
system that appears in real codebases and interview discussions.

Sections
--------
1. ``Protocol`` — structural subtyping (PEP 544)
2. ``TypeVar`` with default (PEP 696)
3. ``ParamSpec`` + ``Concatenate`` — signature-preserving decorators (PEP 612)
4. ``TypeGuard`` — user-defined type narrowing (PEP 647)
5. ``@overload`` — multi-signature functions (``typing.overload``)
6. Generic ``Stack[T]`` — PEP 695 syntax (``class Foo[T]``)

References
----------
* PEP 544  — https://peps.python.org/pep-0544/
* PEP 612  — https://peps.python.org/pep-0612/
* PEP 647  — https://peps.python.org/pep-0647/
* PEP 695  — https://peps.python.org/pep-0695/
* PEP 696  — https://peps.python.org/pep-0696/
* typing docs — https://docs.python.org/3.14/library/typing.html
"""

from typing import (
    TYPE_CHECKING,
    Protocol,
    TypeGuard,
    TypeVar,
    overload,
    runtime_checkable,
)

if TYPE_CHECKING:
    from collections.abc import Callable
    from typing import Concatenate

# =========================================================================== #
# 1. Protocol — structural ("duck") typing made explicit          (PEP 544)
# =========================================================================== #
# A Protocol defines a set of methods/attributes that a class must have.
# Unlike ABCs, the conforming class does NOT inherit from the protocol —
# it just needs to have the right shape (structural subtyping).
#
# ``@runtime_checkable`` additionally enables ``isinstance()`` checks,
# though those only verify method *existence*, not signatures.


@runtime_checkable
class Drawable(Protocol):
    """Any object that can ``draw`` itself to a string."""

    def draw(self) -> str: ...


class Circle:
    """A simple shape — satisfies ``Drawable`` without inheriting it.

    >>> c = Circle(5.0)
    >>> c.draw()
    'Circle(radius=5.0)'
    """

    def __init__(self, radius: float) -> None:
        self.radius = radius

    def draw(self) -> str:
        return f"Circle(radius={self.radius})"


def render(item: Drawable) -> str:
    """Call ``.draw()`` on anything that satisfies the ``Drawable`` protocol.

    >>> render(Circle(3.0))
    'Circle(radius=3.0)'
    """
    return item.draw()


# =========================================================================== #
# 2. TypeVar with default                                         (PEP 696)
# =========================================================================== #
# PEP 696 (Python 3.13+) lets a TypeVar specify a *default* type, so
# users of a generic class can omit the type parameter and get a
# sensible default.
#
# Here we define ``NumberT`` bound to int | float, defaulting to int.
# ``Container`` is generic over any type T (no bound, no default) to
# stay flexible.

NumberT = TypeVar("NumberT", bound=int | float, default=int)


class Container[T]:
    """A trivial single-value container, generic over T (PEP 695 syntax).

    Demonstrates:
    * PEP 695 ``class Foo[T]`` generics
    * A ``.transform`` method that maps the contained value

    >>> c = Container(10)
    >>> c.value
    10
    >>> c.transform(lambda x: x * 2).value
    20
    """

    def __init__(self, value: T) -> None:
        self.value: T = value

    def transform[U](self, func: Callable[[T], U]) -> Container[U]:
        """Apply *func* to the contained value, returning a new Container.

        >>> Container("hello").transform(len).value
        5
        """
        return Container(func(self.value))

    def __repr__(self) -> str:
        return f"Container({self.value!r})"


# =========================================================================== #
# 3. ParamSpec + Concatenate — decorators that add parameters     (PEP 612)
# =========================================================================== #
# ``ParamSpec`` captures the *entire* parameter list of a function so
# that decorators can preserve it in type-checker output.
# ``Concatenate`` lets you prepend extra parameters.
#
# Here we build ``add_logging``, which wraps any function and prepends
# a ``verbose: bool`` flag.  When verbose is True, a message is printed.


def add_logging[R, **P](
    func: Callable[P, R],
) -> Callable[Concatenate[bool, P], R]:
    """Decorator that prepends a ``verbose`` boolean parameter.

    When ``verbose=True``, the function name and arguments are printed
    before the call.

    >>> @add_logging
    ... def add(a: int, b: int) -> int:
    ...     return a + b
    >>> add(False, 1, 2)
    3
    """
    # _calls is a list we attach to the wrapper so tests can inspect it.
    calls: list[str] = []

    def wrapper(verbose: bool, /, *args: P.args, **kwargs: P.kwargs) -> R:
        if verbose:
            msg = f"Calling {func.__name__}(args={args}, kwargs={kwargs})"
            calls.append(msg)
        return func(*args, **kwargs)

    # Attach the log list so tests can assert on it without capturing
    # stdout.
    wrapper._calls = calls  # type: ignore[attr-defined]
    return wrapper


# =========================================================================== #
# 4. TypeGuard — user-defined type narrowing                      (PEP 647)
# =========================================================================== #
# A function returning TypeGuard[X] tells the type-checker that when
# the function returns True the argument is narrowed to type X.
#
# This is essential when you do runtime checks that the type-checker
# cannot infer on its own (e.g., verifying every element is a str).


def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    """Check whether *val* is a list consisting entirely of strings.

    >>> is_str_list(["a", "b", "c"])
    True
    >>> is_str_list(["a", 1])
    False
    >>> is_str_list([])
    True
    """
    return all(isinstance(x, str) for x in val)


# =========================================================================== #
# 5. @overload — multiple signatures for one function
# =========================================================================== #
# ``@overload`` lets you declare several type signatures for the same
# function.  The type-checker uses them to determine the return type
# based on the argument types.  Only the *implementation* (the one
# without ``@overload``) runs at runtime.


@overload
def process(x: int) -> int: ...
@overload
def process(x: str) -> list[str]: ...


def process(x: int | str) -> int | list[str]:
    """Return different types based on input type.

    * ``int`` input -> doubled integer
    * ``str`` input -> list of characters

    >>> process(5)
    10
    >>> process("hi")
    ['h', 'i']
    """
    if isinstance(x, int):
        return x * 2
    return list(x)


# =========================================================================== #
# 6. Generic Stack[T] — PEP 695 syntax
# =========================================================================== #
# PEP 695 (Python 3.12+) introduces a compact syntax for generics:
#   ``class Foo[T]:`` instead of ``class Foo(Generic[T]):``
#
# This Stack is the canonical generic-collection example.


class Stack[T]:
    """A LIFO stack, generic over element type T.

    >>> s = Stack[int]()
    >>> s.push(1)
    >>> s.push(2)
    >>> s.peek()
    2
    >>> s.pop()
    2
    >>> s.pop()
    1
    >>> s.is_empty()
    True
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        """Push *item* onto the top of the stack."""
        self._items.append(item)

    def pop(self) -> T:
        """Remove and return the top item.

        Raises ``IndexError`` if the stack is empty.

        >>> Stack[int]().pop()
        Traceback (most recent call last):
            ...
        IndexError: pop from empty stack
        """
        if not self._items:
            msg = "pop from empty stack"
            raise IndexError(msg)
        return self._items.pop()

    def peek(self) -> T:
        """Return the top item without removing it.

        Raises ``IndexError`` if the stack is empty.

        >>> Stack[int]().peek()
        Traceback (most recent call last):
            ...
        IndexError: peek at empty stack
        """
        if not self._items:
            msg = "peek at empty stack"
            raise IndexError(msg)
        return self._items[-1]

    def is_empty(self) -> bool:
        """Return ``True`` if the stack contains no items.

        >>> Stack[int]().is_empty()
        True
        """
        return len(self._items) == 0

    def __len__(self) -> int:
        return len(self._items)

    def __repr__(self) -> str:
        return f"Stack({self._items!r})"
