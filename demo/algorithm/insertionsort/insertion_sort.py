# coding: utf-8
"""
        :date: 2023-11-25
        :author: linshukai
        :description: About Insertion Sort Demo`
"""


def insertion_sort(unsort_list: list):
    """
    时间复杂度： O(n^2)
    空间复杂度： O(1)
    """
    tmp_index = 1
    while tmp_index < len(unsort_list):
        index_key = unsort_list[tmp_index]
        compare_index = tmp_index - 1

        while compare_index >= 0 and index_key < unsort_list[compare_index]:
            unsort_list[compare_index + 1] = unsort_list[compare_index]
            compare_index -= 1

        # 补全原来替换位置上的值
        unsort_list[compare_index + 1] = index_key
        tmp_index += 1


if __name__ == "__main__":
    unsort = [33, 1, 23, 31, 2, 3, 1, 22, 11, 11, 23, 1, 2, 3]
    insertion_sort(unsort)
    print(unsort)

