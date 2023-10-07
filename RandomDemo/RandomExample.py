# coding: utf-8

import random


def random_text():
    values = [1, 1, 2, 2, 3, 3, 4, 4,  5, 6, 6]

    # 随机选择列表中的一个元素
    print(random.choices(values))

    # 提取N个不同元素进行操作
    print(random.sample(values, 5))

    # 打乱列表中的顺序
    random.shuffle(values)
    print(values)

    #  生成随机整数
    num = random.randint(0, 10000)
    print(num)


if __name__ == "__main__":
    random_text()