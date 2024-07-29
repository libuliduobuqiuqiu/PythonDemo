## 导语
> 关于Python的异常处理机制一直想总结一下，因为在日常工作场景中，代码的异常处理能够让
开发人员在程序报错的时候及时地定位到Bug的源头，通过分析异常抛出的代码是否存在设计不合理的情况，
所以异常处理是程序不可缺少的一部分。


## 异常
> 关于异常这里首先要分清楚异常和句法错误的区别，句法错误（如：SyntaxError）会在解析器编译过程中无法通过，然后抛出；
而异常则是编译解析通过了，在执行过程可能触发错误。


### 内置异常
> 对于内置的异常我们可能在使用过程中，如Exception：
```python
try:
    print(1/0)
except Exception as e:
    print(e)
```
> 常用的Exception是所有内置的非系统退出类异常的基类，当我们自定义异常时也应该继承此类。

对于常用的基类，查阅了Python的官方文档，这里做做总结，对此我们可以当做扩展，实际使用还是Exception较多：

异常基类     | 描述
---|---
BaseException | 所有内置异常的基类
Exception | 所有内置的非系统退出类异常都派生自此类
ArithmeticError | 此基类用于派生针对各种算术类错误
BufferError | 当与 缓冲区 相关的操作无法执行时将被引发
LookupError | 此基类用于派生当映射或序列所使用的键或索引无效时引发的异常

我们仔细看了一下异常基类，可能会发现一个细节就是**Exception基类的描述这里说到所有内置的非系统退出类异常**，<br>
所以不是所有的异常都能给处理Exception的异常代码捕获的，而Python的这些异常是直接继承BaseException：
- SystemExit：退出函数sys.exit()触发；
- KeyboardInterrupt：当按下中断键 (通常为 Control-C 或 Delete) 触发；
- GeneratorExit：当一个 generator 或 coroutine 被关闭时将被引发；

对于更多内置异常的详细信息这里不做过多的赘述，有兴趣可以看看Python的官方文档，这里面还包括了异常的层级结构等：
> https://docs.python.org/zh-cn/3/library/exceptions.html#bltin-exceptions

## 异常处理
这里我们先写一下关于异常处理的伪代码：
```python
try:
    可能抛出异常的语句
except 可能被捕获的异常1 as 变量a:
    打印变量a信息
except 可能被捕获的异常2 as 变量b:
    打印变量b信息
else:
    未发生异常时执行的语句
finally：
    最终的语句
```
接下来我们分析一下改伪代码：
- 如果try中语句抛出异常，依次顺序经常异常1，然后异常2，如果首先被异常1捕获，则程序会恢复成正常的状态，后面except捕获异常2的子句就不会执行了，如果except没有捕获到指定的异常，会执行finally里面的语句，并且将异常一直抛到最上层，如果此时异常还是没有被处理，则解释器会终止程序的运行；
- 如果try中语句不会抛出异常，依次则是执行else中语句，最后执行finally里的语句；

## raise触发异常
> 在使用的异常处理的过程中，经常会遇到手动去触发异常的情况，这里可以使用raise语句强制触发指定的异常：

```python
def calculate_num(num):
    try:
        if num == 0:
            raise Exception("除数不能为0")
        print(10/num)
    except Exception as e:
        print(e)
calculate_num(0)
```
备注：
- 这里示例直接判断传入的参数是否等于0，如果等于0直接抛出异常，然后外层的except语句捕获打印异常信息
- 还有一种用法就是捕获了异常之后，在这一层代码不处理异常可以再except语句中直接raise抛出该异常

## finally使用
> finally子句是try使用过程中必须要执行的操作，经常用来做清理缓存，断开连接，实际场景还可以用作数据库的回滚等操作；

```python
def calculate_num(num):
    try:
        print(num*num)
    except Exception as e:
        raise
    finally:
        print("test finally")
calculate_num(0)
```
备注：
- 示例中就只是简单的在try过程最后打印了"test finally"；

> 但是在实际使用过程中可能会有几个特殊的情况需要注意，这也是日常使用有可能会碰到的：

**1、try语句中触发了某个异常，但是没有except子句捕获处理，此时finally子句会执行后重新触发**
```python
def calculate_num(num):
    try:
        print(num/num)
    except ZeroDivisionError as e:
        print(e)
    finally:
        print("test finally")

calculate_num("test")
```
返回结果：
```shell
>>> calculate_num("test")
test finally
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
  File "<stdin>", line 3, in calculate_num
TypeError: unsupported operand type(s) for /: 'str' and 'str'
```
备注：
- 传入一个字符串到calculate_num函数里，由于类型异常抛出错误；

**2、如果在except、else子句中触发异常，该异常会在finally子句执行完之后重新触发**

**3、如果在finally子句中包含continue、break、reaturn语句，则异常不会重新触发**

**4、如果在try过程中包含continue、break、return语句，则finally会在执行continue、break、return之前执行**
```python
def calculate_num(num):
    a = []
    try:
        a.append(num)
        return a
    finally:
        a.append("test")

a = calculate_num(1000)
print(a)
```
返回结果：
```shell
[1000, 'test']
```
备注：
- 通过这个示例能够很好的验证finally子句的执行情况，列表a在return前有添加了一个"test"字符串

**5、如果finally子句中包含了return语句，则返回值是来自于finally中return的返回值，而不是try子句中的return返回值**
```python
def bool_return():
    try:
        return False
    finally:
        return True

a = bool_return()
print(a)
```
返回结果：
```shell
True
```

## 自定义异常
> 基本上自定义异常都应该派生于Exception异常类

```python
class AuthenticateError(Exception):
    def __init__(self, username):
        self.username = username

    def __str__(self):
        return f"{self.username}权限不足，无法访问."


def login(username):
    try:
        if username not in ["root", "admin"]:
            raise AuthenticateError(username)
    except Exception as e:
        print(str(e))

login("zhangsan")
```
执行结果：
```shell
zhangsan权限不足，无法访问.
```
备注：
- 设置__str__方法，可以让except捕获返回的详细错误信息；

## 总结
> 有关Python的异常处理可以参考Python的官方文档，里面详细的介绍了使用的注意事项以及一些特殊情况，对于这部分的内容，主要
是考虑到平时使用过程中的使用频率，以及使用中会遇到的一些问题，所以会将此部分内容做一个总结性的文章，如果具体有什么问题可以提出一起讨论。

## 备注
- Python错误信息堆栈处理，打印详细的异常信息
```python
import traceback

traceback.print_exc()
```

参考：
> https://docs.python.org/zh-cn/3/tutorial/errors.html#user-defined-exceptions


表明一个异常是另外一个异常的直接后果，可以直接使用raise...from
```python
class Person:
    name = "zhansan"
    age = 12

    def hello(self):
        raise RuntimeError("hello function is error.")


def person_hello():
    a = Person()

    try:
        a.hello()
    except RuntimeError as err:
        raise ConnectionError("test connection error.") from err


if __name__ == "__main__":
    person_hello()
```

禁用异常链：raise...from None
```python
class Person:
    name = "zhansan"
    age = 12

    def hello(self):
        raise RuntimeError("hello function is error.")


def person_hello():
    a = Person()

    try:
        a.hello()
    except RuntimeError as err:
        raise ConnectionError("test connection error.") from None


if __name__ == "__main__":
    person_hello()
```

