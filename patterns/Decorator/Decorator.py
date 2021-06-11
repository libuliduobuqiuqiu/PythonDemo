# -*- coding: utf-8 -*-
# 装饰器模式

def memorize(func):
    known = {}

    def memorizer(*args):
        if args not in known:
            known[args] = func(*args)
        return known[args]
    return memorizer


@memorize
def fib(n):
    if n < 0:
        raise ValueError("不能小于0")
    return n if n in (0, 1) else fib(n-1) + fib(n-2)


if __name__ == "__main__":
    result = fib(100)
    print(result)
