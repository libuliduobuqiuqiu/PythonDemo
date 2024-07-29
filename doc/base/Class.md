## Descriptor

descriptor（描述器）基本定义：
> 当一个class定义了__get__,__set__,__delete__这三个函数之中的任意一个都会变成一个descriptor

需要解决的几个问题：
1、描述器的作用
2、描述器的应用范围

关于LOAD_ATTR原理：
```python
class Name:
    def __get__(self, obj, objtype):
        return "Peter"

class A:
    name = Name()


if __name__ == "__main__":
    a = A()
    print(a.name)
    a.name = "Bob"
    print(a.__dict__)
    print(a.name)
    Name.__set__ = lambda x,y,z: None
    print(a.name)
```
代码注释：
- 当调用A的实例对象a上的name时，由于name是描述器对象，则获取的是__get__方法返回的值；
- 当通过a.name='Bob'时，将变量name绑定绑定对象a上的，即将这个name属性保存到对象a的__dict__上，由于Name描述器没有__set__方法，所以LOAD ATTR时，先从__dict__上获取到name
- 最后通过匿名函数，把Name描述器设置了__set__方法， Name描述器的优先级大于__dict__，即优先返回Name描述器上的__get__函数，所以就打印出Peter

总结：
-LOAD_ATTR过程中，Python会尝试获取object是否是定义了__get__函数的descriptor，如果是还需要判断是否定义了__set__函数，只有当这个descriptor既有了__set__函数又有了__get__函数，才会立刻返回__get__函数的返回值；
- 如果不满足上述的情况，才会找到object本身的__dict__，是否存在需要获取的值；
- 如果上一环节，还没获取到对应的值，就会尝试通过descriptor的__get__函数；
- 最后如果object没有__get__函数，就直接原样返回

_get__,__set__ > __dict__ > __get__

## Class底层机制 

- 底层是通过__ build_class__函数构造一个类，该函数返回的值是一个type
- 在Python语言中通过Class定义的类的type都是type
- 当定义一个新的Class时候，相当于运行了所有在这个class里面的代码，然后将产生的所有局部变量的名字和他们对应的值
都保存到了这个class的__dict__里面，（例如使用到这个类的变量A.f的时候就会从A的__dict__里面找到对应的f名称的变量） 

通过类的名字、继承的父类、对应的字典可以通过type动态创建class
```python
def f(self):
    print(self.name)

temp_dict = {
    "name": "zhangsan",
    "f": f
}

A = type("A", (), temp_dict)
print(A.__dict__)
a = A()
a.f()
```
> type()函数创建类，本质上是Claas语句的一种动态形式


## MRO机制（method resolution order)方法解析顺序
简单来说就是Python中类优先使用哪个父类的函数

打印类的MRO(类的优先继承关系)
```python
A.__mro__
A.mro()
```

每一个类会将所有的父类和自己，做一个线性化，把所有继承的类和自身做一个排队，保证自身是最高优先级，
当调用一个方法或者使用一个变量时，会根据队列优先级顺序从前往后找；
总结:写继承关系的时候尽量写明白类的继承关系，以及懂得如何获取类的优先继承顺序；

## Class定义的function怎么变成method

关于self：（有趣的现象）
```python
class A:
    def f(self, data):
        print(self.name)
        print(data)
    

if __name__ == "__main__":
    a = A()
    a.name = "zhangsan"
    a.f("success")
```
> 思考背后的现象，为什么对象调用f方法时，不需要传入self参数，只需要传入self后面的data参数？

背后逻辑梳理（现在可以先对比A.f和a.f这两者之间的区别）
```
print(a.f)
print(A.f)

# 结果：
# <bound method A.f of <__main__.A object at 0x016BA350>>
# <function A.f at 0x01813540>
```
结论：
可以看得出来，实际上直接调用类上的f，实际返回的是一个函数，对象调用f，实际返回的是一个绑定自身的方法，所以当一个对象直接调用自身的方法时，就不需要给自身的self参数传递值。

> 继续思考：为什么在一个类和他自身对象里面获取同样的attribute，但是却是不一样的结果，怎么理解？

背后的逻辑就是有关描述器：
- 在使用A.f的过程中，由于对象A的__dict__里面有f的变量，所以直接返回的function object
- 在使用a.f的过程中，由于对象a的__dict__里面没有f的变量，需要到A里面寻找，而到A里面寻找f，则返回这个function object，而在LOAD ATTR的过程中会检查这个object有没有descriptor __get__函数，有的话则直接返回的不是这个f变量，而是返回f 调用__get__函数返回的值。返回的值则是一个绑定了对象a的方法object。所以调用这个method，只需要传输self后面的参数，而 这个method会自动把这个object补充到第一个参数上。


## MetaClass入门

MetaClass是什么？
MetaClass可以说是一个创建类的类，即通过MetaClass控制创建类的行为，
 
MetaClaas作用简单来说就是解决继承无法解决的事情
```
class M:
    def __new__(cls, name, bases, dict):
        print(name, bases, dict)
    
        for key in dict.keys():
            if key.startswith("test_"):
                raise ValueError()
        
        return type.__new__(cls, name, bases, dict)


A = M("A", (), {})
# 等价于class A(metaclass=M)
```
备注：
- A通过M来建立Class，而不是直接用type
- 上述M还能够限制class中不能出现test_开头的函数
- name字符串为类名称，bases元组为基类（继承的父类），dict字典为包含属性和方法的定义

