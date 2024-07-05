# coding: utf-8
"""
    :date: 2023-11-25
    :author: linshukai
    :description: About Merge Sort Demo
"""


def merge_sort(unsort_list: list):
    """
    时间复杂度：O(nlogn)
    空间复杂度：O(n)
    """
    if len(unsort_list) <= 1:
        return unsort_list

    half = len(unsort_list) // 2
    left = unsort_list[half:]
    right = unsort_list[:half]

    left_sort = merge_sort(left)
    right_sort = merge_sort(right)

    return merge(left_sort, right_sort)


def merge(left: list, right: list):
    i = j = 0
    sort_list = []

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            sort_list.append(left[i])
            i += 1
        else:
            sort_list.append(right[j])
            j += 1

    if i < len(left):
        sort_list.extend(left[i:])
    if j < len(right):
        sort_list.extend(right[j:])

    return sort_list


if __name__ == "__main__":
    unsort = [1, 23, 31, 2, 3, 1, 22, 11, 11, 23, 1, 2, 3]
    sort = merge_sort(unsort)
    print(sort)
