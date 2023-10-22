
import secrets

# generate random 32 bytes as private key, cast as hex
pk = secrets.token_hex(32)
assert len(pk) == 64

pk = "0x" + pk
print("The random private key generated is: {}".format(pk))
