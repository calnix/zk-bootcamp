# Under mod p
from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq, curve_order 

p = 21888242871839275222246405745257275088696311157297823662689037894645226208583
n = curve_order

a = 1
b = 1
c = 2

num = 2
den = 1

A = multiply(G1, a)
B = multiply(G1, b)
C = multiply(G1, c)

print("A is: {}", A)
print("B is: {}", B)
print("C is: {}", C)

print("num is: {}", num)
print("den is: {}", den)
