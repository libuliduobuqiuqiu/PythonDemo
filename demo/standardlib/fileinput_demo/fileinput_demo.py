# coding: utf-8
"""
    :date: 2023-10-25
    :author: linshukai
    :description: About FileInput Demo
"""

import fileinput


if __name__ == "__main__":
    with fileinput.FileInput("D://cube.csv") as f:
        for line in f:
            print(f.filename(), f.fileno(), line)