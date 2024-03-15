# coding: utf-8
import sys
from collections import OrderedDict, Counter


def handle_interview_case():
    tmp_dict1 = OrderedDict()
    tmp_dict2 = {}
    print(sys.getsizeof(tmp_dict1), sys.getsizeof(tmp_dict2))


def handel_dict_case():
    # 获取字典中最大的value已经对应的key
    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    print(max(zip(prices.values(), prices.keys())))
    print(min(zip(prices.values(), prices.keys())))

    # 查找两个字典的相同点

    a = {
        'x': 1,
        'y': 2,
        'z': 3
    }

    b = {
        'w': 10,
        'x': 11,
        'y': 2
    }

    print(a.keys() & b.keys())
    print(a.keys() - b.keys()) # 相差
    print(a.items() & b.items())


def dedupe(items):
    seen = set()

    for i in items:
        if i not in seen:
            yield i
            seen.add(i)


def count_words(words: list):
    result = Counter(words)

    print(result.most_common(3))


if __name__ == "__main__":
    w = [
        'look', 'into', 'my', 'eyes', 'look', 'into', 'my', 'eyes',
        'the', 'eyes', 'the', 'eyes', 'the', 'eyes', 'not', 'around', 'the',
        'eyes', "don't", 'look', 'around', 'the', 'eyes', 'look', 'into',
        'my', 'eyes', "you're", 'under'
    ]
    count_words(w)

    a = {"name": "zhangsan"}
    print(a.get("age", 22))

    from operator import itemgetter
    print(itemgetter("name")(a))

    tmp = [1,2,3,4,5,6,7,8]
    print(sum(x * x for x in tmp))
    print(sum([x * x for x in tmp]))

    a = {'x': 1, 'z': 3}
    b = {'y': 2, 'z': 4}
    print(dict(Counter(a) + Counter(b)))

    from collections import ChainMap
    c = ChainMap(a, b)
    print(c['x'], c['z'])

    tmp1 = "https://www.baidu.com"
    tmp2 = "http://www.qq.com"
    tmp3 = "ftps://10.21.12.1"

    choices = ["http:", "https:", "ftp:"]
    for i in [tmp1, tmp2, tmp3]:
        if i.startswith(tuple(choices)):
            print("success: ", i)