## 导语
> 之所以总结Python 魔术方法，是因为有关这部分的内容在Python官方文档中相对松散，但是在后续相关的日常业务场景中我们可能会碰到一些需要注意的地方，所以打算参考官方文档以及结合自身日常使用总结记录一下。


**什么是魔术方法？**
> 关于魔术方法，Python官方文档中没有特别明确的定义，这里的魔术方法常指的是双下划线在方法名前后的特殊方法；而参考网上的
资料，魔术方法的特点就是一般都不需要主动调用，而是常常在类或者对象触发某个事件自动执行；而如果需要定制特殊功能的类，则需要对指定的特殊方法进行重写；

## 基本定制

### 构造和初始化
> 在Python中，类的构造，初始化，销毁操作主要涉及到__new__,__init__,__del__这几个常用的魔术方法，针对这三个方法
可以重点讲讲主要需要注意的地方。

**object.\_\_new\_\_(cls[, ...]):**
1. \_\_new\_\_ 方法的作用就是定制类的创建过程，但在一般的情况下不需要显式地声明；
2. \_\_new\_\_ 方法主要是在创建类的实例时所调用的第一个方法，第一个参数是接受类的本身，其余的参数一般都传递给__init__方法；
3. \_\_new\_\_ 方法在定制化过程中，**必须要返回一个cls的实例**，否则新实例的\_\_init\_\_方法就不会执行；

**object.\_\_init\_\_(self[, ...])**
1. \_\_init\_\_() 方法的作用是创建实例后返回给调用者之前的初始化，即类的初始化方法；
2. 如果一个基类中有\_\_init\_\_()方法，则派生类如果也有\_\_init\_\_()方法，就必须显示调用它确保实例的基类部分的正确初始化（
如：super().\_\_init\_\_([args...])
3. \_\_init\_\_() 方法只能返回None，即默认不返回任何对象，否则会抛出异常TypeError;


**object.\_\_del\_\_(self)**
1. \_\_del\_\_() 方法主要是用于实例销毁时调用的方法；
2. 这里可能出现的误区就是比如del x，这样并不会显示调用x.\_\_del\_\_()方法，前者只是让x的引用计数减一，后者指的是
x引用计数为0时被调用；


