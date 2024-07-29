## 浅析装饰器
> 通常情况下，给一个对象添加新功能有三种方式：
- 直接给对象所属的类添加方法；
- 使用组合；（在新类中创建原有类的对象，重复利用已有类的功能）
- 使用继承；(可以使用现有类的，无需重复编写原有类进行功能上的扩展)
> 一般情况下，优先使用组合，而不是继承。但是装饰器属于第四种，动态的改变对象从而扩展对象的功能。
一般装饰器的应用场景有打印日志，性能测试，事务处理，权限校验；

## Python 内置装饰器的工作原理
> 理解Python装饰器工作原理，首先需要理解闭包这一概念。闭包指的是一个函数嵌套一个函数，内部嵌套的函数调用外部函数的
变量，外部函数返回内嵌函数，这样的结构就是闭包。<br>
> 装饰器就是闭包的一种应用，但是装饰器参数传递的是函数。

简单的闭包示例：
```python
def add_num(x):
    def sum_num(y):
        return x+y
    return sum_num

add_num5 = add_num(5)
total_num = add_num5(100)
print(total_num)
```
**注解：**<br>
- add_num外函数接受参数x，返回内函数sum_num，而内函数sum_num接受参数y，将和add_num外函数接受参数x相加，返回结果。add_num5对象则是定义了add_num外函数接受的参数x为5，最后add_num5(100)返回的结果则是105。

## 装饰器的基本使用
**简单计算函数运行时间装饰器示例：**
```Python
def times_use(func):
    def count_times(*args, **kwargs):
        start = time.time()
        result  = func(*args, **kwargs)
        end = time.time()
        print(end-start)
        return result
    return count_times

@times_use
def test_decorator():
    time.sleep(2)
    print("Test Decorator")
test_decorator()
```
**注解：**<br>
- 这里将函数test_decorator作为参数，传入到times_use函数中，然后内部函数count_times则是会保留原有test_decorator函数代码逻辑，在执行test_decorator前保存执行前时间，然后和执行后的时间进行比较，得出相应的耗时。
- 通过装饰器的好处则是能在保留原有函数的基础上，不用进行对原有函数的修改或者增加新的封装，就能修饰函数增加新的功能。
- test_decorator = time_use(test_decorator)

**根据日志等级打印日志装饰器示例(带参数的装饰器）：**
```python
def use_logging(level):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if level == "warn":
                logging.warn("%s is running"% func.__name__)
            result = func(*args, **kwargs)
            print(result) 
            return result
        return wrapper
    return decorator

@use_logging("warn")
def test_decorator():
    print("Test Decorator")
    return "Success"
test_decorator()
```

**计算函数运行时间的类装饰器示例：**
```python
class logTime:
    def __init__(self, use_log=False):
        self._use_log = use_log

    def __call__(self, func):

        def _log(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            print(result)
            end_time = time.time()
            if self._use_log:
                print(end_time-start_time)
            return result
        return _log

    
@logTime(True)
def test_decorator():
    time.sleep(2)
    print("Test Decorator")
    return "Success"
```
## functools wraps使用场景
> 使用装饰器虽然能在保存原有代码逻辑的基础上扩展功能，但是原有函数中的元信息会丢失，比如__name__, \_\_doc\_\_,参数列表。针对这种情况
可以使用functools.wraps，wraps也是一个装饰器，但是会将原函数的元信息拷贝到装饰器函数中。

**具体使用方法：**

```python
from functools import wraps

def use_logging(level):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if level == "warn":
                logging.warn("%s is running"% func.__name__)
            result = func(*args, **kwargs)
            print(result) 
            return result
        return wrapper
    return decorator

@use_logging("warn")
def test_decorator():
    """" Test Decorator DocString""""
    time.sleep(2)
    print("Test Decorator")
    return "Success"

print(test_decorator.__name__)
print(test_decorator.__doc__)
```
**注解：**<br>
- wraps装饰器将传入的test_decorator函数中的元信息拷贝到wrapper这个装饰器函数中，使得wrapper拥有和test_decorator的
元信息。


## 关于装饰器的执行顺序
> 在日常业务中经常会使用多个装饰器，比如权限验证，登录验证，日志记录，性能检测等等使用场景。所以在使用多个装饰器
时，就会涉及到装饰器执行顺序的问题。先说结论，关于装饰器执行顺序，可以分为两个阶段：（被装饰函数）定义阶段、（被装饰函数）执行阶段。
- 函数定义阶段，执行顺序时从最靠近函数的装饰器开始，从内向外的执行；
- 函数执行阶段，执行顺序时从外而内，一层层的执行；

**多装饰器示例：**
```python
def decorator_a(func):
    print("Get in Decorator_a")

    def inner_a(*args, **kwargs):
        print("Get in Inner_a")
        result = func(*args, **kwargs)
        return result
    return inner_a

def decorator_b(func):
    print("Get in Decorator_b")

    def inner_b(*args, **kwargs):
        print("Get in Inner_b")
        result = func(*args, **kwargs)
        return result
    return inner_b

@decorator_b    
@decorator_a
def test_decorator():
    """test decorator DocString"""
    print("Test Decorator")
    return "Success"
```

**运行结果：**
```
Get in Decorator_a
Get in Decorator_b
Get in Inner_b
Get in Inner_a
Test Decorator
```

**代码注解：**
- 上述函数使用装饰器可以相当于decorator_b(decorator_a(test_decorator())，即test_dcorator函数作为参数传入到decorator_a函数中，然后打印"Get in Decorator_a"，并且返回inner_a函数，给上层decorator_b函数，decorator_b函数接受了作为参数的inner_a函数，打印"Get in Decorator_b",然后返回inner_b函数；
- 此时test_decorator(),即调用了该inner_b函数，inner_b函数打印"Get in inner_b"，然后调用inner_a函数，inner_a打印了"Get in Decorator_a",最后调用test_decorator函数。这样从最外层看，就像直接调用了test_decorator函数一样，但是可以在刚刚的过程中实现功能的扩展；

## 参考链接
> https://www.zhihu.com/question/26930016
> https://segmentfault.com/a/1190000007837364
> https://blog.csdn.net/u013411246/article/details/80571462


## 高级使用
装饰器：
    - 日常使用过程中，传入是函数返回也是函数的函数
    - 装饰器的本身既可以是函数也可以是类
    - 装饰器装饰的对象既可以是函数也可以是类
    
装饰器的类：
```python
class Timer:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        start = time.time()

        ret = self.func(*args, **kwargs)

        end = time.time()
        print(end - start)

        return ret


class Timer2:
    def __init__(self, prefix_time):
        self.prefix_time = prefix_time

    def __call__(self, func):

        def wrapper(*args, **kwargs):
            start = time.time()

            ret = func(*args, **kwargs)

            end = time.time()
            print(self.prefix_time, end-start)
            return ret

        return wrapper


@Timer
def add(a, b):
    time.sleep(1)
    return a+b


@Timer2(prefix_time="current time: ")
def add2(a, b):
    time.sleep(1)
    return a+b

```

装饰类的装饰器
```python
def add_str(cls):

    def __str__(self):
        return str(self.__dict__)

    cls.__str__ = __str__
    return cls

@add_str
class MyObj:
    def __init__(self, a, b):
        self.a = a
        self.b = b


obj = MyObj(1, 2)
print(obj)
```
备注：
- 可以理解为MyObj = add_str(MyObj)
