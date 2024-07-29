## 协程
### 协程是什么？
> 协程简单来说就是一个更加轻量级的线程（用户态线程），并且不由操作系统内核管理，完全由程序所控制（在用户态执行）。协程在子程序内部是可中断的，然后转而执行其他子程序，在适当的时候返回过来继续执行。

### 协程的优势？
> 协程拥有自己的寄存器上下文和栈，调度切换时，寄存器上下文和栈保存到其他地方，在切换回来的时候，恢复先前保存的寄存器上下文和栈，直接操作栈则基本没有内核切换的开销，可以不加锁的访问全局变量，所以上下文非常快。

## yield关键字
1. 协程中的yield通常出现在表达式的右边, 如果yield的右边没有表达式，默认产出的值是None，现在右边有表达式，所以返回的是data这个值。
```python
x = yield data
```
2. 协程可以从调用法接受数据，调用通过send(x)方式将数据提供给协程，同时send方法中包含next方法，所以程序会继续执行。
3. 协程可以中断执行，去执行另外的协程。

**代码示例：**
```python
def hello():
    data = "mima"
    while True:
        x = yield data  
        print(x)
a = hello()
next(a)
data = a.send("hello")
print(data)
```

**代码详解：**
- 程序开始执行，函数hello不会真的执行，而是返回一个生成器给a。
- 当调用到next()方法时，hello函数才开始真正执行，执行print方法，继续进入while循环；
- 程序遇到yield关键字，程序再次中断，此时执行到a.send("hello")时，程序会从yield关键字继续向下执行，然后又再次进入while循环，再次遇到yield关键字，程序再次中断；

**协程运行状态：**
- GEN_CREATE:等待开始执行
- GEN_RUNNING:解释器正在执行
- GEN_SUSPENDED:在yield表达式处暂停
- GEN_CLOSED:执行结束

### 生产者-消费者模式（协程）
```python
import time

def consumer():
    r = ""
    while True:
        res = yield r
        if not res:
            print("Starting.....")
            return
        print("[CONSUMER] Consuming %s...." %res)
        time.sleep(1)
        r = "200 OK"

def produce(c):
    next(c)
    n = 0
    while n<6:
        n+=1
        print("[PRODUCER] Producing %s ...."%n)
        r = c.send(n)
        print("[CONSUMER] Consumer return: %s ...."%r)
    c.close()

c = consumer()
produce(c)     
```

代码详解：
- 调用next(c)启动生成器；
- 消费者一旦生产东西，通过c.send切换到消费者consumer执行；
- consumer通过yield关键字获取到消息，在通过yield把结果执行；
- 生产者拿到消费者处理过的结果，继续生成下一条消息；
- 当跳出循环后，生产者不生产了，通过close关闭消费者，整个过程结束；

## gevent第三方库协程支持
**使用原理：**
> gevent基于协程的Python网络库，当一个greenlet遇到IO操作（访问网络）自动切换到其他的greenlet等到IO操作完成后，在适当的时候切换回来继续执行。
>换而言之就是greenlet通过帮我们自动切换协程，保证有greenlet在运行，而不是一直等待IO操作。

### 经典代码
由于切换时在发生IO操作时自动完成，所以gevent需要修改Python内置库，这里可以打上猴子补丁（用来在运行时动态修改已有的代码，而不需要原有的代码）
```python
#!/usr/bin/python2
# coding=utf8

from gevent import monkey
monkey.patch_all()

import gevent
import requests


def handle_html(url):
    print("Starting %s。。。。" % url)
    response = requests.get(url)
    code = response.status_code

    print("%s: %s" % (url, str(code)))


if __name__ == "__main__":
    urls = ["https://www.baidu.com", "https://www.douban.com", "https://www.qq.com"]
    jobs = [ gevent.spawn(handle_html, url) for url in urls ]

    gevent.joinall(jobs)
```
代码详解：
- 先打上猴子补丁（monkey.patch_all）；
- 示例中模拟并发请求多个网址的情况，普通情况将会串行访问；

