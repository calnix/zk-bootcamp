// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract HW3 {

    struct ECPoint {
        uint256 X;
        uint256 Y;
    }

    //  bn128 G1: (1, 2)
    ECPoint public G1;

    // field modulus: 
    uint256 immutable public field_modulus = 21888242871839275222246405745257275088696311157297823662689037894645226208583;

    constructor(){
        G1 = ECPoint(1,2);
    }

    /*//////////////////////////////////////////////////////////////
                             HW4 FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    



    /*//////////////////////////////////////////////////////////////
                              HW3 FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    // a + b = c
    function rationalAdd(ECPoint calldata A, ECPoint calldata B, uint256 num, uint256 den) public view returns (bool) {

        // scalar = num * den-1
        uint256 inverse = modInverse(den, field_modulus);
        require(inverse * den == 1, "mod inverse failed");
        uint256 scalar = (num * inverse) % field_modulus;

        // G^c = G * scalar
        ECPoint memory C = scalarMul(G1, scalar);

        // assert A + B == (G * scalar)
        bool verified = arePointsEqual(C, pointAddition(A, B));

        // return true if the prover knows two numbers that add up to num/den
        return verified;
    }

    // M: n x n square matrix
    // s: n elements (scalar vector)
    // o: n elements (scalar vector)
    // check if Ms == o*G
    function matmul(uint256[] calldata matrix, uint256 n, ECPoint[] calldata s, uint256[] calldata o) public view returns (bool verified) {

	    // revert if dimensions don't make sense or the matrices are empty
        require(matrix.length == n*n, "matrix incorrect dimension");
        require(s.length == n, "s incorrect dimension");
        require(o.length == n, "o incorrect dimension");

        // M * s
        uint256 rowIndex = 0;
        ECPoint[] memory Ms = new ECPoint[](n);

        for (uint256 i = 0; i < n; i++){
            // 1st element of each row
            rowIndex = i * n;
            //ele: (rowStartIndex, colIndex: j)
            for (uint256 j = 0; j < n; j++){
                uint256 ele = matrix[rowIndex + j];    
                ECPoint memory product = scalarMul(s[j], ele);

                // |1,2| *  | 🇵​​​​​ |  =   | 1🇵​​​​​ + 2🇶​​​​​ |
                // |4,5|    | 🇶​​​​​ |     | 4🇵​​​​​ + 5🇶​​​​​ |
                // we are doing the addition here
                if (j == 0) Ms[i] = product;            //1st element for the seq.
                else Ms[i] = pointAddition(Ms[i], product);
            }
        }

        // verify Ms = o*G
        for (uint256 i = 0; i < n; i++) {
            verified = arePointsEqual(Ms[i], scalarMul(G1, o[i]));
            if (verified == false) return verified;                 //early break
        }   

        // return true if Ms == 0 elementwise.
        return verified;
    } 

    /*//////////////////////////////////////////////////////////////
                                HELPERS
    //////////////////////////////////////////////////////////////*/

    function modInverse(uint256 a, uint256 m) public pure returns (uint256) {
        require(m > 0, "m > 0");
        require(a > 0 && a < m, "a > 0 & a < m");   // else no remainder

        int256 t1;
        int256 t2;
        int256 t3;
        int256 t4;

        t1 = int256(0);
        t2 = int256(1);
        t3 = int256(m);
        t4 = int256(a);

        
        while (t4 != 0) {
            int256 q = t3 / t4;
            (t1, t2) = (t2, t1 - q * t2);
            (t3, t4) = (t4, t3 - q * t4);
        }

        if (t3 > 1) {
            // a and m are not coprime
            revert("Modular inverse does not exist");
        }

        if (t1 < 0) {
            t1 += int256(m);
        }

        return uint256(t1);
    }

    /*
    * @return r the product of a point on G1 and a scalar, i.e.
    *         p == p.scalar_mul(1) and p.plus(p) == p.scalar_mul(2) for all
    *         points p.
    */
    function scalarMul(ECPoint memory p, uint256 s) internal view returns (ECPoint memory r) {
        
        uint256[3] memory input;
        input[0] = p.X;
        input[1] = p.Y;
        input[2] = s;
        bool success;
        
        // solium-disable-next-line security/no-inline-assembly
        assembly {
            success := staticcall(sub(gas(), 2000), 7, input, 0x80, r, 0x60)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }

        require(success, "pairing-mul-failed");
    }


    /*
    * @return r the sum of two points of G1
    */
    function pointAddition(ECPoint memory p1, ECPoint memory p2) internal view returns (ECPoint memory r) {
        uint256[4] memory input;
        input[0] = p1.X;
        input[1] = p1.Y;
        input[2] = p2.X;
        input[3] = p2.Y;
        bool success;

        // solium-disable-next-line security/no-inline-assembly
        assembly {
            success := staticcall(sub(gas(), 2000), 6, input, 0xc0, r, 0x60)
            // Use "invalid" to make gas estimation work
            switch success case 0 { invalid() }
        }

        require(success, "pairing-add-failed");
    }

    function arePointsEqual(ECPoint memory p1, ECPoint memory p2) internal pure returns (bool) {
        return (p1.X == p2.X) && (p1.Y == p2.Y);
    }
}
