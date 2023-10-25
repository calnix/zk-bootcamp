import random
import hashlib

# Using secp256k1 parameters
a = 0
b = 7
p = 2**256 - 2**32 - 977
G = (0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798, 
     0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8)
# in decimal n = 115792089237316195423570985008687907852837564279074904382605163141518161494337

n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 # in hex

def inverse_mod(k, p):
    """ Return the modular inverse of k modulo p."""
    if k == 0:
        raise ZeroDivisionError('division by zero')
    if k < 0:
        return p - inverse_mod(-k, p)
    return pow(k, p - 2, p)

def point_add(point1, point2):
    """ Elliptic curve point addition. """
    x1, y1 = point1
    x2, y2 = point2
    
    if x1 == x2 and y1 == y2:
        m = (3 * x1 * x1) * inverse_mod(2 * y1, p)
    else:
        m = (y2 - y1) * inverse_mod(x2 - x1, p)

    x3 = m*m - x1 - x2
    y3 = m*(x1 - x3) - y1
    return (x3 % p, y3 % p)

def point_mul(point, scalar):
    """ Elliptic curve point multiplication. """
    result = None
    addend = point
    while scalar:
        if scalar & 1:
            if result is None:
                result = addend
            else:
                result = point_add(result, addend)
        addend = point_add(addend, addend)
        scalar >>= 1
    return result

def generate_keypair():
    d = random.randint(1, n-1)
    Q = point_mul(G, d)
    return d, Q

def hash(message):
    return hashlib.sha256(message).digest()

def sign_message(d, message):
    z = int.from_bytes(hash(message), 'big')
    r = 0
    s = 0
    while not r or not s:
        k = random.randint(1, n-1) # nonce
        P = point_mul(G, k)
        r = P[0] % n
        s = (inverse_mod(k, n) * (z + r * d)) % n
    return r, s

def verify_signature(pubkey, message, signature):
    r, s = signature
    z = int.from_bytes(hash(message), 'big')
    
    w = inverse_mod(s, n)
    u1 = (z * w) % n
    u2 = (r * w) % n
    
    P = point_add(point_mul(G, u1), point_mul(pubkey, u2))
    return r == P[0] % n

private_key, public_key = generate_keypair()
print(private_key, public_key)
message = b"Hello, there"
signature = sign_message(private_key, message)
is_valid = verify_signature(public_key, message, signature)
print("Signature valid?", is_valid)