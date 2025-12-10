// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract EmployeePayroll {
    address public owner;

    struct Employee {
        string name;
        uint salary;
        uint lastPaid;
    }

    mapping(address => Employee) public employees;

    event Paid(address indexed to, uint amount);

    constructor() { owner = msg.sender; }

    modifier onlyOwner() { require(msg.sender == owner, "Not Owner"); _; }

    // State-Changing: Add a new employee
    function addEmployee(address _addr, string memory _name, uint _salary) external onlyOwner {
        employees[_addr] = Employee(_name, _salary, 0);
    }

    // Transaction: Pay an employee their salary
    function payEmployee(address payable _addr) external onlyOwner {
        uint salary = employees[_addr].salary;
        require(salary > 0, "Employee not found");
        require(address(this).balance >= salary, "Insufficient contract funds");
        
        employees[_addr].lastPaid = block.timestamp;
        _addr.transfer(salary);
        emit Paid(_addr, salary);
    }

    // View: Read employee data
    function getEmployee(address _addr) external view returns (string memory, uint, uint) {
        return (employees[_addr].name, employees[_addr].salary, employees[_addr].lastPaid);
    }

    // Allow contract to accept funds
    receive() external payable {}
}
