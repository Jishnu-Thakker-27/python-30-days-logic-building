import json
def passwords():
    password=input("Enter password. ")
    confirm_password=input("Confirm password. ")
    if password != confirm_password:
        print("Password doesn't match.")
        print("Retry entering same password.")
        return passwords()
    else:
        pass
def register():
    username=input("Enter your name. ")
    passwords()
    account_number=int(input("Enter your account number. "))
    
    # for account in 
    # if account_number==

def login():
    pass