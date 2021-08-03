# -*- coding: utf-8 -*-
# 享元模式

import random
from enum import Enum
TreeType = Enum("TreeType", "apple_tree cherry_tree peach_tree")


class Tree:
    pool = dict()

    def __new__(cls, tree_type):
        obj = cls.pool.get(tree_type)

        if not obj:
            obj = object.__new__(cls)
            cls.pool[tree_type] = obj
            obj.tree_type = tree_type
        return obj

    def render(self, age, x, y):
        print(f"render a tree of type {self.tree_type} and age {age} at ({x}, {y})")


if __name__ == "__main__":
    rand = random.randint
    age_min, age_max = 1, 100
    min_point, max_point = 1, 100

    t1 = Tree(TreeType.apple_tree)
    t1.render(rand(age_min, age_max), rand(min_point, max_point), rand(min_point, max_point))

    t2 = Tree(TreeType.cherry_tree)
    t2.render(rand(age_min, age_max), rand(min_point, max_point), rand(min_point, max_point))

    t3 = Tree(TreeType.apple_tree)

    print(t1 == t2)
    print(t1 == t3)
