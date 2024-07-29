## 导语
> 日常开发中，定位程序异常，追溯事件发生场景都需要通过日志记录的方式。可以说一个好的开发日志设计可以让开发人员在后续项目维护的过程中节省时间成本，提升解决问题的效率。  
目前在网上已经有许多关于Python日志操作的文章，部分文章总结的非常到位，Python官方也有日志常用的手册。自己写这篇文章是主要围绕Python官方的logging模块展开，结合自己学习过程以及项目开发中应用场景，总结归纳下Python日志使用，方便自己梳理相关知识，更好的理解；

## 关于开发日志
> 对于开发日志，很多程序员误区可能就是停留在直接print打印到后台日志中，好的地方方便快捷，但是坏的地方就是日志输出的内容十分混乱，不方便排查。面对不同级别的事件，以及需要执行的任务时，采取的日志操作动作是不一样的。

**对此结合Python官方文档总结以下执行任务对应的工具：**
需要执行的任务| 任务对应的工具
---|---
直接打印程序结果 | print
记录程序普通操作（比如请求记录，状态监控） | logging.info()
程序发生特殊事件引发的警告信息 | logging.warning()
程序发生特殊事件引发错误 | 直接抛出异常（raise Exception)
报告错误而不引发异常 | logging.error()、logging.exception()、logging.critical() 分别使用特定错误


**日志功能事件级别对应应用场景（以严重性递增）**

级别 | 应用场景
---|---
DEBUG | 细节信息，仅当诊断问题适用 
INFO | 确认程序预期运行，记录程序正常运行状态
WARNING | 表明有已经或即将发生的意外
ERROR | 由于严重的问题，程序某些功能不能使用
CRTICAL | 严重的错误，程序已不能继续执行

> logging模块默认级别是WARNING，意味着只会追踪该级别以上的事件，除非更改日志配置；

## 关于logging基础使用

日志记录保存到文件
```python
import logging 


logging.basicConfig(filename="example.log", level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S",
                    encoding='utf-8')

# 记录日志信息
logging.debug("test DEBUG")
logging.info("test Info")
logging.warning("test Warning")
logging.warning('%s before you %s', 'Look', 'leap!')
logging.error("test Error")
```
代码注解：
- 3.9版本中才更新了encoding，encoding参数在更早的Python版本中没有指定时，编码会使用open()的默认值；
- level是设置默认日志追踪级别的阈值，默认级别是WARNING
- filename是日志文件的存放路径；
(上述脚本如果连续多次运行，连续运行的消息将追缴到指定的example.log日志文件，如果想每次都是重新开始，即example.log日志不保存之前的日志信息，则修改filemode参数为'w'；)


## 关于logging进阶使用

> 结合Python官方文档，日志库采用模块化的方法，并提供几类组件：记录器、处理器、过滤器和格式器。
- 记录器：暴露了应用程序代码直接使用的接口。
- 处理器：将日志记录（由记录器创建）发送到适当的目标。
- 过滤器：提供了更细粒度的功能，用于确定要输出的日志记录。
- 格式器：指定最终输出中日志记录的样式。

