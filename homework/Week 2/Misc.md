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


# ECDSA 

### To get public key:
(x, y) = pk * G, G is an EC point

so essentially its like point addition/doubling: 2 * G or 4 * G
 you are adding the same point to itself, repeatedly.
 the pk just tells you how many times

concat coordinates together,
then hash them.

# On Point multiplication

2A = A + A
4A = 2A + 2A

- given k and A, kA can be computed efficiently
- For K = kA, given K and P, k is hard to compute; have to brute-force by repeatedly adding the point to itself.

# On converting text to UTF+8
In Python, you need to encode a string as bytes when you're working with hash functions or performing operations that involve binary data. Here's why you need to encode the string as bytes:

Strings Are Text, Bytes Are Binary Data: In Python, strings are sequences of characters (text), while bytes represent binary data. Hash functions operate on binary data, not text. When you encode a string, you are converting it from its human-readable text representation to a sequence of bytes that a hash function can process.

Hash Function Requirements: Hash functions expect their input to be binary data. They process the binary representation of the data, not the characters themselves. Encoding the string as bytes ensures that the hash function works as expected.

