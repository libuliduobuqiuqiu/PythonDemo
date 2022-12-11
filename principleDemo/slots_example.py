# -*- coding: utf-8 -*-

from objprint import op
import time

class Person:
    def __init__(self, name: str):
        self.name = name

class Male(Person):
    def __init__(self, name: str):
        # super(Male, self).__init__(name)
        Person.__init__(self, name)
        self.gender = "Male"

    def get_info(self):
        print(f"{self.name}: {self.gender}")


if __name__ == "__main__":
    male = Male("linshukai")
    print(male)
    op(male)