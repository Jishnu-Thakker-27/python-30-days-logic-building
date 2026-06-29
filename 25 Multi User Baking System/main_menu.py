import random
import datetime
from storage import user_save, banking_load, banking_save, transactions_load, transactions_save

def register(user_data):
    print("\n--- REGISTER NEW ACCOUNT ---")
    print("(Type 'cancel' at any prompt to go back to the main menu)")
    
    username = input("Enter your name: ").strip()
    if username.lower() == 'cancel':
        return None
    if not username:
        print("Name cannot be empty.")
        return None
        
    existing_accs = {acc["account_number"] for acc in user_data}
    while True:
        acc_choice = input("Would you like to: \n1. Auto-generate account number\n2. Choose your own\nEnter choice: ").strip()
        if acc_choice.lower() == 'cancel':
            return None
        if acc_choice == '1':
            while True:
                account_number = str(random.randint(1000, 9999))
                if account_number not in existing_accs:
                    break
            print(f"Your auto-generated account number is: {account_number}")
            break
        elif acc_choice == '2':
            account_number = input("Enter a unique 4-digit account number: ").strip()
            if account_number.lower() == 'cancel':
                return None
            if len(account_number) != 4 or not account_number.isdigit():
                print("Account number must be exactly 4 digits.")
                continue
            if account_number in existing_accs:
                print("This account number is already taken. Please choose another one.")
                continue
            break
        else:
            print("Invalid choice. Please select 1 or 2.")

    # Password prompt loop
    while True:
        password = input("Enter password: ")
        if password.lower() == 'cancel':
            return None
        if not password:
            print("Password cannot be empty.")
            continue
        confirm_password = input("Confirm password: ")
        if confirm_password.lower() == 'cancel':
            return None
        if password != confirm_password:
            print("Password doesn't match. Please try again.")
            continue
        break

    # Transaction PIN prompt loop
    while True:
        transaction_pin = input("Create a 4-digit transaction PIN: ").strip()
        if transaction_pin.lower() == 'cancel':
            return None
        if len(transaction_pin) != 4 or not transaction_pin.isdigit():
            print("Transaction PIN must be exactly 4 digits.")
            continue
        confirm_transaction_pin = input("Confirm transaction PIN: ").strip()
        if confirm_transaction_pin.lower() == 'cancel':
            return None
        if transaction_pin != confirm_transaction_pin:
            print("Transaction PIN doesn't match. Please try again.")
            continue
        break

    # Account type prompt
    while True:
        acc_type_choice = input("Select Account Type:\n1. Savings\n2. Current\nEnter choice: ").strip()
        if acc_type_choice.lower() == 'cancel':
            return None
        if acc_type_choice == '1':
            account_type = "Savings"
            break
        elif acc_type_choice == '2':
            account_type = "Current"
            break
        else:
            print("Invalid choice. Please choose 1 or 2.")

    # Starting balance prompt
    while True:
        starting_bal_str = input("Enter initial deposit amount (minimum 0): ").strip()
        if starting_bal_str.lower() == 'cancel':
            return None
        try:
            starting_bal = float(starting_bal_str)
            if starting_bal < 0:
                print("Amount cannot be negative.")
                continue
            break
        except ValueError:
            print("Invalid amount. Please enter a valid number.")

    # Save to users.json
    account = {
        "username": username,
        "password": password,
        "account_number": account_number,
        "transaction_pin": transaction_pin
    }
    user_data.append(account)
    user_save(user_data)

    # Save to banking_data.json
    banking_data = banking_load()
    banking_data[account_number] = {
        "name": username,
        "balance": starting_bal,
        "account_type": account_type
    }
    banking_save(banking_data)

    # Initialize transactions.json
    transactions = transactions_load()
    transactions[account_number] = []
    if starting_bal > 0:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transactions[account_number].append({
            "timestamp": timestamp,
            "type": "Deposit",
            "amount": starting_bal,
            "description": "Initial deposit at registration",
            "balance_after": starting_bal
        })
    transactions_save(transactions)

    print(f"\nAccount registered successfully! Account Number: {account_number}")
    return account


def login(user_data):
    print("\n--- LOGIN ---")
    print("(Type 'cancel' at any prompt to go back)")
    
    attempts = 3
    while attempts > 0:
        account_number = input("Enter your account number: ").strip()
        if account_number.lower() == 'cancel':
            return None
        
        # Check if user exists
        user_found = None
        for user in user_data:
            if user["account_number"] == account_number:
                user_found = user
                break
        
        if not user_found:
            print("Account number not registered. Please register first.")
            return None
        
        # Verify password
        password = input("Enter password: ")
        if password.lower() == 'cancel':
            return None
            
        if password == user_found["password"]:
            print(f"\nLogin successful! Welcome, {user_found['username']}.")
            return user_found
        else:
            attempts -= 1
            print(f"Incorrect password. {attempts} attempt(s) remaining.")
            
    print("Too many failed login attempts. Returning to main menu.")
    return None