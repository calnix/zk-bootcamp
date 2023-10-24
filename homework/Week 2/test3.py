import secrets
import hashlib
import hmac

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
priv_key_bytes = secrets.token_bytes(32)
assert len(priv_key_bytes) == 32

# Convert the bytes to a hexadecimal string
private_key_hex = priv_key_bytes.hex()
print("The private key in hex is: {}".format(private_key_hex))

# convert to int
priv_key_int = int(private_key_hex, 16)    
print("The scalar for point addition is: {}".format(priv_key_int))

# 2. Generate the public key 
# use double and add algo. algo runtime is O(log_2 n) vs O(n)
pub_key = double_and_add(G, priv_key_int, p)
print("The public key: {}".format(pub_key))



# 3. pick message m and hash it to produce h (h can be thought of as a 256 bit number)

# Encode the message as bytes
message = "struct{orderType:buy, address:0x1234, amount:10}"
message_bytes = message.encode('utf-8')

# hash message
digest = hashlib.sha256(message_bytes).hexdigest()
# Assert that the hash is 256 bits (64 hex chars)
assert len(digest) == 64
print("The SHA256 hash digest: {}".format(digest))



#    /*//////////////////////////////////////////////////////////////
#                  SIGN MESSAGE WITH PRIVATE KEY AND K
#    //////////////////////////////////////////////////////////////*/
# 4. sign m using your private key and a randomly chosen nonce k. produce (r, s, h, PubKey)

# generate random number K

# Convert the digest to bytes
digest_bytes = bytes.fromhex(digest)

# Calculate the HMAC using digest_bytes and privKey
k = hmac.new(priv_key_bytes, digest_bytes, hashlib.sha256).digest()

# k in hexadecimal format
k_hex = k.hex()
print(k_hex)

# generate random point R: k * G and take its x-coordinate: r = R.x
k_integer = int.from_bytes(k, byteorder='big')
assert k_integer < p, "k is not smaller than p"

R = double_and_add(G, k_integer, p)

# x-coord of r
r = R[0]
print(r)

# generate s, the signature proof:  s = k^-1 * (h + r * privKey) (mod p)
# k^-1 which is the ‘modular multiplicative inverse‘ of k
# 

digest_int = int.from_bytes(digest_bytes, byteorder='big')

s = pow(k_integer, -1, p) * (digest_int + (r * priv_key_int)) % p
assert s < p, "s is not smaller than p"
print(s)

sig = (r, s)

#    /*//////////////////////////////////////////////////////////////
#                        VERIFYING THE SIGNATURE
#    //////////////////////////////////////////////////////////////*/

# Verifier will receive the cleartext message and sig (not hiding anything, just providing auth)
# The idea of signature verification is to recover the point R' using the public key,
# and check whether it is same point R, generated randomly during the signing process.

# input: sig(r,s) & message

#1. hash the message
#2. Calculate the modular inverse of the signature proof: s1 = mod_inv(s)
#3. Recover the random point used during the signing: R' = [(h * s1) * G] + [(r * s1) * pubKey]
#       u1 = s1 * h (mod p)
#       u2 = s1 * r (mod p)
#4. Take from R' its x-coordinate: r' = R'.x
#5. Calculate the signature validation result by comparing whether r' == r

def verify(message, sig, generator_point, pub_key, p):
    r,s = sig[0], sig[1]

    # convert to bytes and hash the message
    message_bytes = message.encode('utf-8')
    message_hash = hashlib.sha256(message_bytes).digest() #binary

    # mod_inv of sig. proof, s
    s_inv = pow(s, -1, p)
    
    # recover the random EC point, R
    h = int.from_bytes(message_hash, byteorder='big')
    u1 = (s_inv * h) % p
    u2 = (s_inv * r) % p
    
    # u1*G + u2*PubKey
    R = double_and_add(generator_point, u1, p) + double_and_add(pub_key, u2, p)

    # extract recovered x-coord
    r_recovered = R[0]

    # signature validation
    print(r_recovered)
    print(r)
    assert r_recovered == r, "signature validation failed"

    return r_recovered



verify(message, sig, G, pub_key, p)

