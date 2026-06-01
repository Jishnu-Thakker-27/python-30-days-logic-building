from main_menu import register
from main_menu import login
from user_menu import balance
from user_menu import deposit
from user_menu import withdraw
from user_menu import transfer
from user_menu import transaction_history
from storage import user_load

user_data=user_load()

def main_menu():
    while True:
        print("\n===== MULTI-USER BANKING SYSTEM =====")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Register selected")
            # Write register logic here
            continue

        elif choice == "2":
            print("Login selected")
            # Write login logic here
            user_menu()

        elif choice == "3":
            print("Thank you for using the banking system.")
            break

        else:
            print("Invalid choice. Please try again.")


def user_menu():
    while True:
        print("\n===== USER MENU =====")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. View Transaction History")
        print("6. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            print("Check Balance selected")
            # Write balance logic here

        elif choice == "2":
            print("Deposit Money selected")
            # Write deposit logic here

        elif choice == "3":
            print("Withdraw Money selected")
            # Write withdraw logic here

        elif choice == "4":
            print("Transfer Money selected")
            # Write transfer logic here

        elif choice == "5":
            print("Transaction History selected")
            # Write transaction history logic here

        elif choice == "6":
            print("Logged out successfully.")
            break

        else:
            print("Invalid choice. Please try again.")


main_menu()