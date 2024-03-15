# coding: utf-8
import os
from functools import partial


def open_partial_file(file_name: str, record_size: int):
    with open(file_name, "rb") as f:

        records = iter(partial(f.read, record_size), b"")

        for r in records:
            print(r)


def filter_files(dir_name: str):
    files = [name for name in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, name))]
    print(files)

    dirs = [name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, name))]
    print(dirs)


def search_all_files(dir_name: str):
    # 递归遍历目录下的所有文件

    files = [name for name in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name, name))]
    if len(files) != 0:
        print(dir_name, ":", files)

    dirs = [name for name in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name, name))]
    for tmp_dir in dirs:
        search_all_files(os.path.join(dir_name, tmp_dir))


def gen_read_file(file_name: str):

    with open(file_name, "rb") as f:
        for tmp in f:
            yield tmp


def spam(a, b, c, d):
    print(a,b,c,d)


if __name__ == "__main__":

    s1 = partial(spam, b=2, c=3, d=4)
    s1(1)

    # open_partial_file("D:\\Backup\\test.txt", 12)

    # search_all_files("D:\\Download")
    #
    # for i in gen_read_file("D:\\Backup\\test.txt"):
    #     print(i)