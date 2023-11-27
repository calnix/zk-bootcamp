# https://almondine-song-c43.notion.site/Homework-7-Encrypted-QAP-4d75259eac0246aa86ed48b51e7700b6


# Interpolate
import numpy as np
from scipy.interpolate import lagrange

# arbitrary x-values
x = np.array([1,2,3])

#column vectors to interpolate

# A -> U
a_1 = np.array([1, 0, 0])
a_2 = np.array([0, 1, 0])
a_3 = np.array([0, 0, 4])

poly_a1 = lagrange(x, a_1)
poly_a2 = lagrange(x, a_2)
poly_a3 = lagrange(x, a_3)
print(poly_a1)
print(".........................")
print(poly_a2)
print(".........................")
print(poly_a3)
print("............a done ...........")

# B -> V
b_1 = np.array([1, 0, 1])
b_2 = np.array([0, 1, 0])

poly_b1 = lagrange(x, b_1)
poly_b2 = lagrange(x, b_2)
print(poly_b1)
print(".........................")
print(poly_b2)
print("............b done ...........")

# C -> W
c_1 = np.array([0, 0, 2])
c_2 = np.array([0, 0, 1])
c_3 = np.array([1, 0, -1])
c_4 = np.array([0, 1, 0])


poly_c1 = lagrange(x, c_1)
poly_c2 = lagrange(x, c_2)
poly_c3 = lagrange(x, c_3)
poly_c4 = lagrange(x, c_4)
print(poly_c1)
print(".........................")
print(poly_c2)
print(".........................")
print(poly_c3)
print(".........................")
print(poly_c4)
print(".........................")


# Find h(x)
import numpy as np

# Define the polynomials
u = np.poly1d([6.5, -18.5, 13])      #x^2, x, const
v = np.poly1d([-1, 4, -2])
w = np.poly1d([4.5, -10.5, 7])
t = np.poly1d([1, -1]) * np.poly1d([1, -2]) * np.poly1d([1, -3])

h = (u * v - w) / t
print(h)
# (poly1d([-6.5,  5.5]), poly1d([0.])) -> - 6.5x + 5.5
