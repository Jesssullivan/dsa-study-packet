# Python 3.14, Modern Typing, and Advanced Patterns

---

## 1. Python 3.14 New Features

**Released**: October 7, 2025 | **EOL**: ~October 2030
**Release Manager**: Hugo van Kemenade

### PEP 750: Template Strings (t-strings)

T-strings are a generalization of f-strings that return a `Template` object instead of a string, giving access to static and interpolated parts before combination.

```python
from string.templatelib import Template, Interpolation

name = "World"
template = t"Hello {name}!"
# Returns Template, NOT a string

# Access components
template.strings         # ('Hello ', '!')
template.interpolations  # (Interpolation(value='World', expression='name', ...),)
template.values          # ('World',)

# Iteration (skips empty strings)
list(template)  # ['Hello ', Interpolation(value='World', ...), '!']
```

#### Interpolation Object Attributes

```python
template = t"Value: {price!s:.2f}"
interp = template.interpolations[0]
interp.value       # the evaluated result (e.g., 42.5)
interp.expression  # 'price' (source text)
interp.conversion  # 's' (or 'r', 'a', None)
interp.format_spec # '.2f'

# __match_args__ = ("value", "expression", "conversion", "format_spec")
```

#### Processing with Pattern Matching (recommended pattern)

```python
def process(template: Template) -> str:
    parts = []
    for item in template:
        match item:
            case str() as s:
                parts.append(s)
            case Interpolation(value, _, conversion, format_spec):
                value = convert(value, conversion)
                parts.append(format(value, format_spec))
    return "".join(parts)

def convert(value, conversion):
    match conversion:
        case "a": return ascii(value)
        case "r": return repr(value)
        case "s": return str(value)
        case _:   return value
```

#### SQL Injection Prevention

```python
def safe_sql(template: Template) -> tuple[str, tuple]:
    parts, params = [], []
    for item in template:
        match item:
            case str() as s:
                parts.append(s)
            case Interpolation() as interp:
                parts.append("?")
                params.append(interp.value)
    return "".join(parts), tuple(params)

username = "'; DROP TABLE students;--"
query, params = safe_sql(t"SELECT * FROM students WHERE name = {username}")
# ("SELECT * FROM students WHERE name = ?", ("'; DROP TABLE students;--",))
```

#### HTML Escaping (XSS Prevention)

```python
import html as html_mod

def safe_html(template: Template) -> str:
    parts = []
    for item in template:
        match item:
            case str() as s:
                parts.append(s)
            case Interpolation() as interp:
                parts.append(html_mod.escape(str(interp.value)))
    return "".join(parts)

evil = "<b onmouseover='steal()'>evil</b>"
safe_html(t"<p>{evil}</p>")
# '<p>&lt;b onmouseover=&#x27;steal()&#x27;&gt;evil&lt;/b&gt;</p>'
```

#### Structured Logging

```python
import json, logging

class TemplateMessage:
    def __init__(self, template: Template) -> None:
        self.template = template

    @property
    def values(self) -> dict[str, object]:
        return {
            item.expression: item.value
            for item in self.template
            if isinstance(item, Interpolation)
        }

    def __str__(self) -> str:
        parts = []
        for item in self.template:
            match item:
                case str() as s: parts.append(s)
                case Interpolation() as i: parts.append(str(i.value))
        msg = "".join(parts)
        return f"{msg} >>> {json.dumps(self.values)}"

action, amount = "refund", 42.0
logging.info(TemplateMessage(t"Process {action}: {amount:.2f}"))
# "Process refund: 42.00 >>> {"action": "refund", "amount": 42.0}"
```

#### Concatenation Rules

```python
# Template + Template = Template
t"Hello " + t"{name}" == t"Hello {name}"  # OK
t"Hello " t"{name}"                        # Implicit concat OK

# Template + str is PROHIBITED (ambiguous)
# Must be explicit:
t"Hello " + Template(name)                  # treat as static text
t"Hello " + Template(Interpolation(name))   # treat as interpolation
```

#### Other t-string Details

```python
# Raw t-strings
rt"path: {p}\n"   # backslashes literal, interpolations processed
tr"path: {p}\n"   # same

# Debug specifier
t"Hello {name=}"
# strings[0] == "Hello name="  (expression embedded in static part)
# interpolations[0].conversion == "r"

# No __str__: Template has no default string conversion
# str(template) raises TypeError -- must use a processing function

# No __eq__: Templates compare by identity, not structural equality
```

### PEP 649/749: Deferred Evaluation of Annotations

Annotations are no longer evaluated eagerly. Stored as special annotate functions.

```python
from annotationlib import get_annotations, Format

def func(arg: Undefined):  # No NameError at definition time!
    pass

get_annotations(func, format=Format.VALUE)       # raises NameError
get_annotations(func, format=Format.FORWARDREF)   # returns ForwardRef objects
get_annotations(func, format=Format.STRING)        # returns strings
```

New module: `annotationlib`

### PEP 734: Multiple Interpreters (Subinterpreters)

True multi-core parallelism without GIL limitations.

