### 冒泡排序
```python
def my_sort(unsort_list: list):
    if len(unsort_list) < 1:
        return

    index = 0
    while index < len(unsort_list) - 1:
        tmpIndex = index + 1

        while tmpIndex < len(unsort_list):
            if unsort_list[index] > unsort_list[tmpIndex]:
                unsort_list[index], unsort_list[tmpIndex] = unsort_list[tmpIndex], unsort_list[index]
            tmpIndex += 1
        index += 1


if __name__ == "__main__":
    unsort = [1, 23, 31, 2, 3, 1, 22, 11, 11, 23, 1, 2, 3]
    my_sort(unsort)
    print(unsort)
```
时间复杂度：O(n^2)
空间复杂度：O(1)

### 选择排序
```python
def selection_sort(unsort_list: list):
    index = 0

    while index < len(unsort_list) - 1:
        exchange_index = index
        tmp_index = index + 1

        while tmp_index < len(unsort_list):
            if unsort_list[exchange_index] > unsort_list[tmp_index]:
                exchange_index = tmp_index
            tmp_index += 1

        if exchange_index != index:
            unsort_list[index], unsort_list[exchange_index] = unsort_list[exchange_index], unsort_list[index]

        index += 1
```
时间复杂度：O(n^2)
空间复杂度：O(1)


### 插入排序
```python
def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1

        # 将比 key 大的元素向后移动
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

        # 插入 key 到正确的位置
        arr[j + 1] = key

if __name__ == "__main__":
    unsorted_list = [64, 34, 25, 12, 22, 11, 90]
    insertion_sort(unsorted_list)
    print("Sorted array:", unsorted_list)
```
时间复杂度：O(n^2)
空间复杂度：O(1)
这个插入排序算法的基本思想是将数组分为已排序和未排序两部分，初始时已排序部分只有一个元素。然后，逐个将未排序部分的元素插入到已排序部分的正确位置，使得已排序部分始终保持有序。
在代码中，key 变量表示当前待插入的元素，通过逐个比较并向后移动已排序部分的元素，找到合适的位置插入 key。
插入排序的时间复杂度为 O(n^2)，空间复杂度为 O(1)。虽然插入排序不如一些高级排序算法在大规模数据上高效，但在小规模数据或部分有序数据上表现良好。

### 快速排序
```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    else:
        pivot = arr[0]
        less = [x for x in arr[1:] if x <= pivot]
        greater = [x for x in arr[1:] if x > pivot]
        return quick_sort(less) + [pivot] + quick_sort(greater)

if __name__ == "__main__":
    unsorted_list = [64, 34, 25, 12, 22, 11, 90]
    sorted_list = quick_sort(unsorted_list)
    print("Sorted array:", sorted_list)
```
这个快速排序算法使用了递归的思想。基本思路是选择一个基准元素（通常是数组的第一个元素），然后将数组分为两部分，一部分包含所有小于等于基准的元素，另一部分包含所有大于基准的元素。然后，对这两部分递归地应用相同的方法，直到整个数组有序。
在代码中，pivot 是基准元素，less 列表包含所有小于等于基准的元素，greater 列表包含所有大于基准的元素。然后通过递归对 less 和 greater 进行快速排序，最后将排序好的列表连接在一起。
快速排序的平均时间复杂度为 O(n log n)，最坏情况下为 O(n^2)（当选择的基准元素总是最大或最小元素时）。空间复杂度取决于递归深度，为 O(log n)。


### 归并排序
```python
def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    # 将数组分为两半
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    # 对每一半递归应用归并排序
    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    # 合并两个有序的子数组
    return merge(left_half, right_half)

def merge(left, right):
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # 将剩余元素添加到结果中
    result.extend(left[i:])
    result.extend(right[j:])

    return result

if __name__ == "__main__":
    unsorted_list = [64, 34, 25, 12, 22, 11, 90]
    sorted_list = merge_sort(unsorted_list)
    print("Sorted array:", sorted_list)
```
在归并排序中，基本思想是将数组递归地分成两半，对每一半进行排序，然后再将两个有序的子数组合并成一个有序的数组。上述代码中，merge_sort 函数对数组进行递归拆分，而 merge 函数负责合并两个有序的子数组。
归并排序的时间复杂度始终为 O(n log n)，无论是在最坏情况、平均情况还是最好情况下。它的空间复杂度为 O(n)，因为在合并过程中需要额外的空间来存储临时数组。
