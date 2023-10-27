'''
Premise:

To solve the elliptic curve cyclic group:

    y² = x³ + 3 (mod 11)

obtaining (x,y) values, we need to compute sqrt(x³ + 3).


We use the Tonelli Shanks Algorithm to compute modular square roots. 
For now you can treat it as a black box that computes the mathematical square root of a field element over a modulus, or lets you know if the square root does not exist.

Example: the square root of 5 modulo 11 is 4 (4 x 4 mod 11 = 5), but there is no square root of 6 modulo 11.

Negative roots:
Square roots often have two solutions, a positive and a negative one.
Although we don’t have numbers with a negative sign in a finite field, we still have a notion of “negative numbers” in the sense of having an inverse.

To use Tonelli Shanks algo, we use libnum library.

'''

import libnum
from libnum import has_sqrtmod_prime_power

# the functions take arguments: has_sqrtmod_prime_power(n, field_mod, k), where n**k,
# but we aren't interested in powers in modular fields, so we set k = 1
# n is what you are trying to sqrt, while field_mod is the modulus.

# check if sqrt(8) mod 11 exists
print(has_sqrtmod_prime_power(8, 11, 1))
# False

# check if sqrt(5) mod 11 exists
print(has_sqrtmod_prime_power(5, 11, 1))
# True

# compute sqrt(5) mod 11
print(list(libnum.sqrtmod_prime_power(5, 11, 1)))
# [4, 7]

result = list(libnum.sqrtmod_prime_power(5, 11, 1))
print("The square roots of 5 mod(11) is: {}".format(result))

# Both roots raised to the power of 2, return 5 under mod 11
assert (4 ** 2) % 11 == 5
assert (7 ** 2) % 11 == 5

# Roots are inverse of each other.
# we expect 4 and 7 to be inverses of each other, because in "regular" math, the two solutions to a square root are sqrt and -sqrt
assert (4 + 7) % 11 == 0