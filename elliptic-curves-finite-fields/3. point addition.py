'''
Elliptic curve point addition/doubling
- still works over a finite field
- use the code below to verify that it does

These formulas are taken from the Wikipedia page on elliptic curve point multiplication.
'''

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
