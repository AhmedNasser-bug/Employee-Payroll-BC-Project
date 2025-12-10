
===============================================================
   EMPLOYEE PAYROLL PROJECT - IMPLEMENTATION GUIDE
===============================================================

STEP 1: INSTALL GANACHE
1. Download Ganache GUI from: https://trufflesuite.com/ganache/
2. Install and Open it.
3. Click "Quickstart" (Ethereum).
4. You will see a list of accounts and a "RPC SERVER" on port 7545.

STEP 2: PREPARE DEPENDENCIES
(If you haven't successfully run 'npm install' yet)
1. Open your terminal inside this 'EmployeePayrollProject' folder.
2. Run: npm install

STEP 3: DEPLOY TO BLOCKCHAIN
1. In your terminal, run:
   npx truffle migrate

   Success Message Example:
   > "Deploying 'EmployeePayroll'..."
   > "contract address:    0x123..."

STEP 4: INTERACT (CONSOLE)
1. Run: npx truffle console
2. In the console, type these commands to test:
   
   // Get your contract instance
   let instance = await EmployeePayroll.deployed()
   
   // Get accounts
   let accounts = await web3.eth.getAccounts()
   
   // Add Employee (Simulate Admin)
   await instance.addEmployee(accounts[1], "Alice", web3.utils.toWei("1", "ether"))
   
   // Check Employee
   await instance.getEmployee(accounts[1])
   
   // Pay Employee (Send 1 Ether)
   await instance.payEmployee(accounts[1], {value: web3.utils.toWei("1", "ether")})

===============================================================
