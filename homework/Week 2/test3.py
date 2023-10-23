import secrets

def point_add(P, Q, p, a=0, b=7):
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

def point_double(P, p, a=0, b=7):
    x1, y1 = P

    # Check if the point is the point at infinity
    if x1 is None:
        return None, None

    # Calculate the slope of the tangent line
    # a has impact here (coeff. of x^2)
    lambd = (3 * x1**2 + a) * pow(2 * y1, -1, p) % p

    # Calculate the new x and y coordinates
    x2 = (lambd**2 - 2 * x1) % p
    y2 = (lambd * (x1 - x2) - y1) % p
    
    # check if 2P is on the curve: y2 = x3 + 7
    assert pow(y2, 2, p) == (pow(x2, 3) + b) % p, "2P not on curve"
    return x2, y2

def double_and_add(generator_point, scalar, p, a=0):
    result = (None, None)
    binary_scalar = bin(scalar)[2:]

    for bit in binary_scalar:
        result = point_double(result, p)
        if bit == '1':
            result = point_add(result, generator_point, p)

    return result



# secp256k1 curve under mod p:
p = 2**256 - 2**32 - 977

# G, generator point of secp256k1:
x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (x, y)

res = double_and_add(G, 2, p)
print(res)



# 1. generate random 32 bytes as private key, cast as hex
pk = secrets.token_bytes(32)
assert len(pk) == 32

# cast pk to integer
scalar = int.from_bytes(pk, byteorder='big')
print("The scalar for point addition is: {}".format(scalar))

# use double and add algo. algo runtime is O(log_2 n) vs O(n)
pub_key = double_and_add(G, 5, p)
print(pub_key)