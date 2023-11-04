// SPDX-License-Identifier: UNLICENSED
pragma solidity ^0.8.13;

import {Test, console2} from "forge-std/Test.sol";
import {HW4} from "../src/HW4.sol";

contract HW4Test is Test {
    HW4 public pairings;

    function setUp() public {
        pairings = new HW4();
    }

    function testPairings() public {
        bool result = pairings.pairing(1,1,1,1,1,6);

       assertEq(result, true);
    }

}
