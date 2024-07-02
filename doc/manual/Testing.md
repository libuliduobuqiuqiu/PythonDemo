简单的unittest示例
```python
import concurrent.futures
from unittest import TestCase
from concurrent.futures import ThreadPoolExecutor

import unittest
import logging
import threading


class MyTest(TestCase):
    _num = 0

    def setUp(self) -> None:
        self.logger = logging.getLogger(__name__)

    def add(self):
        self._num += 1

    def sub(self):
        self._num -= 1

    def count(self):
        self.add()
        self.sub()
        self.logger.info(self._num)
        self.logger.info(f"活跃的线程:{threading.active_count()}")

    def test_correct_num(self):
        with ThreadPoolExecutor(128) as pool:
            all_task = [pool.submit(self.count) for _ in range(200)]

        concurrent.futures.wait(all_task)
        self.assertEquals(self._num, 0)


if __name__ == "__main__":
    unittest.main()
```


性能测试

性能测试需要根据业务需求，以及实际业务场景，区分测试的粒度定制性能测试的途径：
- Unix的time函数，打印执行该Python脚本的实际耗时；
- cProfile：打印程序的各个细节的详细报告；
- 自定义时间统计的装饰器函数：测试函数或者方法的具体耗时；
- 自定义部分代码耗时统计

装饰器测试函数性能
```python
from functools import wraps
import time

def time_count(func):
    @wraps(func)
    def count(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        end = time.perf_counter()
        print(f"{func.__module__}.{func.__name__}: {end - start}")
        return result

    return count


@time_count
def hello_world():
    print("hello")
    time.sleep(2)
    print("world")
```

