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

def double_and_add(P, scalar, p, a=0, b=7):
    x1, y1 = P

    if scalar == 0:
        raise "InvalidScalarError"

    current = P
    result = (None, None)

    # Optimized approach using binary expansion
    while scalar:
        if scalar & 1:  # same as scalar % 2
            result = point_add(result, current, p)
        current = point_double(current, p) 
        scalar >>= 1  # same as scalar / 2

    # check if point is on the curve: y2 = x3 + 7
    x2, y2 = result
    assert pow(y2, 2, p) == (pow(x2, 3) + b) % p, "kP not on curve"

    return result

#  y^2 = x^3 + ax + b mod p
class EllipticCurve():
    def __init__(self, a, b, p, x, y):
        # coeff and modulus
        self.a = a
        self.b = b
        self.p = p
        # generator point
        self.x = x
        self.y = y
        self.G = (x, y)
    
    def is_on_curve(self, point):
        if point is None:
            return True
    
        x, y = point
        return (y**2 % self.p) == (x**3 + self.a * x + self.b) % self.p
    
    def add(self, point1, point2):
        if not self.is_on_curve(point1) or not self.is_on_curve(point2):
            raise Exception("Invalid result")
        
        if point1 is None:
            return point2
        if point2 is None:
            return point1
        x1, y1 = point1
        x2, y2 = point2

        # vertical
        if x1 == x2 and y1 + y2 == 0 :
            return None  # Identity element
        if point1 == point2:
            return self.double(point1)
        else:
            if x1 == x2:
                return None   # Identity element
            m = (y2 - y1) * pow(x2 - x1, -1, self.p)

        x3 = (m**2 - x1 - x2) % self.p
        y3 = (m * (x1 - x3) - y1) % self.p

        return (x3, y3)
    
    def double(self, point):
        if not self.is_on_curve(point):
            raise Exception("Invalid result")
        
        if point is None:
            return None  # Identity element
        x1, y1 = point
        if y1 == 0:
            return None  # Identity element

        # s = (3 * x1^2 + a) / (2 * y1) mod p
        numerator = pow(x1, 2, self.p) * 3 + self.a
        denominator = (y1 * 2) % self.p
        s = (numerator * pow(denominator, -1, self.p)) % self.p

        x3 = (pow(s, 2, self.p) - x1 - x1) % self.p
        y3 = (s * (x1 - x3) - y1) % self.p

        return (x3, y3)

    def scalar_mul(self, point, scalar):
        
        assert self.is_on_curve(point), "point not on curve"
        assert scalar > 0 and scalar % curve.p, "invalid scalar"

        result = None
        addend = point

        # Optimized approach using binary expansion
        while scalar:
            if scalar & 1:  # same as scalar % 2
                result = point_add(result, current, p)
                
            current = point_double(current, p) 
            scalar >>= 1  # same as scalar / 2

        assert self.is_on_curve(result)
        return result


# secp256k1 curve under mod p:
p= 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
# Curve coefficients.
a=0
b=7
# G, generator point:
x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

# convert to integers
p = int(p)
x = int(x)
y = int(y)

# secp256k1: y^2 = x^3 + 7:
curve = EllipticCurve(a, b, p, x, y)

# sanity check
G = (x, y)
q1 = curve.add(G, G)
q2 = curve.double(G)
q3 = double_and_add(G, 2, p)

print(f"q1: {q1}\n q2:{q2}\n q3:{q3}".format(q1, q2, q3))
assert q1 == q2 == q3, "something wrong w/ point_double and double_and_add"

q1 = point_double(point_double(G, p), p)
q2 = double_and_add(G, 4, p)
assert q1 == q2, "something wrong w/ point_double and double_and_add"

#    /*//////////////////////////////////////////////////////////////
#                          GENERATE PRIVATE KEY
#    //////////////////////////////////////////////////////////////*/

# 1. generate random 32 bytes as private key, cast as hex

