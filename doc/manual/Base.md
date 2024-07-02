## 数据结构和算法

实现一个优先级队列
```python
# coding: utf-8

import heapq


class PriorityQueue:
    def __init__(self):
        self.queue = []
        self._index = 0

    def push(self, item, priority):
        heapq.heappush(self.queue, (-priority, self._index, item))
        self._index += 1

    def pop(self):
        return heapq.heappop(self.queue)[-1]


if __name__ == "__main__":
    p = PriorityQueue()
    p.push(100, 1)
    p.push(200, 1)
    p.push(300,1)

    print(p.pop())
    print(p.queue)
```

在一个序列上保持元素顺序相同的同时去除重复元素：
```python
def dedupe(items):
    seen = set()

    for i in items:
        if i not in seen:
            yield i
            seen.add(i)

if __name__ == "__main__":
    a = [1,2,3,43,1,2,3,1,23,4,6,2]
    print(list(dedupe(a)))
```

## 字符串和文本

字符串替换：
```python
def search_text():
    text = 'Today is 11/27/2012. PyCon starts 3/13/2013.'

    # 替换字符串
    tmp_text = re.sub(r"(\d+)/(\d+)/(\d+)", r"\3-\2-\1", text)
    print(tmp_text)

    # 搜索字符串所有符合要求
    text_list = re.findall(r"(\d+)/(\d+)/(\d+)", text)
    print(text_list)
```


## 数字日期和时间

随机选择：
```python
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
```

计算上一个周五的日期
```python
# 计算上个星期几是多少号
def datetime_handle(spec: str):
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday',
                'Friday', 'Saturday', 'Sunday']

    if spec not in weekdays:
        print("无效的星期，仅支持：", weekdays)

    start_date = datetime.today()
    week_day = start_date.weekday()
    day_target = weekdays.index(spec)
    days_ago = (7 + week_day - day_target) % 7
    if days_ago == 0:
        days_ago = 7

    target_date = start_date - timedelta(days=days_ago)
    print(target_date)
```


## 迭代器和生成器

> Python的迭代器协议是需要__iter__()方法返回一个实现了__next__()方法的迭代器对象；

实现迭代器协议：
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []

    def __repr__(self):
        return f"Node({self.value})"

    def __iter__(self):
        return iter(self.children)

    def add_children(self, node):
        self.children.append(node)

    def depth_first(self):
        yield self

        for c in self:
            yield from c.depth_first()


if __name__ == "__main__":
    n1 = Node(1)
    n2 = Node(2)
    n3 = Node(3)
    n1.add_children(n2)
    n1.add_children(n3)

    n4 = Node(4)
    n5 = Node(5)
    n2.add_children(n4)
    n3.add_children(n5)

    for n in n1.depth_first():
        print(n)
```

不同集合上元素的迭代：
```python
if __name__ == "__main__":
    from itertools import chain
    a = [1,2,3,4,5,1,2,3]
    b = [3,4,1,5,1,2,3,1000]

    for i in chain(a, b):
        print(i)
```
备注： itertools.chain()可接受一个或者多个迭代器作为传入参数，创建一个迭代器，依次连续返回每个可迭代对象的元素


## 文件与IO

固定大小记录的文件迭代

```python
def open_partial_file(file_name: str, record_size: int):
    with open(file_name, "rb") as f:

        records = iter(partial(f.read, record_size), b"")

        for r in records:
            print(r)
```

备注：
- 如果传递给iter()函数一个可调用对象和标记值，iter函数会返回一个迭代器，迭代器对象会一直迭代直到返回标记值位置，这时候迭代终止；
- partial创建一个每一次调用时，从文件对象返回固定数目字节的可调用对象，标记值b''就是到达文件末尾；
·

文件路径、大小、类型、详细信息可以通过os.path工具获取

快速打印所有目录下所有文件和所有目录，并且递归打印目录下的所有文件
```python
def search_all_files(dir_name: str):
    files = [name for name in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, name))]
    if len(files) != 0:
        print(dir_name, ":", files)

    dirs = [name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, name))]
    for tmp_dir in dirs:
        search_all_files(os.path.join(dir_name, tmp_dir))


if __name__ == "__main__":
    # open_partial_file("D:\\Backup\\test.txt", 12)

    search_all_files("D:\\Download")
```


内存映射一个二进制文件到可变字节数组中，目的是随机访问他的内容或者原地做些修改
```python
import os
import mmap

def memory_map(filename, access=mmap.ACCESS_WRITE):
    size = os.path.getsize(filename)
    fd = os.open(filename, os.O_RDWR)
    return mmap.mmap(fd, size, access=access)

m = memory_map('D:\\Backup\\test.txt')
m[0:11] = b"Hello,world"
m.close()

```
