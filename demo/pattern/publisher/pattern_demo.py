# coding: utf-8
"""
    :date: 2023-11-20
    :author: linshukai
    :description: About Pattern Demo
"""


class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I'm {self.name}"

    def execute(self):
        return "I'm executing program."


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I'm {self.name}"

    def speak(self):
        return "I'm speaking."


class Animal:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I'm {self.name}"

    def eat(self):
        return "I'm eating other animals."


class Adapter:
    def __init__(self, obj, update_func):
        self.obj = obj
        self.__dict__.update(update_func)

    def __str__(self):
        return str(self.obj)


class Publisher:
    def __init__(self):
        self.observer_list = []

    def add(self, observer):
        if observer not in self.observer_list:
            self.observer_list.append(observer)
        else:
            print(f"Failed to add {observer}")

    def remove(self, observer):
        if observer in self.observer_list:
            self.observer_list.remove(observer)
        else:
            print(f"Failed to remove {observer}")

    def notify(self):
        _ = [o.notify_by(self) for o in self.observer_list]


class DefaultFormatter(Publisher):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._data = 0

    def __str__(self):
        return f"{type(self).__name__}： {self.name} has {self._data}"

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        try:
            self._data = new_data
        except Exception as e:
            print(f"Error {e}")
        finally:
            self.notify()


class BinaryFormatter:
    def notify_by(self, publisher):
        print(f"{type(self).__name__}: {publisher.name} has now bin data = {bin(publisher.data)}")


class HexFormatter:
    def notify_by(self, publisher):
        print(f"{type(self).__name__}: {publisher.name} has now hex data = {hex(publisher.data)}")


class Exchange:
    def __init__(self):
        self._subscribers = set()

    def add(self, subscriber):
        self._subscribers.add(subscriber)

    def remove(self, subscriber):
        if subscriber in self._subscribers:
            self._subscribers.remove(subscriber)
        else:
            print(f"Failed remove: {subscriber}")

    def send(self, msg):
        _ = [subscriber.send(msg) for subscriber in self._subscribers]


class Task:
    def __init__(self, name):
        self.name = name

    def send(self, msg):
        print(f"{self.name}: Got {msg}")


if __name__ == "__main__":
    e = Exchange()
    t1 = Task("linshukai")
    t2 = Task("zhangsan")
    e.add(t1)
    e.add(t2)
    e.send("Hello, World")
