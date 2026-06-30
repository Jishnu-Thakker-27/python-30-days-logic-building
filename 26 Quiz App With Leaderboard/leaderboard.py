def show_leaderboard_menu(users):
    while True:
        print("\n" + "=" * 35)
        print("          LEADERBOARD MENU")
        print("=" * 35)
        print("1. View Global Leaderboard")
        print("2. View Category Leaderboards")
        print("3. Back to Main Menu")
        print("=" * 35)

        choice = input("Enter your choice (1-3): ").strip()
        if choice == '1':
            show_global_leaderboard(users)
        elif choice == '2':
            show_category_leaderboard(users)
        elif choice == '3':
            break
        else:
            print("\n[Invalid Selection] Please choose a valid option (1-3).")

def show_global_leaderboard(users):
    # Filter out admin accounts and users who haven't played any quiz yet
    players = [u for u in users if not u.get("is_admin", False) and u.get("quizzes_played", 0) > 0]

    print("\n" + "=" * 65)
    print("                      GLOBAL LEADERBOARD")
    print("=" * 65)

    if not players:
        print("  No entries yet! Play a quiz to claim the first spot.")
        print("=" * 65)
        input("\nPress Enter to continue...")
        return

    # Sort: 1) high_score (desc), 2) total_score (desc), 3) quizzes_played (asc)
    players.sort(key=lambda u: (-u.get("high_score", 0), -u.get("total_score", 0), u.get("quizzes_played", 0)))

    # Print Table Header
    print(f"{'Rank':<6} | {'Username':<20} | {'High Score':<12} | {'Total Score':<12} | {'Played':<6}")
    print("-" * 65)

    for rank, player in enumerate(players, 1):
        print(f"{rank:<6} | {player['username']:<20} | {player.get('high_score', 0):<12} | {player.get('total_score', 0):<12} | {player.get('quizzes_played', 0):<6}")
    
    print("=" * 65)
    input("\nPress Enter to continue...")

def show_category_leaderboard(users):
    # Collect all categories played across all non-admin users
    categories = set()
    players = [u for u in users if not u.get("is_admin", False)]
    
    for u in players:
        if "category_stats" in u:
            for cat in u["category_stats"].keys():
                categories.add(cat)

    if not categories:
        print("\nNo category data available yet. Play a category-specific quiz first!")
        input("\nPress Enter to continue...")
        return

    sorted_categories = sorted(list(categories))

    print("\n" + "=" * 35)
    print("        SELECT CATEGORY LEADERBOARD")
    print("=" * 35)
    for idx, cat in enumerate(sorted_categories, 1):
        print(f"{idx}. {cat}")
    print(f"{len(sorted_categories) + 1}. Cancel")
    print("=" * 35)

    while True:
        choice = input(f"Enter choice (1-{len(sorted_categories) + 1}): ").strip()
        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        choice_num = int(choice)
        if choice_num == len(sorted_categories) + 1:
            return
        elif 1 <= choice_num <= len(sorted_categories):
            selected_cat = sorted_categories[choice_num - 1]
            break
        else:
            print(f"Please select a number between 1 and {len(sorted_categories) + 1}.")

    # Gather players who played this category
    cat_players = []
    for u in players:
        if "category_stats" in u and selected_cat in u["category_stats"]:
            stats = u["category_stats"][selected_cat]
            if stats.get("played", 0) > 0:
                cat_players.append({
                    "username": u["username"],
                    "high_score": stats.get("high_score", 0),
                    "total_score": stats.get("total_score", 0),
                    "played": stats.get("played", 0)
                })

    print("\n" + "=" * 65)
    print(f"             LEADERBOARD FOR CATEGORY: {selected_cat.upper()}")
    print("=" * 65)

    if not cat_players:
        print("  No entries yet for this category! Be the first to play.")
        print("=" * 65)
        input("\nPress Enter to continue...")
        return

    # Sort by high score (desc), total score (desc), played (asc)
    cat_players.sort(key=lambda p: (-p["high_score"], -p["total_score"], p["played"]))

    # Print Table Header
    print(f"{'Rank':<6} | {'Username':<20} | {'High Score':<12} | {'Total Score':<12} | {'Played':<6}")
    print("-" * 65)

    for rank, player in enumerate(cat_players, 1):
        print(f"{rank:<6} | {player['username']:<20} | {player['high_score']:<12} | {player['total_score']:<12} | {player['played']:<6}")

    print("=" * 65)
    input("\nPress Enter to continue...")

def show_user_stats(logged_user):
    print("\n" + "=" * 45)
    print(f"       PERSONAL STATISTICS - {logged_user['username'].upper()}")
    print("=" * 45)
    print(f"Quizzes Played:   {logged_user.get('quizzes_played', 0)}")
    print(f"Accumulated Score: {logged_user.get('total_score', 0)} pts")
    print(f"Personal High:    {logged_user.get('high_score', 0)} pts")
    print("-" * 45)
    print("Category Breakdown:")
    
    cat_stats = logged_user.get("category_stats", {})
    if not cat_stats:
        print("  No category data recorded yet.")
    else:
        print(f"  {'Category':<20} | {'Played':<6} | {'High Score':<10}")
        print("  " + "-" * 41)
        for cat, stats in sorted(cat_stats.items()):
            print(f"  {cat:<20} | {stats.get('played', 0):<6} | {stats.get('high_score', 0):<10}")
            
    print("=" * 45)
    input("\nPress Enter to return to the menu...")
