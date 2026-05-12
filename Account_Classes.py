class Account_Info:
    def __init__(self):
        self.Bal_info = 0
        pass

    def Deposit(self, Amount):
        current_balance = self.Bal_info
        self.Bal_info = current_balance + Amount
        return self.Bal_info

    def Withdraw(self, Amount):
        current_balance = self.Bal_info
        self.Bal_info = current_balance - Amount
        return self.Bal_info

    def Move_money(self, Amount, Account_Target):
        self.Withdraw(Amount)
        Account_Target.Deposit(Amount)
        return self.Bal_info

    def Get_Bal(self):
        return self.Bal_info


#class Checking(Account_Info):
#
#    def __init__():


#class Savings(Account_Info):
#    def __init__