```python
from concurrent.interpreters import Interpreter
import concurrent.futures

interp = Interpreter()
interp.run("print('Hello from subinterpreter')")

# Thread pool equivalent for interpreters
with concurrent.futures.InterpreterPoolExecutor() as executor:
    results = executor.map(compute, data)
```

New module: `concurrent.interpreters`

### PEP 784: Zstandard Compression

```python
from compression import zstd

compressed = zstd.compress(b"data" * 100)
original = zstd.decompress(compressed)

# Also integrated into tarfile, zipfile, shutil
```

### PEP 758: Bracketless Exception Groups

```python
try:
    connect()
except TimeoutError, ConnectionRefusedError:  # no parens needed (without 'as')
    print("Network error")

# With 'as' still requires parens:
except (TimeoutError, ConnectionRefusedError) as e:
    print(e)
```

### PEP 768: Safe External Debugger Interface

```python
import sys
sys.remote_exec(pid, script_path)  # zero-overhead remote debugging

# pdb remote attach
# python -m pdb -p <PID>
```

### heapq Max-Heap Functions (NEW)

```python
import heapq

# NEW in 3.14 -- native max-heap support
h = [3, 1, 4, 1, 5, 9]
heapq.heapify_max(h)        # transform to max-heap in O(n)
h[0]                         # peek at largest

heapq.heappush_max(h, 7)    # push maintaining max-heap
heapq.heappop_max(h)        # pop largest O(log n)
heapq.heappushpop_max(h, 6) # push then pop largest (efficient)
heapq.heapreplace_max(h, 2) # pop largest then push (efficient)

# Running median using both heap types
def running_median(iterable):
    lo = []  # max-heap (lower half)
    hi = []  # min-heap (upper half)
    for x in iterable:
        if len(lo) == len(hi):
            heapq.heappush_max(lo, heapq.heappushpop(hi, x))
            yield lo[0]
        else:
            heapq.heappush(hi, heapq.heappushpop_max(lo, x))
            yield (lo[0] + hi[0]) / 2
```

### functools.Placeholder (NEW)

```python
from functools import partial, Placeholder as _

# Skip positional arguments with placeholder
say_to = partial(print, _, _, "world!")
say_to("Hello", "dear")  # Hello dear world!

# Nested placeholders
remove = partial(str.replace, _, _, "")
remove("Hello world", " world")  # "Hello"
```

### Other Notable 3.14 Changes

- **Tail-call interpreter**: 3-5% faster (Clang 19+, x86-64/AArch64)
- **Incremental GC**: order of magnitude fewer pause times, only 2 generations
- **Free-threaded mode (PEP 779)**: officially supported, 5-10% single-thread penalty
- **REPL syntax highlighting**: enabled by default
- **pathlib**: `copy()`, `copy_into()`, `move()`, `move_into()` methods
- **asyncio introspection**: `python -m asyncio ps PID`, `capture_call_graph()`
- **json CLI**: `python -m json` with color highlighting
- **map() strict flag**: `map(fn, a, b, strict=True)` raises on unequal lengths
- **Decimal.from_number()**: new constructor
- **http.server.HTTPSServer**: built-in HTTPS support
- **multiprocessing**: `forkserver` default on Unix, `Process.interrupt()`

---

## 2. Modern Python Typing (2025-2026)

### Type Parameter Syntax (PEP 695, Python 3.12+)

```python
# OLD way
from typing import TypeVar, Generic
T = TypeVar('T')
class Stack(Generic[T]):
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...

# NEW way (3.12+)
class Stack[T]:
    def push(self, item: T) -> None: ...
    def pop(self) -> T: ...

# Bounded
class StrContainer[S: str]:
    def get(self) -> S: ...

# Constrained
class NumContainer[N: (int, float)]:
    def get(self) -> N: ...

# Generic functions
def first[T](lst: list[T]) -> T:
    return lst[0]

# Generic type aliases (PEP 695)
type Vector = list[float]
type Response[S] = Iterable[S] | int
type Matrix[T] = list[list[T]]
```

### Type Defaults (PEP 696, Python 3.13+)

```python
# TypeVar with default
from typing import TypeVar
T = TypeVar('T', default=int)

# In new syntax
class Container[T = int]:
    def __init__(self, value: T) -> None: ...

Container()       # Container[int] inferred
Container("hi")   # Container[str] inferred
```

### ParamSpec (PEP 612)

Captures the full parameter signature of callables -- essential for typed decorators.

```python
from collections.abc import Callable
from typing import ParamSpec

P = ParamSpec('P')

# New syntax
def add_logging[T, **P](f: Callable[P, T]) -> Callable[P, T]:
    def inner(*args: P.args, **kwargs: P.kwargs) -> T:
        print(f"Calling {f.__name__}")
        return f(*args, **kwargs)
    return inner

@add_logging
def greet(name: str, excited: bool = False) -> str:
    return f"Hello {name}{'!' if excited else '.'}"

# greet still has correct type signature: (name: str, excited: bool = False) -> str
```

### Concatenate (with ParamSpec)

