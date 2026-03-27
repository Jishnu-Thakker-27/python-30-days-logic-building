def signin():
    name = input("Enter Your Name: ")
    password = input("Enter your password: ")
    confirm_password = input("Confirm your password: ")

    if password != confirm_password:
        print("Invalid Password Confirmation")
        return

    with open("login.txt", "r") as f:
        data = f.readlines()

    for line in data:
        stored_name, stored_password = line.strip().split("\t")

        if name == stored_name:
            print("User already exists! Please login.")
            return

    with open("login.txt", "a") as f:
        f.write(f"{name}\t{password}\n")

    print("Signup successful!")


def login():
    name = input("Enter Your Name: ")
    password = input("Enter your password: ")

    with open("login.txt", "r") as f:
        data = f.readlines()

    for line in data:
        stored_name, stored_password = line.strip().split("\t")

        if name == stored_name and password == stored_password:
            print("Login successful!")
            return

    print("Invalid Login credentials")

print("Welcome to the website.")
print("1. Login")
print("2. Sign Up")

user = int(input("Enter 1 for Login and 2 for SignUp: "))

if user == 1:
    login()
elif user == 2:
    signin()
else:
    print("Invalid choice")
