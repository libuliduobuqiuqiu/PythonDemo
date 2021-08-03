# -*- coding: utf-8 -*-
# 外观模式

from abc import ABCMeta, abstractmethod
from enum import Enum

State = Enum("State", "new running sleeping restart zombie")


class Server(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    def __str__(self):
        return self.name

    @abstractmethod
    def boot(self):
        pass

    @abstractmethod
    def kill(self):
        pass


class FileServer(Server):
    def __init__(self):
        self.name = "FileServer"
        self.state = State.new

    def boot(self):
        print(f"booting the {self}")
        self.state = State.running

    def kill(self, restart=True):
        print(f"killing {self}")
        self.state = State.restart if restart else State.zombie

    def create_file(self, user, name, permission):
        print(f"trying to create {name} for user {user} with permission {permission}")


class ProcessServer(Server):
    def __init__(self):
        self.name = "ProcessServer"
        self.state = State.new

    def boot(self):
        print(f"booting the {self}")

    def kill(self, restart=True):
        self.state = State.restart if restart else State.zombie
        print(f"killing {self}:{self.state}")

    def create_process(self, user, name):
        print(f"trying create process {name} for user {user}")


class OperationSystem:
    def __init__(self):
        self.fs = FileServer()
        self.ps = ProcessServer()

    def start(self):
        [i.boot() for i in (self.fs, self.ps)]

    def create_file(self, user, name, permission):
        self.fs.create_file(user, name, permission)

    def create_process(self, user, name):
        self.ps.create_process(user, name)

    def restart(self):
        [i.kill() for i in (self.fs, self.ps)]

    def stop(self):
        [i.kill(False) for i in (self.fs, self.ps)]


if __name__ == "__main__":
    op_system = OperationSystem()
    op_system.start()
    op_system.create_file("root", "pythonic.txt", "-rwx-r-r")
    op_system.create_process("root", "httpd")
    op_system.restart()
    op_system.stop()
