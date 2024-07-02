Concurrency.md
并发编程
思考Python解释器、线程、进程、GIL之间的关系？如何理清之间的互相影响？

### 进程、线程、协程

进程（Process）
> 操作系统独立的执行单元，独立的内存空间和系统资源；（Python中可以使用multiprocessing模块进行管理）

线程（Thread）
> 线程是同一进程内共享内存空间的轻量执行单元；（Python中可以使用threading模块进行管理）

协程（Coroutine）
> 协程是一种轻量级的并发执行单元，可以由用户自己控制，在执行过程中暂停、恢复和传递数据；（asyncio）
协程使用`async`和`await`关键字定义，通过实践循环管理和调度；

GIL（Global Interpretor Lock）
> GIL是在CPython解释器中存在额一个机制，确保任何时刻只有一个线程执行Python字节码。
GIL的设计初衷就是为了保护Python解释器内部的数据结构，防止多线程环境下发生数据竞争和不一致性；

GIL和进程、线程、协程的关系：
- GIL和进程：由于每个进程都有独立的Python解释器和独立的GIL，并发执行不会受到限制，所以多进程之间可以充分用多核心处理器；
- GIL和线程：由于同一个进程内，只允许一个线程获取GIL，确保了多线程并发执行时，只有一个线程在执行字节码，所以各个线程无法充分利用多核处理器；
- GIL和协程：多个协程可以在单个线程实现并发，避免多线程之间的锁竞争和线程切换的开销。由于线程受到GIL影响，协程也间接无法充分用多核心；

其中名词介绍（参考chatgpt）

#### 字节码(Bytecode)
> 字节码是一种中间代码，它是源代码编译后的一种低级表示形式。Python解释器不直接执行源代码，而是首先将源代码编译成字节码，然后在运行时解释执行这些字节码。这个字节码是一种与平台无关的二进制代码，可以在不同的操作系统上运行。

#### 解释器（Interpreter)
> 解释器是执行字节码的程序，它负责将源代码翻译成可执行的指令。在Python中，CPython是官方的解释器，它执行Python程序。其他还有一些使用不同实现的解释器，如Jython（Java平台上的Python解释器）、IronPython（.NET平台上的Python解释器）等。

#### 全局解释器锁（Global Interpreter Lock，GIL）
> GIL是CPython解释器中的一种锁，它确保在任何时刻只有一个线程能够执行Python字节码。这是为了保护Python解释器内部的数据结构，防止多线程之间的数据竞争导致不一致性。由于GIL的存在，多线程在执行CPU密集型任务时无法充分利用多核处理器。

关于动态语言（Python）
- 代码是在运行时被解释执行
- 动态类型系统，变量类型运行时确定
- 提供高级抽象和灵活

关于静态语言（Go）
- 源代码在编译时被翻译成机器码
- 静态类型系统、变量类型在编译时确定
- 注重性能和编译时的类型检查

### 协程

事件循环、Coroutine、await、Task、

await接收的三种类型对象 ：
Coroutine、Task、Future

为什么await一个 Coroutine的时候会完整等待，而await一个task的时候，是将task注册到Event Loop中 ，然后event loop进行调度？



### 判断线程是否启动

> 启动一个线程，但是想知道是否真的已经开始运行，可以通过threading.Event对象，在主线程中被等待触发，其他线程中设置已触发；

```python
def count_down(n, start_event):
    print("counting down start....")

    while n >0:
        print("T-minus: ", n)
        n -= 1
        time.sleep(5)
    start_event.set()


if __name__ == "__main__":
    event = Event()
    t = Thread(target=count_down, args=(5, event))
    t.start()

    event.wait()
    print("count down end....")
```

### 线程间的通信

> 程序中存在多个线程，需要这些线程之间安全的交换信息或数据

