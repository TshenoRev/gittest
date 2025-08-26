# Import required libraries
import sys
import stdio  # Stellenbosch University standard I/O library

class BankAccount:
    """
    A class representing a basic bank account with Stellenbosch University's CS syntax
    """
    
    # Class attribute for automatic account numbering
    defaultAccNumber = 1  

    def __init__(self, name, balance=0):
        """
        Constructor method to initialize a BankAccount instance
        :param name: Account holder name (str)
        :param balance: Initial balance (float, default=0)
        """
        self.name = name
        self.balance = balance
        self.accountNumber = BankAccount.defaultAccNumber
        BankAccount.defaultAccNumber += 1  # Increment for next account

    def deposit(self, amount):
        """
        Deposits amount into account
        :param amount: Amount to deposit (float)
        """
        self.balance += amount
        stdio.writeln(f"Deposited {amount}. New balance: {self.balance}")

    def withdraw(self, amount):
        """
        Withdraws amount from account if sufficient funds
        :param amount: Amount to withdraw (float)
        """
        if self.balance < amount:
            stdio.writeln("Error: Insufficient funds!")
        else:
            self.balance -= amount
            stdio.writeln(f"Withdrew {amount}. New balance: {self.balance}")

    def getBalance(self):
        """
        Returns current account balance
        :return: Current balance (float)
        """
        return self.balance

    def displayAccountInfo(self):
        """
        Displays complete account information using stdio
        """
        stdio.writeln("\n==== Account Information ====")
        stdio.writeln(f"Account Holder: {self.name}")
        stdio.writeln(f"Account Number: {self.accountNumber}")
        stdio.writeln(f"Current Balance: {self.balance}")
        stdio.writeln("============================")

if __name__ == '__main__':
    # Demonstration of the BankAccount class
    try:
        # Create account using stdio for input
        stdio.writeln("\n=== Creating New Bank Account ===")
        name = stdio.readString("Enter account holder name: ")
        initial_deposit = stdio.readFloat("Enter initial deposit amount: ")
        
        account = BankAccount(name, initial_deposit)
        account.displayAccountInfo()
        
        # Perform transactions
        account.deposit(stdio.readFloat("\nEnter deposit amount: "))
        account.withdraw(stdio.readFloat("Enter withdrawal amount: "))
        
        # Final balance check
        account.displayAccountInfo()
        
    except Exception as e:
        stdio.writeln(f"Error: {str(e)}")
        sys.exit(1)
