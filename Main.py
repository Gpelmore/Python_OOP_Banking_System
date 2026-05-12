from Bank_class import Bank
from Account_Classes import Checking, Savings
def main():
    my_bank = Bank()

    dummy_acc = [Checking(0), Savings(1), Savings(2), Checking(3), Savings(4)]

    my_bank.Register("Admin", "password123", dummy_acc)

    token = my_bank.Login("Admin", "password123")

    session = my_bank.Get_Session(token)


    if not session:
        print("Session failed.")
        return
    
    Accounts = session["Accounts"]




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

if __name__ == "__main__":
    main()

