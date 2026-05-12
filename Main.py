from Account_Classes import Account_Info
def main():

    Accounts = [Account_Info(1), Account_Info(2), Account_Info(3), Account_Info(4), Account_Info(5)]
    Accounts[0].Deposit(100)

    Accounts[1].Deposit(100)

    Accounts[2].Deposit(100)

    Accounts[3].Deposit(100)

    Accounts[4].Deposit(100)
    

    Money = float(input("How much money would you like deposited? "))
    Accounts[0].Deposit(Money)

    Money = float(input("How much money would you like deposited? "))
    Accounts[1].Deposit(Money)

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
#add cant withdraw cuz it will go (-)
#add cant transfer into the same account
#add 
            

        else:
            print("Invalid option. Try again!")

        
main()

