import time
from Bank_class import Bank
from Account_Classes import Checking, Savings
def main():
    my_bank = Bank()
    next_account_num = 0

    while True:

        print("\n========= Welcome to Python Bank =========")
        print("1. Register a new user")
        print("2. Login")
        print("3. Exit")

        start_menu = input("Select an option(1, 2, or 3): ")

        if start_menu == "1":
            print("\n---- Registration ----")
            
            username = input("Enter a username: ")
            password = input("Enter a password: ")

            new_accounts = [Checking(next_account_num), Savings(next_account_num + 1)]
            next_account_num += 2

            my_bank.Register(username, password, new_accounts)

        elif start_menu == "2":
            print("\n---- Login ----")
            print("(Type 'cancel' at any time to return to the main menu)")
            
            token = None

            while token is None:
                username = input("Username: ").strip()
                if username.lower() == 'cancel':
                    break
            
                password = input("Password: ").strip()
                if password.lower() == 'cancel':
                    break


                token = my_bank.Login(username, password)


                if not token:
                    print("Please try again.")
                    print("-" * 30)


            if token:
                
                logged_in = True

                while logged_in:

                    

                    Accounts = session["Accounts"]

                    print(f"\n---- Account Menu: {username} ----")

                    print("Your Accounts:")
                    for i, acc in enumerate(Accounts):
                        acc_type = type(acc).__name__

                        print(f" [{i}] {acc_type} (ID: {acc.Acc_num}) - Balance: ${acc.Get_Bal():.2f}")

                    funct = input("What would you like to do next (Withdraw, Deposit, Transfer, or Logout): ")

                    session = my_bank.Get_Session(token)

                    if not session:
                        logged_in = False
                        break

                    if funct == "Withdraw":
                        try:
                            Money = float(input("how much withdraw: "))
                            print("New balance: ", Accounts[0].Withdraw(Money))
                        except ValueError as e:
                            print(f"Transaction failed: {e}")


                    elif funct == "Deposit":
                        try:
                            Money = float(input("how much deposit: "))
                            print("New balance: ", Accounts[0].Deposit(Money))
                        except ValueError as e:
                            print(f"Transaction failed: {e}")
                    

                    elif funct == "Transfer":
                        try:
                            Money = float(input("Enter how much you would like to transfer: "))
                            Acc = int(input("Enter which account you would like to tranfer to: "))
                            if Acc < 5:
                                print("you have", Accounts[0].Move_money(Money, Accounts[Acc]), "remaining...")
                            else:
                                print("Invalid account number.")
                        except ValueError as e:
                            print(f"Transaction failed: {e}")

                    elif funct == "Logout":
                        my_bank.Logout(token)
                        logged_in = False


                    else:
                        print("Invalid option. Try again!")

        elif start_menu == '3':
            print("Exiting the application...")
            break

if __name__ == "__main__":
    main()