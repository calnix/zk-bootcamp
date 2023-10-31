from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq, curve_order 

p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
n = curve_order
print(p - n)    #147946756881789318990833708069417712966
assert( n != p, "n vs p")

# a + b = c => 1 + 4 = 5
a = 1
b = 1
c = a + b

# c = num/den (n + 1 / 2)
# a + b = c => a + b = num/den
num = 2*(p + 1)
den = p

assert(c == num/den, "num/den")

# bn128 curve:  y^2 = x^3 + 3 (mod p)

print(G1)
# (1, 2)

A = multiply(G1, a)
B = multiply(G1, b)
C = multiply(G1, c)

assert add(A, B) == C, "A+B != C"

#given A,B, num, den:

# set mod
m = n

# scalar = num * den-1
inv_den = pow(den, -1, m)
scalar = (num * den) % m

C_prime = multiply(G1, c)

assert C == C_prime, "verification fails"
print("all good")