```python
from typing import Concatenate
from threading import Lock

def with_lock[**P, R](
    f: Callable[Concatenate[Lock, P], R]
) -> Callable[P, R]:
    lock = Lock()
    def inner(*args: P.args, **kwargs: P.kwargs) -> R:
        with lock:
            return f(lock, *args, **kwargs)
    return inner
```

### TypeVarTuple (PEP 646)

Variadic generics -- parameterize with arbitrary number of types.

```python
# New syntax
def move_first[T, *Ts](tup: tuple[T, *Ts]) -> tuple[*Ts, T]:
    return (*tup[1:], tup[0])

move_first((1, "a", 3.0))  # tuple[str, float, int]

# Typed array shapes
class Array[DType, *Shape]:
    def __getitem__(self, key: tuple[*Shape]) -> DType: ...

class H: ...
class W: ...
img: Array[float, H, W]  # 2D float array
```

### Protocol (Structural Subtyping)

```python
from typing import Protocol, runtime_checkable

class Drawable(Protocol):
    def draw(self) -> None: ...

class Circle:
    def draw(self) -> None:
        print("O")

def render(shape: Drawable) -> None:
    shape.draw()

render(Circle())  # OK -- no inheritance needed

# Runtime checking
@runtime_checkable
class Named(Protocol):
    name: str

import threading
isinstance(threading.Thread(name="t"), Named)  # True
# WARNING: only checks attribute existence, not types

# Callable Protocol (for complex signatures)
class Combiner(Protocol):
    def __call__(self, *vals: bytes, maxlen: int | None = None) -> list[bytes]: ...
```

### TypeGuard vs TypeIs

```python
from typing import TypeGuard, TypeIs  # TypeIs is 3.13+

# TypeGuard: narrows type on True only
def is_str_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

def f(val: list[object]):
    if is_str_list(val):
        print(" ".join(val))  # narrowed to list[str]

# TypeIs (3.13+): uses intersection, narrows on BOTH branches
class Parent: ...
class Child(Parent): ...

def is_parent(val: object) -> TypeIs[Parent]:
    return isinstance(val, Parent)

def g(arg: Child | int):
    if is_parent(arg):
        # narrowed to Child (intersection of Parent & (Child|int))
        reveal_type(arg)  # Child
    else:
        reveal_type(arg)  # int
```

### ReadOnly TypedDict (3.13+)

```python
from typing import TypedDict, ReadOnly

class Config(TypedDict):
    name: ReadOnly[str]     # immutable
    version: ReadOnly[int]  # immutable
    debug: bool             # mutable

def update(c: Config) -> None:
    c["debug"] = True       # OK
    c["name"] = "new"       # type checker ERROR
```

### Union Syntax and Other Modern Forms

```python
# Union (3.10+)
x: int | str | None

# Self type (3.11+)
from typing import Self
class Builder:
    def set_name(self, name: str) -> Self:
        self.name = name
        return self

# Unpack for TypedDict kwargs (3.12+)
from typing import Unpack
class Options(TypedDict):
    timeout: int
    retries: int

def fetch(url: str, **kwargs: Unpack[Options]) -> bytes: ...

# Never type (3.11+)
from typing import Never
def fail(msg: str) -> Never:
    raise RuntimeError(msg)

# assert_type (3.11+)
from typing import assert_type
assert_type(42, int)  # passes type checking
```

---

## 3. Structural Pattern Matching (Advanced)

### All Pattern Types

```python
# 1. Literal patterns
match command:
    case "quit": sys.exit()
    case 42: print("the answer")
    case True: print("truthy")
    case None: print("nothing")

# 2. Capture patterns (bind to variable)
match point:
    case (x, y): print(f"({x}, {y})")

# 3. Wildcard
    case _: print("no match")

# 4. OR patterns
    case "quit" | "exit" | "q": sys.exit()

# 5. AS patterns
    case ("quit" | "exit") as cmd: log(cmd)

# 6. Guard clauses
    case int(x) if x > 0: print("positive")
    case int(x) if x % 2 == 0: print("even")

# 7. Sequence patterns (with star)
    case []: print("empty")
    case [x]: print(f"one: {x}")
    case [first, *middle, last]: print(f"{len(middle)+2} items")
    case [x, y, z, *rest] if not rest: print("exactly 3")

# 8. Mapping patterns
    case {"name": name, "age": age, "role": "admin"}:
        print(f"admin {name}")
    case {"name": name, **rest}:  # capture remaining keys
        print(f"{name}, extras: {rest}")

# 9. Class patterns
    case Point(x=0, y=0): print("origin")
    case Point(x=0, y=y): print(f"y-axis at {y}")
    case Point(x, y) if x == y: print("diagonal")

# 10. Nested patterns
    case {"users": [{"name": name, "role": "admin"}, *_]}:
        print(f"first admin: {name}")

# 11. Type patterns
    case int(n): print(f"int: {n}")
    case str(s) if len(s) > 10: print("long string")
    case list() as lst: print(f"list of {len(lst)}")
```

