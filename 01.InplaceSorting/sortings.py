"""
Sorting algorithms
"""


def builtin_sort(data):
    """
    Standard library sorting algorithm


    :param data: data to sort inplace
    :type data: list[BasicType] or other indexable sequence[BasicType]
    """
    if isinstance(data, list):
        data.sort()
    else:  # assume it is counting container
        # TODO: скормить корректно, или оставить эту идею, и
        # сделать less & swap
        tmp = list(data._array)
        tmp.sort()

        for i, v in enumerate(tmp):
            data[i] = v
        
def bubble_sort(data):

    n = len(data)

    for i in range(n):
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                tmp = data[j]
                data[j] = data[j + 1]
                data[j + 1] = tmp
                
def merge_sort(data):


    def _merge_sort(left, right):
        if right - left <= 1:
            return

        mid = (left + right) // 2

        _merge_sort(left, mid)
        _merge_sort(mid, right)

        merge(left, mid, right)

    def merge(left, mid, right):
        temp = []
        i = left
        j = mid

        while i < mid and j < right:
            if data[i] <= data[j]:
                temp.append(data[i])
                i += 1
            else:
                temp.append(data[j])
                j += 1

        while i < mid:
            temp.append(data[i])
            i += 1

        while j < right:
            temp.append(data[j])
            j += 1


        for k, v in enumerate(temp):
            data[left + k] = v

    _merge_sort(0, len(data))          

