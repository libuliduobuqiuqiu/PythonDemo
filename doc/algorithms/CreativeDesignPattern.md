## The Factory Pattern 工厂模式（解决对象创建问题）
- 目的：简化对象创建过程，隐藏创建细节；
- 本质：对象创建过程的抽象；

### 简单工厂
```python
# -*- coding: utf-8 -*-


class BMW:
    def __repr__(self):
        return "I am a bmw car."


class BYD:
    def __repr__(self):
        return "I am a byd car."


class SimpleFactory:

    @staticmethod
    def factory_car(car_name):
        if car_name == "bmw":
            return BMW()
        elif car_name == "byd":
            return BYD()
        else:
            return "No more car."


if __name__ == "__main__":
    print(SimpleFactory.factory_car("bmw"))
```
### 工厂方法
```python
# -*- coding: utf-8 -*-

import abc


class BYD:
    def __repr__(self):
        return "比亚迪"


class BMW:
    def __repr__(self):
        return "宝马"


class AbstractFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def product_car(self):
        pass


class BydFactory(AbstractFactory):
    def __str__(self):
        return "BYD工厂"

    def product_car(self):
        return BYD()


class BmwFactory(AbstractFactory):
    def __str__(self):
        return "BMW工厂"

    def product_car(self):
        return BMW()


if __name__ == "__main__":
    byd_factory = BydFactory()
    print(byd_factory.product_car())

    bmw_factory = BmwFactory()
    print(bmw_factory.product_car())
```
注解
- 将工厂类抽象，让不同的工厂生成对应的产品，如果后期需求增加，则需要添加相应的产品类和工厂子类；


### 抽象工厂
```python
# -*- coding: utf-8 -*-

import abc


class BYD:
    def __repr__(self):
        return "比亚迪"


class BMW:
    def __repr__(self):
        return "宝马"


class BMW_SUV:
    def __repr__(self):
        return "宝马SUV"


class BYD_SUV:
    def __repr__(self):
        return "比亚迪SUV"


class AbstractFactory(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def product_car(self):
        pass

    @abc.abstractmethod
    def product_suv(self):
        pass


class BydFactory(AbstractFactory):
    def __str__(self):
        return "BYD工厂"

    def product_car(self):
        return BYD()

    def product_suv(self):
        return BYD_SUV()


class BmwFactory(AbstractFactory):
    def __str__(self):
        return "BMW工厂"

    def product_car(self):
        return BMW()

    def product_suv(self):
        return BMW_SUV()


if __name__ == "__main__":
    byd_factory = BydFactory()
    print(byd_factory.product_car())
    print(byd_factory.product_suv())

    bmw_factory = BmwFactory()
    print(bmw_factory.product_car())
    print(bmw_factory.product_suv())
```
注解：
- 抽象工厂和工厂方法的区别，就是工厂方法的基础上扩展对多个产品的支持，让工厂类能够生产同一类的多个产品；

## The builder Pattern 建造者模式（控制复杂对象创建问题）
- 目的：创建一个复杂的对象（对象由多个部分构成，且对象的创建要经过多个不同的步骤，步骤还经过特定的顺序）
- 本质：对象的构造与表现解耦

```python
# -*- coding: utf-8 -*-
import uuid


class Computer:
    def __init__(self, serial):
        self.serial = serial

        self.cpu = None
        self.mem = None
        self.disk = None
        self.system = None

    def __str__(self):
        computer_info = f"Serial: {self.serial}, Cpu: {self.cpu}, Mem: {self.mem}, " \
                        f"Disk: {self.disk}, System: {self.system}."
        return computer_info


class ComputerBuilder:
    def __init__(self):
        random_uuid = uuid.uuid1()
        self.computer = Computer(random_uuid)

    def set_cpu(self, cpu_info):
        self.computer.cpu = cpu_info

    def set_mem(self, mem_info):
        self.computer.mem = mem_info

    def set_disk(self, disk_info):
        self.computer.disk = disk_info

    def set_system(self, system_info):
        self.computer.system = system_info


class HardwareEngineer:
    def __init__(self):
        self.builder = None

    def construct_builder(self, cpu_info, mem_info, disk_info, system_info):
        self.builder = ComputerBuilder()
        construct_step = (self.builder.set_cpu(cpu_info),
                          self.builder.set_mem(mem_info),
                          self.builder.set_disk(disk_info),
                          self.builder.set_system(system_info))
        [step for step in construct_step]

    @property
    def computer(self):
        print(self.builder.computer)


if __name__ == "__main__":
    computer_info = ("Intel xen", "8 GB", "128GB SSD", "Linux 2.4")
    enginner = HardwareEngineer()
    enginner.construct_builder(*computer_info)
    enginner.computer
```
> 注解：
- Computer是创建对象，ComputerBuilder是建造者，HardwareEngineer则是指挥调度者，电脑需要按照顺序
一步一步的安装，最后完成电脑对象的创建。
- 这就符合了创建一个复杂的对象（需要一步一步按照顺序，创建多个部分，然后组成一个对象）

