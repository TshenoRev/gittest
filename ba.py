import stdio  # Stellenbosch University standard I/O library

class BankAccount:
    """
    A class representing a basic bank account with Stellenbosch University's CS syntax.
    """
    
    # Class attribute for automatic account numbering
    defaultAccNumber = 1  

    def __init__(self, name, balance=0):
        """
        Constructor method to initialize a BankAccount instance.
        :param name: Account holder name (str)
        :param balance: Initial balance (float, default=0)
        """
        self.name = name
        self.balance = balance
        self.accountNumber = BankAccount.defaultAccNumber
        BankAccount.defaultAccNumber += 1  # Increment for next account

    def deposit(self, amount):
        """
        Deposits amount into account.
        :param amount: Amount to deposit (float)
        """
        if amount < 0:
            stdio.writeln("Error: Deposit amount must be positive!")
            return
        self.balance += amount
        stdio.writeln(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        """
        Withdraws amount from account if sufficient funds.
        :param amount: Amount to withdraw (float)
        """
        if amount < 0:
            stdio.writeln("Error: Withdrawal amount must be positive!")
            return
        if self.balance < amount:
            stdio.writeln("Error: Insufficient funds!")
        else:
            self.balance -= amount
            stdio.writeln(f"Withdrew {amount}. New balance: {self.balance}")

    def getBalance(self):
        """
        Returns current account balance.
        :return: Current balance (float)
        """
        return self.balance

    def displayAccountInfo(self):
        """
        Displays complete account information using stdio.
        """
        stdio.writeln("\n==== Account Information ====")
        stdio.writeln(f"Account Holder: {self.name}")
        stdio.writeln(f"Account Number: {self.accountNumber}")
        stdio.writeln(f"Current Balance: {self.balance}")
        stdio.writeln("============================")

if __name__ == '__main__':
    # Demonstration of the BankAccount class
    # Create account using stdio for input
    stdio.writeln("\n=== Creating New Bank Account ===")
    
    stdio.write("Enter account holder name: ")  # Display prompt
    name = stdio.readString()  # Read input without arguments
    
    stdio.write("Enter initial deposit amount: ")  # Display prompt
    initial_deposit = stdio.readFloat()  # Read float input without arguments
    
    account = BankAccount(name, initial_deposit)
    account.displayAccountInfo()
    
    # Perform transactions
    stdio.write("\nEnter deposit amount: ")  # Display prompt
    deposit_amount = stdio.readFloat()  # Read float input without arguments
    account.deposit(deposit_amount)
    
    stdio.write("Enter withdrawal amount: ")  # Display prompt
    withdrawal_amount = stdio.readFloat()  # Read float input without arguments
    account.withdraw(withdrawal_amount)
    
    # Final balance check
    account.displayAccountInfo()