**这一小结内容的示例：**
```python
# -*- coding: utf-8 -*-


class FileCache:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.file = open("D:\\test.txt", "r")

    def __del__(self):
        self.file.close()

    def get_content(self):
        return self.file.readline()


if __name__ == "__main__":
    file1 = FileCache()
    file2 = FileCache()
    # 判断是否为同一实例
    print(id(file1) == id(file2))

    file1_content = file1.get_content()
    print(file1_content)
    file2_content = file2.get_content()
    print(file2_content)
```
备注：
- 这里的FileCache相当于一个文件流的缓存类，通过__new__方法，实现一个单例模式，主要原理通过cls即FileCache类本身，
将super().\_\_new\_\_(cls)创建的新实例作为cls的类变量，所以他能在所有的实例之间共享，当实例化FileCache类时，如果已
存在该_instance变量则返回，不存在则创建；
- \_\_del\_\_()方法主要是在FileCache的实例被gc销毁时，关闭文件流（这里只是作为示例，实际打开文件流最好使用with...open(）方式；

### 类的表现

**object.\_\_repr\_\_(self):**
1. 由repr()内置函数调用以输出一个“官方”的字符串表示，\_\_repr\_\_()方法返回值必须是一个字符串对象；
2. 如果一个类中只定义了\_\_repr\_\_()，但是没定义\_\_str\_\_()方法，则该类的实例表示时也会使用到\_\_repr\_\_()方法；

**object.\_\_str\_\_(self)**
1. 由str(),print()等内置函数调用时触发生成字符串，\_\_str\_\_()方法返回值必须是一个字符串对象；
2. \_\_str\_\_()方法应该提供可读性强的信息，面向用户，\_\_repr\_\_()方法应该提供更加准确的结果信息，面向开发者便于调试；


## 自定义属性访问

**object.\_\_getattr\_\_(self, name):**
1. 当访问属性触发AttributeError时调用\_\_getattr\_\_()方法，比如访问一个实例不存在的属性时；
2. \_\_getattr\_\_()方法应当返回一个属性值或者继续向上层抛出AttributeError异常，实际使用过程可以为找不到的属性设置默认值；

示例：
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __getattr__(self, item):
        return f"Attribute {item} Not Found"


if __name__ == "__main__":
    p = Person("zhangsan", 33)
    print(p.name)
    print(p.address)
```
备注：
- 访问p对象中的address属性时，实例中不存在该属性触发调用\_\_getattr\_\_()方法，返回一个字符串；


**object.\_\_getattribute\_\_(self, name):**
1. 当类的实例属性被访问时，就会触发\_\_getattribute\_\_()方法，相对于\_\_getattr\_\_()方法，无论属性是否存在都会被调用；
2. 类同时定义了\_\_getattribute\_\_方法和\_\_getattr\_\_方法，后者正常情况下不会被调用，除非前者显式调用后者，或者抛出AttributeError；
3. 在实际使用情况下，\_\_getattribute\_\_方法一般较少重写，因为可能会涉及到无限递归的问题，想要避免此类问题可以调用基类方法来访问需要的属性：super().\_\_getattribute\_\_(item)


**object.\_\_setattr\_\_(self, name, value):**
1. 当一个类的实例属性尝试被赋值时则会调用\_\_setattr\_\_()方法，这个调用会取代默认机制;（属性访问的默认行为是从一个对象的字典中获取、设置或删除属性)
2. 在方法中设置实例属性可以通过调用基类的方法,super().__setattr__(name, value);

示例：
```python
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __setattr__(self, name, value):
        print(f"{name}:{value}")
        super().__setattr__(name, value)

if __name__ == "__main__":
    p = Person("zhangsan", 33)
```
备注：
- 这部分代码主要是用于实例设置属性时会打印对应name和value，然后通过调用基类的方法设置实例属性（这里单纯作为示例，具体该方法还可以用于控制设置属性的权限）

**object.\_\_delattr\_\_(self, name)**
1. 当del删除类的实例属性时会触发调用\_\_delattr\_\_()方法；
2. 同样在方法中删除实例属性，可以使用基类的方法：super().__delattr__(name)；


## with语句上下文管理
> 根据Python的官方文档的解释是实现了\_\_enter\_\_()方法和\_\_exit\_\_()方法的对象都可以称作上下文对象，上下文管理器对象则定义了语句体被执行前进入上下文，语句体被执行完毕时退出该上下文。  
如果通俗的解释就是一段代码执行前执行一段代码用于预处理的工作，在执行之后又执行一批代码用于一些清理的工作。实际使用可以参考file object对象，读写完毕后会关闭对象。  
**with语句就是用于执行上下文管理器对象定义的方法**。

**object.\_\_enter\_\_(self)：**
- 进入运行时上下文并返回此对象或关联到运行时上下文的其他对象；
- 这个方法会将返回值绑定到此上下文管理器的with语句的as子句中的标识符

**object.\_\_exit\_\_(self, exc_type, exc_value, traceback)**
- 退出运行时上下文并且返回一个布尔值表示来表明所发生的异常是否应当屏蔽；
- 如果在执行with语句中的语句体期间发生异常，则参数会包含异常的类型，值以及回溯信息，其他情况下，三个参数均为None

通过一个示例了解一下with如何工作：
```python
class FileExample:
    def __enter__(self):
        print("In __enter__()")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"In __exit__(): {exc_type}")
        return True

    def read(self):
        raise Exception("test")
        return "File Content"

if __name__ == "__main__":
    with FileExample() as f:
        print(f.read())
    print("exex success")
