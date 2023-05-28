# 确定堆性质
def parent(i):
    return int(i / 2)


def left(i):
    return 2 * i


def right(i):
    return 2 * i + 1


# 在0~n位上维护堆性质
def heapify(A, i, n):
    largest = 0
    while True:
        if right(i) <= n:
            l = left(i)
            r = right(i)
            if A[l - 1] > A[r - 1]:
                largest = l
            else:
                largest = r
            if A[i - 1] > A[largest - 1]:
                return A
            else:
                A[i - 1], A[largest - 1] = A[largest - 1], A[i - 1]
            i = largest
        elif left(i) <= n:
            l = left(i)
            if A[l - 1] > A[i - 1]:
                A[l - 1], A[i - 1] = A[i - 1], A[l - 1]
                i = l
            return A
        else:
            return A


# 生成最大堆
def build_max_heap(A):
    for i in range(int(len(A) / 2), 0, -1):
        A = heapify(A, i, len(A))
    return A


# 堆排序
def heapsort(A):
    A = build_max_heap(A)
    for i in range(len(A) - 1, -1, -1):
        A[0], A[i] = A[i], A[0]
        heapify(A, 1, i)
    return A


# 优先队列——maximum
def heap_maximum(A):
    return A[0]


def heap_extract_max(A):
    if len(A) < 1:
        return "heap underflow"
    else:
        max = A[0]
        A[0] = A[len(A) - 1]
        A.pop()
        heapify(A, 1, len(A))
        return max, A


def heap_increase_key(A, i, key):
    if key < A[i - 1]:
        return "new key is smaller than current key"
    A[i - 1] = key
    print(A)
    while key > A[parent(i) - 1] and i > 1:
        A[i - 1] = A[parent(i) - 1]
        i = parent(i)
        print(A)
    A[i - 1] = key
    return A


def heap_insert(A, key):
    A.append(key)
    heap_increase_key(A, len(A), key)
    return A


temp = [15, 13, 9, 5, 12, 8, 7, 4, 0, 6, 2, 1]
print(heap_insert(temp, 10))
