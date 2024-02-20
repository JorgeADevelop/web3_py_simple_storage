// SPDX-License-Identifier: MIT

pragma solidity ^0.6.0;

contract SimpleStorage {
    uint256 favoriteNumber;

    Person[] public people;

    mapping(string => uint256) public nameToFavorite;

    struct Person {
        uint256 favoriteNumber;
        string name;
    }

    function store(uint256 _favoriteNumber) public {
        favoriteNumber = _favoriteNumber;
    }

    function retrive() public view returns (uint256) {
        return favoriteNumber;
    }

    //memory - vive durante la ejecución de la funcion
    //storage - vive siempre en memoria
    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(Person(_favoriteNumber, _name));
        nameToFavorite[_name] = _favoriteNumber;
    }
}