# coding: utf-8
"""
    :date: 2023-10-27
   :author: linshukai
   :description: About os Demo
"""

import os


def search_files(dir_path: str):
    for root, dirs, files in os.walk(dir_path):
        print(root, dirs, files)


if __name__ == "__main__":
    search_files("D:\\Download")