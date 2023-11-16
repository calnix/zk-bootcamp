# Problem 1

out = 5*x**3 - 4*y**2*x**2 + 13*x*y**2 + x**2 - 10*y
out - 5*x**3 + 4*y**2*x**2 + 10y - x**2 = 13*x*y**2
out - 5v3 + 4v4 + 10y - v1 = - 13x*v2

## Constraints
(x**2):      v1 = x * x
(y**2):      v2 = y * y
(x**3):      v3 = v1 * x
(y**2*x**3): v4 = v1 * v2
out - 5v3 + 4v4 + 10y - v1 = 13x * v2

There are 5 constraints and 4 intermediate variables.

## Witness matrix, w

w = | 1   |
    | out | 
    | x   |
    | y   |
    | v1  |
    | v2  |
    | v3  |
    | v4  |
    
The vector w has 8 rows, reflecting 8 variables (input, output, intermediate).

## R1CS

Dimension of R1CS: 5 rows * 8 cols

- 5 rows: 5 constraints
- 8 cols: 8 witness variables

Cw = Aw * Bw

### Matrix A
            
             [1 out x y v1 v2 v3 v4]
              [0,0,1,0,0,0,0,0],
              [0,0,0,1,0,0,0,0],
              [0,0,0,0,1,0,0,0],
              [0,0,0,0,1,0,0,0],
              [0,0,13,0,0,0,0,0]

### Matrix B

             [1 out x y v1 v2 v3 v4]
              [0,0,1,0,0,0,0,0],
              [0,0,0,1,0,0,0,0],
              [0,0,1,0,0,0,0,0],
              [0,0,0,0,0,1,0,0],
              [0,0,0,0,0,1,0,0]

### Matrix C

             [1 out x y v1 v2 v3 v4]
              [0,0,0,0,1,0,0,0],
              [0,0,0,0,0,1,0,0],
              [0,0,0,0,0,0,1,0],
              [0,0,0,0,0,0,0,1],
              [0,1,0,10,-1,0,-5,4]
              
## Problem 2

y can only be 0, 1, 2, as per the assert statement.

polynomial constraint:
    y(y - 1)(y - 2) = 0

### If-else condition

if y = 0, out = x
if y = 1, out = x^2
if y = 2, out = x^3

polynomial constraint:
    out = ax + bx^2 + c^3

#### Finding c

for y = 0 or 1:
    c = 0

for y = 2:
    c = 1

    c = y(y-1)/2

> if y=2: cx^3 = 2/2 x^3 = x^3 

#### Finding b

for y = 0 or 2:
    b = 0

for y = 1:
    b = 1

    b = -y(y-2)

> if y=1: bx^2 = -1(-1)x^2 = x^2 

#### Finding a

for y = 1 or 2:
    a = 0

for y = 0:
    a = 1

    a = (y-1)(y-2)/2

> if y=0: ax = -1(-2)/2 x = x

Therefore out = [(y-1)(y-2)/2]x + [-y(y-2)]x^2 + [y(y-1)/2]x^3

2out = [(y-1)(y-2)]x + 2[-y(y-2)]x^2 + [y(y-1)]x^3

## R1CS constraints

Convert the following into R1CS constraints:
1) y(y - 1)(y - 2) = 0
2) 2out = [(y-1)(y-2)]x - 2[y(y-2)]x^2 + [y(y-1)]x^3

From y(y - 1)(y - 2):
    y^3 - 3y^2 + 2y
(v1 = y * y)
    3v1 - 2y = (v1 * y)

From 2out = [(y-1)(y-2)]x - 2[y(y-2)]x^2 + [y(y-1)]x^3:
    2out = xy^2 - 3xy + 2x - 2x^2y^2 + 4x^2y + x^3y^3 - x^3y

(v2 = x * y)

    2out = yv2 - 3v2 + 2x - 2(v2)^2 + 4xv2 + x(v2)^2 - v2(x^2)

(v3 = v2 * x)

    2out = v2(y - 3 - 2v2 + v3) + 2x + 4v3 - xv3

(v4 = v3 * x)

    2out = v2(y - 3 - 2v2 + v3) + 2x + 4v3 - v4
    2out - 2x - 4v3 + v4 = v2 * (y - 3 - 2v2 + v3)

Constraints:
(1) [y*y]:       v1 = y * y
(2)        3v1 - 2y = v1 * y
(3)              v2 = x * y
(4)              v3 = v2 * x
(5)              v4 = v3 * x
(6) 2out - 2x - 4v3 + v4 = v2 * (y - 3 - 2v2 + v3)


w = [1, out, x, y, v1, v2, v3, v4]
    
## R1CS

Dimension of R1CS: 6 rows * 8 cols

- 6 rows: 5 constraints
- 8 cols: 8 witness variables

Cw = Aw * Bw

### Matrix A
            
             [1 out x y v1 v2 v3 v4]
              [0,0,0,1,0,0,0,0],
              [0,0,0,0,1,0,0,0],
              [0,0,1,0,0,0,0,0],
              [0,0,0,0,0,1,0,0],
              [0,0,0,0,0,0,1,0],
              [0,0,0,0,0,1,0,0]

### Matrix B

             [1 out x y v1 v2 v3 v4]
              [0,0,0,1,0,0,0,0],
              [0,0,0,1,0,0,0,0],
              [0,0,0,1,0,0,0,0],
              [0,0,1,0,0,0,0,0],
              [0,0,1,0,0,0,0,0],
              [-3,0,0,1,0,-2,1,0]

### Matrix C

             [1 out x y v1 v2 v3 v4]
              [0,0,0,0,1,0,0,0],
              [0,0,0,-2,3,0,0,0],
              [0,0,0,0,0,1,0,0],
              [0,0,0,1,0,0,1,0],
              [0,0,0,1,0,0,0,1],
              [0,2,-2,1,0,0,-4,1]




# Ignore

This approach has too many constraints

(1) [y*y]:       v1 = y * y
(2) [y(y-1)(y-2)]:  v2 = v1 * (y-2)

(3) [y(y-2)]:       v3 = y * (y-2)
(4) [(y-1)(y-2)]:   v4 = (y-1) * (y-2)
(5) [x^2]:          v5 = x * x
(6) [x^3]:

2out = [(y-1)(y-2)]x - 2[y(y-2)]x^2 + [y(y-1)]x^3
2out = v4*x - 2(v3)(v5) + v1*x^3
2out + 2(v3)(v5) - v1*x^3 = v4*x 


Constraints 1 and 2 apply to `y(y - 1)(y - 2) = 0`.
How do I ensure `v2 = 0` so tt y(y-1)(y-2) = 0?