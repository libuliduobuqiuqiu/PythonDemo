# -*- coding: utf-8 -*-

from random import randint


def default(nums: list):
    num = randint(1, 1000)
    nums.append(num)
    print(nums)
    return nums


def print_text():
    with open("D:\\test.txt", "r", encoding='utf-8') as f:
        text = f.read()
        print(f.tell())

    r_text = "".join(text.split())
    print(len(r_text))


class A:
    def say(self):
        print("A")


class B2:
    pass

class B(A):
    def say(self):
        print("B")


class C(A):
    pass


class M(C, B):
    pass


if __name__ == "__main__":
    print(M.mro())
    M().say()