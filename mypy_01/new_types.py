from typing import NewType


# NewTypes can be used as a safer alternative to type aliases. They are,
# unfortunately, a bit cumbersome to use.
Name = NewType('Name', str)
Colour = NewType('Colour', str)
# Name and Colour are treated as if they were subtypes of str.


def foo(name: Name, favourite_colour: Colour) -> None:
    name = favourite_colour  # incompatible types
    reveal_type(name + favourite_colour)  # becomes str


foo('Pinky', 'pink')  # incompatible type
name = Name('Pinky')
colour = Colour('pink')
foo(name, colour)  # fine

# Now if we mix up the args, we get an error:
foo(colour, name)  # isn't that neat?


# 2 big downsides:
# 1. NewType returns a function (not a type), so isinstance doesn't work with its instances
isinstance(colour, Colour)  # Cannot use isinstance, Colour is really a function :(
# 2. Interfacing with external code that doesn't know about the NewTypes
# requires constant casts.


# Often, named arguments are easier to use and almost as safe.
# Here is an alternative to foo where accidentally swapping arguments requires
# real effort:
def safe_foo(*, name: str, colour: str) -> None:
    ...

safe_foo(colour, name)  # TypeError
safe_foo(colour=name, name=colour)  # brain error
