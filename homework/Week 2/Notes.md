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

