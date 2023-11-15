import numpy as np
import random

# define the matrices
C = np.array([[0,1,0,0]])
A = np.array([[0,0,1,0]])
B = np.array([[0,0,0,1]])

# witness vector
witness = [1, 4223, 41, 103]

# Multiplication is element-wise, not matrix multiplication. # Result contains a bool indicating an element-wise indicator that the equality is true for that element.
result = C.dot(witness) == A.dot(witness) * B.dot(witness)

# check that every element-wise equality is true
assert result.all(), "result contains an inequality"


def solution(A, B, C, w):

    # Check if A, B, and C have the same dimensions
    if A.shape != B.shape or B.shape != C.shape:
        print("A, B, and C must have the same dimensions.")
        return False
    
    # Check if w is a 1D array
    if w.ndim != 1:
        print("w must be a 1D array.")
        return False
    
    # Check R1CS
    result = C.dot(witness) == A.dot(witness) * B.dot(witness)

    # check that every element-wise equality is true
    assert result.all(), "result contains an inequality"
    print("true")


# test example
w = np.array(witness)
solution(A,B,C, w)


# test problem 1

# w:     | 1  out  x  y  v1  v2  v3  v4  v5  |

C = np.array([[0,0,0,0,1,0,0,0,0],
              [0,0,0,0,0,1,0,0,0],
              [0,0,0,0,0,0,1,0,0],
              [0,0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,0,1],
              [0,1,0,10,0,0,-5,4,-13]
              ])

A = np.array([[0,0,1,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,0,0],
              [0,0,0,0,1,0,0,0,0],
              [0,0,0,0,0,1,0,0,0],
              [0,0,0,0,0,1,0,0,0],
              [0,0,0,0,1,0,0,0,0]
              ])

B = np.array([[0,0,1,0,0,0,0,0,0],
              [0,0,0,1,0,0,0,0,0],
              [0,0,1,0,0,0,0,0,0],
              [0,0,0,0,1,0,0,0,0],
              [0,0,1,0,0,0,0,0,0],
              [1,0,0,0,0,0,0,0,0]
              ])

# pick random values for x and y
x = random.randint(1,1000)
y = random.randint(1,1000)

# intermediates 
v1 = x * x 
v2 = y * y 
v3 = v1 * x
v4 = v2 * v1
v5 = v2 * x

out = (5)*(x**3) - (4)*(x**2)*(y**2) + 13*(x)*(y**2) + (x**2) - 10*(y)

w = np.array([1, out, x, y, v1, v2, v3, v4, v5])

solution(A,B,C, w)