// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console2} from "forge-std/Test.sol";
import {HW3} from "../src/HW3.sol";

contract CounterTest is Test {
    HW3 public hw;

    struct ECPoint {
        uint256 X;
        uint256 Y;
    }

    function setUp() public {
        hw = new HW3();
    }

    function test_Increment() public {
        
        HW3.ECPoint memory A = HW3.ECPoint(1, 2); 
        HW3.ECPoint memory B = HW3.ECPoint(1, 2); 

        HW3.ECPoint memory C = HW3.ECPoint(
            1368015179489954701390400359078579693043519447331113978918064868415326638035,
            9918110051302171585080402603319702774565515993150576347155970296011118125764); 

        uint256 num = 2;
        uint256 den = 1;

        bool verified = hw.rationalAdd(A, B, num, den);
        
        assertEq(verified, true);
    }

}
