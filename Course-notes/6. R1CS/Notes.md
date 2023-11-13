# Converting Algebraic Circuits to R1CS (Rank One Constraint System)

We explain how to turn a set of polynomial constraints into rank one constraint system (r1cs).

## Witness

The witness is a vector of dimension n x 1.
It contains:

- values of input variables
- intermediate variables
- output variable

For example, if we have the polynomial: `out = x²y`
for which we claim to know the solution for.

Which means we know x, y and out.

Because rank-1 constraint systems allow for only 1 multiplication between unknown variables, per constraint (quadratic), the polynomial above must be rewritten as:

```solidity
    
    v = x * x  
    out = v * y
```

The witness vector in this example would be: [1, out, x, y, v], such tt each term satisfies the constraints above.
>By convention, the first element is always 1 to make some calculations easier, which we will demonstrate later.

For example, [1, 18, 3, 2, 9] is a valid witness because when we plug the values in,
[constant = 1, out = 18, x = 3, y = 2, v = 9], satisfies the constraints:

```solidity
1) v = x * x => 9 == 3 * 3
2) out = v * y => 18 == 9 * 2
```
> The extra 1 term is not used in this example and is a convenience we will explain later.

### Transforming `out = x * y`

In the circuit `out = x * y`, there are no intermediate variables.

For our example, we will say we are proving 41 x 103 = 4223.
Therefore, our witness vector is [1, 4223, 41, 103], or [1, out, x, y].

Before we can create an r1cs, our polynomials and constraints need to be of the form

`result = left_hand_side × right_hand_side`

To create a valid r1cs, you need a list of variables that contain exactly one multiplication.
Our goal is to create a system of equations of the form:
Cw=Aw⋅Bw



r1cs communicates exactly the same information as a set of polynomial equations, but with a lot of extra zeros.

## Addition w/ constant

out = xy + 2

-----------------
out - 2 = x * y
Cw = Aw * Bw
-----------------

w = [1, out, x, y]
A = [0, 0, 0, 1, 0]
B = [0, 0, 0, 0, 1]
C = [-2, 1, 0, 0, 0]

This is where the `1` in the witness vector comes into play.
Addition is free => we don't have to create an additional constant when we have an addition operation.

>Rule for addition: move the terms to the output C. this applies regardless if addition /w constant or variable.

## Multiplication w/ constant

out = 2x**2 + y

-----------------
out - 2x**2 = y
Cw = Aw * Bw
-----------------

A = [0, 0, 0, 2, 0]
B = [0, 0, 0, 2, 0]
C = [0, 0, 0, 2, 0]

Addition: move the addition term to LHS

