# coding: utf-8
"""
    :date: 2023-10-27
   :author: linshukai
   :description: About os Demo
"""

import os

a = 1

def search_files(dir_path: str):
    for root, dirs, files in os.walk(dir_path):
        print(root, dirs, files)


if __name__ == "__main__":
    a = dict.fromkeys(["a", "b"])
    print(a)

    a = " i like the Python"
    print(a.rstrip())

    a = "Asssa"
    print(a.count("a"))