### Pattern Matching with Dataclasses

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

@dataclass
class Circle:
    center: Point
    radius: float

@dataclass
class Rect:
    corner: Point
    width: float
    height: float

def describe(shape):
    match shape:
        case Circle(center=Point(0, 0), radius=r):
            return f"Circle at origin, r={r}"
        case Circle(center=Point(x, y), radius=r) if r > 10:
            return f"Large circle at ({x},{y})"
        case Rect(corner=Point(x, y), width=w, height=h) if w == h:
            return f"Square at ({x},{y}), side={w}"
        case Rect(width=w, height=h):
            return f"Rectangle {w}x{h}"
```

### Pattern Matching with Enums

```python
from enum import Enum

class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3

match color:
    case Color.RED: ...
    case Color.GREEN | Color.BLUE: ...
```

### Type Narrowing with Match

```python
def process(value: int | str | list[int]) -> str:
    match value:
        case int(n):
            # type narrowed to int
            return str(n * 2)
        case str(s):
            # type narrowed to str
            return s.upper()
        case [*items]:
            # type narrowed to list
            return str(sum(items))
```

---

## 4. Dataclasses vs NamedTuple vs TypedDict

### Comparison Table

| Feature | dataclass | NamedTuple | TypedDict |
|---------|-----------|------------|-----------|
| Mutable | Yes (unless `frozen`) | No | Yes (dict) |
| Hashable | Only if `frozen` | Yes | No |
| Indexable | No | Yes (`t[0]`) | Yes (`d["key"]`) |
| Methods | Yes | Limited | No |
| Inheritance | Full | Limited | Yes |
| `__slots__` | 3.10+ | Implicit | N/A |
| Memory | Medium | Low | Medium |
| Runtime validation | No | No | No |
| Iterable | No | Yes (tuple) | Yes (dict) |

### When to Use Each

```python
# DATACLASS: general-purpose data objects, internal logic
from dataclasses import dataclass, field

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float
    label: str = ""
    tags: list[str] = field(default_factory=list)

    def distance(self, other: "Point") -> float:
        return ((self.x - other.x)**2 + (self.y - other.y)**2) ** 0.5

# Post-init processing
@dataclass
class Temperature:
    celsius: float
    fahrenheit: float = field(init=False)

    def __post_init__(self):
        self.fahrenheit = self.celsius * 9/5 + 32

# NAMEDTUPLE: immutable records, function returns, lightweight
from typing import NamedTuple

class Coordinate(NamedTuple):
    lat: float
    lon: float
    alt: float = 0.0

c = Coordinate(40.7, -74.0)
lat, lon, alt = c           # unpacking
c[0]                         # indexing
c._asdict()                  # {'lat': 40.7, 'lon': -74.0, 'alt': 0.0}
c._replace(alt=100.0)        # new instance with changed field

# TYPEDDICT: typed dicts for JSON/API interfaces
from typing import TypedDict, Required, NotRequired, ReadOnly

class UserResponse(TypedDict):
    id: Required[int]
    name: str
    email: NotRequired[str]    # optional key
    role: ReadOnly[str]        # 3.13+

def parse_user(data: dict) -> UserResponse:
    return data  # type checker validates structure
```

---

## 5. functools Patterns

### cache / lru_cache

```python
from functools import cache, lru_cache

@cache  # unbounded, thread-safe (3.9+)
def fib(n):
    return n if n < 2 else fib(n-1) + fib(n-2)

@lru_cache(maxsize=256, typed=True)  # bounded, typed caching
def fetch(url: str) -> bytes: ...

fetch.cache_info()    # CacheInfo(hits=3, misses=8, maxsize=256, currsize=8)
fetch.cache_clear()   # clear entire cache

# GOTCHA: args must be hashable
# Convert: tuple(lst), frozenset(s), tuple(sorted(d.items()))
```

### reduce

```python
from functools import reduce

reduce(lambda a, b: a + b, [1,2,3,4])       # 10
reduce(lambda a, b: a * b, [1,2,3,4])       # 24
reduce(lambda a, b: a if a > b else b, lst)  # max
reduce(lambda a, b: {**a, **b}, dicts)       # merge dicts

# Flatten nested lists
reduce(lambda a, b: a + b, [[1,2],[3,4],[5]], [])  # [1,2,3,4,5]

# 3.14: initial as keyword arg
reduce(lambda a, b: a + b, [1,2,3], initial=100)  # 106
```

### partial and Placeholder (3.14+)

```python
from functools import partial, Placeholder as _

# Classic partial
int_from_binary = partial(int, base=2)
int_from_binary("1010")  # 10

# Placeholder (3.14+) -- skip positional args
remove_spaces = partial(str.replace, _, " ", "")
remove_spaces("hello world")  # "helloworld"

# Partial as factory
from operator import mul
double = partial(mul, 2)
double(21)  # 42
```

### singledispatch

```python
from functools import singledispatch

@singledispatch
def serialize(obj) -> str:
    raise TypeError(f"Cannot serialize {type(obj)}")

