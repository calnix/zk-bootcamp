import numpy as np

# Define a 2x2 matrix of unit vectors
unit_matrix = np.array([[1, 0], [0, 1]])

# Accessing rows and columns
row_1 = unit_matrix[0]    # First row
row_2 = unit_matrix[1]    # Second row
column_1 = unit_matrix[:, 0]  # First column
column_2 = unit_matrix[:, 1]  # Second column

print("Matrix:")
print(unit_matrix)  

print("\nFirst Row:")
print(row_1)        #1st row: [1 0]  

print("\nSecond Row:")
print(row_2)        #2nd row: [0 1]  

print("\nFirst Column:")
print(column_1)

print("\nSecond Column:")
print(column_2)


'''
Matrix representation
- each row is a list
- each column is the nth element from each list
--> the 1st column comprises of all the 1st elements from each row sequentially
'''

'''
Why use numpy arrays instead of native python lists?
- NumPy arrays are faster and more compact than Python lists. 
- Consumes less memory. More convenient to use.
- NumPy gives you an enormous range of fast and efficient ways of creating arrays and manipulating numerical data inside them 

For example, filtering the first column of a matrix.
'''

'''
What is an array?

- An array is a central data structure of the NumPy library.
- One way we can initialize NumPy arrays is from Python lists, using nested lists for two- or higher-dimensional data.

For example:

a = np.array([1, 2, 3, 4, 5, 6])

or:

a = np.array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]])

'''

# https://numpy.org/devdocs/user/absolute_beginners.html