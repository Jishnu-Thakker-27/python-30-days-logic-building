from storage import save_users

def register(users):
    print("\n" + "-" * 35)
    print("       REGISTER NEW ACCOUNT")
    print("-" * 35)
    print("(Type 'cancel' at any prompt to return to the menu)")

    while True:
        username = input("Choose a username: ").strip()
        if username.lower() == 'cancel':
            print("Registration cancelled.")
            return None
        if not username:
            print("Username cannot be empty. Please try again.")
            continue
        if " " in username:
            print("Username cannot contain spaces. Please try again.")
            continue
            
        # Check if username already exists (case-insensitive)
        user_exists = any(u["username"].lower() == username.lower() for u in users)
        if user_exists:
            print("Username is already taken. Please choose another one.")
            continue
        break

    while True:
        password = input("Choose a password: ")
        if password.lower() == 'cancel':
            print("Registration cancelled.")
            return None
        if not password:
            print("Password cannot be empty. Please try again.")
            continue
            
        confirm_password = input("Confirm your password: ")
        if confirm_password.lower() == 'cancel':
            print("Registration cancelled.")
            return None
            
        if password != confirm_password:
            print("Passwords do not match. Please try again.")
            continue
        break

    # Construct the user dictionary with empty stats
    new_user = {
        "username": username,
        "password": password,
        "is_admin": False,
        "quizzes_played": 0,
        "total_score": 0,
        "high_score": 0,
        "category_stats": {}
    }
    
    users.append(new_user)
    save_users(users)
    print(f"\n[Success] Account for '{username}' created successfully! You can now log in.")
    return new_user

def login(users):
    print("\n" + "-" * 35)
    print("            USER LOGIN")
    print("-" * 35)
    print("(Type 'cancel' at any prompt to return to the menu)")

    attempts = 3
    while attempts > 0:
        username = input("Enter username: ").strip()
        if username.lower() == 'cancel':
            print("Login cancelled.")
            return None
        if not username:
            print("Username cannot be empty.")
            continue

        # Find user
        matched_user = None
        for u in users:
            if u["username"].lower() == username.lower():
                matched_user = u
                break

        if not matched_user:
            attempts -= 1
            print(f"Username not found. {attempts} attempt(s) remaining.")
            if attempts == 0:
                break
            continue

        password = input("Enter password: ")
        if password.lower() == 'cancel':
            print("Login cancelled.")
            return None

        if matched_user["password"] == password:
            print(f"\n[Success] Welcome back, {matched_user['username']}!")
            return matched_user
        else:
            attempts -= 1
            print(f"Incorrect password. {attempts} attempt(s) remaining.")

    print("\n[Failed] Too many failed login attempts. Returning to the main menu.")
    return None
