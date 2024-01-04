import numpy as np
from scipy.interpolate import lagrange

# arbitrary x-values
# 3 elements per col.
x = np.array([1,2,3])

#  y^2 + 4yx^2 -2 
# Cw = Aw * Bw

# A ---> U 
#| 0  0  0  1  0  0 | 
#| 0  0  1  0  0  0 | 
#| 0  0  0  0  0  4 |  

# interpolation has to be done per column of A
# The zero vectors get turned into the polynomial 0 (this obviously interpolates all the zero values in the column). 
a_3 = np.array([0, 1, 0])
a_4 = np.array([1, 0, 0])
a_5 = np.array([0, 0, 4])

poly_a3 = lagrange(x, a_3)
poly_a4 = lagrange(x, a_4)
poly_a5 = lagrange(x, a_5)
print(poly_a3)
print(".........................")
print(poly_a4)
print(".........................")
print(poly_a5)
print("...........A done ...........")

# B -> V
#| 0  0  1  0 | 
#| 5  0  0  0 | 

b_1 = np.array([0, 5])
b_3 = np.array([1, 0])

poly_b1 = lagrange(x, b_1)
poly_b3 = lagrange(x, b_3)
print(poly_b1)
print(".........................")
print(poly_b3)
print("............B done ...........")

# C -> W
#| 0  0  0  1 | 
#| 0  1  0  0 | 

c_2 = np.array([0, 1])
c_4 = np.array([1, 0])

poly_c2 = lagrange(x, c_2)
poly_c4 = lagrange(x, c_4)
print(poly_c2)
print(".........................")
print(poly_c4)
print("...........C done............")