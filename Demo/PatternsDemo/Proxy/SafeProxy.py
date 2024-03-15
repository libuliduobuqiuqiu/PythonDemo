# -*- coding: utf-8 -*-
# 代理模式

from abc import ABC, abstractmethod


class SensitiveInfo(ABC):
    def __init__(self):
        self.users = ["tom", "nike", "admin", "root"]

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def add(self, user):
        pass


class Info(SensitiveInfo):
    def __init__(self):
        super().__init__()
        self.secret = "abc"

    def read(self):
        print(f"User: {','.join(self.users)}")

    def add(self, user):
        key = input("Input the Secret:")
        self.users.append(user) if key == self.secret else print("No authentication")


if __name__ == "__main__":
    info = Info()
    info.read()
    info.add("zhangsan")
    info.read()