## The Prototype Pattern 原型模式（用于拷贝复杂对象）
- 目的：生成复杂对象的副本
- 本质：简化对象的创建，降低资源的消耗

```python
# -*- coding: utf-8 -*-

from collections import OrderedDict
import copy


class Book:
    def __init__(self, name, authors, price, **rest):
        self.name = name
        self.authors = authors
        self.price = price
        self.__dict__.update(**rest)

    def __str__(self):
        my_list = []
        ordered_list = OrderedDict(sorted(self.__dict__.items()))
        for ordered in ordered_list:
            ord_str = f"{ordered}:{self.__dict__[ordered]}"
            my_list.append(ord_str)
        my_str = " \n".join(my_list)
        return my_str


class Prototype:
    def __init__(self):
        self.objects = {}

    def register(self, identifier, obj):
        self.objects[identifier] = obj

    def unregister(self, identifier):
        del self.objects[identifier]

    def clone(self, identifier, **attr):
        found = self.objects.get(identifier)

        if not found:
            raise ValueError(f"找不到对应{identifier}对象")
        obj = copy.deepcopy(found)
        obj.__dict__.update(**attr)     # 自定义更新属性
        return obj


if __name__ == "__main__":
    b = Book('The C Programming Language', ('Brian W. Kernighan', 'Dennis M.Ritchie'),
             price=118, publisher='Prentice Hall', length=228, publication_date='1978-02-22',
             tags=('C', 'programming', 'algorithms', 'data structures'))
    print(b)
    p = Prototype()
    p.register("b1", b)
    b2 = p.clone("b1", name='The C Programming Language (ANSI)', price=48.99, length=274,
                 publication_date='1988-04-01', edition=2)
    print(b2)
```
> 注解：
- 使用原型模式复制对象，不会调用到类的构造方法，直接从内存中复制数据；
- 如果复制对象会进行修改，则需要进行深拷贝copy.deepcopy，保证不会影响到被拷贝的对象；如果复制对象不进行修改则进行浅拷贝，直接引用对象即可；


## The Singleton Pattern（单例模式）
- 目的： 保证一个类仅有一个实例
- 本质：在创建的类的过程中判断是否已经存在实例，存在即返回
> 类继承
```python
# -*- coding: utf-8 -*-


class Singleton:
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, "_instance"):
            _instance = super().__new__(cls)
            cls._instance = _instance
        return cls._instance


class TestSingleton(Singleton):
    def __init__(self, new_value):
        self._name = new_value

    @property
    def get_name(self):
        return self._name


if __name__ == "__main__":
    a = TestSingleton("lisi")
    b = TestSingleton("zhangsan")
    print(a.get_name)
    print(b.get_name)
    print(a == b)
    print(id(a), id(b))
```

> 装饰器

```python
def Singleton2(class_):
    _instances = {}

    def get_instances(*args, **kwargs):
        if class_ not in _instances:
            _instances[class_] = class_(*args, **kwargs)
        return _instances[class_]
    return get_instances


@Singleton2
class TestSingleton2:
    def __init__(self, new_value):
        self._name = new_value

    @property
    def get_name(self):
        return self._name


if __name__ == "__main__":
    a = TestSingleton2("lisi")
    b = TestSingleton2("zhangsan")
    print(a.get_name)
    print(b.get_name)
    print(a == b)
    print(id(a), id(b))
```
> 备注：
- 调用super().__new__函数，只需传递cls，不然会报错，其余会自动传给构造器函数__init__
