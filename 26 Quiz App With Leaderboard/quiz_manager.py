import random
import time
from storage import load_quizzes, save_users

def calculate_score(difficulty, time_taken):
    # Base score by difficulty
    if difficulty == "Easy":
        base_points = 10
    elif difficulty == "Medium":
        base_points = 20
    else: # Hard
        base_points = 30

    # Speed bonus multiplier
    multiplier = 1.0
    bonus_earned = 0
    if time_taken <= 5.0:
        multiplier = 2.0
        bonus_earned = 1
    elif time_taken <= 10.0:
        multiplier = 1.5
        bonus_earned = 1

    points_earned = int(base_points * multiplier)
    return points_earned, bonus_earned, multiplier

def play_quiz(logged_user, users_list):
    questions = load_quizzes()
    if not questions:
        print("\n[Error] No questions available in the database. Please contact an admin.")
        return

    # Extract unique categories
    categories = sorted(list(set(q["category"] for q in questions)))

    print("\n" + "=" * 35)
    print("           START A NEW QUIZ")
    print("=" * 35)
    print("Select a Category:")
    for idx, cat in enumerate(categories, 1):
        print(f"{idx}. {cat}")
    print(f"{len(categories) + 1}. All Categories (Mixed)")
    print(f"{len(categories) + 2}. Cancel")

    # Category selection prompt
    while True:
        cat_choice = input(f"Enter choice (1-{len(categories) + 2}): ").strip()
        if not cat_choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue
        choice_num = int(cat_choice)
        if choice_num == len(categories) + 2:
            print("Quiz cancelled.")
            return
        elif choice_num == len(categories) + 1:
            selected_category = "Mixed"
            break
        elif 1 <= choice_num <= len(categories):
            selected_category = categories[choice_num - 1]
            break
        else:
            print(f"Please select a number between 1 and {len(categories) + 2}.")

    # Difficulty selection prompt
    print("\nSelect Difficulty:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    print("4. Any Difficulty")
    print("5. Cancel")

    while True:
        diff_choice = input("Enter choice (1-5): ").strip()
        if diff_choice == '5':
            print("Quiz cancelled.")
            return
        elif diff_choice == '1':
            selected_difficulty = "Easy"
            break
        elif diff_choice == '2':
            selected_difficulty = "Medium"
            break
        elif diff_choice == '3':
            selected_difficulty = "Hard"
            break
        elif diff_choice == '4':
            selected_difficulty = "Any"
            break
        else:
            print("Please select a valid option (1-5).")

    # Filter questions
    filtered_questions = []
    for q in questions:
        # Match category
        cat_match = (selected_category == "Mixed" or q["category"] == selected_category)
        # Match difficulty
        diff_match = (selected_difficulty == "Any" or q["difficulty"] == selected_difficulty)
        
        if cat_match and diff_match:
            filtered_questions.append(q)

    if not filtered_questions:
        print(f"\n[Warning] No questions found for Category: '{selected_category}' and Difficulty: '{selected_difficulty}'.")
        return

    # Shuffle and select up to 5 questions
    random.shuffle(filtered_questions)
    quiz_questions = filtered_questions[:5]
    total_quiz_questions = len(quiz_questions)

    print("\n" + "=" * 35)
    print(f" Quiz Category: {selected_category}")
    print(f" Difficulty: {selected_difficulty}")
    print(f" Questions: {total_quiz_questions}")
    print("=" * 35)
    print("Answering Speed Bonus System:")
    print("  * Under 5 seconds  -> 2.0x Score Bonus")
    print("  * Under 10 seconds -> 1.5x Score Bonus")
    print("  * Type 'quit' to exit the quiz early.")
    print("=" * 35)
    input("Press Enter to begin the quiz...")

    quiz_score = 0
    correct_count = 0
    speed_bonuses_earned = 0

    for i, q in enumerate(quiz_questions, 1):
        print("\n" + "-" * 50)
        print(f"Question {i} of {total_quiz_questions} [{q['difficulty']} - {q['category']}]")
        print("-" * 50)
        print(q["question"])
        for opt_key, opt_val in sorted(q["options"].items()):
            print(f"  {opt_key}. {opt_val}")
        print("-" * 50)

        # Start timer
        start_time = time.time()

        # Prompt for answer
        while True:
            ans = input("Your Answer (A/B/C/D or 'quit'): ").strip().upper()
            if ans == 'QUIT':
                print("\nYou exited the quiz early.")
                break
            if ans in ['A', 'B', 'C', 'D']:
                break
            print("Invalid input. Please choose A, B, C, D, or 'quit'.")

        if ans == 'QUIT':
            break

        end_time = time.time()
        time_taken = end_time - start_time

        # Scoring
        is_correct = (ans == q["answer"].upper())
        if is_correct:
            correct_count += 1
            points_earned, bonus_earned, multiplier = calculate_score(q["difficulty"], time_taken)
            speed_bonuses_earned += bonus_earned
            quiz_score += points_earned
            
            bonus_msg = ""
            if multiplier == 2.0:
                bonus_msg = " (2x Time Speed Bonus!)"
            elif multiplier == 1.5:
                bonus_msg = " (1.5x Time Speed Bonus!)"
                
            print(f"\n[CORRECT] Answering time: {time_taken:.2f}s{bonus_msg}")
            print(f"Points Earned: +{points_earned} (Current Score: {quiz_score})")
        else:
            print(f"\n[INCORRECT] Answering time: {time_taken:.2f}s")
            print(f"The correct answer was: {q['answer']}")
        
        print(f"\nExplanation:\n{q['explanation']}")
        time.sleep(1)

    # Quiz finished summary
    print("\n" + "=" * 35)
    print("          QUIZ COMPLETED")
    print("=" * 35)
    print(f"Correct Answers: {correct_count}/{total_quiz_questions}")
    print(f"Speed Bonuses:   {speed_bonuses_earned}")
    print(f"Final Score:     {quiz_score} pts")
    print("=" * 35)

    # Save user statistics
    if logged_user:
        # Mutate in place since it's passed from main's logged_user
        logged_user["quizzes_played"] += 1
        logged_user["total_score"] += quiz_score
        if quiz_score > logged_user["high_score"]:
            logged_user["high_score"] = quiz_score

        # Update category stats
        if "category_stats" not in logged_user:
            logged_user["category_stats"] = {}
        
        cat_stats = logged_user["category_stats"].get(selected_category, {
            "played": 0,
            "high_score": 0,
            "total_score": 0
        })
        cat_stats["played"] += 1
        cat_stats["total_score"] += quiz_score
        if quiz_score > cat_stats["high_score"]:
            cat_stats["high_score"] = quiz_score
            
        logged_user["category_stats"][selected_category] = cat_stats
        
        # Save back to database file
        save_users(users_list)
        print("Your progress has been saved to your profile!")
    else:
        print("Playing as Guest. Log in to save scores to the leaderboard!")
    
    input("\nPress Enter to return to the menu...")
