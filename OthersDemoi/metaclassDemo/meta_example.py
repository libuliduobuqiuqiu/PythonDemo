# coding: utf-8
"""
    :date: 2023-10-26
    :author: linshukai
    :description: About Singleton Demo by MetaClass
"""


class Singleton(type):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._instance = None

    def __call__(self, *args, **kwargs):
        if self._instance is None:
            self._instance = super().__call__(*args, **kwargs)
        return self._instance


class Spam(metaclass=Singleton):
    def __init__(self):
        print("Spam")


if __name__ == "__main__":
   a = Spam()
   a2 = Spam()

   print(a == a2)
   print(id(a), id(a2))