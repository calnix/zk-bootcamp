// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

contract HW4 {

    struct ECPoint {
        uint256 X;
        uint256 Y;
    }

    struct ECPoint2 {
        uint256 X1;
        uint256 Y1;
        uint256 X2;
        uint256 Y2;
    }


    //  bn128 G1: (1, 2)
    ECPoint public G1;
    ECPoint2 public G2;

    // field modulus: 
    uint256 immutable public field_modulus = 21888242871839275222246405745257275088696311157297823662689037894645226208583;

    constructor(){
        G1 = ECPoint(1,2);
        G2 = ECPoint2({
            X1: 10857046999023057135944570762232829481370756359578518086990519993285655852781, 
            Y1: 11559732032986387107991004021392285783925812861821192530917403151452391805634,
            X2: 8495653923123431417604973247489272438418190587263600148770280649306958101930,
            Y2: 4082367875863433681332203403145435568316851327593401208105741076214120093531
            });
    }

    /*//////////////////////////////////////////////////////////////
                             HW4 FUNCTIONS
    //////////////////////////////////////////////////////////////*/

    // W₁z₂ = A₁b₂ + X₁y₂ + C₁d₂, where X₁ = x₁G₁ + x₂G₁ + x₃G₁ 
    // 0 = -W₁z₂ + A₁b₂ + X₁y₂ + C₁d₂, where X₁ = x₁G₁ + x₂G₁ + x₃G₁ 
    
    // w(G1*G2) = a(G1*G2) + x(G1*G2) + c(G1*G2), where x = x₁ + x₂ + x₃
    // 0 = -w(G1*G2) + a(G1*G2) + x(G1*G2) + c(G1*G2), where x = x₁ + x₂ + x₃
    // 0 = -5(G1*G2) + 1(G1*G2) + 3(G1*G2) + 1(G1*G2)
    // 0 = -5 + 1 + 3 + 1

    // 1. tack all the scalars onto the G1 points via scalarMul
    // 2. find the inverse of W, by flipping y-coord under field_modulus
    // 3. submit the sequence of points into pairing: uint256[12] memory points

    //G1 points: A₁, X₁, C₁ and W₁
    //G2 points: b₂, y₂, d₂ and z₂
    function pairing(uint256 x1, uint256 x2, uint256 x3, uint256 a, uint256 c, uint256 w) public view returns(bool) {
        
        // calc X₁ = x₁G₁ + x₂G₁ + x₃G₁ 
        uint256 x = x1 + x2 + x3;
        ECPoint memory X =  scalarMul(G1, x);

        //cal G1 points: A = aG1, C = cG1, W = wG1
        ECPoint memory A = scalarMul(G1, a);
        ECPoint memory C = scalarMul(G1, c);
        ECPoint memory W = scalarMul(G1, w);

        // calc inverse of W: -W = (x, -y mod p)
        uint256 inverted_y = calculateModulo(-int(W.Y), field_modulus);        
        ECPoint memory W_Inv = ECPoint(W.X, inverted_y);

        ECPoint memory identity = pointAddition(W_Inv, W);
        require(identity.X == 0 && identity.Y == 0, 'identity check');

        //G2 points cannot be calc w/ precompiles: must be done off-chain
        // (G1 + G2) = 6 points for 1 pair
        uint256[24] memory points = [
            W_Inv.X,
            W_Inv.Y,
            G2.X1,
            G2.Y1,
            G2.X2,
            G2.Y2,
            //next pair
            A.X,
            A.Y,
            G2.X1,
            G2.Y1,
            G2.X2,
            G2.Y2,
            //next pair
            X.X,
            X.Y,
            G2.X1,
            G2.Y1,
            G2.X2,
            G2.Y2,
            //next pair
            C.X,
            C.Y,
            G2.X1,
            G2.Y1,
            G2.X2,
            G2.Y2
        ];

        bool result = run(points);

        return result;
    }

    /** 
     *  returns true if == 0,
     *  returns false if != 0,
     *  reverts with "Wrong pairing" if invalid pairing
     */
     function run(uint256[24] memory input) public view returns (bool) {
        assembly {
            let success := staticcall(gas(), 0x08, input, 0x0180, input, 0x20)
            if success {
                return(input, 0x20)
            }
        }
        revert("Wrong pairing");
    }

    function calculateModulo(int x, uint p) public pure returns (uint) {
        require(p > 0, "Modulus (p) must be a positive integer");

        uint result;
        if (x >= 0) {
            result = uint(x) % p;
        } else {
            result = p - uint(-x) % p;
        }
        
        return result;
    }

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
