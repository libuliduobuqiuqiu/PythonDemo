## 导语
> 由于项目程序开发过程中，自测环节是一项非常重要的环节，平常经常使用到python自带的单元测试框架unittest，本文介绍基本的使用方式。

## 基本组成部分
### TestFixture（测试脚手架）
> test fixture 表示为了开展一项或多项测试所需要进行的准备工作，以及所有相关的清理操作。举个例子，这可能包含创建临时或代理的数据库、目录，再或者启动一个服务器进程。

### TestCase（测试用例）
> 一个测试用例是一个独立的测试单元。它检查输入特定的数据时的响应。 unittest 提供一个基类： TestCase ，用于新建测试用例。

### TestSuite（测试套件）
> test suite 是一系列的测试用例，或测试套件，或两者皆有。它用于归档需要一起执行的测试。

### TestRunner（测试运行器）
> test runner 是一个用于执行和输出测试结果的组件。这个运行器可能使用图形接口、文本接口，或返回一个特定的值表示运行测试的结果。

## 实际使用

### 基本实例
```
#!/usr/bin/python

import unittest


class Test1(unittest.TestCase):

    def test_hello(self):
        word = "hello,world"
        split_word = word.split(",")
        self.assertEqual(["hello", "world"], split_word)

    def test_upper(self):
        word1 = "FOO"
        word2 = "Foo"
        self.assertTrue(word1.isupper())
        self.assertFalse(word2.isupper())

    def test_upper2(self):
        self.assertEqual("foo".upper(), "FOO")


if __name__ == "__main__":
    unittest.main()

```
解析：
- 继承unittest.TestCase创建一个测试样例，测试样例中以test开头的方法都是单独测试；
- 测试方法中assertEqual,assertFalse,assertTrue代表测试过程中会验证条件，如果错误则抛出异常；
- unittest.main()提供测试脚本的命令行接口，可以直接在命令行调用脚本执行测试；

命令行调用
```
python simple.py -v
python -m unittest -v simple
python -m unittest -v simple.Test1
python -m unittest -v simple.Test1.test_hello
```

### 进阶使用
```
#!/usr/bin/python

import unittest
import paramiko


class Test1(unittest.TestCase):

    def setUp(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(hostname='120.77.144.48', port=22, username='root', password='929833867Lin./')

    def tearDown(self):
        self.client.close()

    def test_Command(self):
        cmd = "hostname"
        stdin, stdout, stderr = self.client.exec_command(cmd)
        hostname = stdout.read()
        print(hostname)
        self.assertEqual("mbb-48", hostname)

    def test_memcache(self):
        cmd = "free -m"
        stdin, stdout, stderr = self.client.exec_command(cmd)
        memcache_info = stdout.read()
        print(memcache_info)


def TestSuite1():
    suite = unittest.TestSuite()
    suite.addTest(Test1("test_Command"))
    suite.addTest(Test1("test_memcache"))
    return suite


if __name__ == "__main__":
    suite = TestSuite1()
    runner = unittest.TextTestRunner()
    runner.run(suite)
```
解析：
- 若 setUp() 成功运行，无论测试方法是否成功，都会运行 tearDown() 。
这样的一个测试代码运行的环境被称为 test fixture 。一个新的 TestCase 实例作为一个测试脚手架，用于运行各个独立的测试方法。在运行每个测试时，setUp() 、tearDown() 和 __init__() 会被调用一次。
- TestSuite1函数返回一个TestSuite类型，通过这个suite可以将测试的方法组织起来，然后执行起来。
- test runner执行和输出结果的组件。


后续备注：
TestCase提供的方法：
- setUp(),tearDown()每个测试用例在执行时会运行的方法
- setUpClass(),tearDownClass()在每个test class运行和结束时会运行的方法（需要使用classmethod装饰）
- 可通过SkipIf，skip方法在指定条件下跳过测试；

```python
@unittest.skipIf(sys.version_info > (3, 7), "only support 3.7-")
    def test_print_version(self):
        self.assertTrue(sys.version_info > (3, 7))
```
