## 导语
> 由于日常开发场景中经常涉及到关于正则匹配，比如设备采集信息，筛选配置文件，过滤相关网页元素等，所有针对Python中
正则匹配的Re模块，需要总结和梳理的地方挺多。这篇文章主要是归纳平时会经常使用到的一些函数，以及在使用过程中会遇到的坑。

## 正则表达式
正则匹配的使用心得：
- 可以将一大批数据进行预处理，去除掉一些多余的符号，比如换行，如果出现多个空格，可以换成单个空格。
- 在获取数据进行处理时，尽可能获取指定需要的数据，减少其他数据的干扰，同时也能提高传输的效率；
- 可以设置起始符和终结符用于筛选多个子元素

> 关于正则表达式语法，不再赘述，可以参考网上的文档，这里具体不做总结；

## Re模块
re模块是Python用来处理正则表达式匹配操作的模块。

### Re模块常用函数：
> re.search(pattern, string, flags=0)

```python
import re

text= "Hello, World!"
re.search("[A-Z]", text)
```
备注：
- pattern为正则表达式，string为需要匹配的字符串，flags为正则表达式的标志；
- search函数扫描整个字符串找到匹配正则表达式的第一个位置，并且返回相应的匹配对象， 如果没匹配到
则返回None；

> re.match(pattern, string, flags=0)<br>
> re.fullmatch(pattern, string, flags=0)

```python
import re

text="Hello,World"
re.match("[a-z]", text)
re.fullmatch("\S+", text)
```
备注：
- match函数从开头开始匹配正则表达式，如果开头的单个或多个字符匹配到了正则表达式样式，则返回一个匹配对象，
反之，返回None；
- 注意区分match和search，match函数是检查字符串开头，search函数是检查字符串的任意位置；
- fullmatch是如果整个string都匹配到正则表达式，返回一个相应的匹配对象，否则返回一个None；

> re.split(pattern, string, maxsplit=0, flags=0)

```python
import re

text = "aJ33Sjd3231ssfj22323SSdjdSSSDddss"
re.split("([0-9]+)", text)
re.split("[0-9]+", text)
```
备注：
- split函数中使用正则表达式分开string，如果在正则表达式中能检测到括号，则分割的字符串会保留在列表中；
- maxsplit，最大的分割次数，分割完剩下的字符串都会全部返回到列表中最后一个元素；

> re.findall(pattern, string, flags=0)<br>
> re.finditer(pattern, string, flags=0)

```python
import re
text = "aJ33Sjd3231ssfj22323SSdjdSSSDddss"
a = re.findall("[0-9]+", text)
print(a)

b = re.finditer("[0-9]+", text)
for i in b:
    print(i.group())
```
备注：
- findall()函数，string从左往右进行扫描，匹配正则表达式，将所有匹配到的按顺序排列组成列表返回；
- finditer()函数，string从左往右进行扫描，匹配正则表达式，将结果按照顺序排列返回一个迭代器iterator，迭代器中保存了
匹配对象；

> re.sub(pattern, repl, string, count=0, flags=0)
> re.subn(pattern, repl, string, count=0, flags=0)

```python
text = "aJ33Sjd3231ssfj22323SSdjdSSSDddss"
a = re.sub("[0-9]", "*", text)
b = re.subn("[0-9]", "*", text)
print(a)
print(b)
```
备注：
- sub函数使用repl替换string中每一个匹配的结果，然后返回替补的结果，count参数表示替换次数，默认全部替换；
- subn函数行为sub相同，但是返回一个元组（字符串，替换次数）

## Re正则表达式对象
> re.compile(pattern, flags=0)

```python
import re

prog = re.compile("\<div[\s\S]*?class=\"([\s\S]*?)\"[\s\S]*?\>")
text = '<div class="tab" style="overflow: hidden;text-overflow: ellipsis;white-space: nowrap;">'
prog.search(text)
prog.findall(text)
```
备注：
- compile函数可以将正则表达式编译成一个正则表达式对象，通过对象提供的方法进行匹配搜索；
- 一般在需要多次使用这个正则表达式的情况下，使用re.compile()和保存这个正则对象以便复用，可以使程序更加高效；
- 正则表达式对象提供的方法可以参看以上Re常用函数；