## asyncio内置库协程支持
**使用原理:**
> asyncio的编程模型就是一个消息循环，从asyncio模块中直接获取一个Eventloop（事件循环）的应用，然后把需要执行的协程放入EventLoop中执行，实现异步IO。

**代码示例：**
```python
import asyncio
import threading

async def hello():
    print("hello, world: %s"%threading.currentThread())
    await asyncio.sleep(1) # 
    print('hello, man %s'%threading.currentThread())

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([hello(), hello()]))
    loop.close()
```

**代码解析：**
- 首先获取一个EventLoop
- 然后将这个hello的协程放进EventLoop，运行EventLoop，它会运行知道future被完成
- hello协程内部执行await asyncio.sleep(1)模拟耗时1秒的IO操作，在此期间，主线程并未等待，而是去执行EventLoop中的其他线程，实现并发执行。

代码结果：


### 异步爬虫实例
```python
#!/usr/bin/python3

import aiohttp
import asyncio

async def fetch(url, session):
    print("starting: %s" % url)
    async with session.get(url) as response:
        print("%s : %s" % (url,response.status))
        return await response.read()

async def run():
    urls = ["https://www.baidu.com", "https://www.douban.com", "http://www.mi.com"]
    tasks = []
    async with aiohttp.ClientSession() as session:
        tasks = [asyncio.ensure_future(fetch(url, session)) for url in urls] # 创建任务
        response = await asyncio.gather(*tasks) # 并发执行任务

        for body in response:
            print(len(response))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.close()
```

**代码解析：**
- 创建一个事件循环，然后将任务放到时间循环中；
- run()方法中主要是创建任务，并发执行任务，返回读取到的网页内容；
- fetch()方法通过aiohttp发出指定的请求，以及返回 可等待对象；

（结束输出网址和list中网址的顺序不同，证明协程中异步I/O操作）


## 关于aiohttp
> asyncio实现类TCP、UDP、SSL等协议，aiohttp则是基于asyncio实现的HTTP框架，由此可以用来编写一个微型的HTTP服务器。

**代码示例：**
```python
from aiohttp import web

async def index(request):
    await asyncio.sleep(0.5)
    print(request.path)
    return web.Response(body='<h1> Hello, World</h1>')

async def hello(request):
    await asyncio.sleep(0.5)
    text = '<h1>hello, %s</h1>'%request.match_info['name']
    print(request.path)
    return web.Response(body=text.encode('utf-8'))

async def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route("GET", "/" , index)
    app.router.add_route("GET","/hello/{name}", hello)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8000)
    print("Server started at http://127.0.0.0.1:8000....")
    return srv

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
```

**代码解析：**
- 创建一个事件循环，传入到init协程中；
- 创建Application实例，然后添加路由处理指定的请求；
- 通过loop创建TCP服务，最后启动事件循环；

## 参考
> https://www.liaoxuefeng.com/wiki/1016959663602400/1017985577429536
> https://docs.aiohttp.org/en/stable/web_quickstart.html
> https://docs.python.org/zh-cn/3.7/library/asyncio-task.html


## 对比gevent、asyncio、concurrent.futrures

gevent
> Gevent直接修改标准库钟大部分阻塞式系统调用，其中包括socket,ssl,threading,select模块，变为协作式运行，无法保证在复杂的生产环境中这些标准库会因为打了补丁，产生无法预测的问题。

asyncio
> 创建一个事件循环Eventloop，将需要运行的协程对象，注册到事件循环池中，由事件循环调用。

concurrent.futures
> concurrent.futures提供了ThreadPoolExecutor,ProcessPoolExecutor两种并发模型，通过executor对象，提交任务后获取到future对象，最后通过获取future对象的返回结果，future对象是主线程和子线程通信的媒介。

示例：
```python
# -*- coding: utf-8 -*-
from concurrent.futures import ThreadPoolExecutor
import time


def hello(name):
    print(f"Hello, {name}")
    time.sleep(2)

if __name__ == "__main__":
    with ThreadPoolExecutor(4) as executor:
        executor.submit(hello, "zhangsan")
        executor.submit(hello, "lis")
```

剖析源码：
> https://zhuanlan.zhihu.com/p/31544936
