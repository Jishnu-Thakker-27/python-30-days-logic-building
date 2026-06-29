from main_menu import register, login
from user_menu import balance, deposit, withdraw, transfer, transaction_history
from storage import user_load

def main_menu():
    while True:
        print("\n" + "=" * 37)
        print("     MULTI-USER BANKING SYSTEM     ")
        print("=" * 37)
        print("1. Register New Account")
        print("2. Login to Account")
        print("3. Exit")
        print("=" * 37)

        choice = input("Enter your choice (1-3): ").strip()

        if choice == '1':
            user_data = user_load()
            register(user_data)
        elif choice == '2':
            user_data = user_load()
            logged_user = login(user_data)
            if logged_user:
                user_menu(logged_user)
        elif choice == '3':
            print("\nThank you for using the banking system. Goodbye!")
            break
        else:
            print("\n[Invalid Selection] Please choose a valid option (1, 2, or 3).")

def user_menu(logged_user):
    while True:
        print("\n" + "=" * 35)
        print(f"  USER MENU - {logged_user['username'].upper()} ({logged_user['account_number']})")
        print("=" * 35)
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. View Transaction History")
        print("6. Logout")
        print("=" * 35)

        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            balance(logged_user)
        elif choice == '2':
            deposit(logged_user)
        elif choice == '3':
            withdraw(logged_user)
        elif choice == '4':
            transfer(logged_user)
        elif choice == '5':
            transaction_history(logged_user)
        elif choice == '6':
            print("\nLogged out successfully.")
            break
        else:
            print("\n[Invalid Selection] Please choose a valid option (1-6).")

if __name__ == "__main__":
    main_menu()