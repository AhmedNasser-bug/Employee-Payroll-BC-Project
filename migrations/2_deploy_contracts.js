const EmployeePayroll = artifacts.require("EmployeePayroll");

module.exports = async function (deployer, network, accounts) {
  // 1. Deploy the contract
  await deployer.deploy(EmployeePayroll);
  const instance = await EmployeePayroll.deployed();

  // Only run simulation on local development networks (Ganache)
  if (network === "development" || network === "ganache") {
      console.log("\n--- STARTING DEPLOYMENT SIMULATION ---");
      
      const owner = accounts[0];
      const employee = accounts[1];
      // Use web3 utility (available globally in Truffle) to convert Ether to Wei
      const salary = web3.utils.toWei("1", "ether"); 

      // 2. Add Employee
      console.log(`[*] Adding Employee: ${employee}`);
      await instance.addEmployee(employee, "Simulated User", salary, { from: owner });

      // 3. Fund Contract (Deposit 5 ETH)
      console.log("[*] Funding Contract with 5 ETH...");
      await instance.sendTransaction({ 
          from: owner, 
          value: web3.utils.toWei("5", "ether") 
      });

      // 4. Pay Employee
      console.log("[*] Executing First Payroll...");
      await instance.payEmployee(employee, { from: owner });

      console.log("--- SIMULATION COMPLETE ---\n");
  }
};
