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
out - y = 2x**2
Cw      = Aw * Bw

note: A * B => 2 * x**2
-----------------

w = [1, out, x, y]
A = [0, 0, 0, 2, 0]     //representing 2x
B = [0, 0, 0, 1, 0]     //representing x
C = [0, 1, 0, 0, -1]    //representing out - y  

As a general rule:
The number of constraints in a rank one constraint system should be equal the number of non-constant multiplications.

## Larger example

out = 3(x^2)y + 5xy - x - 2y + 3

Break it up into the following constraints:

v1 = 3x * x
v2 = v1 * y
-v2 + x + 2y - 3 + out = 5xy

> Note how all the addition terms have been moved to the left. Leaving the right hand side as 5xy in the third row is arbitrary. 

We could divide both sides by 5 and have the final constraint be: -v2/5 + x/5 + 2y/5 - 3/5 + out/5 = xy.
This doesn’t change the witness however, so both are valid.

R1CS dimension:
    3 constraints => 3 rows
    6 witness elements => 6 cols

w = [1, out, x, y, v1, v2]

A = [0, 0, 0, 3, 0, 0, 0]
    [0, 0, 0, 0, 0, 1, 0]
    [0, 0, 0, 5x, 0, 0, 0]

B = [0, 0, 0, 1, 0, 0, 0]
    [0, 0, 0, 0, 1, 0, 0]
    [0, 0, 0, 0, 1, 0, 0]

C = [0, 0, 0, 0, 0, 1, 0]
    [0, 0, 0, 0, 0, 0, 1]
    [-3, 1, 1, 2, 0, -1]

## Everything is done modulo prime in r1cs

In the above examples, we used traditional arithmetic for the sake of simplicity, but real world implementations use modular arithmetic instead.
The reason is simple: encoding numbers like 2/3 leads to ill-behaved floats which are computationally intensive and error prone.

If we do all our math modulo a prime number, then encoding 2/3 is straightforward.
It’s the same as 2 * 3^-1, and multiplying by two and raising to the power of negative 1 are straightforward in modular arithmetic.

### Example

```python
p = 23

# 2 * 3^-1 mod p
two_thirds = 2 * pow(3, -1, p)

assert (two_thirds * 3) % p == 2

# ⅓ = 3 * 1^-1
one_third = pow(3, -1, p)

# check that ⅓ + ⅔ == 1 mod p
assert (two_thirds + one_third) % p == 1

```

## Circom implementation

In Circom (and many other frameworks), math is done modulo 21888242871839275222246405745257275088548364400416034343698204186575808495617.

If we write out = x * y in Circom, it would look like the following:

```rust
pragma circom 2.0.0;

template Multiply2() {
    signal input x;
    signal input y;
    signal output out;

    out <== x * y;
 }

component main = Multiply2();
```

Let’s turn this into an r1cs file and print the r1cs file:

```bash 
circom multiply2.circom --r1cs --sym
snarkjs r1cs print multiply2.r1cs
```

rest: https://www.rareskills.io/post/rank-1-constraint-system

## Rank One Constraint Systems are for convenience

The original papers for pinocchio and groth16 don’t have any reference to the term rank one constraint system. 
R1CS is handy from an implementation perspective, but from a pure math perspective, it is simply explicitly labeling and grouping the coefficients of different variables. 
So when you read academic papers on the subject, it is usually missing because it is an implementation detail of a more abstract concept.