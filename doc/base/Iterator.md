可迭代对象（iterable)
- for loop in 后面必须是iterable，即在迭代过程中先会通过__iter__方法获取到iterator，然后执行__next__获取数据流的项

迭代器（iterator)
- 用来表示一连串数据流的对象，能够重复调用__next__()方法(或者将其传给next()函数)将逐个返回流中的项（当没有时将会出发StopIterException)
- 在Python设计中，iterator本身也应该是个iterable，即实现__iter__方法
- 在实现iterator时，必须结束时抛出StopIteration异常，否则无法正常使用；

迭代器（iterator)和可迭代对象（iterable)之间的区别：
- 可以将iterable理解为一个无状态的container，用于产生返回iterator。而iterator一定是有状态，它代表了iterable里面的数据，但是不需要通过其他方法去修改iterable里面数据，即用next方法返回容器里面的数据；
- 从实现上看，iterable需要实现__iter__方法或者序列语义上的__getitem__方法，iterator必须要有__next__方法（__iter__方法官方也是要求需要实现）

备注：
> 在使用可迭代对象时，你通常不需要调用 iter() 或者自己处理迭代器对象。for 语句会为你自动处理那些操作，创建一个临时的未命名变量用来在循环期间保存迭代器。  
> 容器对象（例如 list）在你每次向其传入 iter() 函数或是在 for 循环中使用它时都会产生一个新的迭代器。如果在此情况下你尝试用迭代器则会返回在之前迭代过程中被耗尽的同一迭代器对象，使其看起来就像是一个空容器。

示例代码：
```python
class NodeIter:
    def __init__(self, node):
        self.current_node = node

    def __next__(self):
        if not self.current_node:
            raise StopIteration

        node, self.current_node = self.current_node, self.current_node.next
        return node

    def __iter__(self):
        return self


class Node:
    def __init__(self, name):
        self.name = name
        self.next = None

    def __iter__(self):
        return NodeIter(self)


node1 = Node("node1")
node2 = Node("node2")
node3 = Node("node3")

node1.next = node2
node2.next = node3

node = iter(node1)

for item in node:
    print(item.name)
```

参考文档链接：
> https://docs.python.org/zh-cn/3/glossary.html
> https://docs.python.org/zh-cn/3/library/stdtypes.html#typeiter


生成器函数
返回一个generator iterator的函数
在编译过程中，python发现带有yield关键字，则自动将该函数识别为生成器函数

生成器对象（生成器迭代器）
- generator函数创建的对象，只有当对这个生成器对象使用next()函数时，才会运行生成器函数本体。
- 当使用next函数运行生成函数时，到达yield关键字的时候，就会将yield右边的值返回回去，但是不会结束该函数，可以理解暂停
该函数运行，等待下一次next函数执行该生成器，会继续运行yield关键字后面的代码；
- 生成器函数中的return相当于迭代器的raise StopIterException，无论return任意值，都不会在next的时候返回回去；
- 可以通过send()函数和生成器函数进行交互，当使用send函数时，将值赋给yield关键字的左边变量


```python
class Node2:
    def __init__(self, name):
        self.name = name
        self.next = None

    def __iter__(self):
        node = self
        while node is not None:
            yield node.name
            node = node.next


node1 = Node2("node1")
node2 = Node2("node2")
node3 = Node2("node3")

node1.next = node2
node2.next = node3

for i in node1:
    print(i)
```

send的高级用法
```python
def gen(num):
    while num > 0:
        temp = yield num

        if temp:
            num = temp
        num -= 1

g = gen(10)
print("first:", next(g))
print("send:", g.send(10))
for i in g:
    print(i)
```
备注：
- 当send(10)时，会将10赋值给temp变量，然后继续运行函数，下一个yield num返回num
- 当yield num 左边没有赋值给任何变量时，next(g) = g.send(10)，10会将抛弃，返回yield num的值
