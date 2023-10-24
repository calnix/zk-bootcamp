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

## What defines an elliptic curve?

typically defined by its formula and modulus.
however to generate all the points on the EC, you simply need:

- modulus, p
- generator point, G

You can then simply add G to itself repeatedly, p-1 times, generating all the other points.

## secp256k1

The NIST curve secp256k1 (used in Bitcoin) is based on an elliptic curve in the form:
y^2 = x^3 + 7 

Bitcoin uses secp256k1: y^2 = x^3 + 7 (mod p), over Fp, 
 where p = 2^256 - 2^32 - 2^9 - 2^6 - 2^4 -1

# ECDSA

 ECDSA keys and signatures are shorter than in RSA for the same security level. A 256-bit ECDSA signature has the same security strength like 3072-bit RSA signature.

# ECDSA key-pair generation

The ECDSA key-pair consists of:

- private key (integer): privKey
- public key (EC point): pubKey = privKey * G,

> G is the generator point of the EC curve

## ECDSA Sign

The ECDSA signing algorithm takes as input: 

- a message (msg), 
- a private key (privKey), 

and produces as output a signature, which consists of pair of integers {r, s}.

The ECDSA signing algorithm is based on the ElGamal signature scheme and works as follows (with minor simplifications):

1. Calculate the message hash, using a hash function like SHA-256: h = hash(msg)
2. Generate securely a random number k in the range [1..p-1].   
    > p is the modulus of the field
    > In case of deterministic-ECDSA, the value k is HMAC-derived from h + privKey
3. Calculate the random point R = k * G and take its x-coordinate: r = R.x
4. Calculate the signature proof: s = k^-1 * (h + r * privKey) (mod p)
    > The modular inverse  is an integer, such that
5. Return the signature {r, s}.

The calculated signature {r, s} is a pair of integers, each in the range [1...p-1]. 
It encodes the random point R = k * G, along with a proof s, confirming that the signer knows the message h and the private key privKey. 
The proof s is by idea verifiable using the corresponding pubKey.

### generating r: 
RFC 6979. 
It essentially prescribes not using randomness at all at signing time, but computing the nonce using a (specific) hash function that takes the message and private key as input. Under reasonable assumptions, this is just as unpredictable to attackers (who don't know the private key) as using actual randomness, but avoids the engineering challenges with having access to a good RNG.

https://bitcoin.stackexchange.com/questions/101634/how-is-the-random-number-r-for-transaction-signatures-created


## ECDSA Verify


