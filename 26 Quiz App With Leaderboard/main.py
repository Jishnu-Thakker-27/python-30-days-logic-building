from storage import load_users, load_quizzes
from auth import login, register
from quiz_manager import play_quiz
from leaderboard import show_leaderboard_menu, show_user_stats
from admin import admin_menu

def main_menu():
    # Initial load and seeding
    users = load_users()
    load_quizzes()

    while True:
        print("\n" + "=" * 45)
        print("       INTERMEDIATE QUIZ APP & LEADERBOARD")
        print("=" * 45)
        print("1. User Login")
        print("2. Register New Account")
        print("3. Play as Guest")
        print("4. View Leaderboards")
        print("5. Exit")
        print("=" * 45)

        choice = input("Enter choice (1-5): ").strip()
        users = load_users()  # Reload in case file changed in background

        if choice == '1':
            logged_user = login(users)
            if logged_user:
                user_menu(logged_user, users)
        elif choice == '2':
            register(users)
        elif choice == '3':
            play_quiz(None, users)
        elif choice == '4':
            show_leaderboard_menu(users)
        elif choice == '5':
            print("\nThank you for playing! Goodbye!")
            break
        else:
            print("\n[Invalid Selection] Please choose a valid option (1-5).")

def user_menu(logged_user, users):
    is_admin = logged_user.get("is_admin", False)
    
    while True:
        print("\n" + "=" * 45)
        print(f"  PLAYER PORTAL - {logged_user['username'].upper()}")
        print("=" * 45)
        print("1. Play Quiz")
        print("2. View My Statistics")
        print("3. View Leaderboards")
        if is_admin:
            print("4. Administrator Panel")
            print("5. Logout")
        else:
            print("4. Logout")
        print("=" * 45)

        max_val = 5 if is_admin else 4
        choice = input(f"Enter choice (1-{max_val}): ").strip()

        users = load_users()  # Reload users database
        # Find active user object inside reloaded list to ensure we reference mutated state
        active_user = None
        for u in users:
            if u["username"].lower() == logged_user["username"].lower():
                active_user = u
                break
        
        if not active_user:
            print("\n[Session Error] Active user session not found. Logging out.")
            break

        if choice == '1':
            play_quiz(active_user, users)
        elif choice == '2':
            show_user_stats(active_user)
        elif choice == '3':
            show_leaderboard_menu(users)
        elif choice == '4':
            if is_admin:
                admin_menu(users, active_user)
            else:
                print("\nLogged out successfully.")
                break
        elif choice == '5' and is_admin:
            print("\nLogged out successfully.")
            break
        else:
            print(f"\n[Invalid Selection] Please choose a valid option (1-{max_val}).")

if __name__ == "__main__":
    main_menu()
