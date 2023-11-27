

# Find h(x)
import numpy as np

# Define the polynomials
u = np.poly1d([6.5, -18.5, 13])
v = np.poly1d([-1, 4, -2])
w = np.poly1d([4.5, -10.5, 7])
t = np.poly1d([1, -1]) * np.poly1d([1, -2]) * np.poly1d([1, -3])

h = (u * v - w) / t
print(h)
# quotient, remainder# (poly1d([-29.5,  28.5]), poly1d([0.]))
