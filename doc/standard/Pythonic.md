## 变量命名
> 规范的变量命名能够传递更多信息量，降低阅读代码难度，提高代码开发效率；

小写下划线命名(常用于模块、变量、方法、函数定义）：
```
def get_vs_name():
def print_text():
vs_name
user_name
```

大写下划线命名（常用于常量表示）：
```python
MYSQL_URL = ""
MONGODB_URL = ""
DEVICE_TYPE = "F5"
DEVICE_VERSION = "15.1"
```

大写驼峰命名（常用于类的定义）：
```python
class F5SshDriver:
class DevicePlatConnect:
class LogUtil:
```

**下划线：**
- _xxx      "单下划线 " 开始的成员变量叫做保护变量，意思是只有类实例和子类实例能访问到这些变量，需通过类提供的接口进行访问；不能用'from module import *'导入（弱私有，语义上不建议引用，实际上还是能够强制使用）
- __xxx    类中的私有变量/方法名 （Python的函数也是对象，所以成员方法称为成员变量也行得通。）," 双下划线 " 开始的是私有成员，意思是只有类对象自己能访问，连子类对象也不能访问到这个数据。（强私有，除类以外无法引用，实际python内部对这类变量进行了name mangling)
- \_\_xxx\_\_ 系统定义名字，前后均有一个“双下划线” 代表python里特殊方法专用的标识，如 \_\_init\_\_（）代表类的构造函数。
（日常的自定义方法命名不要用）

## 类型注解
> 简单来说，类型注解用来对于函数的变量和返回值的类型做注解，方便代码阅读的，并不是强制。  
如果传入的参数不符合类型注解的要求运行时也能通过的，但是在IDE中一般有对此类型注解的支持。

```python
from typing import Optional

def test_typing(num: int, key: Union[str, int] = None, value: Optional[str] = None):
    result = {
        "num": num,
        "key": key,
        "value": value
    }
    print(json.dumps(result, indent=2))
```
- 使用Union可以检测参数有多种可能使用到的类型，即Union[str, int],
- Optional[x]则是Union[x, None],即能够传入None
- 使用typing的好处就是能通过导入List，Set，Tuple，声明其中类型
```python
from typing import List, Optional

var: Optional[List[str]] = ["sss", "ddd"]
```

# TODO
> 为什么要使用Optional，直接用不行吗？为什么要那么麻烦？

类型注解参考：
> https://www.gairuo.com/p/python-library-typing  
> https://www.python.org/dev/peps/pep-0484/

## 参考
> https://zh-google-styleguide.readthedocs.io/en/latest/google-python-styleguide/python_style_rules/  

腾讯代码安全规范：
> https://github.com/Tencent/secguide/blob/main/Python%E5%AE%89%E5%85%A8%E6%8C%87%E5%8D%97.md
