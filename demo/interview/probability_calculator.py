"""
    :Date: 2024-06-4
    :Author: linshukai
    :Description: About Probability caculator
"""

import copy
import random


class Hat:
    def __init__(self, **kwargs):
        self.contents = []
        for k, v in kwargs.items():
            while v > 0:
                self.contents.append(k)
                v -= 1

    def draw(self, num_balls):
        if num_balls > len(self.contents):
            res = copy.copy(self.contents)
            self.contents = []
            return res

        res = random.sample(self.contents, num_balls)
        for ball in res:
            self.contents.remove(ball)
        return res


def balls_matched(expected_balls, drawn_balls):
    for k, nums in expected_balls.items():
        c = drawn_balls.count(k)
        if c < nums:
            return False
    return True


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    matched = 0
    tmp_experiments = num_experiments

    while tmp_experiments > 0:
        tmp = copy.deepcopy(hat)
        res = tmp.draw(num_balls_drawn)

        if balls_matched(expected_balls, res):
            print(res)
            matched += 1
        tmp_experiments -= 1

    return matched / num_experiments


if __name__ == "__main__":
    hat = Hat(black=6, red=4, green=3)
    probability = experiment(
        hat=hat,
        expected_balls={"red": 2, "green": 1},
        num_balls_drawn=5,
        num_experiments=2000,
    )
    print(probability)
