## The Chain of Responsibility Pattern(责任链模式：创建链式对象用于接收对象)
- 目的：避免请求发送者和接收者耦合
- 本质：职责链上负责处理请求，客户只需要将请求发送到职责链上

```python
# -*- coding: utf-8 -*-


class Event:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Widget:
    def __init__(self, parent=None):
        self.parent = parent

    def handle(self, event):
        method_name = f"handle_{event}"

        if hasattr(self, method_name):
            method = getattr(self, method_name)
            method(event)
        elif self.parent:
            self.parent.handle(event)
        elif hasattr(self, "handle_default"):
            self.handle_default(event)


class MainWindow(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def handle_close(self, event):
        print(f"MainWindow: {event}")

    def handle_default(self, event):
        print(f"MainWindow: Default {event}")


class SendDialog(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def handle_paint(self, event):
        print(f"SendDialog: {event}")


class MsgText(Widget):
    def __init__(self, parent=None):
        super().__init__(parent)

    def handle_down(self, event):
        print(f"MsgText: {event}")


if __name__ == "__main__":
    md = MainWindow()
    sd = SendDialog(md)
    msg = MsgText(sd)

    for e in ("close", "paint", "down"):
        event = Event(e)
        print('\nSending event -{}- to MainWindow'.format(event))
        md.handle(event)
        print('Sending event -{}- to SendDialog'.format(event))
        sd.handle(event)
        print('Sending event -{}- to MsgText'.format(event))
        msg.handle(event)
```

> 备注：
- md，sd，msg对象，通过指定parent确定父级关系，形成一条职责链；
- 当客户发出请求时，当前对象会接收该请求，判断是否能找到对应方法处理，没有则将该请求传递给上级对象处理；

## The Command Pattern（命令模式：用来给应用添加Undo操作）
- 目的：将请求封装成一个对象，从而可以使用不同的请求对客户进行参数化；
- 本质：通过调用者调用执行者执行命令（调用者-》命令-》接收者）

```python
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
```
> 备注：
- 不太懂用法

## The Interpreter Pattern（解释器模式）
- 目的：用于解释特定的上下文。（SQL解析，特定配置文件解析）
- 本质：构建语法树，设置特定的起始符和终止符

> 备注：实际上利用场景比较少

## The Observer Pattern（观察者模式）
- 目的：一个对象状态修改，会自动通知所有依赖它的对象；
- 本质：抽象类中会有个存放观察者的列表；

```python
# -*- coding: utf-8 -*-


class Publisher:
    def __init__(self):
        self.observer_list = []

    def add(self, observer):
        if observer not in self.observer_list:
            self.observer_list.append(observer)
        else:
            print(f"Failed to add {observer}")

    def remove(self, observer):
        try:
            self.observer_list.remove(observer)
        except:
            print(f"Failed to delete {observer}")

    def notify(self):
        [o.notify_by(self) for o in self.observer_list]


class DefaultFormatter(Publisher):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._data = 0

    def __str__(self):
        return f"{type(self).__name__}: {self.name} has {self._data}"

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_value):
        try:
            self._data = new_value
        except Exception as e:
            print(f"Error {e}")
        else:
            self.notify()


class BinaryFormatter:
    def notify_by(self, publisher):
        print(f"{type(self).__name__}: {publisher.name} has now bin data = {bin(publisher.data)}")


class HexFormatter:
    def notify_by(self, publisher):
        print(f"{type(self).__name__}: {publisher.name} has now hex data = {hex(publisher.data)}")


if __name__ == "__main__":
    df = DefaultFormatter("test_formatter")
    bin_ob = BinaryFormatter()
    hex_ob = HexFormatter()
    df.add(bin_ob)
    df.add(hex_ob)
    df.data = 100
```
> 备注：
- DefaultFormatter是默认格式化数据的类，它可以将多个不同格式化数据的对象注册到本身的观察者队列中；
- 当DefaultFormatter设置data值时，会自动通知到观察者队列中的观察者对象；
