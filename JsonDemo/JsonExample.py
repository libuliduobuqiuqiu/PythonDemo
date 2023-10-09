# coding: utf-8

import json


class JsonObject:
    def __init__(self, d):
        self.__dict__ = d


if __name__ == "__main__":
    a = '{"name": "linshukai", "age":22}'
    b = json.loads(a, object_hook=JsonObject)

    print(b.name, b.age)