@serialize.register
def _(obj: int | float) -> str:
    return str(obj)

@serialize.register
def _(obj: str) -> str:
    return f'"{obj}"'

@serialize.register(list)
def _(obj: list) -> str:
    items = ", ".join(serialize(x) for x in obj)
    return f"[{items}]"

@serialize.register(dict)
def _(obj: dict) -> str:
    pairs = ", ".join(f"{serialize(k)}: {serialize(v)}" for k, v in obj.items())
    return f"{{{pairs}}}"

serialize(42)                    # "42"
serialize("hello")               # '"hello"'
serialize([1, "a", [2]])         # '[1, "a", [2]]'
serialize.dispatch(float)        # returns the int|float handler
serialize.registry.keys()        # all registered types
```

### singledispatchmethod (for classes)

```python
from functools import singledispatchmethod

class Formatter:
    @singledispatchmethod
    def format(self, arg):
        raise TypeError(f"Unsupported: {type(arg)}")

    @format.register
    def _(self, arg: int):
        return f"int({arg})"

    @format.register
    def _(self, arg: str):
        return f"str({arg!r})"

    # With classmethod -- singledispatchmethod MUST be outermost
    @singledispatchmethod
    @classmethod
    def from_value(cls, val):
        raise TypeError

    @from_value.register
    @classmethod
    def _(cls, val: int):
        return cls(val)
```

### total_ordering

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, major: int, minor: int, patch: int):
        self.major, self.minor, self.patch = major, minor, patch

    def __eq__(self, other):
        if not isinstance(other, Version): return NotImplemented
        return (self.major, self.minor, self.patch) == (other.major, other.minor, other.patch)

    def __lt__(self, other):
        if not isinstance(other, Version): return NotImplemented
        return (self.major, self.minor, self.patch) < (other.major, other.minor, other.patch)

# Automatically generates __le__, __gt__, __ge__
Version(1, 2, 0) >= Version(1, 1, 9)  # True
```

### cached_property

```python
from functools import cached_property

class Dataset:
    def __init__(self, data: list[float]):
        self._data = data

    @cached_property
    def mean(self) -> float:
        return sum(self._data) / len(self._data)

    @cached_property
    def variance(self) -> float:
        m = self.mean
        return sum((x - m)**2 for x in self._data) / len(self._data)

ds = Dataset([1.0, 2.0, 3.0])
ds.mean      # computed once, then cached as instance attribute
del ds.mean  # clear cache; next access recomputes
# NOTE: NOT thread-safe in 3.12+
```

---

## 6. Factory and Functional Patterns

### Why Abstract Factory Is Unnecessary in Python

Python has first-class functions and classes -- they ARE factories.

```python
import json
from decimal import Decimal

# The class itself is a factory
json.loads('{"price": 42.5}', parse_float=Decimal)

# Any callable works as a factory
def create_connection(host: str, port: int):
    return Connection(host, port)

factory = create_connection  # pass around as value
conn = factory("localhost", 5432)
```

### Callable Protocol (typed factory interface)

```python
from typing import Protocol

class WidgetFactory(Protocol):
    def __call__(self, name: str, width: int = 100) -> "Widget": ...

# Any of these satisfy WidgetFactory:

# 1. A function
def make_button(name: str, width: int = 100) -> Widget:
    return Button(name, width)

# 2. A class (its __init__ matches)
class Label(Widget):
    def __init__(self, name: str, width: int = 100): ...

# 3. An object with __call__
class ThemedFactory:
    def __init__(self, theme: str):
        self.theme = theme
    def __call__(self, name: str, width: int = 100) -> Widget:
        return ThemedWidget(name, width, self.theme)

def render(factory: WidgetFactory) -> None:
    w = factory("submit", width=200)
```

### Closures as Factories

```python
def make_multiplier(factor: float):
    def multiply(x: float) -> float:
        return x * factor
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)
double(21)  # 42

# Closure with mutable state
def make_counter(start: int = 0):
    count = start
    def counter() -> int:
        nonlocal count
        count += 1
        return count
    return counter

c = make_counter()
c(), c(), c()  # 1, 2, 3
```

### Decorator as Factory

```python
from functools import wraps
from time import time

# Decorator factory (parametrized decorator)
def retry(max_attempts: int = 3, delay: float = 1.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt == max_attempts - 1:
                        raise
            return None  # unreachable
        return wrapper
    return decorator

@retry(max_attempts=5, delay=0.5)
def fetch_data(url: str) -> dict: ...

# Registry pattern (decorator factory for plugins)
registry: dict[str, type] = {}

def register(name: str):
    def decorator(cls):
        registry[name] = cls
        return cls
    return decorator

@register("csv")
class CSVParser: ...

@register("json")
class JSONParser: ...

parser = registry["csv"]()  # instantiate by name
```

### singledispatch as Factory

```python
from functools import singledispatch

@singledispatch
def create_from(source) -> "Document":
    raise TypeError(f"Cannot create from {type(source)}")

@create_from.register
def _(source: str) -> "Document":
    return Document.from_text(source)

@create_from.register
def _(source: dict) -> "Document":
    return Document.from_dict(source)

@create_from.register
def _(source: bytes) -> "Document":
    return Document.from_binary(source)
```

