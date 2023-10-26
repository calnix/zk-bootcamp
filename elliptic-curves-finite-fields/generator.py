# Point addition as per wikipedia
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
Every elliptic curve point in a cyclic group has a “number”
A cyclic group, by definition, can be generated by repeatedly adding the generator to itself.

Let’s use a real example of y² = x³ + 3 (mod 11) with the generator point being (4, 10).

Using the python functions above, we can start with the point (4, 10) and generate every point in the group:
'''

# for our purposes, (4, 10) is the generator point G
next_x, next_y = 4, 10
print(0, 4, 10)

points = [(next_x, next_y)]

for i in range(1, 14):
    # repeatedly add G to the next point to generate all the elements
    next_x, next_y = add_points(next_x, next_y, 4, 10, 11)
    print(i, next_x, next_y)
    points.append((next_x, next_y))

'''
Result:
-------
0  4 10
-------
1  7 7
2  1 9
3  0 6
4  8 8
5  2 0
6  8 3
7  0 5
8  1 2
9  7 4
10 4 1
11 None None    
-------------
12 4 10     (overflow)

Under mod 11, the field has an order of 11. (p = 11)
We can plug in 11 field elements (x-values) from [0, 10] into the curve equation.

There would be a max of 11 EC points, excluding the identity; point at infinity is not included.

Since all the x-values yield a solutions; this means that the curve has a total of 11 + 1 = 12 points. 
Curve has an order of 12. (n = 12)

> Here “None” means the point at infinity. 

Observe that (order + 1)G = G. Just like modular addition, when we “overflow”, the cycle starts over.
-> (12 + 1)G = 13G = G 

By multiplying the generator element, G by integers [1, 12], we get all 12 points of the curve.
'''

#%%
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
        #assert scalar > 0 and scalar % curve.p, "invalid scalar"

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
p = 11
n = 12 
# Curve coefficients:
a=0
b=3
# G, generator point:
x = 4
y = 10

# y^2 = x^3 + 7 mod 11
curve = EllipticCurve(a, b, p, n, x, y)

# Sanity checks
G = (x, y)

res = curve.double_and_add(G, 10)
print("10G: {}".format(res))

res = curve.double_and_add(G, 11)
print("11G: {}".format(res))

res = curve.double_and_add(G, 12)
print("12G: {}".format(res))

res = curve.double_and_add(G, 13)
print("13G: {}".format(res))

res = curve.double_and_add(G, 14)
print("14G: {}".format(res))


# %%
'''
 We can assign each point a “number” based on how many times we added the generator to itself to arrive at that point.
 We can use the following code to plot the curve and assign a number next to it.
'''
import libnum
import matplotlib.pyplot as plt

def generate_points(mod):
    xs = []
    ys = []

    def y_squared(x):
        return (x**3 + 3) % mod

    for x in range(0, mod):
        if libnum.has_sqrtmod_prime_power(y_squared(x), mod, 1):
            square_roots = libnum.sqrtmod_prime_power(y_squared(x), mod, 1)

            # we might have two solutions 
            for sr in square_roots:
                ys.append(sr)
                xs.append(x)
    return xs, ys

xs11, ys11 = generate_points(11)

fig, (ax1) = plt.subplots(1, 1);
fig.suptitle('y^2 = x^3 + 3 (mod 11)');
fig.set_size_inches(13, 6);

ax1.set_title("modulo 11")
ax1.scatter(xs11, ys11, marker='o');
ax1.set_xticks(range(0,11));
ax1.set_yticks(range(0,11));
ax1.grid()

for i in range(0, 11):
    plt.annotate(str(i+1), (points[i][0] + 0.1, points[i][1]), color="red");


''''
The red text can be thought of as starting with the identity element, and how many times we added the generator to it.

# Point inverses are still vertically symmetric
Here is an interesting observation: note that points that share the same x-value add up to 11, which corresponds to the identity element (12 mod 11 = 0).

'''

# %%
