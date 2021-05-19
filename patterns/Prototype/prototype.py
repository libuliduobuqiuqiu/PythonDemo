# -*- coding: utf-8 -*-

from collections import OrderedDict


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


