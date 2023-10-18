import abc
from abc import ABCMeta, abstractmethod


class BMW:
    def __repr__(self):
        return "I'm BMW"


class BYD:
    def __repr__(self):
        return "I'm BYD"


class SimpleFactory:

    @staticmethod
    def create_car(name: str):

        if name == "bmw":
            return BMW()
        elif name == "byd":
            return BYD()
        else:
            return "No more car"


class CarFactory(metaclass=abc.ABCMeta):

    @abstractmethod
    def product_car(self):
        pass


class BmwFactory(CarFactory):

    def product_car(self):
        return BMW()


class BydFactory(CarFactory):
    def product_car(self):
        return BYD()


if __name__ == "__main__":
    bmw_factory = BmwFactory()
    print(bmw_factory.product_car())

    byd_factory = BydFactory()
    print(byd_factory.product_car())
