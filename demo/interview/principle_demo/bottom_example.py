# -*- coding: utf-8 -*-
import random

class M(type):
    def __new__(cls, name, bases, dict):
        print(name, bases, dict)

        for key in dict.keys():
            if key.startswith("test_"):
                raise ValueError()
        
        return type.__new__(cls, name, bases, dict)

    def __init__(self, name, base, dict):
        self.random_id = random.randint(1, 100000)
        return type.__init__(self, name, base, dict)

    def __call__(cls, *args, **kwargs):
        print("call: ", args)
        return type.__call__(cls, *args, **kwargs)

class A(metaclass=M):
    def __init__(self, name):
        self.name = name
        print(name)
        print(self.random_id)


class SingletonMetaclass(type):
    def __call__(cls,*args, **kwargs):
        if hasattr(cls, "_instance"):
            return cls._instance
        
        cls._instance = type.__call__(cls, *args, **kwargs)
        return cls._instance

class Singleton(metaclass=SingletonMetaclass):
    pass

t1 = Singleton()
t2 = Singleton()
print(id(t1), id(t2))
print(t1 == t2)