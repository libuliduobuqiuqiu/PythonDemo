# -*- coding: utf-8 -*-
# 代理模式


class LazyProperty:
    """ 用描述符实现延迟加载的属性 """
    def __init__(self, method):
        self.method = method
        self.method_name = method.__name__
        print(self.method, self.method_name)

    def __get__(self, obj, cls):
        if not obj:
            return None
        value = self.method(obj)
        print('value {}'.format(value))
        setattr(obj, self.method_name, value)
        return value


class Test:
    def __init__(self):
        self.x = 'foo'
        self.y = 'bar'
        self._resource = None

    @LazyProperty
    def resource(self):    # 构造函数里没有初始化，第一次访问才会被调用
        print('initializing self._resource which is: {}'.format(self._resource))
        self._resource = tuple(range(5))    # 模拟一个耗时计算
        return self._resource


def main():
    t = Test()
    print(t.x)
    print(t.y)
    # 访问LazyProperty, resource里的print语句只执行一次，实现了延迟加载和一次执行
    print(t.resource)
    print(t.resource)


main()


