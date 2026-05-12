from Account_Classes import Account_Info
def main():
    Acc1 = input("What is the account number? ")
    Acc2 = input("What is the account number? ")

    Account1 = Account_Info(Acc1)
    Account2 = Account_Info(Acc2)

    Money = input("How much money would you like deposited? ")
    Account1.Deposit(Money)

    Money = input("How much money would you like deposited? ")
    Account2.Deposit(Money)

    while True:
        funct = input("What would you like to do next (Withdraw or Deposit): ")

        if funct == "Withdraw":
            Money = input("how much withdraw: ")
            print(Account1.Withdraw(Money))
        
        elif funct == "Deposit":
            Money = input("how much deposit: ")
            print(Account1.Deposit(Money))

        else:
            print("Invalid option. Try again!")

        

main()

