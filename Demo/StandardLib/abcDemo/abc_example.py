#  coding: utf-8

from abc import ABCMeta, abstractmethod


class IStream(metaclass=ABCMeta):

    @abstractmethod
    def read(self, max_types=1):
        pass

    @abstractmethod
    def write(self, data):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, name):
        pass

    @staticmethod
    @abstractmethod
    def method1():
        pass

    @classmethod
    def method2(cls):
        pass


class SocketStream(IStream):
    def __init__(self, name, address):
        self.address = address
        self.data = None
        self.name = name

    def read(self, max_types=2):
        print(self.address)

    def write(self, data):
        self.data = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @staticmethod
    def method1():
        print("method1.....")

    @classmethod
    def method2(cls):
        print("method2......")


if __name__ == "__main__":
    s = SocketStream("zhangsan", "localhost")
    s.read()
    print(s.name)

    SocketStream.method1()
    s.method2()
