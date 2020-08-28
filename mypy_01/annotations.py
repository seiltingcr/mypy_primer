#!/usr/bin/env python

# To the compiler, annotations don't have to be types. They just have to be
# valid expressions. They get executed at definition time, i.e. generally
# during import. After that, the interpreter stores their values in
# __annotations__ and doesn't care about them any more.

#
# This example prints 'hello', but it won't pass any type checks.

def foo(a: 'is a parameter', b: 2 + 3) -> lambda: print('hello'):
    pass


foo.__annotations__['return']()  # prints 'hello'


#
# Class annotations are accessible at `cls.__annotations__`, and global ones
# are in `__annotations__`. (I haven't yet found where it stores the local
# ones.)


variable: "Ceci n'est pas une variable"  # It's not defined...
print(__annotations__['variable'])       # But its annotation is!
