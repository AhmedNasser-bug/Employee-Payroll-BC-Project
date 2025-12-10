import os
import sys

# Ensure we can import git_utils from the current directory
try:
    from git_utils import start_feature
except ImportError:
    print("[!] Error: git_utils.py not found. Make sure you are inside 'EmployeePayrollProject'.")
    sys.exit(1)

def add_simulation_to_migration():
    """
    Modifies the migration script to perform initial seeding:
    1. Deploys Contract
    2. Adds a test employee (Account[1])
    3. Funds the contract (5 ETH)
    4. Pays the employee (1 ETH)
    """
    migration_path = os.path.join("migrations", "2_deploy_contracts.js")
    
    # New content with Async/Await simulation logic
    new_content = """const EmployeePayroll = artifacts.require("EmployeePayroll");

module.exports = async function (deployer, network, accounts) {
  // 1. Deploy the contract
  await deployer.deploy(EmployeePayroll);
  const instance = await EmployeePayroll.deployed();

  // Only run simulation on local development networks (Ganache)
  if (network === "development" || network === "ganache") {
      console.log("\\n--- STARTING DEPLOYMENT SIMULATION ---");
      
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

      console.log("--- SIMULATION COMPLETE ---\\n");
  }
};
"""
    
    with open(migration_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"    [+] rewritten {migration_path} with simulation logic.")

# Define manual validation steps for the user
validation_steps = """
1. Ensure Ganache is running on port 7545.
2. Run command: 'npx truffle migrate --reset'
3. Observe the terminal output.
4. Verify you see lines like:
   - "Adding Employee: 0x..."
   - "Funding Contract..."
   - "Executing First Payroll..."
5. Verify no red error text appears.
"""

if __name__ == "__main__":
    # Execute the feature workflow
    # This will: Create Branch -> Modify File -> Commit -> Save Validation Steps
    start_feature(add_simulation_to_migration, validation_steps)