官方文档中记录器和处理在日志信息记录流程：
![image](https://docs.python.org/zh-cn/3/_images/logging_flow.png)

解析：
- 首先是判断Logger对象执行的方法是否大于设置的最低严重性，大于则创建LogRecord对象，小于则终止；
- 注册的Filter对象进行过滤，如果为False不记录日志；
- 将LogRecord对象传递到当前注册到Logger对象中的Handler对象；判断Handler对象设置的级别大于Logger对象则证明有效，以及注册到Handler对象中Filter过滤后是否返回True；
- 最后判断当前是否还有父Logger对象，如果是重复第三步，知道当前Logger设置为root Looger；

### 记录器
关于记录器，主要的任务总结有三个：
- 暴露接口给应用程序记录消息；
- 根据严重性（默认严重级别）或者过滤器决定要处理的日志信息；
- 将日志信息发送传递给对应日志处理器；

> 关于记录器方法总结为两类，配置和消息发送.

记录器配置方法：
- Logger.setLevel()：设置记录器处理的最低严重性日志信息（这就如果后续日志处理器设置的日志级别比记录器低是无效的）；
- Logger.addHandler()和Logger.removeHandler()：从记录器对象中增加和删除日志处理器对象；
- Logger.addFilter()和Logger.removeFilter()：从记录器对象中增加和删除过滤器；

记录器常用创建信息方法：
- Logger.debug() 、 Logger.info() 、 Logger.warning() 、 Logger.error() 和 Logger.critical() ；
- Logger.exception()和以上的方法有点不同，只在异常处理程序中调用此方法，同时还记录当前堆栈跟踪信息；

### 处理器
关于处理器，简单的可以理解为将特定严重级别的日志信息发送到特定的位置，常用的处理类型主要有两个：
- FileHandler
- StreamHandler

由于内置处理对象常用的配置方法：
- setLevel()方法，设置处理器中的最低严重性，即决定处理器该发送哪些级别的日志信息；
- addFormatter，选择该处理器使用的Formatter对象；
- addFilter和removeFilter，在处理器上增加和删除过滤器对象；

### 格式器
格式器配置日志消息的最终顺序、结构和内容，格式器类的构造函数有三个可选参数：
- 消息格式字符串
- 日期格式字符串
- 样式指示符

```python
logging.Formatter.__init__(fmt=None, datefmt=None, style='%')
```
备注：
- fmt消息格式字符串一般不为空，为空默认就只打印message信息；
- datefmt默认日期格式为：%Y-%m-%d %H:%M:%S；
- style参数可选的范围为：%、{、$这三个，主要用于fmt消息中字符串替换；

关于style：
```python
fm = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s",
                   "%Y-%m-%d %H:%M:%S", style='{')
                   
fm = Formatter("{asctime} - {name} - {levelname} - {message}",
                   "%Y-%m-%d %H:%M:%S", style='{')

fm = Formatter("$asctime - $name - $levelname - $message",
                   "%Y-%m-%d %H:%M:%S", style='$')
```
(这三种style使用方式，效果都一样)

### 配置记录
开发人员可以通过三种方式配置日志记录：
1. 使用提供的接口，显示创建记录器，处理器，格式器等直接配置；
2. 通过fileConfig()函数读取已经创建好的配置文件；
3. 创建好配置函数字典传递到dictConfig()函数；

关于fileConfig()读取的配置文件(官方示例）：
```
[loggers]
keys=root,simpleExample

[handlers]
keys=consoleHandler

[formatters]
keys=simpleFormatter

[logger_root]
level=DEBUG
handlers=consoleHandler

[logger_simpleExample]
level=DEBUG
handlers=consoleHandler
qualname=simpleExample
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=simpleFormatter
args=(sys.stdout,)

[formatter_simpleFormatter]
format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
```
（关于读取的配置文件格式类似ini格式）

## 实战
> 关于logging模块，这里介绍一下我目前最常用的业务场景：调用方请求一个后端的rest api接口，我需要记录**调用方请求的时间，地址，请求参数，处理请求后的结果**，以及我需要将报错的信息保存到指定的文件里，方便排查。    
  为了后期使用方便，在不更改原有处理函数的基础下增加日志记录的功能，我会选择将日志记录操作封装在一个装饰器函数。  
  所以我只需将这部分功能分成两部分：生成记录器、请求处理的装饰器函数

### 生成记录器
```python
# -*- coding: utf-8 -*-

from logging import handlers
from datetime import date
import logging


def init_logger():
    """
    生成记录器
    :return:
    """
    app_logger = logging.getLogger(APP_NAME)
    app_logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s %(levelname)s: %(message)s", "%Y-%m-%d %H:%M:%S")

    # 正常日志打印到控制台
    console = logging.StreamHandler()
    console.setFormatter(fmt)
    console.setLevel(logging.INFO)

    # 异常日志记录到log文件
    today = date.today()
    file_name = "logs/exceptions_" + str(today) + ".log"
    fh = handlers.TimedRotatingFileHandler(filename=file_name, when='D', backupCount=30, encoding='utf-8')
    fh.setLevel("ERROR")
    fh.setFormatter(fmt)

    app_logger.addHandler(console)
    app_logger.addHandler(fh)

    return app_logger
```
代码解析：
- APP_NAME是预设好的项目名称，可根据实际业务进行调整；
- 关于普通的StreamHandler前面已经提到了使用的方法，我这里之所选择，是由于这个项目时Flask框架，后期部署通过uWSGI部署后端服务，我希望正常请求直接就打印在uwsgi的日志文件中，所以普通请求的处理器就选择了StreamHandler
- 关于异常日志处理器，这里用到特殊的TimeRotatingFileHandler，这个内置的处理器可以根据不同的时间跨度进行保存日志，就可以将异常日志信息按照一天的时间进行保存，注意设置最低严重性是ERROR

### 请求处理装饰器
```python
from functools import wraps
from flask import request

app_logger = init_logger()

def rest_log(return_type="dict"):

    def decorator(func):

        @wraps(func)
        def inner(*args, **kwargs):
            # 组装打印的Message消息日志格式（请求URL，目标主机，请求方法，请求参数，响应内容）
            log_params = {
                "request": request.base_url,
                "host": request.host,
                "method": request.method
            }

            req_data = {}
            if request.method == "POST":
                req_data = dict(request.json)

            elif request.method == "GET":
                req_data = dict(request.args)

            log_params.update({"params": req_data})

            # 请求处理函数
            try:
                result = func(*args, **kwargs)

            except Exception as e:
                # 异常信息处理
                err_msg = str(e)
                result = {"ret_code": 500, "ret_info": err_msg}
                app_logger.error(log_params, exc_info=True)

                if return_type == "tuple":
                    result = (result, 500)

            if return_type == "tuple":
                log_params['result'] = result[0].data
            else:
                log_params['result'] = result

            app_logger.info(log_params)
            return result
        return inner
    return decorator
```
代码解析：
- 主要分为三部分：HTTP请求request解析、异常请求信息处理、请求结果处理；
- app_logger.error(log_params, exc_info=True)中的exc_info可以将异常信息添加到日志信息中，即app_logger.exception()的效果；
- 关于return_type参数是考虑到flask支持返回元组，即返回相应对象，响应状态码。考虑到日常使用场景会出现这种情况；


简单使用示例：
```python
# -*- coding: utf-8 -*-

from flask import request, Blueprint
from common.LogUtils import rest_log

test_api = Blueprint("TestApi", __name__)

@test_api.route("/log/test", methods=["GET"])
@rest_log()
def test_log():
    name = request.args.get("name", "")
    number = request.args.get('number', "")

    if not name or not number:
        raise Exception("number和name参数都不能为空")

    response = {
        "data": {
            "name": f"Hello, {name}",
            "number": number
        },
        "ret_code": 200,
        "ret_info": "success"
    }
    return response
```
备注：
- rest_log装饰器不能放在test_api.route的前面，因为只有当路由注册函数执行后，才能从request中获取到对应的信息（base_url,host,method)

控制台日志打印效果：
```shell
2022-05-22 12:01:01 INFO: {'request': 'http://127.0.0.1:23102/log/test', 'host': '1
