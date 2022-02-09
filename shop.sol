// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

contract Shop {
    address owner;
    Products[] public products;

    struct Products {
        string name;
        int price;
    }

    function store(address _owner) public {
        owner = _owner;
    }
    
    function retrieve() public view returns(address) {
        return owner;
    }

    function addProduct(string memory _name, int _price) public{
        products.push(Products(_name, _price));
    }
    
}