def generate_priv_key():
    priv_key_bytes = secrets.token_bytes(32)
    assert len(priv_key_bytes) == 32

    # Convert the bytes to a hexadecimal string
    private_key_hex = priv_key_bytes.hex()
    print("The private key in hex is: {}".format(private_key_hex))

    # convert to int
    priv_key_int = int(private_key_hex, 16)    
    return priv_key_int, priv_key_bytes

priv_key_int, priv_key_bytes = generate_priv_key()
print("The scalar for point addition is: {}".format(priv_key_int))

#    /*//////////////////////////////////////////////////////////////
#                             GET PUBLIC KEY
#    //////////////////////////////////////////////////////////////*/

# 2. Generate the public key 
# use double and add algo. algo runtime is O(log_2 n) vs O(n)
pub_key = curve.scalar_mul(curve.G, priv_key_int)
print("The public key: {}".format(pub_key))

#    /*//////////////////////////////////////////////////////////////
#                           HASH THE MESSAGE, h
#    //////////////////////////////////////////////////////////////*/

# 3. pick message m and hash it to produce h (h can be thought of as a 256 bit number)

# Encode the message as bytes
#message = "struct{orderType:buy, address:0x1234, amount:10}"
message = 4

def generate_hash(message, n):
    # convert to string and encode to bytes
    message_str = str(message)
    message_bytes = message_str.encode('utf-8')
    
    # Hash the message using SHA-256 
    h_hex = hashlib.sha256(message_bytes).hexdigest()
    assert len(h_hex) == 64                                 # Assert that the hash is 256 bits (64 hex chars)
    print("The SHA256 hash digest in hex: {}".format(h_hex))

    # Ensure the hash value is less than order of curve
    h_int = int(h_hex, 16)
    message_hash = pow(h_int, 1, n-1)
    message_hash += 1

    return h_int

h_int = generate_hash(message, p)


#    /*//////////////////////////////////////////////////////////////
#                  SIGN MESSAGE WITH PRIVATE KEY AND K
#    //////////////////////////////////////////////////////////////*/

# 4. sign m using your private key and a randomly chosen nonce k. produce (r, s, h, PubKey)

# generate random number K: Calculate via HMAC using h_bytes and priv_key_bytes
#h_bytes = bytes.fromhex(h_hex)
#k_hex = hmac.new(priv_key_bytes, h_bytes, hashlib.sha256).hexdigest()

# sanity check on k
#k_int = int(k_hex, 16)
#assert k_int < p, "k > p"
#print("The random number, k is: {}".format(k_int))

k_int = 38

# generate random point R: k * G and take its x-coordinate: r = R.x
R = curve.scalar_mul(G, k_int)
r = R[0]           
print("The x-coord of R, r is: {}".format(r))


# generate s, the signature proof:  s = k^-1 * (h + r * privKey) (mod p)
# k^-1 which is the ‘modular multiplicative inverse‘ of k
s = (pow(k_int, -1, p) * (h_int + (r * priv_key_int))) % p
assert s < p, "s is not smaller than p"
print("The signature proof, s is: {}".format(s))

sig = (r, s)


#    /*//////////////////////////////////////////////////////////////
#                        VERIFYING THE SIGNATURE
#    //////////////////////////////////////////////////////////////*/

def verify(message, r, s, pub_key, p) -> int:
    
    # hash the received message
    h_int = generate_hash(message, p)
    
    # mod_inv of sig. proof, s
    s_inv = pow(s, -1, p)

    # recover the random EC point, R
    u1 = pow(s_inv * h_int, 1, p)
    u2 = pow(s_inv * r, 1, p)

    # point multiplication
    res_1 = curve.scalar_mul(G, u1)
    res_2 = curve.scalar_mul(pub_key, u2)
    
    # point addition: u1*G + u2*PubKey
    R = curve.add(res_1, res_2)

    # extract recovered x-coord
    r_recovered = R[0]

    assert r_recovered == r, "signature validation failed"

    return r_recovered

# signature validation
r_recovered = verify(message, r, s, pub_key, p)

print(r_recovered)
print(r)



