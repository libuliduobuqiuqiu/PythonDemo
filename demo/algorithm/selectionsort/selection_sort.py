# coding: utf-8
"""
    :date: 2023-11-24
    :author: linshukai
    :description: About Selection Sort Demo
"""


def selection_sort(unsort_list: list):
    """
    时间复杂度：O(n^2)
    空间复杂度：O(1)
    """
    index = 0

    while index < len(unsort_list) - 1:
        exchange_index = index
        tmp_index = index + 1

        while tmp_index < len(unsort_list):
            if unsort_list[exchange_index] > unsort_list[tmp_index]:
                exchange_index = tmp_index
            tmp_index += 1

        if exchange_index != index:
            unsort_list[index], unsort_list[exchange_index] = (
                unsort_list[exchange_index],
                unsort_list[index],
            )

        index += 1


if __name__ == "__main__":
    unsort = [1, 23, 31, 2, 3, 1, 22, 11, 11, 23, 1, 2, 3]
    selection_sort(unsort)
    print(unsort)
