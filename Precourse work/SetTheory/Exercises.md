# Definition of a set

> Exercise: Assume you have a proper definition for integers. Create a well-defined set of rational numbers.
'''
Rational numbers are numbers that can be expressed as the quotient or fraction of two integers, where the numerator is an integer, and the denominator is a non-zero integer.

Now, let's define the set of rational numbers (Q):

Q = {(a/b) | a, b ∈ ℤ, b ≠ 0}

In this definition:

"a" represents the numerator, and it can be any integer.
"b" represents the denominator, and it can be any non-zero integer.
The vertical bar "|" means "such that."

So, the set Q consists of all possible ordered pairs (a, b) where "a" is an integer and "b" is a non-zero integer, representing the numerator and denominator of a rational number, respectively. 
This set includes pairs like (1, 2), (-3, 4), (7, 1), and so on, covering all rational numbers.

'''

## Superset and subsets

Subset:
- all integers are rational numbers, but not all rational numbers are integers. 
- The relationship between them is that integers are a subset of rational numbers. 

> A subset need not be strictly smaller than the set it is a part of. It is perfectly okay to say that integers are a subset of integers.

Superset:
- rational numbers are a superset of integers.

>Exercise: Define the subset relationship between integers, rational numbers, real numbers, and complex numbers.
>Exercise: Define the relationship between the set of transcendental numbers and the set of complex numbers in terms of subsets. Is it a proper subset?
> Transcendental numbers are a subset of complex numbers, but they are not a proper subset because both sets are infinite and neither one is strictly smaller than the other.>

## Set Equality
Sets are defined to be equal if they contain the same elements, regardless of order. 
- For example, {4, 2, 5} is the same set as {2, 5, 4}. 

When doing formal proofs for sets, we say that if A is a subset of B and B is a subset of A, then A = B.
- Or in more mathy notation: A = B ⟷ A ⊆ B and B ⊆ A. 
- That’s read as A = B if and only if A is a subset of B and B is a subset of A.


## Cardinality

- Can define sets in a finite way, such as the numbers {0,1,2,3,4,5,6,7,8,9,10}
- The cardinality of the previous set is 11
- If A = {5,9,10}, then |A| = 3, where the two vertical bars around the A mean cardinality

There are different levels of infinite in set theory.
- For example, there are infinitely many more real numbers than there are integers.
- Specifically, we say integers are countably infinite because you can literally count them out
- But there is no way to start counting real numbers which are uncountably infinite.

> Exercise: Using the formal definition of equality, show that if two finite sets have different cardinality, they cannot be equal. 
> (Demonstrating this for infinite sets is a little trickier, so we skip that).

# Notation

The symbol ℕ is the set of natural numbers (1,2,3,…). 
- It definitely does not include negative numbers, but whether it includes zero depends on who you are talking to.

The symbol ℤ is the set of all integers (because “zahl” is integer in German)
The symbol ℚ is the set of all rational numbers (I remember it as the quotient of the numerator and denominator)
The symbol ℝ is the set of all real numbers, because R stands for real.
The symbol ℂ is the set of all complex numbers for similarly obvious reasons.

> Sometimes people write ℝ² as a vector of two real numbers, so a ∈ ℝ² means “a” is a 2d vector.

# Ordered pairs

Although sets do not respect order, a new type of data structure can emerge from sets called the ordered pair. 
- For example, (a, b) is an ordered pair while {a, b} is a set.
- programmers typically think of this as a tuple. 
- We say two ordered pairs are equal in the same sense we say two tuples are equal.

How do we create order out of something that is unordered?
- The implementation detail is that we write (a, b) in set form as {a, {b}}
- We can do this because we can define our set as containing either letters or a set of cardinality one that contains a letter.
- This is why we can say (a, b) ≠ (b, a) because {a, {b}} ≠ {b, {a}}.

# Cartesian product