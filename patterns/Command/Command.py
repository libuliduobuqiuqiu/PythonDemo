# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod


class Order(ABC):

    @abstractmethod
    def execute(self):
        pass

# 请求类
class Stock:
    _name = "ABC"
    _prices = 1000

    def buy(self):
        print(f"Buy {self._name} Stock: values {self._prices}")

    def sell(self):
        print(f"Sell {self._name} Stock: values {self._prices}")


# Order接口实体类
class BuyStock(Order):
    in_stock = None

    def __init__(self, in_stock):
        self.in_stock = in_stock

    def execute(self):
        if self.in_stock:
            self.in_stock.buy()


class SellStock(Order):
    in_stock = None

    def __init__(self, in_stock):
        self.in_stock = in_stock

    def execute(self):
        if self.in_stock:
            self.in_stock.sell()

# 命令调用类
class Broker:
    order_list = []

    def take_order(self, in_order):
        self.order_list.append(in_order)

    def place_order(self):
        for order_item in self.order_list:
            order_item.execute()
        self.order_list.clear()


if __name__ == "__main__":
    stock = Stock()
    buy_stock = BuyStock(stock)
    sell_stock = SellStock(stock)

    broker = Broker()
    broker.take_order(buy_stock)
    broker.take_order(sell_stock)
    broker.place_order()