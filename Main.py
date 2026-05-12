from Bank_class import Bank
from Account_Classes import Account_Info
def main():


    while True:
        funct = input("What would you like to do next (Withdraw, Deposit, or Transfer): ")

        if funct == "Withdraw":
            Money = float(input("how much withdraw: "))
            print(Accounts[0].Withdraw(Money))
        
        elif funct == "Deposit":
            Money = float(input("how much deposit: "))
            print(Accounts[0].Deposit(Money))
        
        elif funct == "Transfer":
            Money = float(input("how much transfer: "))
            Acc = int(input("Which account tranfer: "))
            if Acc < 5:
                print("you have", Accounts[0].Move_money(Money, Accounts[Acc]), "remaining...")
            else:
                print("invalid")

        else:
            print("Invalid option. Try again!")

        
main()

