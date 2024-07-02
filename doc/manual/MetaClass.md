
简单装饰器

```python
from functools import wraps
import time


def time_use(func):
    @wraps(func)
    def count_time(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(func.__name__, time.time() - start_time)
        return result

    return count_time


@time_use
def hello_world():
    print("starting")
    time.sleep(2.4)
    print("end...")


if __name__ == "__main__":
    hello_world()
```
备注：
- 使用@wraps装饰器来注解底层包装函数，复制被包装函数的元信息；

按照上述的使用wraps装饰函数，则实际使用过程中可以支持跳过装饰函数，直接访问底层函数(可以理解为接触装饰函数)
```python
if __name__ == "__main__":
    f = hello_world.__wrapped__
    f()
```


带可选参数的装饰器
```python


def simple_logged(func=None, *, level=logging.DEBUG, name=None, message=None):
    print(func)
    if func is None:
        return partial(simple_logged, level=level, name=name, message=message)

    log_name = name if name else func.__module__
    logger = logging.getLogger(log_name)
    log_message = message if message else func.__name__

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.log(level, log_message)
        return func(*args, **kwargs)

    return wrapper


@simple_logged
def hello_world():
    print("starting")
    time.sleep(2.4)
    print("end...")


@simple_logged(level=logging.WARNING, name="hello_world", message="simple logged")
def hello_world2():
    print("hello,world...")


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    hello_world()
    hello_world2()
```

避免重复的属性方法
> 你在类中需要重复的定义一些执行相同逻辑的属性方法，比如进行类型检查，如何简化这类代码？

```
from functools import partial


def typed_property(name, expected_type):
    storage_name = "_" + name

    @property
    def prop(self):
        return getattr(self, storage_name)

    @prop.setter
    def prop(self, value):
        if not isinstance(value, expected_type):
            raise TypeError(f"{name} must be {expected_type}")
        setattr(self, storage_name, value)

    return prop


class Person:
    str_property = partial(typed_property, expected_type=str)
    int_property = partial(typed_property, expected_type=int)
    name = str_property("name")
    age = int_property("age")

    def __init__(self, name, age):
        self.name = name
        self.age = age


if __name__ == "__main__":
    p = Person("zhangsan", 22)
    p.name = "zhangsdna"
    p.age = 100
    print(p.name, p.age)
```
备注:
- 使用partial固定部分参数的值生成新的函数
- 在Person中的使用typed_property，利用了闭包的特性，通过self，用setattr和getattr设置和访问闭包内的变量；

定义上下文管理器的简单方法
```python
from contextlib import contextmanager
import time

@contextmanager
def time_block(label):
    start = time.perf_counter()
    try:
        yield
    finally:
        end = time.perf_counter()
        print(f"{label}: {end - start}")
        
if __name__ == "__main__":
    with time_block("counting"):
        n = 1000000
        while n > 0:
            n -= 1
```
备注：
- yield之前的代码在上下文管理器中会作为__enter__方法执行
- yield之后的代码在上下文管理器中会作为__exit__方法执行
- 如果出现异常会在yield语句那抛出
