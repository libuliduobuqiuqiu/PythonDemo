# -*- coding: utf-8 -*-
# 简单工厂


class BMW:
    def __repr__(self):
        return "I am a bmw car."


class BYD:
    def __repr__(self):
        return "I am a byd car."


class SimpleFactory:
    @staticmethod
    def factory_car(car_name):
        if car_name == "bmw":
            return BMW()
        elif car_name == "byd":
            return BYD()
        else:
            return "No more car."


if __name__ == "__main__":
    print(SimpleFactory.factory_car("bmw"))
