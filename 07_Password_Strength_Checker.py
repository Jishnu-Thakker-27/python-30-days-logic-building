print("Password Should:-")
print("- Contains lowercase letters")
print("- Contains numbers")
print("- Contains uppercase letters")
print("- Contains special characters")
print("- Length is at least 8 characters\n")

special = "@#&%!?"

while True:
    password = input("Enter Your Password: ")

    contains_lowercase = False
    contains_uppercase = False
    contains_digit = False
    contains_special = False
    contains_space = False

    for char in password:
        if char.islower():
            contains_lowercase = True
        if char.isupper():
            contains_uppercase = True
        if char.isdigit():
            contains_digit = True
        if char in special:
            contains_special = True
        if char.isspace():
            contains_space = True

    error_found = False

    if len(password) < 8:
        print("Length must be at least 8 characters.")
        error_found = True

    if not contains_lowercase:
        print("Password should contain a lowercase letter.")
        error_found = True

    if not contains_uppercase:
        print("Password should contain an uppercase letter.")
        error_found = True

    if not contains_digit:
        print("Password should contain a number.")
        error_found = True

    if not contains_special:
        print("Password should contain a special character.")
        error_found = True

    if contains_space:
        print("Password should not contain spaces.")
        error_found = True

    if error_found:
        print("Enter password again.\n")
        continue
    else:
        print("Your password has been created successfully.")
        break