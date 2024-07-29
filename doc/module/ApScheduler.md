## 导语
在工作场景遇到了这么一个场景，就是需要定期去执行一个缓存接口，用于同步设备配置。首先想到的就是Linux上的crontab，可以定期，或者间隔一段时间去执行任务。但是如果你想要把这个定时任务作为一个模块集成到Python项目中，或者想持久化任务，显然crontab不太适用。Python的APScheduler模块能够很好的解决此类问题，所以专门写这篇文章，从简单入门开始记录关于APScheduler最基础的使用场景，以及解决持久化任务的问题，最后结合其他框架深层次定制定时任务模块这几个点入手。

## 简单介绍
先简单介绍一下Apscheduler模块包含的四种组件：
- Trigger触发器
- Job作业
- Excutor执行器
- Scheduler调度器

大概了解了Apscheduler包含的几种概念，现在先来看一下一个简单的示例：
```python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler
import time


def hello():
    print(time.strftime("%c"))


if __name__ == "__main__":
    scheduler = BlockingScheduler()
    scheduler.add_job(hello, 'interval', seconds=5)
    scheduler.start()
```
示例的输出：
```
Thu Dec  3 16:01:20 2020
Thu Dec  3 16:01:25 2020
Thu Dec  3 16:01:30 2020
Thu Dec  3 16:01:35 2020
Thu Dec  3 16:01:40 2020
..........
```
这个简单的示例，我们用上面提到几种组件分析一下运行逻辑：
-首先是Scheduler调度器，这个示例使用的BlockingScheduler调度器，在官方文档中的解释是，BlockingScheduler适合当你的这个定时任务程序是唯一运行的程序；换言之，则是BlockingScheduler调度器是一个阻塞调度器，当程序运行这种调度器，进程则会阻塞，无法执行其他操作；
- 其次是Job作业和触发器，这两个放在一起讲是因为，在定义作业的时候，你就需要选择一个触发器，这里选择的是interval触发器，这种触发器会以固定时间间隔运行作业。换言之，为调度器添加一个hello的工作，并以每5秒的时间间隔执行任务。
- 最后就是执行器，默认是ThreadPoolExcutor执行器，他们将任务中可调用对象交给线程池执行操作，等完成操作后，执行器会通知调度程序。

内置的三种Trigger触发器类型：
- date:特定时间仅运行一次作业
- interval: 固定的时间间隔内运行一次作业
- cron: 在一天内特定的时间定期运行作业

常见的Scheduler调度器:
- BlockingScheduler: 调度程序是流程中唯一运行的东西
- BackgroundScheduler: 调度程序在应用程序内部的后台运行时使用
- AsyncIOScheduler: 应用程序使用asyncio模块
- GeventScheduler: 应用程序使用gevent模块
- TornadoScheduler：构建Tornado应用程序时使用
- TwistedScheduler: 构建Tornado应用程序时使用
- QtScheduler: 在构建QT应用程序时使用

常见的JobStore：
- MemoryJobStore
- MongoDBJobStore
- SQLAlchemyJobStore
- RedisJobStore

## 进阶使用
通过上面一个简单的示例了解大概的工作流程，以及各个组件在整个流程中的作用，以下的示例是Flask Web框架结合使用Apscheduler定时器，定时执行任务。

```python
# -*- coding: utf-8 -*-

from flask import Flask, Blueprint, request
from apscheduler.executors.pool import ThreadPoolExecutor 
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
import time

app = Flask(__name__)
executors = {"default": ThreadPoolExecutor(5)}
default_redis_jobstore = RedisJobStore(db=2, 
        jobs_key="apschedulers.default_jobs",
        run_times_key="apschedulers.default_run_times",
        host = '127.0.0.1',
        port = 6379
        )

scheduler = BackgroundScheduler(executors=executors)
scheduler.add_jobstore(default_redis_jobstore)
scheduler.start()

def say_hello():
    print(time.strftime("%c"))


@app.route("/get_job", methods=['GET'])
def get_job():
    if scheduler.get_job("say_hello_test"):
        return "YES"
    else:
        return "NO"

@app.route("/start_job", methods=["GET"])
def start_job():
    if not scheduler.get_job("say_hello_test"):
        scheduler.add_job(say_hello, "interval", seconds=5, id="say_hello_test")
        return "Start Scuessfully!"
    else:
        return "Started Failed"
   
@app.route("/remove_job", methods=["GET"])
def remove_job():
    if scheduler.get_job("say_hello_test"):
        scheduler.remove_job("say_hello_test")
        return "Delete Successfully!"
    else:
        return "Delete Failed"


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8787, debug=True)
```
- 先分析Jobstore，这里使用的是RedisJobstore，将任务序列化存入到Redis数据库中。这里顺便提一下，为什么需要设置作业存储器，原因是当调度器程序崩溃时，仍然能够保留作业，当然选择什么作业存储器，可以根据具体的工作场景，目前主流的mysql，mongodb，redis，SQLite基本都支持;
- 然后再看看Scheduler，这里使用的时BackgroundScheduler，因为这里要求调度程序不能阻塞flask程序的正常接收请求，所以选在BackgrounScheduler让它在开始执行任务时是在后台运行的，不会阻塞主线程;
- 最后看看工作的逻辑，这里get_job获取作业的状态，查看作业是否存在，start_job则是先判断作业是否启动，然后再决定启动操作，remove_job则是停止作业。而这里的作业定义则是通过interval触发器，每五秒执行一次say_hello任务；

## 总结
最后总结一下，首先你要设置一个作业存储器用于在调度程序崩溃重新恢复时，还能够在作业存储器中获取到作业继续执行；然后你需要设置一个执行器，这个根据作业的类型，比如时一个CPU密集型的任务，那就可以用进程池执行器，默认是用线程池执行器；最后创建配置调度器，启动调度，可以在启动前添加作业，也可以在启动后添加，删除，获取作业。(在这里需要明白的一点就是应用程序不会直接去操作作业存储器，作业或者执行器，而是调度器提供适当的接口来处理这些接口。)
<br/>ApScheduler是一个不错的定时任务库，能够动态的添加删除，同时也支持不同的触发器类型，这也是它的优势，相反一些如果是静态任务，其实可以用如linux的crontab工具去做定时任务。有关这方面的记录还会持续更新，如果有什么问题，可以提出来，大家一起探讨。
