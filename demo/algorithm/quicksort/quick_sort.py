# coding: utf-8
"""
    :date: 2023-11-24
    :author: linshukai
    :description: About Quick Sort
"""


def quick_sort(unsort_list: list):
    """
    时间复杂度：平均时间复杂度：O(nlog(n)) 最坏时间复杂度：O(n^2)
    空间复杂度：O(log(n))
    """
    if len(unsort_list) < 1:
        return unsort_list

    tmp = unsort_list[0]
    less_list = [x for x in unsort_list[1:] if x <= tmp]
    greater_list = [x for x in unsort_list[1:] if x > tmp]
    return quick_sort(less_list) + [tmp] + quick_sort(greater_list)


if __name__ == "__main__":
    unsort = [1, 23, 31, 2, 3, 1, 22, 11, 11, 23, 1, 2, 3]
    unsort = quick_sort(unsort)
    print(unsort)