```python
class M(type):
    def __new__(cls, name, bases, dict):
        print(name, bases, dict)

        for key in dict.keys():
            if key.startswith("test_"):
                raise ValueError()
        
        return type.__new__(cls, name, bases, dict)

    def __init__(self, name, base, dict):
        self.random_id = random.randint(1, 100000)
        return type.__init__(self, name, base, dict)

    def __call__(cls, *args, **kwargs):
        print("call: ", args)
        return type.__call__(cls, *args, **kwargs)

class A(metaclass=M):
    def __init__(self, name):
        self.name = name
        print(name)
        print(self.random_id)

a =  A("zhangsan")
b = A("wamgwgu")
```

结果：
```
A () {'__module__': '__main__', '__qualname__': 'A', '__init__': <function A.__init__ at 0x0000025736007F40>}
call:  ('zhangsan',)
zhangsan
63184
call:  ('wamgwgu',)
wamgwgu
```
既然可以通过__new__定义创建类时的行为，也可以通过__init__定义在__new__函数之后调用
同时可以定义__call__函数，而这个__call__函数并不是在定义A时候使用的，而是在产生A的实例过程中使用的

通过以上__call__定义，可以写出一个单例示例：
```python
class SingletonMetaclass(type):
    def __call__(cls,*args, **kwargs):
        if hasattr(cls, "_instance"):
            return cls._instance
        
        cls._instance = type.__call__(cls, *args, **kwargs)
        return cls._instance

class Singleton(metaclass=SingletonMetaclass):
    pass

t1 = Singleton()
t2 = Singleton()
print(id(t1), id(t2))
print(t1 == t2)
```
所以可以通过元类定义__call__方法行为，每次只返回第一次产生的实例。


## __slots__
限制实例可以使用属性的种类，可以理解为一个白名单，只允许实例使用__slots__里的属性

```python
class A:
    __slots__ = ["f", "g", "name"]

    def __init__(self, name):
        self.name = name
    
    def fprint(self):
        print(self.name)
```
如果__slots__里面没有name属性，则fprint方法打印self.name的时候就会发生异常；

思考，__slots__设计的目的？以及怎么设计？
> 进行性能比较，一个是利用__slots__定义了可调用的属性，一个是没有
```python
import time

class A:
    __slots__ = ["f", "g", "name"]

class B:
    pass

a = A()
b = B()

start1 = time.time()
for _ in range(100000000):
    a.f = "zhangsan"

start2 = time.time()
print(start2 - start1)

for _ in range(100000000):
    b.f = "wangwau"
print(time.time() - start2)
```
结果：
```
7.018959999084473
7.888837575912476
```
结论，对比分析总结以下几个结论：
- 通过限制属性种类，利用白名单机制，增加程序鲁棒性
- access这些属性的时候速度更快
- 节省内存

考虑以上结论背后的低层机制原理？

简单总结背后底层原理：（由于关于底层C语言不太熟悉，大概看了教程总结，目前知道大概意思即可）
- 通过__slots__定义，底层分别会保存__slots__里面的名字和对应建立的实例中对应的相对位置，然后根据这些数据分别
建立了描述器，并且保存在type的__dict__的里面；
- 所以每次建立实例的过程中，都会预留出slots的空间，通过描述器在这些空间读取。

以上的大致流程，那为什么能够节省内存？
首先根据前面关于Descriptor描述器的学习，首先在类中访问一个attribute的时候，首先会在mro里面对应descriptor，
所以涉及一个过程，就是会在当前的class，当前class没有，继续找父辈class，尝试是否能够访问到该描述器。最后找不到
才会到当前object的__dict__里面找。

## Super
super是什么？他是一个方法？函数？一个关键字？
准确来讲super是一个内置类，super()是建立一个super对象，

super()函数里面默认传入的两个参数：
- 第一个参数是一个type或者是class，决定mro链从哪个class开始寻找
- 第二个参数是一个type或者是object，决定使用的对象和mro

```python
from objprint import op
import time

class Person:
    def __init__(self, name: str):
        self.name = name

class Male(Person):
    def __init__(self, name: str):
        super(Male, self).__init__(name)
        self.gender = "Male"

    def get_info(self):
        print(f"{self.name}: {self.gender}")


if __name__ == "__main__":
    male = Male("linshukai")
    print(male)
    op(male)
```
- super(Male, self).__init__(name)可以等价于Person.__init__(self, name)
- 首先拿到self这个对象的MRO（Male，Person，object），然后根据Male确定其MRO所处的位置，然后从Male后面的Class开始寻找，
然后判断Person这个Class是否有__init__这个函数，有则直接调用。（简单来说，则是方法查找，同样也可以属性查找）
- super方便的地方是调用父类的方法不需要显式的指定它们的名称，从而使代码更加容易维护；
- super的零个参数的形式仅适用于类定义内部，（背后的黑魔法在于它能够获取是在哪个Class被调用，把这个Class放在super的第一个参数，以及在被定义的函数的第一个参数放到super的第二个参数）
