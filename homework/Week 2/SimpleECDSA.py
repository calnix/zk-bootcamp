import secrets
import hashlib
import hmac
import sys, random

#  y^2 = x^3 + ax + b mod p
class EllipticCurve():
    def __init__(self, a, b, p, n, x, y):
        # coeff., order, modulus
        self.a = a
        self.b = b
        self.p = p
        self.n = n
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

    def double_and_add(self, point, scalar):
        
        assert self.is_on_curve(point), "point not on curve"
        assert scalar > 0 and scalar % curve.p, "invalid scalar"

        result = None
        current = point

        # Optimized approach using binary expansion
        while scalar:
            if scalar & 1:  # same as scalar % 2
                result = self.add(result, current)
                
            current = self.double(current) 
            scalar >>= 1  # same as scalar / 2

        assert self.is_on_curve(result)
        return result

# secp256k1 curve under mod p:
p= 0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffefffffc2f
# in decimal n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
n = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141 
# Curve coefficients:
a=0
b=7
# G, generator point:
x = 0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798
y = 0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8

# convert to integers
p = int(p)
n = int(n)
x = int(x)
y = int(y)

# secp256k1: y^2 = x^3 + 7:
curve = EllipticCurve(a, b, p, n, x, y)

# Sanity checks
G = (x, y)
q1 = curve.add(G, G)
q2 = curve.double(G)
q3 = curve.double_and_add(G, 2)

#print(f"q1: {q1}\n q2:{q2}\n q3:{q3}".format(q1, q2, q3))
assert q1 == q2 == q3, "something wrong w/ point_double and double_and_add"

q1 = curve.double(curve.double(G))
q2 = curve.double_and_add(G, 4)
assert q1 == q2, "something wrong w/ point_double and double_and_add"

#    /*//////////////////////////////////////////////////////////////
#                          GENERATE KEY PAIR
#    //////////////////////////////////////////////////////////////*/

# 1. Generate privKey: random integer, k btw [1, n-1], where n is the order of curve
# 2. Generate the public key:  s * G
#    use double and add algo; runtime is O(log_2 n) vs O(n) if you repeatedly add in loop

def generate_keys(curve):
    n = curve.n
    G = curve.G

    if not isinstance(n, int) or n <= 1:
        raise ValueError("n must be an integer greater than 1")

    # generate random integer in [0, n-2]: 
    # add 1 to ensure that the generated number is in the range [1, n-1]
    priv_key:int = random.randint(1, n-1)
    assert priv_key < n, "pk > n"

    pub_key = curve.double_and_add(G, priv_key) 

    return priv_key, pub_key

priv_key, pub_key = generate_keys(curve)
print("The scalar for point addition is: {}".format(priv_key))
print("The public key: {}".format(pub_key))


#    /*//////////////////////////////////////////////////////////////
#                           HASH THE MESSAGE, h
#    //////////////////////////////////////////////////////////////*/

# 3. pick message m and hash it to produce h (h can be thought of as a 256 bit number)

# Encode the message as bytes
message = "struct{orderType:buy, address:0x1234, amount:10}"

def generate_hash(message, p):
    # convert to string and encode to bytes
    message_str = str(message)
    message_bytes = message_str.encode('utf-8')
    
    # Hash the message using SHA-256 
    h_hex = hashlib.sha256(message_bytes).hexdigest()
    assert len(h_hex) == 64                                 # Assert that the hash is 256 bits (64 hex chars)
    print("The SHA256 hash digest in hex: {}".format(h_hex))
    
    #
    h_int = int(h_hex, 16)
    
    return h_int

h:int = generate_hash(message, p)


#    /*//////////////////////////////////////////////////////////////
#                  SIGN MESSAGE WITH PRIVATE KEY AND K
#    //////////////////////////////////////////////////////////////*/

# 4. sign m using your private key and a randomly chosen nonce k. 
# produce (r, s, h, PubKey)

def sign_message(curve, h, priv_key: int):
    
    r = 0
    s = 0
    while r == 0 or s == 0:
        # generate random nonce k
        k = random.randint(1, n-1) # nonce
        
        # R = k * G | take its x-coordinate: r = R.x
        R = curve.double_and_add(G, k)
        r = R[0] % n
        # generate s, the signature proof:  
        # s = k^-1 * (h + r * privKey) (mod p)
        # k^-1 which is the ‘modular multiplicative inverse‘ of k
        s = (pow(k, -1, n) * (h + (r * priv_key))) % n
        assert s < p, "s is not smaller than p"

    return r, s

r, s = sign_message(curve, h, priv_key)

print("The x-coord of R, r is: {}".format(r))
print("The signature proof, s is: {}".format(s))

#    /*//////////////////////////////////////////////////////////////
#                        VERIFYING THE SIGNATURE
#    //////////////////////////////////////////////////////////////*/

def verify(message, r, s, pub_key, n) -> int:
    
    # hash the received message
    h_int:int = generate_hash(message, n)
    
    # mod_inv of sig. proof, s
    s_inv = pow(s, -1, n)

    # recover the random EC point, R
    u1 = (s_inv * h_int) % n
    u2 = (s_inv * r) % n

    # point multiplication
    res_1 = curve.double_and_add(G, u1)
    res_2 = curve.double_and_add(pub_key, u2)
    
    # point addition: u1*G + u2*PubKey
    R = curve.add(res_1, res_2)

    # extract recovered x-coord
    r_recovered = R[0] % n

    assert r_recovered == r, "signature validation failed"

    return r_recovered

# signature validation
r_recovered = verify(message, r, s, pub_key, n)

print(r_recovered)
print(r)



