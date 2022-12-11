# -*- coding: utf-8 -*-

import random
import pytest

test_flag = False


class TestClass:
    @pytest.mark.skip()
    def test_odd(self):
        num = random.randint(0, 100)
        assert num % 2 == 1

    @pytest.mark.skipif(test_flag is False, reason="test_flag is False")
    def test_even(self):
        num = random.randint(0, 1000)
        assert num % 2 == 0

    @pytest.mark.xfail()
    def test_sum(self):
        random_list = [random.randint(0, 100) for x in range(10)]
        num = sum(random_list)
        assert num < 20

    @pytest.mark.parametrize('num,num2', [(1,2),(3,4)])
    def test_many_odd(self, num: int, num2: int):
        assert num % 2 == 1
        assert num2 % 2 == 0

    def test_zero(self):
        num = 0
        with pytest.raises(ZeroDivisionError) as e:
            num = 1/0
        exc_msg = e.value.args[0]
        print(exc_msg)
        assert num == 0

