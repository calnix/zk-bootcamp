# Precompiles in Ethereum

<https://www.rareskills.io/post/solidity-precompiles>

## Address 0x01: ecRecover

## Address 0x02 and 0x03: SHA-256 and RIPEMD-160

## Address 0x04: Identity

## Address 0x05: Modexp

## Address 0x06 and 0x07 and 0x08: ecAdd, ecMul, and ecPairing (EIP-196 and EIP-197)

0x06: [ecAdd](https://github.com/tornadocash/tornado-core/blob/master/contracts/Verifier.sol#L79)
0x07: [ecMul](https://github.com/tornadocash/tornado-core/blob/master/contracts/Verifier.sol#L100)
0x08: [ecPairing](https://github.com/tornadocash/tornado-core/blob/master/contracts/Verifier.sol#L143)

These operations only support the BN-128 Barreto-Naehrig elliptic curves. These are not the same as the Elliptic curves used for digital signatures.
ecAdd and ecMul were added in EIP-196 and ecPairing was added in EIP-197.

## Address 0x09: Blake2 (EIP-152)

Blake2 hash is the preferred hash of zcash. 
Similar to SHA256 and RIPEMD-160, Blake2 was added to enable Ethereum to validate claims about transactions on that blockchain. 
This precompile was added in EIP152 and some sample code is available on the proposal.

Smart contract developers should be careful when copying Solidity code to other EVM compatible chains as the precompiles on those chains might not match what Ethereum has. 
For example, ecrecover and the other cryptographic precompiles are not supported on zksync. 
>(The technical reasons for this is that most cryptography algorithms are not SNARK-friendly, they are expensive to verify from a zero knowledge proof perspective).