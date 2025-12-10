const EmployeePayroll = artifacts.require("EmployeePayroll");

module.exports = function (deployer) {
  // Deploy the EmployeePayroll contract
  deployer.deploy(EmployeePayroll);
};
