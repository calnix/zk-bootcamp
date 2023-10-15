# Exercise 2, element-wise and matrix multiplication
import numpy as np

A = [[1,2,3],[4,5,6],[7,8,9]]
B = [[1,1,1],[2,2,2],[3,3,3]]


def element_wise_multiply(A, B):
    # Cast the input lists to NumPy arrays
    A = np.array(A)
    B = np.array(B)

    C = np.multiply(A, B)

    return C

def matrix_multiply(A, B):
    # Cast the input lists to NumPy arrays
    A = np.array(A)
    B = np.array(B)

    C = np.matmul(A, B)

    return C

def dot_product(A, B):
    # Cast the input lists to NumPy arrays
    A = np.array(A)
    B = np.array(B)

    C = np.dot(A, B)

    return C

# results
print(element_wise_multiply(A, B), "\n")
print(matrix_multiply(A, B), "\n")
print(dot_product(A, B), "\n")

# test dot product
Q = [1,2,3,4]
assert (dot_product(Q, Q) == 30)

'''
matrix multiplication methods

numpy.multiply(arr1, arr2) - Element-wise matrix multiplication of two arrays:
numpy.matmul(arr1, arr2) - Matrix product of two arrays
numpy.dot(arr1, arr2) - Scalar or dot product of two arrays:

'''

'''
numpy.multiply(arr1, arr2)

.multiply() is used to compute the 
1) element-wise multiplication of 2 arrays w/ same shape, (Hadamard product)
2) multiply one array with a single numeric value (scalar multiplication)

src: https://sparkbyexamples.com/numpy/numpy-element-wise-multiplication/
src: https://medium.com/linear-algebra/part-14-dot-and-hadamard-product-b7e0723b9133
'''

'''
np.matmul(arr1, arr2)

.matmul() is used to compute the matrix product of two arrays.
 1st row of A * 1st column of B
 matmul(A, B) might be different from matmul(B, A).
 scalar is produced only when both arr1 and arr2 are 1-dimensional vectors

src: https://www.digitalocean.com/community/tutorials/numpy-matrix-multiplication
'''