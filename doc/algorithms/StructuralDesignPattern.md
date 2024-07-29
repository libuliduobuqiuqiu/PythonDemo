## The Adapter Pattern 适配器模式(解决接口不兼容问题）
- 目的：通过增加中间层来实现不兼容接口的适配；
- 本质：通过继承或者依赖，实现想要的目标接口；

```python
# -*- coding: utf-8 -*-


class Computer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I'm a {self.name} computer."

    def execute(self):
        return "Execute a program"


class Human:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"My name is {self.name}"

    def speak(self):
        return "Speak loudly."


class Synthesizer:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"I am a {self.name} synthesizer."

    def play(self):
        return "Play a game"


class Adapter:
    def __init__(self, obj, adapter_method):
        self.obj = obj
        self.__dict__.update(adapter_method)

    def __str__(self):
        return str(self.obj)


if __name__ == "__main__":
    objs = [Computer("XiaoMi")]
    man = Human("Leijun")
    synth = Synthesizer("Synth")

    # 统一使用execute适配不同对象的方法，这样可以在不修改原有对象的基础上扩展功能
    m_adapter = Adapter(man, {"execute": man.speak})
    s_adapter = Adapter(synth, {"execute": synth.play})
    objs.append(m_adapter)
    objs.append(s_adapter)

    for obj in objs:
        print(f"{str(obj)}:{obj.execute()}")

```
> 注解：
- 在Python中可以通过继承或者class中的__dict__方式去实现适配；
- Synthesizer，Human这两个就是被适配的对象，Computer作为目标对象，适配器通过__dict__方法，将被适配对象的方法统一转换成目标对象的execute方法；


## The Decorator Pattern 装饰器模式 （无需子类化实现扩展对象功能）
- 目的：动态的扩展对象的新功能
- 本质：一个函数嵌套一个函数，内嵌函数调用外嵌函数的参数，外嵌函数返回内嵌函数。而在装饰器中需要动态增加功能的函数一般作为参数传入到外嵌函数中，供内嵌函数调用。（闭包的应用）

```python
# -*- coding: utf-8 -*-


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
```
>注解：
- fib函数主要功能是计算斐波那契数列，装饰器的作用就是缓存已经计算的数值；


## The Facede Pattern 外观模式 （简化复杂对象的访问问题）
- 目的：隐藏系统的复杂性，提供给客户端一个能够访问系统的接口；
- 本质：客户端不和系统耦合，而是提供一个外观类和系统耦合，外观类将调用顺序和依赖关系处理好；

```python
# -*- coding: utf-8 -*-

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
```
>注解：
- OperationSystem作为外观类，处理好FileServer,ProcessServer内部类的细节，然后提供给客户端对应的接口即可；


## 享元模式 The Fly weight (实现对象复用改善资源使用)
- 目的：减少对象的创建，减少内存的占用和提高性能；
- 本质：用唯一标识码判断对象是否存在，如果内存中有则返回该对象；


```python
# -*- coding: utf-8 -*-

import random
from enum import Enum
TreeType = Enum("TreeType", "apple_tree cherry_tree peach_tree")


class Tree:
    pool = dict()

    def __new__(cls, tree_type):
        obj = cls.pool.get(tree_type)

        if not obj:
            obj = object.__new__(cls)
            cls.pool[tree_type] = obj
            obj.tree_type = tree_type
        return obj

    def render(self, age, x, y):
        print(f"render a tree of type {self.tree_type} and age {age} at ({x}, {y})")


if __name__ == "__main__":
    rand = random.randint
    age_min, age_max = 1, 100
    min_point, max_point = 1, 100

    t1 = Tree(TreeType.apple_tree)
    t1.render(rand(age_min, age_max), rand(min_point, max_point), rand(min_point, max_point))

    t2 = Tree(TreeType.cherry_tree)
    t2.render(rand(age_min, age_max), rand(min_point, max_point), rand(min_point, max_point))

    t3 = Tree(TreeType.apple_tree)

    print(t1 == t2)
    print(t1 == t3)
```

## 代理模式 The Proxy Pattern (通过一层间接保护层实现更安全的访问)
- 目的：为其他对象提供一种代理控制目的对象的访问；
- 本质：提供一层中间层，中间层用以代理访问；

```python
# -*- coding: utf-8 -*-

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
```
> 注解：
- 这是个代理安全控制的示例，具体密钥直接在程序中设置，实际情况密钥一般存放在数据库或者指定配置文件中；
- 简单来说，这个示例功能就是在你向指定用户列表添加元素的时候，就需要进行密钥验证；

