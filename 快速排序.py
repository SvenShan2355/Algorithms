# 快速排序算法
import random

A = [13, 19, 6, 5, 12, 8, 6, 7, 4, 21, 2, 6, 11, 9, 6]
B = [3, 3, 3, 3, 3, 3, 3, 3, 3]


def quick_sort(list, a, b):  # 列表，起始位置，结束位置
    global A
    print(A)
    if a < b:
        q = partition(list, a, b)
        quick_sort(list, a, q - 1)
        quick_sort(list, q + 1, b)
    else:
        return


def partition(list, a, b):
    # k = random.randint(a, b)
    # list[k], list[b] = list[b], list[k]
    q = a - 1
    t = a - 1
    for j in range(a, b, 1):
        if list[j] < list[b]:
            q = q + 1
            t = t + 1
            list[q], list[j] = list[j], list[q]
            list[t], list[j] = list[j], list[t]
        elif list[j] == list[b]:
            t = t + 1
            list[t], list[j] = list[j], list[t]
        print(j, q, t, list)
    list[t + 1], list[b] = list[b], list[t + 1]
    return q + 1, t


print(partition(A, 0, 14), A)