```
执行结果：
```bash
In __enter__()
In __exit__(): <class 'Exception'>, test, <traceback object at 0x7f2d4fb77208>
exec success
```
备注：
- FileExample是一个上下文管理器对象，实现了\_\_enter\_\_()方法和\_\_exit\_\_()方法；
- 发起调用上下文管理器的\_\_enter\_\_()方法，然后将\_\_enter\_\_()方法的返回赋值给f；
- 执行语句体中的代码，调用f对象的read()方法，由于read()强制抛出异常，由于异常退出，则会将异常的类型，值和回溯信息做为参数传递给\_\_exit\_\_()方法，由于\_\_exit\_\_()方法里面设置返回值为真，则异常会捕获，不会抛到最上层，继续执行with之后的代码；


## 模拟容器类型
> 通过以下常用的魔术方法能够实现容器对象，而常见的容器对象包括序列（元组和列表）和映射（字典），两种类型容器对象在一些方法中也存在着一些区别需要注意。

**object.\_\_len\_\_(self)**
- 调用此方法实现len()内置函数，返回值必须是>=0的整数；

**object.\_\_setitem\_\_(self, key, value)**
- 调用此方法实现向self[key]赋值，应该仅限于需要映射允许基于键修改该值或添加键；

**object.\_\_getitem\_\_(self, key)**
- 调用此方法实现self[key]的求值，对于序列类型，接受的键应为整数和切片对象，对于映射类型，key不在容器中则抛出KeyError异常；

**object.\_\_delitem\_\_(self, key)**
- 调用此方法实现self[key]删除，具体因为不正确key值引发的异常和\_\_getitem\_\_()相同；

**object.\_\_iter\_\_(self)**
- 此方法在需要为容器创建迭代器时调用，此方法应该返回一个新的迭代器对象，能够逐个迭代容器中的所有对象。对于映射应该逐个迭代容器中的键；

**object.\_\_reversed\_\_(self)**
- 此方法会被reversed()内置函数调用实现逆向迭代，应当返回一个新的已逆序逐个迭代容器内所有对象的迭代器对象；
- 如果没有提供这个方法，reversed()内置函数将回退到使用序列协议__len__()和__getitem__()方法；

**object.\_\_contains\_\_(self, item)**
- 此方法实现成员检测运算符，如果item时self的成员则返回真，否则则返回假，对于映射类型，检测基于键而不是值或者键值对；


模拟实现一个容器类型示例，实现了内置list的方法（主要用于测试魔术方法）：
```python
class PersonalList:
    def __init__(self, values=None):
        if values:
            self.values = values
        else:
            self.values = []

    def append(self, value):
        self.values.append(value)

    def __len__(self):
        return len(self.values)

    def __setitem__(self, key, value):
        self.values[key] = value

    def __getitem__(self, item):
        return self.values[item]

    def __delitem__(self, key):
        return self.values.pop(key)

    def __iter__(self):
        return iter(self.values)

    def __reversed__(self):
        return self.values[::-1]


if __name__ == "__main__":
    a = [1,2,3,4,5]
    p = PersonalList(a)
    print(reversed(p))
    print( 1 in p)
```

## 模拟可调用对象

object.__call__(self[, args...])
- 此方法会将实例当作函数调用时触发，实际使用场景可以将一些复杂的操作合并直接调用，减少调用的步骤，方便使用；

通过一个类重写__call__方法实现生成斐波那契数列功能
```python
class Fib:
    def __init__(self):
        self.fib_list = []

    def __call__(self, num):
        start, end = 0, 1
        self.fib_list = []

        for i in range(num):
            self.fib_list.append(start)
            start, end = end, start+end
        return self.fib_list

    def __str__(self):
        return ",".join([str(x) for x in self.fib_list])


if __name__ == "__main__":
    f = Fib()
    f(10)
    print(f)
```
备注：
- 将生成斐波那契数列功能代码写在__call__方法中，传入参数num为输出到斐波那契数列的第几项；

## 总结
> 以上是我在日常工作场景经常使用到或者需要注意的魔术方法，总体并不是很多，还有许多算数相关的魔术方法因为比较少使用到，感兴趣的同学能去看看官方的文档，那边对于这些内置的方法记录的比较全，这里就不做过多涉猎了。
总的来说，这里面其实需要有很多东西在总结前可能都比较模糊不清，比如with语句执行上下文管理对象，with语句的执行顺序？如果\_\_enter\_\_()方法中异常了，\_\_exit\_\_()方法会正常执行？所以其实很多东西，只有在总结重新输出成知识的时候才能够查漏补缺，有啥问题欢迎大家一起讨论。

**参考链接：**
> https://docs.python.org/zh-cn/3/reference/datamodel.html

> https://www.cnblogs.com/pyxiaomangshe/p/7927540.html

> https://zhuanlan.zhihu.com/p/329962624

> https://pycoders-weekly-chinese.readthedocs.io/en/latest/issue6/a-guide-to-pythons-magic-methods.html#id5

