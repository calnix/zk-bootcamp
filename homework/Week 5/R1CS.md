# Problem 1

out = 5*x**3 - 4*y**2*x**2 + 13*x*y**2 + x**2 - 10*y
out - 5*x**3 + 4*y**2*x**2 - 13*x*y**2 - x**2 = - 10y

## Constraints
(x**2): v1 = x * x
(y**2): v2 = y * y
(5x**3): v3 = 5x * v1
(4y**2*x**3): v4 = 4v1 * v2
(13xy**2): v5 = 13x * v2
out - v3 + v4 - v5 - v1 = - 10y

There are 6 six constraints.

## Witness matrix, w

w = | 1   |
    | out | 
    | x   |
    | y   |
    | v1  |
    | v2  |
    | v3  |
    | v4  |
    | v5  |

The vector w has 9 rows, reflecting 9 variables (input, output, intermediate). 

## R1CS

Dimension of R1CS: 6 rows * 9 cols

- 6 rows: 6 constraints
- 9 cols: 9 witness variables

Cw = Aw * Bw


       | 1  out  x  y  v1  v2  v3  v4  v5  |
(1)    | 0   0   0  0  1   0   0           |   
(2)    |                   1               |     =   
(3)    |
(4)    |
(5)    |
(6)    |

## Problem 2

###  represent the assert statement as a polynomial:
assert:    y = 0, 1, 2

y = 0, return x
y = 1, return x**2
y = 2, return x**3

polynomial constraint:
    y(y - 1)(y - 2) = 0


R1CS constraint:
v1 = y * (y-1)
v2 = v1 * (y-2)
v3 = v1 * v2

out = x(y - 1)(y - 2) + x**2(y - 2)(y) + x**3(y)(y - 1)

for y = 0,
    out = x(-1)(-2) = 2x



