> 模型架构
- Model: 模型层，负责数据库交互逻辑；
- View: 视图层，负责展示逻辑；
- Controller：控制层用于粘合View层和Model层；

```python
# -*- coding: utf-8 -*-

quotes = ('A man is not complete until he is married. Then he is finished.',
        'As I said before, I never repeat myself.',
        'Behind a successful man is an exhausted woman.',
        'Black holes really suck...', 'Facts are stubborn things.')


class QuoteModel:
    def __init__(self):
        self.quotes = quotes

    def get_quote(self, n):
        try:
            quote_value = self.quotes[n]
        except IndexError:
            raise IndexError("Quote Not Found")
        return quote_value


class QuoteView:
    def show(self, quote_value):
        print(f"Show Quote: {quote_value}")

    def error(self, error_msg):
        print(f"Error: {error_msg}")

    def select_quote(self):
        return input("Select Your Quote: ")


class QuoteController:
    def __init__(self):
        self.model = QuoteModel()
        self.view = QuoteView()

    def run(self):
        quote_flag = False

        while not quote_flag:
            try:
                n = self.view.select_quote()
                n = int(n)
                quote_value = self.model.get_quote(n)
            except Exception as e:
                self.view.error(str(e))
            else:
                self.view.show(quote_value)
                quote_flag = True


if __name__ == "__main__":
    quote_c = QuoteController()
    quote_c.run()
```
> 备注：
- QuoteModel用于返回指定的quotes中的元素，QuoteView用于展示选择对应元素后打印的内容，QuoteController用于组合前两者，循环接受前端的输入，合法则打印显示内容然后跳出，反之打印错误等待合法输入；
