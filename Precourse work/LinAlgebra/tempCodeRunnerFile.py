# Exercise 5, modular arithmetic

# The challenge here is to compute the modular inverse of 5 % 1223. That is 5 * x % 1223 == 1

import numpy as np


base = 5
modulus = 1223

# Compute the modular inverse
x = pow(base, -1, modulus)

# Check if the assertion holds
assert (5 * x) % 1223 == 1

print("The modular inverse of 5 modulo 1223 is:", x)