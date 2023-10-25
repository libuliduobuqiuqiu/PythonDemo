# coding: utf-8

"""
    :author: linshukai
    :description: about metaclass Demo
"""

from functools import partial


def typed_property(name, expected_type):
    storage_name = "_" + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be {expected_type}")
        setattr(self, storage_name, value)

    return prop


class Person:
    str_property = partial(typed_property, expected_type=str)
    int_property = partial(typed_property, expected_type=int)
    name = str_property("name")
    age = int_property("age")

    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == "__main__":
    p = Person("zhangsan", 22)
    p.name = "zhangsdna"
    p.age = 100
    print(p.name, p.age)
