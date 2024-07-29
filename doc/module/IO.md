## 读取大文件

>对于这个原因首先需要了解一下什么叫内存泄漏，内存泄漏就是当程序中已经动态分配的堆内存由于某种原因程序未释放或者无法释放，导致系统内存浪费，最后有可能出现系统内存资源耗尽导致系统崩溃等后果；  
所以当一次性读取大文件时，很有可能会达到Python程序内存限制，导致抛出Memoryerror错误，即内存泄漏；

可参考：
> https://stackoverflow.com/questions/11283220/memory-error-in-python

如何解决？
> 思路就是每次读取固定字节数的内容，比如read(size),或者使用逐行读取readline();  

1、通过生成器的方式循环获取大文件中的内容
```python
def read_file(file_path: str):
    f = open(file_path, "r", encoding='utf-8')

    while True:
        content = f.read(1024)

        if not content:
            break
        yield content


if __name__ == "__main__":
    f_path = "D:\\test.txt"
    f = read_file2(f_path)
    for content in f:
        print(content)
```
> 同理也可以通过readline()方法读取

2、通过自带的open函数内置的buffering参数，设置读取流的大小，注意只在二进制模式下可以指定buffering大小
```python
def read_file2(file_path: str):
    f = open(file_path, "rb", buffering=4096)

    for content in f:
        print(content)


if __name__ == "__main__":
    f_path = "D:\\test.txt"
    read_file2(f_path)
```
> buffering参数对读取的结果没有影响，只是对读取的性能有影响，同时这里的文件对象可以看成一个迭代器，通过遍历获取读取到文本内容
