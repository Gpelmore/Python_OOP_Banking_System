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
        if Amount > self.Bal_info:
            raise ValueError("Insufficient funds!")
        current_balance = self.Bal_info
        self.Bal_info = current_balance - Amount
        return self.Bal_info

    def Move_money(self, Amount, Account_Target):
        if Account_Target == self.Acc_num:
            raise ValueError("Cannot move money into the same account!")
        self.Withdraw(Amount)
        Account_Target.Deposit(Amount)
        return self.Bal_info

    def Get_Bal(self):
        return self.Bal_info



class Checking(Account_Info):
    OVERDRAFT_LIM = 100

    def __init__(self, Acc_num):
        super().__init__(Acc_num)

    def Withdraw(self, Amount):
        if Amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if Amount > self.Bal_info + self.OVERDRAFT_LIM:
            raise ValueError("Exceeds overdraft limit!")
        current_balance = self.Bal_info
        self.Bal_info = current_balance - Amount
        return self.Bal_info



class Savings(Account_Info):
    INTEREST_RATE = 0.03

    def __init__(self, Acc_num):
        super().__init__(Acc_num)

    def Withdraw(self, Amount):
        if Amount <= 0:
            raise ValueError("Withdraw amount must be positive")
        if Amount > self.Bal_info:
            raise ValueError("Insufficient funds")
        current_balance = self.Bal_info
        self.Bal_info = current_balance - Amount
        return self.Bal_info
    
    def Interest(self):
        interest = self.Bal_info * self.INTEREST_RATE
        self.Bal_info = self.Bal_info + interest
        return self.Bal_info


