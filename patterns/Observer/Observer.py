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