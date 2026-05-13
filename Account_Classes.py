import json

# Base class for all types of bank accounts
class Account_Info:
    def __init__(self, Acc_num):
        self.Bal_info = 0
        self.Acc_num = Acc_num
        pass

    def Deposit(self, Amount):
        if Amount <= 0:
            raise ValueError("Deposit amount must be positive!")
        current_balance = self.Bal_info
        self.Bal_info = current_balance + Amount
        return self.Bal_info

    def Withdraw(self, Amount):
        if Amount <= 0:
            raise ValueError("Withdraw amount must be positive!")
        # Prevent overdraft in a standard account
        if Amount > self.Bal_info:
            raise ValueError("Insufficient funds!")
        current_balance = self.Bal_info
        self.Bal_info = current_balance - Amount
        return self.Bal_info

    def Move_money(self, Amount, Account_Target):
        # Prevent transferring to the same account
        if Account_Target.Acc_num == self.Acc_num:
            raise ValueError("Cannot move money into the same account!")
        self.Withdraw(Amount)
        Account_Target.Deposit(Amount)
        return self.Bal_info

    # Prepares the account data to be saved as JSON
    def To_dict(self):
        return {
            "type": type(self).__name__,
            "id":   self.Acc_num,
            "balance": self.Bal_info
        }

    def Get_Bal(self):
        return self.Bal_info

#=========================================================================================================

# Checking account inherits from Account_Info but adds an overdraft limit
class Checking(Account_Info):
    OVERDRAFT_LIM = 100

    def __init__(self, Acc_num):
        super().__init__(Acc_num)

    # Overrides standard Withdraw to allow dipping into the overdraft limit
    def Withdraw(self, Amount):
        if Amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if Amount > self.Bal_info + self.OVERDRAFT_LIM:
            raise ValueError("Exceeds overdraft limit!")
        current_balance = self.Bal_info
        self.Bal_info = current_balance - Amount
        return self.Bal_info

#=========================================================================================================

# Savings account inherits from Account_Info but adds an interest feature
class Savings(Account_Info):
    INTEREST_RATE = 0.03

    def __init__(self, Acc_num):
        super().__init__(Acc_num)

    # Standard withdrawal (no overdraft allowed)
    def Withdraw(self, Amount):
        if Amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if Amount > self.Bal_info:
            raise ValueError("Insufficient funds")
        current_balance = self.Bal_info
        self.Bal_info = current_balance - Amount
        return self.Bal_info
    
    # Calculates and adds interest to the current balance
    def Interest(self):
        interest = self.Bal_info * self.INTEREST_RATE
        self.Bal_info = self.Bal_info + interest
        return self.Bal_info

# Class to store the user's credentials and their list of accounts
class user:
    def __init__(self, usern, hsh, slt, accounts):
        self.username = usern
        self.salt = slt
        self.hash = hsh
        self.acct = accounts
    
    # Prepares all user data and nested account data for JSON saving
    def to_dict(self):
        return {
            "username": self.username,
            "hash":     self.hash,
            "salt":     self.salt,
            "acct":     [acc.To_dict() for acc in self.acct]
        }
        
    # Saves the dictionary representation to a file named after the user
    def save_to_json(self):
        filename = f"{self.username}_data.json"

        with open(filename, "w") as f:
            json.dump(self.to_dict(), f, indent = 4)
            print(f"Data for {self.username} saved to {filename}")