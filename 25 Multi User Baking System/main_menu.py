import json

def register(user_data):
    account = {}

    username = input("Enter your name: ")
    account_number = input("Enter your account number: ")

    for existing_account in user_data:
        if account_number == existing_account["account_number"]:
            print("This account has already been registered. Please try to login.")
            return login(user_data)

    while True:
        password = input("Enter password: ")
        confirm_password = input("Confirm password: ")

        if password != confirm_password:
            print("Password doesn't match.")
            print("Retry entering same password.")
            continue
        else:
            break

    while True:
        transaction_pin = input("Create a 4 digit transaction PIN: ")
        confirm_transaction_pin = input("Confirm transaction PIN: ")

        if transaction_pin != confirm_transaction_pin:
            print("Transaction PIN doesn't match.")
            print("Retry entering same transaction PIN.")
            continue

        elif len(transaction_pin) != 4 or not transaction_pin.isdigit():
            print("Transaction PIN must be exactly 4 digits.")
            continue

        else:
            break

    account["username"] = username
    account["password"] = password
    account["account_number"] = account_number
    account["transaction_pin"] = transaction_pin

    user_data.append(account)

    with open("users.json", "w") as f:
        json.dump(user_data, f, indent=4)

    print("Your account has been successfully registered.")
    print("Now login once to get started.")

    return login(user_data)


def login(user_data):
    account_number = input("Enter your account number: ")

    for existing_account in user_data:
        if account_number == existing_account["account_number"]:
            while True:
                password = input("Enter password: ")

                if password != existing_account["password"]:
                    print("Incorrect password. Please enter correct password.")
                    continue
                else:
                    print("Login done successfully.")
                    return existing_account

    print("The given account number is not registered. Please register first.")
    return register(user_data)