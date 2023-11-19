# Quadratic Arithmetic Programs

A program can be represented as an R1CS, but evaluating it is not succinct due to the many operations of matrix multiplication.
QAPs are the primary reason ZK-Snarks are able to be succinct.

A Quadratic Arithmetic Program (QAP) is a system of equations where the coefficients are monovariate polynomials and a valid solution results in a single polynomial equality.
Polynomials allow us to make statements succinctly due to the Schwartz-Zippel Lemma – in a sense, we can compress a polynomial down to a single point.

## What do we achieve by converting it into the QAP form?

Instead of checking the constraints in the R1CS individually, we can now check all of the constraints at the same time by doing the dot product check on the polynomials.

*The key idea behind creating a Quadratic Arithmetic Program is as follows:*

1. Operations in R1CS (addition and Hadamard product) form an algebraic ring when viewed as a set of column vectors (why this is the case will be explained later)
2. Polynomials under addition and multiplication are rings
3. There exists an easily computable homomorphism from R1CS to polynomials

Once we have a monovariate polynomial statement with only one polynomial equality, we can evaluate it succinctly.

## Schwartz-Zippel Lemma

The Schwartz-Zippel Lemma states that if two polynomials are evaluated for the same x value, and their y values are the same, then one can be nearly certain that they are the same polynomial.

    P(X=x) = y  (some y)
    Q(X=x) = y

Therefore, P(x) == Q(x).

> Can’t we just compare their coefficients of P1 and P2? 
> Well, that would not be succinct - it would be too many steps: O(n), where n is number of terms
> we’re back to where we started doing element-wise comparison on matrices.
> Simply comparing the evaluated value is succinct cos' its just 1 step: O(1)


The goal is to prove we know Ls𝇇Rs = Os using only 3 values.

## Rings and Homomorphism

*Vectors under addition and hadamard product are a ring.*
Vectors, the way r1cs was using them, are a ring. A ring must:

1. Closed: addition or hadamard product operations on vectors return vectors of the same dimension
2. Associative, Commutative operations
3. Additive Identity: zero vector
4. Additive Inverse: vector w/ elements multiplied by -1: [1,2,3] + [-1,-2,-3] = [0,0,0]
--
5. Multiplication Inverse: Nope

Group under addition + Monoid under Multiplication => RING!
Hence, n-dimensional vectors of real numbers under the binary operators vector addition and Hadamard product are a ring.

>Weren’t we using matrix multiplication with r1cs, why are we suddenly introducing the Hadamard product?
>We will see later how we can re-write the matrix multiplication in terms of vector addition and the Hadamard product, so don’t worry about this for now.

*Polynomials under polynomial addition and polynomial multiplication are also a ring*

Under Addition:
1. Closed: duh, degree will just get larger: x * x = x^2
2. Identity: zero polynomial (0x^0)
3. Inverse: polynomial w/ opposite signs: 4x + -4x = 0x = 0
--
Under Multiplication: 
1. Closed: duh; poly * poly = polynomial
2. Identity: 1 (1 is a polynomial of degree zero)
3. Inverse: No. x * (1/x) = 1 does not count. 

For a polynomial expression, all the exponents have to be whole numbers. They cannot be negative integers.
To be specific, we are talking about polynomials with real number coefficients.

*What about scalar multiplication of vectors and polynomials?*

Scalar multiplication is shorthand for hadamard product with a vector where each entry is the scalar.

[a,b,c] * s = [a,b,c] . [s,s,s] = [as,bs,cs]

Let’s think back to our elliptic curves. Scalar multiplication there is not real multiplication – it’s just repeated addition.

For polynomials, a scalar is a degree zero polynomial, therefore multiplication by scalar:

(2x + 2) * 2 = 4x + 4

Consequently, there exists a Ring Homomorphism from column vectors of dimension n with real number elements to polynomials with real coefficients.

## A set theoretic definition of polynomial arithmetic

**The plot wAS LOST.**

## Computing the transformation function for the homomorphism

A polynomial contains an infinite amount of points, but an n-dimensional vector only encodes a finite number of points (n, to be specific). 
To make the polynomial convey the same information as a vector, we decide on n predetermined values of x whose y values will represent the elements of the original vector.

*Theorem:*
Given n points on a cartesian (x, y) plane, they can be uniquely interpolated by a polynomial of degree n - 1. 
If the degree is not constrained, an infinite number of polynomials of degree n - 1 or higher can interpolate those points.

*Example:*
A single point can be uniquely interpolated by a vertical line (a polynomial of degree zero).
Two points can be uniquely interpolated by a straight line (a polynomial of degree one). This holds for all larger degrees.

### Interpolation

Interpolating polynomials are mathematical expressions that pass through a given set of data points. 
The goal is to find a polynomial function that fits the data exactly at the specified points. 
The most common method for constructing an interpolating polynomial is the Lagrange interpolation.

### Encoding Vectors as Polynomials

If we are encoding n-dimensional vectors as polynomials, we need n predetermined points. 

Let’s say n = 3.
We will then pick the points x = 1, x = 2, and x = 3 (this is arbitrary, but those values are convenient). 

If we are trying to encode [4, 12, 6], then we want a polynomial that travels through the following cartesian points:
(1, 4), (2, 12), (3, 6)

There are a lot of algorithms for interpolating polynomial points, but lagrange interpolation is probably the most well known, so we will use that.

