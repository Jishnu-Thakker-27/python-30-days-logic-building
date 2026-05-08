def login():
    username = input("Enter the username: ")
    password = input("Enter the password: ")

    try:
        with open("login.txt", "r") as f:
            data = f.readlines()
    except FileNotFoundError:
        print("No account found. Please sign in first.")
        return

    user_found = False

    for user in data:
        try:
            existing_user, existing_password = user.strip().split(":")
        except ValueError:
            continue

        if existing_password == password and existing_user == username:
            user_found = True
            break

    if user_found:
        print("You have been successfully logged in.")
    else:
        print("Invalid Username or Password")


def signin():
    special = "!@#$%^&*()_+-"

    username = input("Enter Unique Username: ")
    password = input("Enter The Password containing any of these special characters (!@#$%^&*()_+-): ")

    try:
        with open("login.txt", "r") as f:
            data = f.readlines()
    except FileNotFoundError:
        data = []

    user_found = False

    for user in data:
        try:
            existing_user, existing_password = user.strip().split(":")
        except ValueError:
            continue

        if existing_user == username:    #password can be same but we ask a user to give unique username while first time sign up.
            user_found = True
            break

    if user_found:
        print(f"{username} username already exists. Try to login or enter a unique username.")
        return signin()
    
    elif username == "" or password == "":
        print("Username and password cannot be empty.")
        return signin()
    
    elif ":" in username or ":" in password:  #while saving in file i save it as username:password so : will be in username or password it would cause confusion while spliting.
        print("Username and password cannot contain ':'.")
        return signin()



    elif any(char in special for char in password):
        with open("login.txt", "a") as f:
            f.write(f"{username}:{password}\n")

        print("Sign In Done Successfully.")
    else:
        print("Password must contain at least one special character.")
        return signin()


print("-----Welcome!-----")
print("1. Login")
print("2. Signin")

while True:
    try:
        action = int(input("Enter 1 for Login and 2 for Signin: "))
    except ValueError:
        print("Please enter only a number.")
        continue

    if action == 1:
        login()
    elif action == 2:
        signin()
    else:
        print("Invalid Input.")
