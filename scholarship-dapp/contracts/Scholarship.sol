// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

contract Scholarship {
    address public owner;
    uint256 public totalBudget;
    uint256 public allocatedAmountTotal;
    uint256 public claimedAmountTotal;

    struct Student {
        uint256 amount;
        bool registered;
        bool claimed;
        uint256 createdAt;
        uint256 claimedAt;
    }

    mapping(address => Student) public students;

    event StudentRegistered(address indexed student, uint256 amount, uint256 timestamp);
    event ScholarshipClaimed(address indexed student, uint256 amount, uint256 timestamp);
    event ScholarshipRevoked(address indexed student, uint256 amount, uint256 timestamp);
    event FundsDeposited(address indexed from, uint256 amount);
    event FundsWithdrawn(address indexed to, uint256 amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "Not owner");
        _;
    }

    modifier onlyRegistered(address studentAddr) {
        require(students[studentAddr].registered, "Student not registered");
        _;
    }

    constructor() {
        owner = msg.sender;
    }

    function depositFunds() external payable {
        require(msg.value > 0, "Must send funds");
        totalBudget += msg.value;
        emit FundsDeposited(msg.sender, msg.value);
    }

    function registerStudent(address studentAddr, uint256 amount) external onlyOwner {
        require(studentAddr != address(0), "Invalid address");
        require(amount > 0, "Invalid amount");
        Student storage s = students[studentAddr];
        require(!s.registered, "Already registered");
        s.amount = amount;
        s.registered = true;
        s.claimed = false;
        s.createdAt = block.timestamp;
        allocatedAmountTotal += amount;
        emit StudentRegistered(studentAddr, amount, block.timestamp);
    }

    function claimScholarship() external onlyRegistered(msg.sender) {
        Student storage s = students[msg.sender];
        require(!s.claimed, "Already claimed");
        require(address(this).balance >= s.amount, "Insufficient contract balance");
        s.claimed = true;
        s.claimedAt = block.timestamp;
        claimedAmountTotal += s.amount;

        (bool ok, ) = msg.sender.call{value: s.amount}("");
        require(ok, "Transfer failed");

        emit ScholarshipClaimed(msg.sender, s.amount, block.timestamp);
    }

    function revokeRegistration(address studentAddr) external onlyOwner onlyRegistered(studentAddr) {
        Student storage s = students[studentAddr];
        require(!s.claimed, "Cannot revoke after claim");
        allocatedAmountTotal -= s.amount;
        uint256 amt = s.amount;
        delete students[studentAddr];
        emit ScholarshipRevoked(studentAddr, amt, block.timestamp);
    }

    function withdraw(uint256 amount, address payable to) external onlyOwner {
        require(amount <= address(this).balance, "Insufficient balance");
        (bool ok, ) = to.call{value: amount}("");
        require(ok, "Withdraw failed");
        emit FundsWithdrawn(to, amount);
    }

    function getStats() external view returns (
        uint256 totalAllocated,
        uint256 claimedAmount,
        uint256 budget,
        uint256 remainingBudget
    ) {
        totalAllocated = allocatedAmountTotal;
        claimedAmount = claimedAmountTotal;
        budget = totalBudget;
        remainingBudget = address(this).balance;
    }

    receive() external payable {
        totalBudget += msg.value;
        emit FundsDeposited(msg.sender, msg.value);
    }
}
