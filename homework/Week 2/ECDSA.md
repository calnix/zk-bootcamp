# On Digital Signatures

Why:

- Authentication: gives received proof that the message was sent by the claimant.
- Non-repudiation: sender cannot deny having sent the message later on
- Integrity: ensures message was not altered in transit

How:

A wants to send B a message/document.
A wants B to be able to authenticate that the message came from A.

1. A hashes the memo.
2. A encrypts the hash digest with his private key.

This encrypted digest is the digital signature for the memo.
A sends both the digest and the signature to B.

1. B can then use A's public key to verify this signature, by decrypting it.
2. B will hash the memo and compare it with the unencrypted digest, ensuring they match.
3. If B cannot decrypt the signature with A's public key; it did not come from A.

# ECDSA 

- ECDSA is based on ECC; is a digital signature scheme.
- ECDSA keys and signatures are shorter than in RSA for the same security level. A 256-bit ECDSA signature has the same security strength like 3072-bit RSA signature.

## secp256k1

The 256-bit elliptic curve, secp256k1 has the form:
`y^2 = x^3 + 7`

### secp256k1 curve parameters:
secp256k1: y^2 = x^3 + 7 (mod p) 
p = 115792089237316195423570985008687907853269984665640564039457584007908834671663
x = 55066263022277343669578718895168534326250603453777594175500187360389116729240
y = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337 

# Prime modulus, p vs Prime Order, n

The prime p should not be confused with the order of the curve. Not every value 0 < n < p satisfies the equation above.
The order of an elliptic curve is the number of points on it (including the "point at infinity").

So, although we have a possible p values from the prime number, not all the points will exist. The number of actual points is then defined by n.

Thus, given x * G, the value of x can only go from 0 to (n-1).

- ECC operations on point coordinates is in modulo p
- DSA operations on multiplier, random number, and signature components is modulo n
- The one exception is when the X coordinate in [0,p) gets reduced modulo n. Here there is room for a coding error if the coordinate is in [n,p). The lower bound n is excluded by the definition of ECDSA, but (n,p) is valid.

Since we have a modulo (p) , it means that the possible values of y^2 are between 0 and p-1, which gives us p total possible values. However, since we are dealing with integers, only a smaller subset of those values will be a “perfect square” (the square value of two integers), which gives us N possible points on the curve where N < p.

# ECDSA Signature/Verify process

1) Pick a private key
2) Generate the public key using that private key
3) For message m and hash it to produce h (h can be thought of as a 256 bit number)
4) Sign m using your private key and a randomly chosen nonce k. produce (r, s, h, PubKey)
5) Verify (r, s, h, PubKey) is valid

# ECDSA key-pair generation

The ECDSA key-pair consists of:

- private key (integer): privKey
- public key (EC point): pubKey = privKey * G,

> G is the generator point of the EC curve

The private key is generated as a random integer in the range [0...n-1]. The public key is a point on the elliptic curve, calculated by the EC point multiplication: `pubKey = privKey * G` (point multiplication)

To create a public / private key pair, a random number s is created (this is the secret key).
The point G is added to itself s times and the new point (x, y) is the public key. 
It is not feasible to derive s from G and (x, y) if s is sufficiently large.

## ECDSA Sign

The ECDSA signing algorithm takes as input:

- a message
- a private key (privKey),

and produces as output a signature, which consists of pair of integers {r, s}.

The ECDSA signing algorithm is based on the ElGamal signature scheme and works as follows (with minor simplifications):

1. Calculate the message hash, using a hash function like SHA-256: h = hash(msg)
2. Generate securely a random number k in the range [1..n-1]. 
    > n is the order of the curve
    > In case of deterministic-ECDSA, the value k is HMAC-derived from h + privKey
3. Calculate the random point R = k * G and take its x-coordinate: r = R.x
4. Calculate the signature proof: s = k^-1 * (h + r * privKey) (mod n)
    > k^-1 is the modular inverse 
5. Return the signature {r, s}.

The calculated signature {r, s} is a pair of integers, each in the range [1...n-1]. 
It encodes the random point R = k * G, along with a proof s, confirming that the signer knows the message h and the private key privKey. 
The proof s is by idea verifiable using the corresponding pubKey.

### On generating r:

RFC 6979 essentially prescribes not using randomness at all at signing time, but computing the nonce using a (specific) hash function that takes the message and private key as input. Under reasonable assumptions, this is just as unpredictable to attackers (who don't know the private key) as using actual randomness, but avoids the engineering challenges with having access to a good RNG.

https://bitcoin.stackexchange.com/questions/101634/how-is-the-random-number-r-for-transaction-signatures-created

## ECDSA Verify

1. Calculate the message hash, with the same cryptographic hash function used during the signing: h = hash(msg)
2. Calculate the modular inverse of the signature proof: s1 = 
3. Recover the random point used during the signing: R' = (h * s1) * G + (r * s1) * pubKey
4. Take from R' its x-coordinate: r' = R'.x
5. Calculate the signature validation result by comparing whether r' == r

The general idea of the signature verification is to recover the point R' using the public key and check whether it is same point R, generated randomly during the signing process.