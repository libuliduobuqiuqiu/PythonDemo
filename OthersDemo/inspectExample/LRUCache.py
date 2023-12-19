# -*- coding: utf-8 -*-

from collections import OrderedDict


class LRUCache:
    def __init__(self, length: int):
        self.od = OrderedDict()
        self.length = length

    def get(self, key):
        value = self.od.get(key)

        if value:
            self.od.move_to_end(key)
            return value
        else:
            return -1

    def put(self, key, value):
        if self.od.get(key):
            self.od[key] = value
            self.od.move_to_end(key)
        else:
            if len(self.od) < self.length:
                self.od[key] = value
            else:
                self.od.popitem(last=False)
                self.od[key] = value


if __name__ == "__main__":
    a = LRUCache(3)
    a.put("name", "zhangsan")
    a.put("age", 12)
    a.put("sex", "man")

    print(a.get("name"))
    a.put("age", 15)
    a.put("address", "beijing")
    print(a.get("sex"), a.od)
