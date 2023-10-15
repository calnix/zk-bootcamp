# Exercise 6, Column and Row Slicing

'''
Numpy let's you select rows and columns from matrices. For example, given

[[1,2,3],
 [4,5,6],
 [7,8,9]] 
you can retrive [2,5,8] or [7,8,9] conveniently. Implement those below:

'''

import numpy as np


def get_column_as_1d(A, col_number):
    # todo
    A = np.array(A)

    return A[:,col_number]

def get_row_as_1d(A, row_number):
    # todo
    A = np.array(A)

    return A[row_number]


A = [[1,2,3],[4,5,6],[7,8,9]] 

print(get_column_as_1d(A, 1)) # [2,5,8]
print(get_row_as_1d(A, 2)) # [7,8,9]


# https://www.earthdatascience.org/courses/intro-to-earth-data-science/scientific-data-structures-python/numpy-arrays/indexing-slicing-numpy-arrays/
# https://numpy.org/devdocs/user/basics.indexing.html