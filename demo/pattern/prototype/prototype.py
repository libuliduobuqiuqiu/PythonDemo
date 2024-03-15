# -*- coding: utf-8 -*-
# 原型模式
from collections import OrderedDict
import copy


class Book:
    def __init__(self, name, authors, price, **rest):
        self.name = name
        self.authors = authors
        self.price = price
        self.__dict__.update(**rest)

    def __str__(self):
        my_list = []
        ordered_list = OrderedDict(sorted(self.__dict__.items()))
        for ordered in ordered_list:
            ord_str = f"{ordered}:{self.__dict__[ordered]}"
            my_list.append(ord_str)
        my_str = " \n".join(my_list)
        return my_str


class Prototype:
    def __init__(self):
        self.objects = {}

    def register(self, identifier, obj):
        self.objects[identifier] = obj

    def unregister(self, identifier):
        del self.objects[identifier]

    def clone(self, identifier, **attr):
        found = self.objects.get(identifier)

        if not found:
            raise ValueError(f"找不到对应{identifier}对象")
        obj = copy.deepcopy(found)
        obj.__dict__.update(**attr)     # 自定义更新属性
        return obj


if __name__ == "__main__":
    b = Book('The C Programming Language', ('Brian W. Kernighan', 'Dennis M.Ritchie'),
             price=118, publisher='Prentice Hall', length=228, publication_date='1978-02-22',
             tags=('C', 'programming', 'algorithms', 'data structures'))
    print(b)
    p = Prototype()
    p.register("b1", b)
    b2 = p.clone("b1", name='The C Programming Language (ANSI)', price=48.99, length=274,
                 publication_date='1988-04-01', edition=2)
    print(b2)
