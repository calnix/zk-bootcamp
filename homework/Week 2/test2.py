import secrets


# 1. generate random 32 bytes as private key, cast as hex
pk = secrets.token_bytes(32)
assert len(pk) == 32

# cast pk to integer
scalar = int.from_bytes(pk, byteorder='big')
print("The scalar for point addition is: {}".format(scalar))

# Convert the integer to a hexadecimal string
pk_hex = hex(scalar)[2:]  # Remove the '0x' prefix

print("The random private key generated is: {}".format(pk_hex))

# 2. generate the public key using that private key

def point_double(P, p, a=0, b=7):
    # check for the zero point 
    if P is None: 
        return None
    
    x, y = P
        
    # a has impact here
    lambd = (((3 * x**2 + a) % p ) *  pow(2 * y, -1, p)) % p
    
    newx = (lambd**2 - 2 * x) % p
    newy = (-lambd * newx + lambd * x - y) % p
    
    assert pow(newy, 2, p) == (pow(newx, 3) + b) % p, "2P not on curve"
    return (newx, newy)

# For curve: y^2 = x^3 + a
def point_add(P, Q, p, a=0, b=7):
    xp, yp = P
    xq, yq = Q

    # Q + I = Q, (if P == I)
    if P is None or Q is None: # check for the zero point 
        return P or Q
    
    if P == Q: # P + P = 2P
        return point_double(Q, p, a, b)
    elif xq == xp and yp == -yq: 
        # P + (-P) = I
        return (None, None)

    # assert closure
    assert pow(yq, 2, p) == (pow(xq, 3) + b) % p, "Q not on curve"
    assert pow(yp, 2, p) == (pow(xp, 3) + b) % p, "P not on curve"
       
    lambd = ((yq - yp) * pow((xq - xp), -1, p) ) % p
    xr = (lambd**2 - xp - xq) % p
    yr = (lambd*(xp - xr) - yp) % p
    return xr, yr

def double_and_add(generator_point, scalar, p):
    # Initialize the result to the point at infinity (0, 0)
    result_x, result_y = None, None
    
    # Convert the scalar to its binary representation
    binary_scalar = bin(scalar)[2:]  # Remove the '0b' prefix
    
    # Iterate through the binary representation of the scalar
    for bit in binary_scalar:
        result = point_double(result, p)  # Double the result point
        
        if bit == '1':
            result = point_add(result, generator_point, p)  # Add the generator point if the bit is 1
    
    return result


# secp256k1 curve under mod p:
p = 2**256 - 2**32 - 977

# G, generator point of secp256k1:
x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
G = (x, y)
assert pow(y, 2, p) == (pow(x, 3) + 7) % p

#
print("...")
print(point_double(G, p))
print("...")

Q = point_double(G, p)
x = Q[0]
y = Q[1]
assert pow(y, 2, p) == (pow(x, 3) + 7) % p

print("...")
R = point_add(G, Q, p)
x = R[0]
y = R[1]
assert pow(y, 2, p) == (pow(x, 3) + 7) % p
print(R)
print("...")


double_and_add(G, 2, p)



