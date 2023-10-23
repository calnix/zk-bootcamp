# Generating public keys in ethereum

## Private key

- An ethereum address first requires a completely unique and random private key to be generated.
- A private key is basically a random positive integer that is 256 bits == 64 hex characters == 32 bytes in length. 
- Basically pick a number btw 1 and 2^256 (a 78 digit number!)

> 2^256 is an astronomically larger number and is equivalent to the number of atoms in the universe!

## Public key generation

- uses elliptic curve cryptography
- its a trapdoor function / 1-way function
- cannot generate the private key from the public key
- The public key algorithm is secp256k1, the same used in bitcoin
- Because it is an elliptic curve algorithm, the public key is an (x, y) pair corresponds to a point on the elliptic curve.

To create a public / private key pair, a random number s is created (this is the secret key).
The point G is added to itself s times and the new point (x, y) is the public key. 
It is not feasible to derive s from G and (x, y) if s is sufficiently large.

> Adding G to itself s times is the same as multiplying s * G. 

## Ethereum address

- An ethereum address is the last 20 bytes of the keccack256 of the public key



## ECDSA: Elliptic Curve Signatures

 ECDSA keys and signatures are shorter than in RSA for the same security level. A 256-bit ECDSA signature has the same security strength like 3072-bit RSA signature.

## What defines an elliptic curve?

typically defined by its formula and modulus.
however to generate all the points on the EC, you simply need:

- modulus, p
- generator point, G

You can then simply add G to itself repeatedly, p-1 times, generating all the other points.


## 

The NIST curve secp256k1 (used in Bitcoin) is based on an elliptic curve in the form:
y^2 = x^3 + 7 

Bitcoin uses secp256k1: y^2 = x^3 + 7 (mod p), over Fp, 
 where p = 2^256 - 2^32 - 2^9 - 2^6 - 2^4 -1

## Sounlt an