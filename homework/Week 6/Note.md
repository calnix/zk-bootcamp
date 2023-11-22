https://almondine-song-c43.notion.site/Homework-6-QAP-9142687e4ff94bda967f088a36cff41d

## Problem 1

    function verify(uint256[] calldata L, uint256[] calldata R, uint256[] calldata O, uint256[] calldata s, uint256 n, uint256 m) external view returns(bool)

1. Form of the function
2. Do proving + verification in SC or,
3. Python for proving and supply output into smart contract?

## Problem 2

Why does an R1CS require exactly one multiplication per row?
How does this relate to bilinear pairings?

*Answer:*

### Why does an R1CS require exactly one multiplication per row?

R1CS requires exactly 1 multiplication per row, so that the constraints can be expressed in the matrix form: Cw = Aw * Bw, where each row is a single contraint.
Adhering to the `Cw = Aw * Bw` form is useful to us as it allows us to apply bilienear pairings.

If there are multiple multiplications per row, the resulting form would be: Cw = Aw * Bw * ...
We would not be able to constructively apply bilinear pairings in this case.

> If we have more than 1 multiplication per row, we would not be able to apply a bilinear mapping between G1 and G2 to G12.
> Without a bilinear mapping we cannot turn this into a ZKP.

### How does this relate to bilinear pairings?

The application of bilinear pairings is important, as it transforms a standard R1CS into a ZK-R1CS.

In Cw = Aw * Bw, we can prove to a verifier that we have a valid vector w by simply providing it; a vector of values.
However, the input values are not obfuscated and therefore this is not a ZKP.

We achieve obfuscation via elliptic curve points - specifically using the generator points.

Aw * Bw = Cw   =>  L(sG1) 𝇇 R(sG2) = O(sG12)

The witness vector w is encrypted via the multiplication with generator points G1, G2.
The prover generates a proof by executing the LHS: L(sG1) 𝇇 R(sG2)

E.g.:
    // hamadard multiplication
    L(sG1) 𝇇 R(sG2) = [kG1 * hG2]  =  [pairing(kG1, hG2)]     
                      [mG1 * nG2]     [pairing(mG1, nG2)]  

The resulting proof is column vector of pairings. Each constraint is reduced to a bilinear pairing of G1 and G2 points to some G12 point.
This vector can be freely communicated over public channels without any concern of information leakage as per the discrete log problem.
This is now a ZKP.
> Discrete log problem: sG1 = P, given P and G1, there exists no computationally efficient method to find the discrete log, s.

*Verification Step*

In the last step, the verifier will check that O(sG12) == the submitted proof. Theoratically, this is what happens:
First the verifier will compute O(sG1) and then pairing(OsG1, 1*G2)

1) O(sG1):

        [5, 6]|xG1|  =  [5xG1 + 6yG1]
        [7, 8]|yG1|     [7xG1 + 8yG1]

2) pairing(OsG1, 1*G2):

Each row/constraint is its own pairing,

    pairing( [5xG1 + 6yG1], G2)
    pairing( [7xG1 + 8yG1], G2)

3) check against ZKP

    [pairing(kG1, hG2)]  ?=  pairing( [5xG1 + 6yG1], G2)
    [pairing(mG1, nG2)]  ?=  pairing( [7xG1 + 8yG1], G2)

*QAP: The S in Succient*

However, in practice this is not how its implemented. In a mildly complex circuit, the number of constraints and therefore, number of pairings would be numerous and therefore computationally intensive to execute.

The complexity is O(n). We can make it O(1) via QAP.
Instead of checking the constraints in the R1CS individually, we can now check all of the constraints at the same time by doing the dot product check on the polynomials.

Fundamentally, the vector 

This form is important because it allows us to apply bilinear pairings such that, L(sG1) 𝇇 R(sG2) = O(sG12)
where s is the supplied values of the witness vectors, encrypted via G1, G2 and G12 generator points respectively.

Each row/constraint is verified by checking if pairing(kG1, hG2) ?= pairing( 5xG1 + 6yG2 , G2).

