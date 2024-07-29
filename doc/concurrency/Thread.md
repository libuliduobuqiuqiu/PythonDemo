## 线程锁
一个线程获得一个锁后，会阻塞尝试获取该锁的对象，直到它被释放，任何线程都可以释放它

```python
# -*- coding: utf-8 -*-
from threading import Lock
from concurrent.futures import ThreadPoolExecutor

num = 100
lock = Lock()

def addition():
    global num
    lock.acquire()
    num += 1
    num -= 1
    lock.release()
    
if __name__ == "__main__":
    with ThreadPoolExecutor(4) as executor:
        for i in range(100):
            executor.submit(addition)
    print(num)
```
备注：
- acquire(blocking=True, timeout=-1),blocking默认为True，指的时当调用该方法时将会阻塞其他线程获取该对象，直到
该锁对象被释放，False则不会阻塞；
- release()该方法释放指定的锁对象，可以在任何线程中调用，不单指的时获取该锁的线程；

```python
# -*- coding: utf-8 -*-

from concurrent.futures import ThreadPoolExecutor
from threading import Lock
import time


class TestLock:
    def __init__(self, name):
        self.name = name
        self.lock = Lock()

    def hello(self):
        with self.lock:
            print(f"hello, {self.name}")
            time.sleep(10)


if __name__ == "__main__":
    t_lock = TestLock("linshukai")
    t_lock2 = TestLock("zhangsan")
    with ThreadPoolExecutor(4) as executor:
        executor.submit(t_lock.hello)
        executor.submit(t_lock2.hello)
```
备注：
- 因为Lock对象实现了__enter__和__exit__方法，可以直接通过with语句进行上下文管理式加锁和解锁，省去了手动获取和手动释放，同时也可以更好的预防死锁的产生