### partial as Factory

```python
from functools import partial

class Connection:
    def __init__(self, host, port, ssl=False, timeout=30): ...

# Pre-configured factories
local_conn = partial(Connection, "localhost", 5432)
prod_conn = partial(Connection, "prod.db.example.com", 5432, ssl=True, timeout=10)

conn = local_conn()             # Connection("localhost", 5432)
conn = prod_conn(timeout=60)    # override timeout
```

---

## 7. contextlib Patterns

### @contextmanager

```python
from contextlib import contextmanager

@contextmanager
def timer(label: str):
    start = time.monotonic()
    try:
        yield
    finally:
        elapsed = time.monotonic() - start
        print(f"{label}: {elapsed:.3f}s")

with timer("query"):
    run_query()

# Can also use as decorator
@timer("process")
def process_data(): ...
```

### @asynccontextmanager

```python
from contextlib import asynccontextmanager

@asynccontextmanager
async def managed_session():
    session = await create_session()
    try:
        yield session
    finally:
        await session.close()

async with managed_session() as s:
    await s.execute("SELECT 1")
```

### suppress

```python
from contextlib import suppress

with suppress(FileNotFoundError):
    os.remove("temp.txt")

# Equivalent to:
try:
    os.remove("temp.txt")
except FileNotFoundError:
    pass

# 3.12+: works with except* / ExceptionGroups
with suppress(ValueError):
    raise ExceptionGroup("g", [ValueError(), ValueError()])
```

### ExitStack (programmatic context management)

```python
from contextlib import ExitStack

# Open variable number of files
with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in filenames]
    # All files closed on exit, even if one open fails

# Conditional cleanup
with ExitStack() as stack:
    conn = stack.enter_context(get_connection())
    stack.callback(log_completion, conn.id)  # arbitrary callback
    if needs_transaction:
        tx = stack.enter_context(conn.begin())

# Transfer ownership
stack = ExitStack()
resource = stack.enter_context(open("data.txt"))
transfer = stack.pop_all()  # moves all cleanup to new stack
# resource stays open; call transfer.close() later
```

### nullcontext

```python
from contextlib import nullcontext

def process(path_or_file):
    if isinstance(path_or_file, str):
        cm = open(path_or_file)
    else:
        cm = nullcontext(path_or_file)
    with cm as f:
        return f.read()

# Optional locking
lock = threading.Lock() if thread_safe else nullcontext()
with lock:
    do_work()
```

### chdir (3.11+)

```python
from contextlib import chdir

with chdir("/tmp"):
    # cwd is /tmp
    files = os.listdir(".")
# original cwd restored
```

---

## 8. Hypothesis: Property-Based Testing

### Basic Usage

```python
from hypothesis import given, example, assume, settings
from hypothesis import strategies as st

@given(st.integers(), st.integers())
def test_addition_commutative(a, b):
    assert a + b == b + a

# Explicit examples alongside generated ones
@given(st.text())
@example("")
@example("edge case")
def test_string_roundtrip(s):
    assert s == s.encode("utf-8").decode("utf-8")

# Filtering with assume
@given(st.integers())
def test_division(n):
    assume(n != 0)
    assert 1 / n != 0
```

### Core Strategies

```python
import hypothesis.strategies as st

# Primitives
st.integers(min_value=0, max_value=100)
st.floats(min_value=0.0, allow_nan=False, allow_infinity=False)
st.text(min_size=1, max_size=50, alphabet=st.characters(whitelist_categories=("L",)))
st.booleans()
st.none()
st.binary(min_size=1, max_size=100)

# Collections
st.lists(st.integers(), min_size=1, max_size=10, unique=True)
st.tuples(st.integers(), st.text())
st.dictionaries(st.text(min_size=1), st.integers())
st.frozensets(st.integers())
st.sets(st.integers(), min_size=1)

# Choices
st.one_of(st.integers(), st.text())       # union of strategies
st.sampled_from(["red", "green", "blue"])  # pick from list
st.just(42)                                # constant value

# Transforms
st.integers().map(lambda n: n * 2)         # transform values
st.integers().filter(lambda n: n % 2 == 0) # filter values

# Recursive structures (e.g., JSON)
json_values = st.recursive(
    st.none() | st.booleans() | st.integers() | st.floats(allow_nan=False) | st.text(),
    lambda children: st.lists(children) | st.dictionaries(st.text(), children),
    max_leaves=50,
)
```

### @composite: Custom Strategies

```python
@st.composite
def ordered_pairs(draw):
    """Generate (a, b) where a <= b."""
    a = draw(st.integers())
    b = draw(st.integers(min_value=a))
    return (a, b)

@st.composite
def sorted_lists(draw, elements=st.integers(), min_size=0):
    """Generate sorted lists."""
    lst = draw(st.lists(elements, min_size=min_size))
    return sorted(lst)

@st.composite
def valid_user(draw):
    """Generate user dicts with consistent data."""
    name = draw(st.text(min_size=1, max_size=50))
    age = draw(st.integers(min_value=0, max_value=150))
    email = draw(st.emails())  # built-in email strategy
    return {"name": name, "age": age, "email": email}

@given(ordered_pairs())
def test_range(pair):
    a, b = pair
    assert a <= b
```

