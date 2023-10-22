# Qn 4

Prove to me that you know the solution to in a zero knowledge fashion:
    2x + 8y = 7944
    5x + 3y = 4764

## Answer

Convert the equations to the form: g^x (mod p) 

 x + y = z 

converted:
 (g^x)(g^y) = g^z   (mod p)

The conversion is a homomorphism:
    The equation x + y = z, exists within the group G: (Z, +); integers under addition.
    The second equation exists within the group H: (g^i modp, *), g^i (mod p) under multiplication where i is some integer.

We know that the homomorphism exists because:
    f(a + b) = f(a) * f(b), where f(a) = g^a
    
    f(a + b) = g^a * g^b
    g^(a + b) = g^a * g^b
    g^(a + b) = g^(a+b)   

Therefore homomorphism exists.
Homomorphism from G: (Z, +) to H: (Zp, *)


So for someone to prove that they know the values of x and y, they can use the relationship x+y=z, and the homomorphism to create a proof
    proof: g^z

The verifier can confirm this to be true.
    



![Alt text](image-1.png)