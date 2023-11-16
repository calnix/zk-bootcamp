## Gates to R1CS

An R1CS is a sequence of groups of three vectors (a, b, c).
The solution to an R1CS is a vector s, where s must satisfy the equation (s . a * s . b) - s . c = 0, where . represents the dot product.
> (s . a * s . b) = s . c

## rank 1

The "rank-1" specifically refers to the rank of the matrix which is produced.
As for the link to circuits, in zk-SNARKS at least, an arithmetic circuit is converted into a R1CS. Each constraint corresponds to one logic gate.

## The Rank of a Matrix

You can think of an r x c matrix as a set of r row vectors, each having c elements; or you can think of it as a set of c column vectors, each having r elements.
The rank of a matrix is defined as (a) the maximum number of linearly independent column vectors in the matrix or (b) the maximum number of linearly independent row vectors in the matrix. Both definitions are equivalent.

For an r x c matrix,

- If r is less than c, then the maximum rank of the matrix is r.
- If r is greater than c, then the maximum rank of the matrix is c.

The rank of a matrix would be zero only if the matrix had no elements. If a matrix had even one element, its minimum rank would be one.

Example:

X =
1	2	4	4
3	4	8	0

X has 2 rows and 4 columns.
Since it has fewer rows than columns, its maximum rank is equal to the maximum number of linearly independent rows.
And because neither row is linearly dependent on the other row, the matrix has 2 linearly independent rows; so its rank is 2.

> https://stattrek.com/matrix-algebra/matrix-rank

Therefore a rank-1 matrix only has 1 linearly independent row/column.
While