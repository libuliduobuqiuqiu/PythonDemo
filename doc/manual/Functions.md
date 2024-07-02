## Functions

Python函数中最核心的就是闭包概念：
- 函数可以内部定义另一个函数，并且内部函数能够访问外部函数内的变量


### 定义有默认参数的函数

默认参数的值在函数定义的时候就已经确定了，所以如果是可变对象，列表、字典这些，
会出现每次调用函数的时候都出现，默认参数不一致的情况；

### 匿名函数捕获变量值

```python
x = 100
a = lambda y: x+y
x = 200
b = lambda y: x+y
a(10)
b(10)
```
x是一个自由变量，是在函数内部，函数运行时绑定值的，所有运行结果都是210


### 减少可调用对象的参数个数

```python
def spam(a, b, c, d):
    print(a,b,c,d)


if __name__ == "__main__":
    s1 = partial(spam, b=2, c=3, d=4)
    s1(1)
```



## Class And Object

### 自定义字符串的格式化

通过format()函数和字符串方法使得一个对象支持自定义的格式化

```python
_formats = {
    'ymd': '{d.year}-{d.month}-{d.day}',
    'mdy': '{d.month}/{d.day}/{d.year}',
    'dmy': '{d.day}/{d.month}/{d.year}'
}


class MyDate:
    def __init__(self, year, month, day):
        self.year = year
        self.month = month
        self.day = day

    def __format__(self, code):
        if code == "":
            code = "ymd"

        fmt = _formats[code]
        return fmt.format(d=self)


if __name__ == "__main__":
    a = MyDate(year=2023, month=9, day=23)
    print(format(a, "mdy"))
```


### 让对象支持上下文管理器协议(with 语句)


```python
from socket import AF_INET, SOCK_STREAM, socket
from functools import partial


class LazyConnection:
    def __init__(self, address, family=AF_INET, sock_type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.sock_type = sock_type
        self.sock = None

    def __enter__(self):
        if self.sock is not None:
            raise RuntimeError("Already Exist Connection.")

        self.sock = socket(self.family, self.sock_type)
        self.sock.connect(self.address)
        return self.sock

    def __exit__(self, exc_ty, exc_val, tb):
        self.sock.close()
        self.sock = None


if __name__ == "__main__":
    conn = LazyConnection(("www.python.org", 80))

    with conn as s:
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host: www.python.org\r\n')
        s.send(b'\r\n')
        content = b''.join(iter(partial(s.recv, 8192), b''))
        print(content.decode("utf-8"))

```

通过with语句可以自动帮我们创建一个网络连接，然后在执行完with语句中的流程之后，会自动关闭网络连接；


### 在类中封装属性名

Python中无法强制限制访问内部名称，但约定俗成会在名称前面加上单划线和双划线：
- 单划线前缀表示不应该在类的外部访问使用，应该在类的内部访问使用；（但是不会强制限制使用）
- 双划线前缀同样表示应该只能在类的内部使用，并且Python还将名称进行重写，防止意外的访问，所以这种属性无法通过类的继承被覆盖（可以通过名称修饰来访问）

### MRO搜索的三条原则

> 子类会先于父类被检查
> 多个父类会根据它们在列表中的顺序被检查
> 如果对下一个类存在两个合法的选择，选择第一个父类

### 创建可管理的属性

给实例的属性增加出修改访问之外的处理逻辑，类型检查和合法性验证

```python
class Person:
    def __init__(self, first_name):
        self.first_name = first_name

    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, first_name):
        if not isinstance(first_name, str):
            raise TypeError("Expected a string")
        self._first_name = first_name

    @first_name.deleter
    def first_name(self):
        raise AttributeError("Can't delete attribute")


if __name__ == "__main__":
    a = Person("linshukai")
    print(a.first_name)
    a.first_name = "zhangsan"
    print(a.first_name)

    del a.first_name
```

备注：
- 不要写没有任何操作的property，这会让python代码变得十分臃肿，并且影响程序运行速度。


### 子类中扩展property


在子类中，扩展定义在父类的property

```python
class SubPerson(Person):
    def __init__(self, first_name):
        super().__init__(first_name)

    @Person.first_name.getter
    def first_name(self):
        print("Getting Name")
        return super().first_name


if __name__ == "__main__":
    a = SubPerson("linshukai")
    print(a.first_name)
    a.first_name = 11
    print(a.first_name)
    del a.first_name
```


### 定义接口或者抽象基类

```python
#  coding: utf-8

from abc import ABCMeta, abstractmethod


class IStream(metaclass=ABCMeta):

    @abstractmethod
    def read(self, max_types=1):
        pass

    @abstractmethod
    def write(self, data):
        pass

    @property
    @abstractmethod
    def name(self):
        pass

    @name.setter
    @abstractmethod
    def name(self, name):
        pass

    @staticmethod
    @abstractmethod
    def method1():
        pass

    @classmethod
    def method2(cls):
        pass


class SocketStream(IStream):
    def __init__(self, name, address):
        self.address = address
        self.data = None
        self.name = name

    def read(self, max_types=2):
        print(self.address)

    def write(self, data):
        self.data = data

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @staticmethod
    def method1():
        print("method1.....")

    @classmethod
    def method2(cls):
        print("method2......")


if __name__ == "__main__":
    s = SocketStream("zhangsan", "localhost")
    s.read()
    print(s.name)

    SocketStream.method1()
    s.method2()
```

抽象基类的目的就是让别的类继承并且实现特定的抽象方法

### 实现自定义容器

实现一个自定义的类来模拟内置容器类功能


通过collections定义的抽象基类，在自定义容器类的过程中，可以实现对应的抽象方法，创建对应的容器
```python
# coding: utf-8

from collections.abc import Iterable


class MyList(Iterable):
    def __init__(self, my_list):
        self._my_list = my_list

    def __iter__(self):
        return iter(self._my_list)


if __name__ == "__main__":
    m = MyList([1, 2, 3, 4, 5])

    for i in m:
        print(i)
```
使用 collections 中的抽象基类可以确保你自定义的容器实现了所有必要的方法。并且还能简化类型检查。


### 属性的代理访问

将某个示例的属性访问代理到内部的另外一个实例中去，目的是作为继承的一个替代方法或者实现代理模式


```python
class A:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print(f"Hello,World {self.name}")


class B:
    def __init__(self):
        self._a = A("B")

    def speak(self):
        print("I'm B")

    def __getattr__(self, item):
        return getattr(self._a, item)


if __name__ == "__main__":
    b = B()
    b.speak()
    b.hello()
```
备注：
__getattr__方法只有在属性不存在时才会调用，是一个后背方法，如果代理类实例存在该属性，则不会触发这个方法；
__getattr__方法对双下划线开始和结尾的属性不适用；
