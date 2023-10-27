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

But how the hell do we multiply two EC points? Thats where bilinear mapping comes in.
    pG * qG = rG ==>  e(P,Q) = e(R,G)
 
 G is the generator point, and can be thought of as “1”.
 G in e(R, G) just means we took G and didn’t add anything. 
 So in a sense, this is the same as saying P x Q = R x 1.








