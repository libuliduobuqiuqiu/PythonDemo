# coding: utf-8
"""
    :date: 2023-11-24
    :author: linshukai
    :description: About Quick Sort
"""


def quick_sort(unsort_list: list):
    if len(unsort_list) <= 0:
        return unsort_list

    p = unsort_list[0]
    greater_list = [x for x in unsort_list[1:] if x > p]
    less_list = [x for x in unsort_list[1:] if x <= p]
    return quick_sort(less_list) + [p] + quick_sort(greater_list)


if __name__ == "__main__":
    unsort = [1, 23, 31, 2, 3, 1, 22, 11, 11, 23, 1, 2, 3]
    unsort = quick_sort(unsort)
    print(unsort)