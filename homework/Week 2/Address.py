
import secrets

# generate random 32 bytes as private key, cast as hex
pk = secrets.token_hex(32)
assert len(pk) == 64

pk = "0x" + pk
print("The random private key generated is: {}".format(pk))

# generate the public key using that private key

# G, generator point coordinates:
x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424

pub_key = pk * G

# use double and add algo. algo runtime O(log2n) 

def double(x, y, a, p):
    lambd = (((3 * x**2) % p ) *  pow(2 * y, -1, p)) % p
    newx = (lambd**2 - 2 * x) % p
    newy = (-lambd * newx + lambd * x - y) % p
    return (newx, newy)

def add_points(xq, yq, xp, yp, p, a=0):
    if xq == yq == None:
        return xp, yp
    if xp == yp == None:
        return xq, yq
    
    assert (xq**3 + 3) % p == (yq ** 2) % p, "q not on curve"
    assert (xp**3 + 3) % p == (yp ** 2) % p, "p not on curve"
    
    if xq == xp and yq == yp:
        return double(xq, yq, a, p)
    elif xq == xp:
        return None, None
    
    lambd = ((yq - yp) * pow((xq - xp), -1, p) ) % p
    xr = (lambd**2 - xp - xq) % p
    yr = (lambd*(xp - xr) - yp) % p
    return xr, yr


'''
Implement ECDSA from scratch

1) pick a private key
2) generate the public key using that private key (not the eth address, the public key)
3) pick message m and hash it to produce h (h can be thought of as a 256 bit number)
4) sign m using your private key and a randomly chosen nonce k. produce (r, s, h, PubKey)
5) verify (r, s, h, PubKey) is valid
 You may use a library for point multiplication, but everything else you must do from scratch
'''
