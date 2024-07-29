## 导语
**什么是反射机制：**
> 在百科上的定义指的是程序能够在运行过程中访问，检测和修改自身的状态或者行为的一种能力；


**Python 反射机制：**
> 从上面的对于反射机制的解释可以得知，在Python中具备这种反射能力的内置函数有很多，如：isinstance(), type(), dir(), getattr(), setattr(), delattr(), hasattr()；

## Python 内置函数

> 重点介绍四个内置的函数,并且提供对应的示例方便理解：
- getattr(object, name)
- hasattr(object, name)
- setattr(object, name, value)
- delattr(object, name)

**getattr(object, name)**
```python
class Hello:
    def __init__(self, name):
        self.name = name

    def f_print(self):
        print(f"Hello, {self.name}")

if __name__ == "__main__":
    t = Hello("zhangsan")
    fprint = getattr(t, "f_print")
    fprint()
    age = getattr(t, "age", 33)
    print(age)
```
备注：
- 获取对象命名属性中的值，name必须为字符串；
- 获取t对象中的f_print属性，然后fprint()则等同于t.f_print()；
- 如果getattr函数获取对象的属性不存在，如果提供了默认值，则返回，如果没有提供默认值则抛出AttributeError错误；

**hasattr(obj, name)**
```python
class Person:
    def __init__(self, name):
        self.name = name
    
    def info(self):
        print(self.name)

if __name__ == "__main__":
    a = Person("zhangsan")
    print(hasattr(a, "name"))
    print(hasattr(a, "age"))

```
备注；
- hasattr()函数判断对象命名属性中是否存在name的值，name也必须为字符串；
- 原理是通过getattr(object, name)函数调用判断是否抛出AttributeError异常；


**setattr(object, name, value)**
```python
class Person:
    def __init__(self, name):
        self.name = name

    def hello(self):
        print(f"Hello, {self.name}")


def get_info(self):
    print(f"Name: {self.name}, Age: {self.age}")


if __name__ == "__main__":
    setattr(Person, "get_info", get_info)
    p = Person("zhangsan")
    p.hello()
    setattr(p, "age", 33)
    p.get_info()
```
示例运行结果：
```
Hello, zhangsan
Name: zhangsan, Age: 33
```
备注:
- setattr()函数和getattr()函数相对应，用于设置对象的属性的值，可以指定现有的属性也可以新增属性；
- 传入第一个参数指定对象，name必须为字符串，value可以为任意对象可以是函数，字符串，字典等；
- setattr(p, "age", 33)等价于p.age=33,setattr(Person, "get_info", get_info)等价于Person.get_info = get_info;


**delattr(object, name)**
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = 33

    def hello(self):
        print(f"Hello, {self.name}")

    def get_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


if __name__ == "__main__":
    p = Person("zhangsan", 33)
    delattr(p, "age")
    p.get_info()
```
执行结果：
```
AttributeError: 'Person' object has no attribute 'age'
```
备注：
- delattr()函数删除对象中的属性，如果属性不存在则会抛出AttributeError异常；
- 传入name参数的必须为字符串；

## 反射使用示例
> 根据前面的定义以及相关的内置函数的了解，初步已经了解到了Python的反射就是通过字符串寻找对象的属性值，可以动态的进行修改，访问，检测，删除等操作；


**动态的导入包以及使用具体的方法：**
```python
def reflection(model: str, function: str, *args, **kwargs):
    try:
        obj = __import__(model)
        func = getattr(obj, function)
        result = func(*args, **kwargs)
        return result
    except Exception as e:
        raise Exception(f"Reflection Error: {e}")


if __name__ == "__main__":
    # 向指定url地址发送http请求
    url = "http://www.baidu.com"
    result = reflection("requests", "get", url)
    print(result.text)

    # 查询指定目录下的所有文件
    dir_path = "D:\\"
    result2 = reflection("os", "listdir", dir_path)
    print(result2)
```
备注：
- 示例代码很简单，就是先通过__import__导入指定的模块，再通过getattr()函数获取模块中的方法（属性），然后调用该方法；
- 执行该reflection()函数只需要将要使用的模块和方法以字符串形式传入，然后具体方法会使用到的参数也传入到该函数即可；


## 反射机制的优点和缺点

> Python的反射机制的优点：
- 在一定程度避免硬编码，提供灵活性和通用性；
- 可以动态的修改源代码的结构（如代码块，类，协议）；
- 可以在运行时像对待源代码语句一样动态解析字符串中可执行的代码；

> 关于Python的反射机制在实际工作场景中很少用到，或者说是很少直接用到，总结有以下的缺点：
- 需要具备一定框架设计知识，反射机制的使用经验，业务场景的设计，不然容易在实际使用场景下出现不稳定的事件；
- 过多的使用反射技术，也不利于团队之间的协作开发，以及后期业务代码的重构优化；


## 总结
> 关于Python 反射机制方面的知识在官方文档中没有详细介绍，只是简单了介绍有关放射的几个内置函数的用法，之所以需要总结这部分的
内容，是因为反射这个概念在java，go中都是一个很核心的机制。
> 虽然python 反射在实际使用中可能很少直接使用到，但是对于一些框架中的
关系映射，对象交互等都会使用到，了解这一原理也是为了方便后续一些框架的学习，如果具体有什么问题欢迎一起讨论。

**参考链接：**
> https://docs.python.org/zh-cn/3/library/functions.html?highlight=getattr#getattr
> https://www.cnblogs.com/Jaryer/p/13599996.html
> https://www.cnblogs.com/vipchenwei/p/6991209.html
