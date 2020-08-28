import datetime
from typing import cast, Any, Callable, Optional, Union, overload  # noqa: F401

# Mypy will infer the type of constant expressions without further help:
INT_EXPR = 5  # int

# use the special expression `reveal_type(e)` to show the type of `e`:
reveal_type(INT_EXPR)  # int
reveal_type(5)  # Literal[5]
reveal_type(5 + 5)  # int
reveal_type('5' * 5)  # str

# Things that would be type errors at runtime are detected while you're writing them:
5 + 'hello'  # unsupported operand types for +

# Also, mypy won't allow reassignment with a different type:
INT_EXPR = '5'  # incompatible types in assignment

# Simple type annotations are pretty straightforward:
example_var: int  # int
# example_var is undefined, but its type is known:
reveal_type(example_var)
# example_var = 5.5  # incompatible types, int/float
example_var = 5  # this is fine

# Variables can be assigned in the same step as their type is declared.
# This is usually only necessary if the RHS expression's type is unknown...
example_var2: str = 'howdy'

# None is its own type and not compatible with anything... but in some simple cases is the
# only exception to the no-reassignment rule:
example_var3 = None
reveal_type(example_var3)  # None
example_var3 = 'has a value now'  # str
reveal_type(example_var3)  # str
example_var3 = None
reveal_type(example_var3)  # None

example_var4: str = None  # incompatible types in assignment

# Optional is a special case of Union: Union[T, None]
example_var5: Union[str, int] = 'hello'
example_var5 + ', world'  # oops, this doesn't work with int
if isinstance(example_var5, str):  # but if we use assert of if isinstance, it's fine:
    example_var5 + ', world'
else:
    example_var5 + 5


# Functions are easy:
def add(a: float, b: float) -> float:
    pass
    # a + 'hello'  # unsupported operand types
    # return a + b


reveal_type(add)
reveal_type(add(2, 3))  # float
add(2, 'hello')  # argument 2 has incompatible type


# Functions as arguments can be not-so-easy, but for simple cases work well:
def operate(operator: Callable[[float, float], float], a: float, b: float) -> float:
    return operator(a, b)


# Types can be aliased to be easier to read and use:
FloatOperator = Callable[[float, float], float]  # TS: type FloatOperator = (a: number, b: number): number


def operate_alt(operator: FloatOperator, a: float, b: float) -> float:
    return operator(a, b)


# Type aliases are not distinct types:
Name = str
Place = str
who: Name = 'Simon'
where: Place = 'Edinburgh'
who = where  # Not an error, though it looks like it should be! Because...
reveal_type(where)  # str, not Place


# Classes
class WithInitAnnotations:
    _how_many: float

    # The type of self and cls is implicit.
    # The return type of __init__ is always None.
    def __init__(self, where: str, how_many: int) -> None:
        self.where = where
        self._how_many = how_many

    @property
    def how_many(self) -> float:
        return self._how_many

    def now(self) -> datetime.datetime:
        return datetime.datetime.now()


with_init_annotations = WithInitAnnotations('nowhere', 23)
reveal_type(with_init_annotations.where)  # str
reveal_type(with_init_annotations.how_many)  # int
reveal_type(with_init_annotations.now())  # datetime


class WithClassLevelAnnotations:
    # This is useful when there is no __init__()
    # But there is no guarantee that this will be set at runtime!
    whence: str

    # Type annotations are evaluated by the compiler, so you can't use
    # things that don't yet exist, like the name of the class being defined.
    # In such cases, we use a str with the name of the type:
    @classmethod
    def make(cls, whence: str) -> 'WithClassLevelAnnotations':
        instance = cls()
        instance.whence = whence
        return instance


with_class_level_annotations = WithClassLevelAnnotations.make('to the batmobile')
reveal_type(with_class_level_annotations.whence)  # str


from dataclasses import dataclass


@dataclass
class DataClassExample:
    a: int


dce = DataClassExample(3)


# Overloading

# Wouldn't it be nice if add supported more types than just float?

@overload
def add2(a: int, b: int) -> int: ...  # noqa: E704

@overload  # noqa: E302
def add2(a: float, b: float) -> float: ...  # noqa: E704

@overload  # noqa: E302
def add2(a: str, b: str) -> str:
    ...

def add2(a: Any, b: Any) -> Any:  # noqa: E302
    return a + b


reveal_type(add2(1, 2))  # int
reveal_type(add2(1, 2.0))  # float
reveal_type(add2('howdy', 'doody'))  # str
reveal_type(add2(datetime.datetime.now(), None))  # no overload


# Casts
# Given some data that we know have a certain type but the type checker doesn't:
def returns_any() -> Any:
    return 3


reveal_type(returns_any())  # hmm, but I *know* it always returns an int
reveal_type(cast(int, returns_any()))  # int!

# Cast() is to be avoided, because it does not actually check if the types are compatible.
# It is a no-op at runtime:
reveal_type(cast(int, None))  # now I'm clearly lying to the type checker, and to myself
