// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Create a smart contract to store student details
contract StudentData {

    // Structure groups student details together
    struct Student {
        uint id;       // Stores student ID
        string name;  // Stores student name
        uint marks;   // Stores student marks
    }

    // Array stores multiple student records
    Student[] public students;

    // Function adds a new student to the array
    function addStudent(uint _id, string memory _name, uint _marks) public {
        students.push(Student(_id, _name, _marks));
    }

    // Function retrieves student details using array index
    function getStudent(uint index) public view returns (uint, string memory, uint) {
        Student memory s = students[index];
        return (s.id, s.name, s.marks);
    }

    // Fallback runs when a call does not match another function
    // Payable allows this function to receive Ether
    fallback() external payable {}
}
