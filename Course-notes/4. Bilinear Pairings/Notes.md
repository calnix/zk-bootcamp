# Bilinear Pairings: Motivation

We can scalar multiply a EC point: 4P = P+P+P+P
We can add two different EC points together: P + Q = R

**But we cannot multiply two different EC points together: P * Q**

## Definition of a pairing

A pairing, also known as a bilinear map, is a function e:G₁ × G₂ → GT between three groups G1,G2 and GT of prime order p, with generators g1=⟨G1⟩, g2=⟨G2⟩ and gT=⟨GT⟩, respectively.

e: G₁ × G₂ → Gᴛ

E.g.
    P,Q: G₁
    S,T: G₂
    e(P, Q) -> 


When G₁ = G₂, the pairing is called symmetric. Otherwise, it is asymmetric. 
> These are EC groups

A bilinear mapping must satisfy the following properties: bilinearity, non-degeneracy and efficiency.

### Bilinearity

Bilinearity requires that, for all u ∈ G₁, v ∈ G₂, and a,b∈Zp:

- e(aP,bQ) = ab[e(P,Q)] = e(P, abQ)
- e(aG,bG) = e(abG, G) = e(G, abG)
- e(uᵃ,vᵇ)=e(u,v)ᵃᵇ

- e(P+Q, S) = e(P, S) * e(Q, S)

The above notation implies that we are using the same generator and elliptic curve group.

### Non-degeneracy

e(G1,G2) ≠ 1Gᴛ

Let 1Gᴛ denote the identity element of the group Gᴛ.
We want non-degeneracy because, without it, it is simple (and useless) to define a (degenerate) bilinear map that, for every input, returns 1Gᴛ.
Such a map would satisfy bilinearity, but would be completely useless.

### Efficiency

Efficiency requires that there exists a polynomial-time algorithm in the size of a group element (i.e.; in λ=log2p) that can be used to evaluate the pairing e on any inputs.
This property allows for feasibility in computation.

## How numbers are encrypted

Assume: p * q = r

What we are trying to do is:
    P = pG,
    Q = qG,
    R = rG

and convince the verifier that P and Q multiply to produce R.
    pG * qG = rG

> the verifier will have access to G and r, to compute R and assert R == P*Q, as provided by the proofer

### But how the hell do we multiply two EC points?

That's where bilinear mapping comes in:
    pG * qG = rG ==>  e(P,Q) = e(R,G)

 G is the generator point, and can be thought of as “1”.
 G in e(R, G) just means we took G and didn’t add anything.
 So in a sense, this is the same as saying P x Q = R x 1.

So a bilinear pairing is a useful obfuscation, in that by plugging in elliptic curve points into the arguments in the manner above,
you can easily determine if p * q = r without knowing p, q, or r (because they’ve been turned into elliptic curve points via G).

## Symmetric and Asymmetric Groups

e: G₁ × G₂ → Gᴛ

Symmetric is where the input groups are the same: e: G₁ == G₂. Asymmetric they would be different.

One could think of G₁, G₂, and Gᴛ being different elliptic curve equations, possibly modulo different primes, and that would be valid because those are different groups.
> In practice we use asymmetric groups. No one has figured out for symmetric groups.
> For asymmetric groups, the curve order of each ecc group must be the same. 


## How are pairings done

- Miller Loop is used to do pairings
- assume its a blackbox like SHA-256

## Field Extensions

Bilinear pairings are rather agnostic to the kinds of groups you opt for, but Ethereum’s bilinear pairing of choice uses elliptic curves with field extensions.
A field extension is a very abstract concept, and frankly, the relationship between a field and its extension doesn’t matter from a purely functional concept.

We usually think of EC points as two points x and y. With field extensions, they consist of several (x, y) pairs. This is analogous to how complex numbers “extend” real numbers.

- Essentially EC points with more than 2 dimensions.
- Adhere to the same group properties:
  - closed under addition, which is associative
  - has an identity element
  - each element has an inverse
  - the group has a generator

You don’t have to worry about how these field extensions are constructed or how to do math in them, they are also cyclic groups that follow the same rules of the groups you are familiar with.
What is the point of this? Field extensions allow for the property of bilinearity.

## Bilinear Pairings in Ethereum

- py_ecc maintained by Eth Foundation
- powers the precompile at address 0x8, in PyEVM implementation
- The Ethereum Precompile defined in EIP 197 works on points in G1 and G2, and implicitly works on points in G12.
- They messed around and found that it was the easiest to compute the pairing from: G1 * G2 -> G12
- This is the Optimal Ate curve and was chosen cos' its pairing friendly.

## Pairing and G12

e: G₁ × G₂ → Gᴛ

G₁: (1,2)  -> 1-d curve
G₂: ((x₁,y₁), (x₂,y₂)) -> 2d curve
    | y₁ |^2  = | x₁ |^3  + ...
    | y₂ |      | x₂ |  

Gᴛ: 12-d curve. each point has 12 sets of coords.

We don't have a way of pairing G12 points together.
A: G12
B: G12
pair(A, B) will return error.

> we can add G12 points: pairing(G2, G1) + pairing(G2, G1)

Given a G12 point, we cannot decompose it into a G1 and G2 point.
Nor can we figure out the scalars that went into its generation.