## Re匹配对象
当常用函数或者正则表达对象匹配搜索返回的_sre.SRE_Match对象则称为匹配对象

> Match.group([gourp1,....])<br>
Match.groups(default=None)<br>
Match.groupdict(default=None)<br>


```python
import re

a = "Hello, World, root"
b = re.search("(\w+), (\w+), (?P<name>\w+)", a)
print(b.group(0))
print(b.group(1))

print(b.groups())
print(b.groupdict())
```
备注：
- group方法返回一个或者多个匹配的子组，即括号()中的组合，默认是返回整个匹配；
- groups方法，返回一个元组，包含所有匹配的子组；
- groupdict方法，返回一个字典，包含所有的命名子组；

## 参考：
> https://docs.python.org/zh-cn/3/library/re.html?highlight=re#module-re  
> https://www.cnblogs.com/huxi/archive/2010/07/04/1771073.html

## 日常正则常用表达式
### 检测IPV4地址
```python
import re


def regex_ipv4(original_str: str) -> bool:
    regex = r"(((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))\.){3}((\d{1,2})|(1\d{2})|(2[0-4]\d)|(25[0-5]))"

    if re.fullmatch(regex, original_str):
        return True
    return False


if __name__ == "__main__":
    o_str = "192.168.1.999"
    print(regex_ipv4(o_str))
```
备注：
- 任何一个1位或2位的数字，即0-99
- 任何一个1开头的2位或3位的数字，即100-199
- 任何一个2开头的第2位是0-4之间的3位数字，即200-249
- 任何一个25开头的第3位是0-5之间的3位数字，即250-255

### 检测email地址
```python
def regex_email(addr: str) -> bool:
    regex = r"^(\w*\.)*\w+@\w+\.\w+"
    if re.fullmatch(regex, addr):
        return True
    return False
```
备注：
- \w（[a-zA-Z0-9_]

### 检测密码强度
```python
def check_strong_password(password: str) -> int:
    """
    检测密码强度
    :param password: 
    :return: 
    """
    regex_list = [r"[a-z]+", r"[A-Z]+", r"[0-9]+", r"\W+"]

    strength = 0
    for regex in regex_list:
        if re.search(regex, password):
            strength += 1

    return strength
```
备注：
- 检测是否包含数字，小写字母，大写字母，标点符号

### 身份证号检测
```python
def check_id(p_id: str)-> bool:
    regex = r"^[1-9]\d{5}(18|19|([2-3]\d))\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}[0-9xX]$"

    if re.fullmatch(regex, p_id):
        return True
    return False
```
备注：
- 地区：[1-9]\d{5}
- 年份前两位：(18|19|([2-3]\d))，1800-3999
- 年份后两位：\d{2}
- 月份：((0[1-9])|10|11|12)
- 日期：(([0-2][1-9])|10|20|30|31)
- 顺序码：\d{3}
- 校验码：}[0-9xX]

### 数字千分位分割，电话号码3-4-4分割

数字千分位
```python
import re
import random


def split_num(num: str):
    regex = r"(?!^)(?=(\d{3})+$)"
    result = re.sub(regex, ",", num)
    return result


if __name__ == "__main__":
    for  i in range(10):
        num = random.randint(100, 999999999)
        print(split_num(str(num)))


```
电话号码分割
```python
import re
import random
 
def split_phone(phone_num: str):
    """
    电话号码3-4-4分割
    :param phone_num:
    :return:
    """
    regex = r"(?=(\d{4})+$)"
    result = re.sub(regex, ',', phone_num)
    return result


if __name__ == "__main__":
    for  i in range(10):
        num = random.randint(15000000000, 18000000000)
        print(split_phone(str(num)))
```

## Xeger

> 根据正则表达式随机生成对应的字符串
随机生成身份证号：
```python
def generate_id() -> str:
    regex = r"^[1-9]\d{5}(18|19|([2-3]\d))\d{2}((0[1-9])|10|11|12)(([0-2][1-9])|10|20|30|31)\d{3}[0-9xX]$"

    x = Xeger()
    new_id = x.xeger(regex)
    return new_id


if __name__ == "__main__":
    print(generate_id())
```
