import numpy as np

array2 = np.random.randint(10, size=(8, 8))
array3 = np.random.randint(10, size=(8, 8))

print(array2)
print(array3)


def strassen(input_array1, input_array2):
    # print("1")
    if input_array1.shape[0] == 1 and input_array2.shape[0] == 1:
        return np.array([[input_array1[0, 0] * input_array2[0, 0]]])
    else:
        length = input_array1.shape[0]
        mid = int(length / 2)
        s1 = input_array2[0:mid, mid:length] - input_array2[mid:length, mid:length]
        s2 = input_array1[0:mid, 0:mid] + input_array1[0:mid, mid:length]
        s3 = input_array1[mid:length, 0:mid] + input_array1[mid:length, mid:length]
        s4 = input_array2[mid:length, 0:mid] - input_array2[0:mid, 0:mid]
        s5 = input_array1[0:mid, 0:mid] + input_array1[mid:length, mid:length]
        s6 = input_array2[0:mid, 0:mid] + input_array2[mid:length, mid:length]
        s7 = input_array1[0:mid, mid:length] - input_array1[mid:length, mid:length]
        s8 = input_array2[mid:length, 0:mid] + input_array2[mid:length, mid:length]
        s9 = input_array1[0:mid, 0:mid] - input_array1[mid:length, 0:mid]
        s10 = input_array2[0:mid, 0:mid] + input_array2[0:mid, mid:length]
        # print("s")
        # print(s1.shape, s2.shape, s3.shape, s4.shape, s5.shape, s6.shape, s7.shape, s8.shape, s9.shape, s10.shape,
        #       sep="\n")

        p1 = strassen(input_array1[0:mid, 0:mid], s1)
        p2 = strassen(s2, input_array2[mid:length, mid:length])
        p3 = strassen(s3, input_array2[0:mid, 0:mid])
        p4 = strassen(input_array1[mid:length, mid:length], s4)
        p5 = strassen(s5, s6)
        p6 = strassen(s7, s8)
        p7 = strassen(s9, s10)
        # print("p")
        # print(p1.shape, p2.shape, p3.shape, p4.shape, p5.shape, p6.shape, p7.shape, sep="\n")

        c11 = p5 + p4 - p2 + p6
        c12 = p1 + p2
        c21 = p3 + p4
        c22 = p5 + p1 - p3 - p7
        # print("c")
        # print(c11, c12, c21, c22, sep="\n")

        return np.block([[c11, c12], [c21, c22]])


print(strassen(array2, array3))
print(np.matmul(array2, array3))
