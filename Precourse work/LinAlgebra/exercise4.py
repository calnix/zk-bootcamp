# Exercise 4, linear combination

# linear combination is a Vector multiplied by a constant plus another Vector multiplied by a constant.
# aA + bB = C (A, B, C are vectors, a and b are scalars)

import numpy as np

def dot_product(A, B):
    # Cast the input lists to NumPy arrays
    A = np.array(A)
    B = np.array(B)

    C = np.dot(A, B)

    return C

def linearCombination(A, B, a, b):
    A = np.array(A)
    B = np.array(B)

    C = dot_product(A,a) + dot_product(B,b)

    return C


# test
vector1 = np.array([1,2])
vector2 = np.array([5,6])
scalar1 = 3
scalar2 = 10

assert (np.array([53, 66]) == linearCombination(vector1, vector2, scalar1, scalar2)).all()
print(linearCombination(vector1, vector2, scalar1, scalar2), "\n")


# column space and null space
# Nonsquare matrices as transformations between dimensions
# Dot products and duality