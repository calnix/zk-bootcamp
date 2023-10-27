from py_ecc.bn128 import G1, neg, multiply

# BN128 curve: a=0, b=3
def point_add(P, Q, p, a=0, b=3):
    x1, y1 = P
    x2, y2 = Q

    # Check if either of the points is the point at infinity
    # if P == I: Q + I = Q
    if x1 is None:
        return x2, y2
    if x2 is None:
        return x1, y1

    # Check if: P + (-P) = I
    if x1 == x2 and y1 == -y2 % p:
        return None, None
    
    # check if points are on the curve: y2 = x3 + 7
    assert pow(y1, 2, p) == (pow(x1, 3) + b) % p, "P not on curve"
    assert pow(y2, 2, p) == (pow(x2, 3) + b) % p, "Q not on curve"

    # Calculate the slope of the secant line
    if x1 == x2 and y1 == y2: # P + P = 2P
        lambd = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p
    else:
        lambd = (y2 - y1) * pow(x2 - x1, -1, p) % p

    # Calculate the new x and y coordinates
    x3 = (lambd**2 - x1 - x2) % p
    y3 = (lambd * (x1 - x3) - y1) % p

    # check if point is on the curve: y2 = x3 + 7
    assert pow(y3, 2, p) == (pow(x3, 3) + b) % p, "R not on curve"

    return x3, y3

field_modulus = 21888242871839275222246405745257275088696311157297823662689037894645226208583

for i in range(1, 4):
    point = multiply(G1, i)
    print(point)
    print(neg(point))
    print('----')
    
    # x values are the same
    assert int(point[0]) == int(neg(point)[0])
    
    # y values are inverses of each other, we are adding y values
    # not ec points
    assert int(point[1]) + int(neg(point)[1]) == field_modulus



P = G1
print(f"The coords of P are {P}".format(P))

x = int(neg(G1)[0])
y = int(neg(G1)[1])
P1 = (x, y)
print(f"The coords of P1 are {P1}".format(P1))

# Point addition of inverses
res = point_add(P, P1, field_modulus)
assert res == (None, None)
print(res)


# Simple addition of y-coords
assert P[0] == P1[0], "x-values not same"
assert (int(P[1]) + int(P1[1])) == field_modulus, "y-values must add up to field modulus"




# Point addition of P and its inverse will return the identity point: point at infinity
# Adding the y-coordinates will return the field modulus
# Adding the s-coordinates will return 0.


