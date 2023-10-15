import numpy as np

def add_arrays(A, B):
    # Cast the input lists to NumPy arrays
    A = np.array(A)
    B = np.array(B)

    # Check if the shapes of A and B are compatible for addition
    if A.shape != B.shape:
        raise ValueError("Input arrays must have the same shape for addition.")
    
    # Perform element-wise addition
    C = A + B

    return C


# A + B = C
A = [[1,2,3],[4,5,6],[7,8,9]]
B = [[1,1,1],[2,2,2],[3,3,3]]
C = [[2,3,4],[6,7,8],[10,11,12]]

res = add_arrays(A, B)
print(res)
print(type(res))  # <class 'numpy.ndarray'>

# What does the .all() do? 
# does an elementwise equality check.
# checks that every item in the array is True.
assert (add_arrays(A, B) == np.array(C)).all()





'''
Difference between Numpy array and Numpy Matrix
- Matrix is 2-dimensional while ndarray can be multi-dimensional
- Different functionality of  * operator in ndarray and Matrix
-> Since a is a matrix, a**2 returns the matrix product a*a.
-> Since c is an ndarray, c**2 returns an ndarray with each component squared element-wise.
-> https://stackoverflow.com/questions/4151128/what-are-the-differences-between-numpy-arrays-and-matrices-which-one-should-i-u#:~:text=The%20main%20advantage%20of%20numpy%20arrays%20is%20that%20they%20are,object%20operations%2C%20and%20ndarray%20operations.

'''

'''
assert (add_arrays(A, B) == np.array(C)).all()
What does the .all() do?

.all() method is a NumPy function that checks whether all elements of the boolean array resulting from the comparison are True.

Breaking down the statement:

add_arrays(A, B) computes the sum of arrays A and B.
np.array(C) creates a NumPy array from the given list C.
The == operator compares each element of the arrays A + B and C element-wise, resulting in a boolean array where True indicates the corresponding elements are equal, and False indicates they are not.

Finally, .all() checks if all elements in the resulting boolean array are True. If all elements are True, it returns True, indicating that the arrays A + B and C are equal element-wise. If any element is False, it returns False, indicating that the arrays are not equal in at least one element.

The assert statement is a Python construct that checks if the provided expression is True. If the expression is False, it raises an AssertionError. In this case, it's used to assert that the sum of arrays A and B is equal to array C element-wise.

'''