### builds: Strategy from Constructor

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
    active: bool = True

# Automatically infers strategies from type hints
users = st.builds(User)

# Or override specific fields
users = st.builds(User, age=st.integers(min_value=18, max_value=99))

@given(users)
def test_user_creation(user):
    assert isinstance(user, User)
    assert 18 <= user.age <= 99
```

### Stateful Testing (RuleBasedStateMachine)

Tests sequences of operations, not just individual calls.

```python
from hypothesis.stateful import (
    RuleBasedStateMachine, Bundle, rule, precondition,
    invariant, initialize, consumes
)
from hypothesis import settings

class SetStateMachine(RuleBasedStateMachine):
    """Test that our CustomSet behaves like Python's set."""

    def __init__(self):
        super().__init__()
        self.model = set()          # reference implementation
        self.real = CustomSet()     # implementation under test

    values = Bundle("values")

    @initialize(target=values)
    def seed_value(self, x=st.integers()):
        return x

    @rule(target=values, x=st.integers())
    def add_value(self, x):
        self.model.add(x)
        self.real.add(x)
        return x

    @rule(x=values)
    def remove_value(self, x):
        self.model.discard(x)
        self.real.discard(x)

    @rule(x=consumes(values))  # removes from bundle after use
    def consume_value(self, x):
        assert (x in self.model) == (x in self.real)

    @precondition(lambda self: len(self.model) > 0)
    @rule()
    def check_length(self):
        assert len(self.model) == len(self.real)

    @invariant()
    def contents_match(self):
        assert self.model == set(self.real)

# Run as pytest test
TestSetMachine = SetStateMachine.TestCase
TestSetMachine.settings = settings(max_examples=100, stateful_step_count=50)
```

### Settings and Configuration

```python
from hypothesis import settings, HealthCheck, Phase

@settings(
    max_examples=500,           # default 100
    deadline=None,              # disable slow-test deadline
    suppress_health_check=[HealthCheck.too_slow],
    database=None,              # disable example database
    derandomize=True,           # reproducible (uses function hash as seed)
)
@given(st.lists(st.integers()))
def test_sort_idempotent(lst):
    assert sorted(sorted(lst)) == sorted(lst)

# Profile-based settings
settings.register_profile("ci", max_examples=1000)
settings.register_profile("dev", max_examples=10)
settings.load_profile("ci")  # or via HYPOTHESIS_PROFILE env var
```

---

## 9. pytest Modern Patterns

### Fixtures: Scope and Lifecycle

```python
import pytest

# Scope: function (default) < class < module < package < session
@pytest.fixture(scope="session")
def db():
    conn = create_db_connection()
    yield conn
    conn.close()

@pytest.fixture(scope="module")
def populated_db(db):
    db.load_fixtures("test_data.sql")
    yield db
    db.truncate_all()

@pytest.fixture  # default: function scope
def user(populated_db):
    return populated_db.create_user("test@example.com")
```

### Factory Fixtures

```python
@pytest.fixture
def make_user(db):
    created = []
    def _make(name: str, role: str = "user") -> User:
        u = db.create_user(name=name, role=role)
        created.append(u)
        return u
    yield _make
    for u in created:
        db.delete_user(u.id)

def test_admin_access(make_user):
    admin = make_user("Alice", role="admin")
    viewer = make_user("Bob", role="viewer")
    assert admin.can_access("/admin")
    assert not viewer.can_access("/admin")
```

### Parametrize

```python
@pytest.mark.parametrize("input,expected", [
    ("hello", 5),
    ("", 0),
    ("world!", 6),
])
def test_string_length(input, expected):
    assert len(input) == expected

# Parametrize with IDs and marks
@pytest.mark.parametrize("n,expected", [
    pytest.param(0, 1, id="base-case"),
    pytest.param(5, 120, id="normal"),
    pytest.param(-1, None, id="negative", marks=pytest.mark.xfail),
])
def test_factorial(n, expected):
    assert factorial(n) == expected

# Multiple parametrize = cartesian product
@pytest.mark.parametrize("x", [1, 2])
@pytest.mark.parametrize("y", [10, 20])
def test_multiply(x, y):
    assert x * y > 0  # runs 4 times: (1,10), (1,20), (2,10), (2,20)
```

### Parametrized Fixtures

```python
@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def db_engine(request):
    engine = create_engine(request.param)
    yield engine
    engine.dispose()

def test_query(db_engine):
    # runs 3 times, once per engine
    result = db_engine.execute("SELECT 1")
    assert result.scalar() == 1
```

### conftest.py Patterns

```
tests/
    conftest.py              # session/package-wide fixtures
    unit/
        conftest.py          # unit-test specific fixtures
        test_models.py
    integration/
        conftest.py          # integration-test fixtures (db, api client)
        test_api.py
