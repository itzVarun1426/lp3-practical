// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

// Create a bank account smart contract
contract BankAccount {

    uint public balance;

    // Deposit Ether into the bank account
    function deposit() public payable {
        balance += msg.value;
    }

    // Withdraw Ether from the bank account
    function withdraw(uint amount) public {
        require(amount <= balance, "Insufficient balance");

        balance -= amount;

        // Send the withdrawn Ether to the caller
        (bool success, ) = payable(msg.sender).call{value: amount}("");
        require(success, "Transfer failed");
    }

    // Display the current account balance
    function showBalance() public view returns (uint) {
        return balance;
    }
}