```python
from threading import Thread
from queue import Queue
import time


_senti = object()

def producer(data: list, deque: Queue):
    for item in data:
        print("Producer: ", item)
        deque.put(item)
        time.sleep(2)

    deque.put(_senti)

def consumer(deque:Queue):
    while True:
        item = deque.get()

        if item is _senti:
            break

        print("Consumer: ", item)
        deque.task_done()


if __name__ == "__main__":
    print("starting....")
    deq = Queue()
    c_data = ["zhangdan", "Guangdong", "China", 222, 20310203, "ifconfig", "netstat -tualnp", "hello,world"]

    p = Thread(target=producer, args=(c_data, deq))
    c = Thread(target=consumer, args=(deq,))

    p.start()
    c.start()

    p.join()
    c.join()
    print("end....")
```
备注：
- 使用task_done方法的目的是告诉deque队列，一个任务已经被处理，保证消费者线程和生产者线程能够正常协同工作，避免出现死锁等其他情况
- 一般Queue队列是通过task_done和join()来作为线程同步的一种机制，task_done能够确认队列中的任务正常处理，join则是能够阻塞当前线程，直到队列中的所有任务都被成功处理；


### 保存线程状态信息
> 可以通过threading.local创建一个本地线程的存储对象，对这个存储对象的操作只有在当前线程才能看见，其他线程看不见

```python
from socket import AF_INET, SOCK_STREAM, socket
from functools import partial
from threading import Thread
import threading


class LazyConnection:

    def __init__(self, address, family=AF_INET, sock_type=SOCK_STREAM):
        self.address = address
        self.family = family
        self.sock_type = sock_type
        self._local = threading.local()

    def __enter__(self):
        if hasattr(self._local, "sock"):
            raise RuntimeError("Already connected.")

        self._local.sock = socket(self.family, self.sock_type)
        self._local.sock.connect(self.address)
        return self._local.sock

    def __exit__(self, exc_ty, exc_val, tb):
        if hasattr(self._local, "sock"):
            self._local.sock.close()
            del self._local.sock

def test(conn):
    with conn as s:
        s.send(b'GET /index.html HTTP/1.0\r\n')
        s.send(b'Host: www.python.org\r\n')

        s.send(b'\r\n')
        resp = b''.join(iter(partial(s.recv, 8192), b''))

    print('Got {} bytes'.format(len(resp)))


if __name__ == "__main__":
    conn = LazyConnection(('www.python.org', 80))

    t1 = Thread(target=test, args=(conn,))
    t2 = Thread(target=test, args=(conn,))

    t1.start()
    t2.start()
    t1.join()
    t2.join()
```


### 创建一个线程池

> 创建一个工作者线程池，用来响应客户端的请求或者执行其他的工作


TCP服务器
```python
from concurrent.futures import ThreadPoolExecutor
from socket import AF_INET, SOCK_STREAM, socket


def echo_client(sock, client_address):
    print("Got Connection ", client_address)

    while True:

        msg = sock.recv(65535)
        if not msg:
            break
        sock.sendall(msg)

    print("Close Connection ", client_address)
    sock.close()


def echo_server(address):
    pool = ThreadPoolExecutor(128)

    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(address)
    print('Server Listening.....')
    sock.listen(5)

    while True:
        client_sock, client_address = sock.accept()
        pool.submit(echo_client, client_sock, client_address)


if __name__ == "__main__":
    echo_server(("", 8992))

```



### 实现消息发布/订阅模型
基于一个线程通信的程序，实现发布/订阅模式的消息通信
```python
from collections import defaultdict


class Exchange:
    def __init__(self):
        self._subscribers = set()

    def attach(self, subscriber):
        self._subscribers.add(subscriber)

    def detach(self, subscriber):
        self._subscribers.remove(subscriber)

    def send(self, msg):
        for subscriber in self._subscribers:
            subscriber.send(msg)


ex = defaultdict(Exchange)


def get_exchange(name):
    return ex[name]


class Task:
    def __init__(self, name):
        self._name = name

    def send(self, msg):
        print(f"{self._name} Got {msg}")


if __name__ == "__main__":
    task_a = Task("A")
    task_b = Task("B")

    tmp_ex = get_exchange("name")
    tmp_ex.attach(task_a)
    tmp_ex.attach(task_b)

    tmp_ex.send("hello")
    tmp_ex.send('world')
```
备注：
- 将信息发布到交换机上，然后通过交换机广播信息到订阅者；
