# -*- coding: utf-8 -*-
# MVC模式


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