```

```python
# tests/conftest.py
import pytest

@pytest.fixture(scope="session")
def app():
    return create_app(testing=True)

# Custom markers
def pytest_configure(config):
    config.addinivalue_line("markers", "slow: marks tests as slow")

# Skip slow tests by default
def pytest_collection_modifyitems(config, items):
    if not config.getoption("--runslow"):
        skip_slow = pytest.mark.skip(reason="need --runslow option")
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(skip_slow)

def pytest_addoption(parser):
    parser.addoption("--runslow", action="store_true", default=False)
```

### Autouse and usefixtures

```python
@pytest.fixture(autouse=True)
def reset_environment():
    """Runs before/after every test automatically."""
    os.environ["MODE"] = "test"
    yield
    os.environ.pop("MODE", None)

@pytest.mark.usefixtures("db_cleanup")
class TestDatabase:
    """All tests in this class use db_cleanup fixture."""
    def test_insert(self, db): ...
    def test_delete(self, db): ...
```

### Dynamic Scope

```python
def determine_scope(fixture_name, config):
    if config.getoption("--reuse-containers"):
        return "session"
    return "function"

@pytest.fixture(scope=determine_scope)
def docker_container():
    container = start_container()
    yield container
    stop_container(container)
```

### Useful Plugins

| Plugin | Purpose |
|--------|---------|
| `pytest-xdist` | Parallel test execution (`-n auto`) |
| `pytest-cov` | Coverage reporting (`--cov=src`) |
| `pytest-mock` | `mocker` fixture (thin `unittest.mock` wrapper) |
| `pytest-asyncio` | Async test support (`@pytest.mark.asyncio`) |
| `pytest-benchmark` | Performance benchmarking |
| `pytest-randomly` | Randomize test order |
| `pytest-timeout` | Per-test timeouts |
| `pytest-lazy-fixtures` | Use fixtures in parametrize (maintained fork) |
| `pytest-httpx` | Mock HTTPX requests |

### pytest + hypothesis Integration

```python
from hypothesis import given, settings
import hypothesis.strategies as st

# Hypothesis works natively with pytest fixtures via @given
@given(st.lists(st.integers()))
def test_sort_preserves_length(xs):
    assert len(sorted(xs)) == len(xs)

# Combine with pytest.mark.parametrize
@pytest.mark.parametrize("fn", [sorted, list.sort])
@given(data=st.data())
def test_sort_functions(fn, data):
    xs = data.draw(st.lists(st.integers()))
    # ...
```

---

## Sources

- [PEP 750 -- Template Strings](https://peps.python.org/pep-0750/)
- [What's New in Python 3.14](https://docs.python.org/3/whatsnew/3.14.html)
- [PEP 745 -- Python 3.14 Release Schedule](https://peps.python.org/pep-0745/)
- [Python 3.14 Template Strings -- Real Python](https://realpython.com/python-t-strings/)
- [Python's New T-Strings -- Dave Peck](https://davepeck.org/2025/04/11/pythons-new-t-strings/)
- [string.templatelib Documentation](https://docs.python.org/3/library/string.templatelib.html)
- [typing Module Documentation](https://docs.python.org/3/library/typing.html)
- [PEP 695 -- Type Parameter Syntax](https://peps.python.org/pep-0695/)
- [PEP 696 -- Type Defaults for Type Parameters](https://peps.python.org/pep-0696/)
- [Generics -- typing spec](https://typing.python.org/en/latest/spec/generics.html)
- [functools Documentation](https://docs.python.org/3/library/functools.html)
- [contextlib Documentation](https://docs.python.org/3/library/contextlib.html)
- [heapq Documentation](https://docs.python.org/3/library/heapq.html)
- [PEP 636 -- Structural Pattern Matching Tutorial](https://peps.python.org/pep-0636/)
- [Pattern Matching Guide -- Better Stack](https://betterstack.com/community/guides/scaling-python/python-pattern-matching/)
- [The Abstract Factory Pattern -- Python Patterns](https://python-patterns.guide/gang-of-four/abstract-factory/)
- [Hypothesis Documentation](https://hypothesis.readthedocs.io/)
- [Hypothesis Stateful Testing](https://hypothesis.readthedocs.io/en/latest/stateful.html)
- [Hypothesis Custom Strategies](https://hypothesis.readthedocs.io/en/latest/tutorial/custom-strategies.html)
- [pytest Fixtures Documentation](https://docs.pytest.org/en/stable/how-to/fixtures.html)
- [pytest Parametrize Documentation](https://docs.pytest.org/en/stable/how-to/parametrize.html)
- [Advanced pytest Patterns -- Fiddler AI](https://www.fiddler.ai/blog/advanced-pytest-patterns-harnessing-the-power-of-parametrization-and-factory-methods)
- [Dataclasses vs NamedTuple vs TypedDict](https://dev.to/hevalhazalkurt/dataclasses-vs-pydantic-vs-typeddict-vs-namedtuple-in-python-41gg)
