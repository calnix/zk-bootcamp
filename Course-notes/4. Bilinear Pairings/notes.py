from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq, field_modulus

# bn128 curve:  y^2 = x^3 + 3 (mod p)

print(G1)
# (1, 2)

print(G2)
# (
# (10857046999023057135944570762232829481370756359578518086990519993285655852781, 11559732032986387107991004021392285783925812861821192530917403151452391805634), 
# (8495653923123431417604973247489272438418190587263600148770280649306958101930, 4082367875863433681332203403145435568316851327593401208105741076214120093531)
# )

# G1 and G2 are the generator points for their respective groups
# G1: (x,y)
# G2: ((x,y), (x, y))

# Regardless of dimensions, the same rules apply

# G1 + G1 = 2G1 
print(eq(add(G1, G1), multiply(G1, 2)))

# G2 + G2 = 2G2
print(eq(add(G2, G2), multiply(G2, 2)))
# True

# Only add elements from the same group [dimension differences]
try:
    add(G1, G2)
except TypeError:
     # TypeError
     print("cannot multiply diff. dimensions")


# py_ecc lib overrides some arithmetic operators (you can do that in python), meaning you can do the following:
print(G1 + G1 + G1 == G1*3)
# True
# The above is the same as this:
eq(add(add(G1, G1), G1), multiply(G1, 3))


# Pairing

# Scalar multiplication, before
A = multiply(G2, 32)
B = multiply(G1, 6)
C = pairing(A, B)

print(C)
# (2737733771970589720147436295258995541017562764748775046990018238171083065584, 7355949162177082646197064865377481127039528955264110892670278171102027012957, 1389120597320745437757553030085914762401499323567753964656133081964131780715, 4070774491543958907062047566637569178763974576144707726129772744684275725184, 10823414137019623021013733227099721415368303324105358213304652659949682568395, 12697986880222911287030392175914090722292212037466224705879408804162602333706, 17697943997237703208660786428217562403504798830995307420075922564993565300645, 2702065915136914071855531840006964465333491722231468583849464437921405019853, 6762652910450025398171695126080749677225757293012137750262928324249233167133, 9495821522287762858490254871883860235240788822777455638443279749602676973720, 17813117134675140440034537765301248350834713246854720915775731738875700896539, 21027635025043266481235488683404016989778194881701554135606154029160033599034)

# Scalar multiplication, after
A = multiply(G2, 5)
B = multiply(G1, 6)
C = multiply(G2, 5 * 6)

# order of scalar mul does not matter
print(pairing(A, B) == pairing(C, G1))

# To be mathematical our bn128 pairing does the following:
# e: G1 × G2 → G12

'''
Note that the pairing implementation requires you to use the G2 point as the first argument and the G1 point as the second argument. 
This is not a mathematical requirement, just an implementation detail in the library.

Note that the library has a strange glitch in it when using the shortcut arithmetic notation in combination with a pairing:
    pairing(G2 * 5, G1 * 6) == pairing(G2 * 30, G1)
    # Typeerror, library bug
'''

from py_ecc.bn128 import G1, G2, pairing, add, multiply, eq, field_modulus
print(field_modulus)
print(pow(-848677436511517736191562425154572367705380862894644942948681172815252343932, 1, field_modulus))

print(G2.)

print(pow(15,-1,13))

print(pow(56, 1, 13))