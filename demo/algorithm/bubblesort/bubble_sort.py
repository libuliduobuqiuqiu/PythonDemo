# coding: utf-8
"""
    :date: 2023-11-24
    :author: linshukai
    :description: About buble sort algorithm
"""


def bubble_sort(unsort_list: list):
    """
    时间复杂度：O(n^2)
    空间复杂度：O(1)
    """
    if len(unsort_list) < 1:
        return

    index = 0
    while index < len(unsort_list) - 1:
        tmpIndex = index + 1

        while tmpIndex < len(unsort_list):
            if unsort_list[index] > unsort_list[tmpIndex]:
                unsort_list[index], unsort_list[tmpIndex] = (
                    unsort_list[tmpIndex],
                    unsort_list[index],
                )
            tmpIndex += 1
        index += 1


if __name__ == "__main__":
    unsort = [1, 23, 31, 2, 3, 1, 22, 11, 11, 23, 1, 2, 3]
    bubble_sort(unsort)
    print(unsort)
