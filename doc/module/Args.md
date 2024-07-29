## sys.argv,argparse,click（命令行参数）

>Python作为一门脚本语言，经常作为脚本接受命令行传入参数，Python接受命令行参数大概有三种方式。因为在日常工作场景会经常使用到，这里对这几种方式进行总结。

## 命令行参数模块
这里命令行参数模块平时工作中用到最多就是这三种模块：sys.argv,argparse,click。sys.argv和argparse都是内置模块，click则是第三方模块。

### sys.argv模块（内置模块）
先看一个简单的示例：

```python
#!/usr/bin/python
import sys

def hello(name, age, sex, *args):
    print("Hello, My name is {name}.".format(name=name))
    print("I'm {age} years old.".format(age=age))
    print("I'm a {sex}".format(sex=sex))

    print("Other word:\n{args}".format(args="\n".join(args)))


if __name__ == "__main__":
    file_name = sys.argv[0]
    name =  sys.argv[1]
    age = sys.argv[2]
    sex = sys.argv[3]
    other = sys.argv[4:]
    hello(name, age, sex, *other)
```
调用脚本：
```bash
python test_sysargv.py zhangsan 13 man nibi ss
```
脚本输出：
```
Hello, My name is zhangsan.
I'm 13 years old.
I'm a man
Other word:
nibi
ss
```
> sys.argv模块不难理解，命令参数作为列表传入Python脚本中，argv[0]是脚本的名字，argv[1]则是第一个参数，后面以此类推。所以在脚本中只需要提取列表中的参数即可使用。上面演示的是正确调用Python脚本的情况，下面则是调用失败的情况。

错误调用脚本：
```bash
python test_sysargv.py zhangsan 13
```
错误输出：
```
Traceback (most recent call last):
  File "test_sysargv.py", line 16, in <module>
    sex = sys.argv[3]
IndexError: list index out of range
```
> 关于错误也很好理解，经典的列表索引超出范围，之所列表索引超出范围，没有传入足够的参数。当然你可以使用try...except捕获错误。但是这种做法太过死板，因为在命令行中必须按照脚本规定的参数顺序输入参数，所以这种模块使用一般是针对一些需要的参数比较少并且固定的脚本。

### argparse模块（内置模块）
同样的先看一个简单的示例：

```python
#!/usr/bin/python
import argparse

parser = argparse.ArgumentParser(description='Test for argparse module.')   # 构建命令参数实例
parser.add_argument("--name", "-n", help="name attribute: 非必要属性")
parser.add_argument("--age", "-a", help="age attribute: 非必要属性")
parser.add_argument("--sex", "-s", help="sex attribute: 非必要属性")
parser.add_argument("--type", "-t", help="type attribute: 非必要属性", required=True)
args = parser.parse_args()


def hello(name, age, sex, *args):
    print("Hello, My name is {name}.".format(name=name))
    print("I'm {age} years old.".format(age=age))
    print("I'm a {sex}".format(sex=sex))

    print("Other word:\n{args}".format(args="\n".join(args)))


if __name__ == "__main__":
    print("Format of transfer file: {type}".format(type=args.type))
    if args.name and args.age and args.sex:
        hello(args.name, args.age, args.sex)
```
执行脚本：
```bash
python3 test_argparse.py -t json -n zhangsan -a 13 -s man
```
脚本成功输出：

```
Format of transfer file: json
Hello, My name is zhangsan.
I'm 13 years old.
I'm a man
Other word:

```
> 关于argparse模块的使用，首先需要生成一个命令行参数的实例，然后通过对这个对象添加属性，添加需要从命令行获取的参数，包括哪些是必要参数（required=True），哪些非必要参数，同时也可以对每个参数进行帮助提示（help=""）。

> 而上面示例中分别添加了四个属性，--name和-n同时可以再命令行中使用，都表示了参数name。ArgumentParser通过parse_ags()方法解析参数，检查命令行，将每个参数转换为适当的类型，所以在脚本中同时也可以使用args.n和args.name获取到参数，相对应的如果没有传入该参数，脚本中则获取到None。

查看命令行参数之后脚本的帮助提示：

```
python3 test_argparse.py -h
usage: test_argparse.py [-h] [--name NAME] [--age AGE] [--sex SEX] --type TYPE

Test for argparse module.

optional arguments:
  -h, --help            show this help message and exit
  --name NAME, -n NAME  name attribute: 非必要属性
  --age AGE, -a AGE     age attribute: 非必要属性
  --sex SEX, -s SEX     sex attribute: 非必要属性
  --type TYPE, -t TYPE  type attribute: 非必要属性
```
> 另外在添加命令行参数的属性中，还有更多的设置，多余的可以参考Python官方文档，里面都有详细的标注，这里就不展开来讲，总结的就是关于argparse模块的使用非常简便，同时十分人性化，也很符合日常工作的需要。

### click模块
先开一个简单的使用示例：
```python
#!/usr/bin/python
import click

@click.command()
@click.option("--name", default="zhangsan", help="name attribute: 非必要属性")
@click.option("--age", help="age attribute", type=int)
@click.option("--sex", help="sex attribute")
@click.option("-t", help="type attribute: 必要属性", required=True)
def hello(t, name, age, sex, *args):
    print("Format of transfer file: {type}".format(type=t))
    print("Hello, My name is {name}.".format(name=name))
    print("I'm {age} years old.".format(age=age))
    print("I'm a {sex}".format(sex=sex))

    print("Other word:\n{args}".format(args="\n".join(args)))


if __name__ == "__main__":
    hello()

```
执行脚本：

```bash
python3 test_click.py -t 1 --age 13 --sex man
```
脚本输出：

```
Format of transfer file: 1
Hello, My name is zhangsan.
I'm 13 years old.
I'm a man
Other word:

```
> click模块是Flask团队优秀的开源项目，使用方法和argparse模块很相似，同样为命令行封装了大量的方法，使用者只需要专注代码功能的实现。<br> click模块和argparse模块不同的地方就是，click模块使用装饰器的方式给函数添加命令行属性，关于装饰器简单来讲就是能够在不修改原有函数的基础上添加功能。虽然使用装饰器但是添加命令行属性的方式和argparse模块很相似，包括options中常用的参数含义也有很多类似的地方。值得注意的就是一开始需要通过command()将函数成为命令行的接口。<br> 关于的click模块的就大致讲到这里，其余有兴趣的可以再去了解一下。

## 总结
关于这三个模块值得注意的是，尽量贴近自己应用场景去选择，真正的做到自己能够方便使用才是你去使用这些模块的原因。
