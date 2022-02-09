// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "./shop.sol";

contract ShopFactory is Shop {

    Shop[] public shopArray;

    function createShop() public {
        Shop shop = new Shop();
        shopArray.push(shop);
    }

    function sfStore(uint _shopIndex, address _shopOwner) public {
        Shop(address(shopArray[_shopIndex])).store(_shopOwner);
    }

    function sfGet(uint _shopIndex) public view returns(address) {
        return Shop(address(shopArray[_shopIndex])).retrieve();
    }
}
