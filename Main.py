import time
from Bank_class import Bank
from Account_Classes import Checking, Savings

def main():
    # Initialize the core Bank engine
    my_bank = Bank()
    next_account_num = 0

    # Main application loop
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

            # Give the new user a default Checking and Savings account
            new_accounts = [Checking(next_account_num), Savings(next_account_num + 1)]
            next_account_num += 2

            my_bank.Register(username, password, new_accounts)

        elif start_menu == "2":
            print("\n---- Login ----")
            print("(Type 'cancel' at any time to return to the main menu)")
            
            token = None

            # Keep asking for credentials until successful or canceled
            while token is None:
                username = input("Username: ").strip()
                if username.lower() == 'cancel':
                    break
            
                password = input("Password: ").strip()
                if password.lower() == 'cancel':
                    break

                # Attempt to get a session token
                token = my_bank.Login(username, password)

                if not token:
                    print("Please try again.")
                    print("-" * 30)

            # If we successfully got a token, enter the secondary user menu loop
            if token:
                logged_in = True

                while logged_in:

                    # Fetch session to ensure it hasn't timed out
                    session = my_bank.Get_Session(token)
                    Accounts = session["Accounts"]

                    print(f"\n---- Account Menu: {username} ----")

                    print("Your Accounts:")
                    # Display all accounts and their balances
                    for i, acc in enumerate(Accounts):
                        acc_type = type(acc).__name__
                        print(f" [{i}] {acc_type} (ID: {acc.Acc_num}) - Balance: ${acc.Get_Bal():.2f}")

                    funct = input("What would you like to do next (Withdraw, Deposit, Transfer, or Logout): ")

                    # Double check session status before executing a transaction
                    session = my_bank.Get_Session(token)
                    if not session:
                        logged_in = False
                        break
                    
                    # User was active, so refresh their timeout clock
                    my_bank.Sesh_Refresh(token)
                    Accounts = session["Accounts"]

                    # Handle Withdrawal logic
                    if funct == "Withdraw":
                        try:
                            acc_idx = int(input("Enter the account index (e.g., 0 for Checking, 1 for Savings): "))
                            # Validate the user picked a real account index
                            if 0 <= acc_idx < len(Accounts):
                                Money = float(input("Enter how much you would like to withdraw: "))
                                print("New balance: $", Accounts[acc_idx].Withdraw(Money))
                            else:
                                print("Invalid account index.")
                        except ValueError as e:
                            print(f"Transaction failed: {e}")

                    # Handle Deposit logic
                    elif funct == "Deposit":
                        try:
                            acc_idx = int(input("Enter the account index (e.g., 0 for Checking, 1 for Savings): "))
                            if 0 <= acc_idx < len(Accounts):
                                Money = float(input("Enter how much you would like to deposit: "))
                                print("New balance: $", Accounts[acc_idx].Deposit(Money))
                            else:
                                print("Invalid account index.")
                        except ValueError as e:
                            print(f"Transaction failed: {e}")
                    
                    # Handle Transfer logic between two accounts
                    elif funct == "Transfer":
                        try:
                            source_idx = int(input("Enter the account index to transfer FROM: "))
                            target_idx = int(input("Enter the account index to transfer TO: "))
                            
                            # Ensure both selected accounts exist
                            if (0 <= source_idx < len(Accounts)) and (0 <= target_idx < len(Accounts)):
                                Money = float(input("Enter how much you would like to transfer: "))
                                # Move money from source to target
                                remaining = Accounts[source_idx].Move_money(Money, Accounts[target_idx])
                                print(f"Transfer successful. You have ${remaining} remaining in the source account.")
                            else:
                                print("Invalid account index.")
                        except ValueError as e:
                            print(f"Transaction failed: {e}")

                    # Handle safe session destruction
                    elif funct == "Logout":
                        my_bank.Logout(token)
                        logged_in = False # Breaks the inner loop

                    else:
                        print("Invalid option. Try again!")

        elif start_menu == '3':
            print("Exiting the application...")
            break # Breaks the outer main loop

if __name__ == "__main__":
    main()