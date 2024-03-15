# coding: utf-8

from socket import AF_INET, SOCK_STREAM, socket
from functools import partial


class LazyConnection:
    def __init__(self, address, family=AF_INET, sock_type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.sock_type = sock_type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError("Already Exist Connection.")

        self.sock = socket(self.family, self.sock_type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None


class SrcClass:
    def __inti__(self, name):
        self.name = name

    def __hello(self):
        print(f"hello,world, {self.name}")

    def _speak(self):
        print(f"I speak loudly: {self.name}")

    def info(self):
        print(self.name)


class DstClass(SrcClass):
    def __init__(self, name):
        self.name = name

    def __hello(self):
        print("hello, world")

    def _speak(self):
        print("I speak loudly")


class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if not isinstance(first_name, str):
            raise TypeError("Expected a string")
        self._first_name = first_name

    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


class SubPerson(Person):
    def __init__(self, first_name):
        super().__init__(first_name)

    @Person.first_name.getter
    def first_name(self):
        print("Getting Name")
        return super().first_name


if __name__ == "__main__":
    a = SubPerson("linshukai")
    print(a.first_name)
    a.first_name = 11
    print(a.first_name)
    del a.first_name
