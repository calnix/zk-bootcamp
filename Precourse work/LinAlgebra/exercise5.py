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


'''
pow() function in Python is a built-in function used for exponentiation
- pow(base, exponent[, modulus])

1) Basic Exponentiation: 
-  pow(2, 3) would return 8 because it calculates 2^3.
-  pow(2, -3) would calculate 2^(-3), which is equivalent to 1/8.
When you call pow(base, exponent), it calculates base raised to the power of exponent without taking any modulus into account. 

2) Modular Exponentiation:
- pow(2, 3, 5)  
- Calculates 2^3 % 5, result is 3

If you provide the modulus parameter, as in pow(base, exponent, modulus), the function performs modular exponentiation. 
This means it calculates base^exponent % modulus. 

therefore,
    pow(base, -1, modulus) = pow(5, -1, 1223)
                           = 5^-1 % 1223


'''
# Python 3.7 and earlier

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    
print(modinv(5, 1223))