```python 
from scipy.interpolate import lagrange

x = np.array([1,2,3])
y = np.array([4,12,6])

polyC = lagrange(x, y)

print(polyC)
# -7x^2 + 29x - 18# check that it passes through x = {1,2,3} as expected
print(polyC(1))
# 4.0
print(polyC(2))
# 12.0
print(polyC(3))
# 6.0
```

So ultimately, we can transform the y values [4, 12, 6] into: `-7x^2 + 29x -18`

*But what about the infinite number of solutions?*
Our original vector has 3 points, but our transformation to a polynomial has infinite points. Doesn’t it seem like we are adding information that should not be there?
As long as we stick to only looking at the y values of the polynomial at x = 1,2,3, nothing changes.

Going back to our set theoretic definition, a vector can be conceptualized as a set of pairs where the first entry is the dimension and the second entry is the value. 
This is extremely similar (ahem, homomorphic) to the polynomial encoding. The “dimension” is the x value and the y value is the value of the “vector” at that dimension.

E.g.

Expressing vector [4,12,6] as (x, y):
- (1, 4)
- (2, 12)
- (3, 6)

**The “dimension” is the x value and the y value is the value of the “vector” at that dimension.**

## Showing binary operator equivalence between vectors and interpolating polynomials

>When we say “polynomials” in these subheadings, we mean “polynomials with positive degree and real coefficients whose y-values interpolate the vector at x = 1, x = 2, … x = n where n is the dimension of the vector.” 
>But to avoid being excessively verbose, we will simply say “polynomials” at the risk of offending some mathematicians.

### Adding two vectors is homomorphic to adding two polynomials

*Example:*

v1 = [1,0,1]
v2 = [-1,5,3]
v3 = v1 + v2 = [0,5,4]

Using x = 1, x = 2, x = 3 we transform v1 and v2 into their polynomial representations:

```python
import numpy as np
from scipy.interpolate import lagrange

x = np.array([1,2,3])
y_v1 = np.array([1, 0, 1])
y_v2 = np.array([-1, 5, 3])
poly_v1 = lagrange(x, y_v1)
poly_v2 = lagrange(x, y_v2)

print(poly_v1)
# 1 x^2 - 4 x + 4print(poly_v2)
#-4 x^2 + 18 x - 15

poly_v3 = poly_v1 + poly_v2

print(poly_v3)
# -3 x^2 + 14 x - 11
print([poly_v3(1), poly_v3(2), poly_v3(3)])
# [0.0, 5.0, 4.0]
```

We observe that poly_v3, the combined polynomial returns the vector v3 by subbing in x=1,2,3.
Homomorphic!

### The Hadamard product of two vectors is homomorphic to multiplying two polynomials

v1 = [1,-1,2]
v2 = [2,2,-2]
v3 = v1 . v2 = [2,-2,-4]

Using x = 1, x = 2, x = 3 we transform v1 and v2 into their polynomial representations:

```python
import numpy as np
from scipy.interpolate import lagrange

x = np.array([1,2,3])
y_v1 = np.array([1, -1, 2])
y_v2 = np.array([2, 2, -2])
poly_v1 = lagrange(x, y_v1)
poly_v2 = lagrange(x, y_v2)

print(poly_v1)
# 2.5 x^2 - 9.5 x + 8print(poly_v2)
# -2 x^2 + 6 x - 2

poly_v3 = poly_v1 * poly_v2
print(poly_v3)
# -5 x^4 + 34 x^3 - 78 x^2 + 67 x - 16
print([poly_v3(1), poly_v3(2), poly_v3(3)])
# [2.0, -2.0, -4.0]
```

### Multiplying a vector by a scalar is homomorphic to multiplying the polynomial by the same scalar

v1 = [1,-1,2]
s = 3 => [3,3,3]

v1 . [3,3,3] => [3,6,-3]

Using x = 1, x = 2, x = 3 we transform v1 into its polynomial representation:

```python
import numpy as np
from scipy.interpolate import lagrange

x = np.array([1,2,3])
y_v1 = np.array([1, 2, -1])
poly_v1 = lagrange(x, y_v1)

print(poly_v1)
# -2 x^2 + 7 x - 4

# IMPORTANT: We multiply by a constant here
poly_final = poly_v1 * 3
print(poly_final)
# -6 x^2 + 21 x - 12
print([poly_final(1), poly_final(2), poly_final(3)])
# [3.0, 6.0, -3.0]
```

## Turning matrix multiplication into the Hadamard product 

| 1  2 | | x |  = | x  + 2y | = | x  | + | 2y |
| 3  4 | | y |    | 3x + 4y |   | 3x |   | 4y |
                            
                              = |1| . |x|  + |2|.|y|
                                |3|   |x|    |4| |y|

## If Ls⊙Rs = Os can be computed with vector arithmetic, then it can be computed with polynomial arithmetic

At this point, computing Ls⊙Rs = Os in polynonmial space is obvious

1. To compute Ls, Rs, and Os we do a scalar multiplication (which is just shorthand for the Hadamard product with a repeating vector) on each column of L, R and O with the appropriate scalar value from vector s.
    > Remember s is the witness vector, which contains the input values.
2. Use Lagrange Interpolation to convert all the columns in each of the matrix into polynomials, and then add them (each column’s polynomial) up all together to get a polynomial.

*If we have U(x) = transform(Ls), V(x) = transform(Rs), and W(x) = transform (Os), then we have three polynomials U(x), V(x), and W(x).*

Because of the homomorphism, we can (with some implementation details we will get to shortly) then do:

    `U(x)V(x) = W(x)`

and now our R1CS is written as a single expression!

**I may have lost the plot**
