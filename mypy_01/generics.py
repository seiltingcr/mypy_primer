from typing import Any, List, Set, Dict, TypedDict, TypeVar, Generic
from typing_extensions import Protocol

# For containers, we need to annotate them with their contained types if it
# can't be inferred. But the builtins (list, set, dict...) don't allow that
# (yet — PEP in progress).
reveal_type([1, 2, 3, 4])  # list[int]

numbers1 = []  # need type annotations!

# These are both fine:
numbers2: List[int] = []
numbers2a = List[int]()

numbers3 = []  # not an error because we can see the type on the next line
numbers3.append(2)
reveal_type(numbers2)  # list[int]
numbers3.append('3')  # incompatible type

numbers_set1 = Set[int]()
numbers_set2 = {1, 2, 3}

some_dict = {'a': 1, 'b': 2}
reveal_type(some_dict)
explicit_dict = Dict[str, int]()

# What we do for a dict that always has certain known keys and value types.
# This is a weak version of TypeScript's interfaces.
class User(TypedDict):
    name: str
    favourite_food: str
    weekly_consumption: float


simon = User(name='Simon', favourite_food='pizza', weekly_consumption=2.3333)
reveal_type(simon['name'])  # str
simon['location']  # that key doesn't exist!


# NamedTuples are great for returning multiple values:
class UserData(NamedTuple):
    name: str
    occupation: str


def get_user_data() -> UserData:
    return UserData('Simon', 'typist')


# They work just like a tuple:
user_data = get_user_data()
name, _ = user_data
occupation = user_data[1]
# But they also support dotted-name access:
reveal_type(user_data.occupation)  # str


# Defining generic functions

# Remember add? It could work for more types than just float, but who wants to
# define endless overloads?

# Defining a generic type:
T = TypeVar('T', str, int, float)


def add(a: T, b: T) -> T:
    return a + b


reveal_type(add(2, 3))  # int
reveal_type(add(2, 3.0))  # float
reveal_type(add('howdy', 'doody'))  # str
reveal_type(add('hello', 2))  # no can do!
