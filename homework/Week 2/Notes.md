pK element of 2^256 -1

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

