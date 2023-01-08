import random

"""
——————最大数组分治法——————
"""


def find_maximum_subarray_cross_mid(input_array):
    mid = int(len(input_array) / 2)
    max_left = float('-inf')
    max_right = float('-inf')
    l = 0
    r = 0
    a = 0
    b = 0
    for i in range(len(input_array[:mid])):
        left_part = input_array[:mid]
        left_part.reverse()
        l = left_part[i] + l
        if max_left < l:
            max_left = l
            a = mid - i - 1
    for i in range(len(input_array[mid:])):
        r = input_array[mid:][i] + r
        if max_right < r:
            max_right = r
            b = mid + i + 1
    return max_right + max_left, input_array[a:b]


def find_maximum_subarray(input_array):
    # print("-----\n", input_array)
    if len(input_array) > 1:
        mid = int(len(input_array) / 2)
        max_low_mid, max_array_l = find_maximum_subarray(input_array[:mid])
        max_mid_high, max_array_r = find_maximum_subarray(input_array[mid:])
        max_cross_mid, max_array_c = find_maximum_subarray_cross_mid(input_array)
        if max(max_low_mid, max_mid_high, max_cross_mid) == max_low_mid:
            # print(max_low_mid, max_array_l, "左侧局部最大")
            return max_low_mid, max_array_l
        elif max(max_low_mid, max_mid_high, max_cross_mid) == max_mid_high:
            # print(max_mid_high, max_array_r, "右侧局部最大")
            return max_mid_high, max_array_r
        elif max(max_low_mid, max_mid_high, max_cross_mid) == max_cross_mid:
            # print(max_cross_mid, max_array_c, "跨中点局部最大")
            return max_cross_mid, max_array_c
    elif len(input_array) == 1:
        if input_array[0] <= 0:
            # print(0, [], "触底返回空数组")
            return 0, []
        else:
            # print(input_array[0], input_array, "触底返回单元素数组")
            return input_array[0], input_array


"""
——————最大数组暴力求解——————
"""


def LoopSolve(input_array):
    max_sum = float('-inf')
    for i in range(len(input_array) + 1):
        for j in range(i + 1):
            s = sum(input_array[j:i])
            if max_sum < s:
                max_sum = s
                a = j
                b = i
    return max_sum, input_array[a:b]


"""
——————最大数组线性优化算法——————
"""


def DynamicProgramming(input_array):
    a0, b = 0, 0
    max_sum = float('-inf')
    loop_sum = float('-inf')
    for i in range(len(input_array)):
        if loop_sum <= 0:
            loop_sum = input_array[i]
            a0 = i
        else:
            loop_sum = loop_sum + input_array[i]
        if loop_sum > max_sum:
            max_sum = loop_sum
            a = a0
            b = i + 1
        # print(a, b, loop_sum, max_sum)
    return sum(input_array[a:b]), input_array[a:b]


"""
——————随机1000个数组进行检验——————
"""


for i in range(1000):
    array1 = []
    for i in range(20):
        array1.append(random.randint(-20, 20))
    a = find_maximum_subarray(array1)
    b = LoopSolve(array1)
    c = DynamicProgramming(array1)
    if a != b or b != c:
        print(array1)
        print(a)
        print(b)
        print(c)


# array1 = [20, 5, -10, -12, 12, -13, 10, 12, -16, -8, 15, 10, 9, 19, -16, 8, 3, -3, 18, -4]
# print(array1)
# print(find_maximum_subarray(array1))
# print(LoopSolve(array1))
# print(DynamicProgramming(array1))
