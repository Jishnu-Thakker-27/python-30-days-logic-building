from storage import load_quizzes, save_quizzes, save_users

def admin_menu(users, logged_user):
    # Security check
    if not logged_user.get("is_admin", False):
        print("\n[Access Denied] Admin privileges required.")
        return

    while True:
        print("\n" + "=" * 35)
        print("            ADMIN MENU")
        print("=" * 35)
        print("1. View All Questions")
        print("2. Add a New Question")
        print("3. Delete a Question")
        print("4. Reset Leaderboards / Stats")
        print("5. Back to Main Menu")
        print("=" * 35)

        choice = input("Enter choice (1-5): ").strip()
        quizzes = load_quizzes()

        if choice == '1':
            view_all_questions(quizzes)
        elif choice == '2':
            add_question(quizzes)
        elif choice == '3':
            delete_question(quizzes)
        elif choice == '4':
            reset_stats(users)
        elif choice == '5':
            break
        else:
            print("\n[Invalid Selection] Please choose a valid option (1-5).")

def view_all_questions(quizzes):
    print("\n--- VIEW ALL QUESTIONS ---")
    if not quizzes:
        print("No questions available.")
        return

    page_size = 5
    for idx, q in enumerate(quizzes):
        if idx > 0 and idx % page_size == 0:
            cont = input(f"\nShown {idx}/{len(quizzes)} questions. Press Enter to view more or type 'q' to quit: ").strip().lower()
            if cont == 'q':
                break

        print(f"\n[ID: {q['id']}] Category: {q['category']} | Difficulty: {q['difficulty']}")
        print(f"Q: {q['question']}")
        print(f"  A. {q['options']['A']}")
        print(f"  B. {q['options']['B']}")
        print(f"  C. {q['options']['C']}")
        print(f"  D. {q['options']['D']}")
        print(f"Correct Answer: {q['answer']}")
        print(f"Explanation: {q['explanation']}")
        print("-" * 50)
    
    input("\nFinished viewing questions. Press Enter to continue...")

def add_question(quizzes):
    print("\n--- ADD A NEW QUESTION ---")
    print("(Type 'cancel' at any prompt to cancel)")

    category = input("Enter category (e.g. Programming, Science): ").strip()
    if category.lower() == 'cancel': return
    if not category:
        print("Category cannot be empty.")
        return

    while True:
        difficulty = input("Enter difficulty (Easy, Medium, Hard): ").strip().capitalize()
        if difficulty.lower() == 'cancel': return
        if difficulty in ["Easy", "Medium", "Hard"]:
            break
        print("Invalid difficulty. Must be Easy, Medium, or Hard.")

    question_text = input("Enter question text: ").strip()
    if question_text.lower() == 'cancel': return
    if not question_text:
        print("Question text cannot be empty.")
        return

    options = {}
    for letter in ["A", "B", "C", "D"]:
        opt_text = input(f"Enter option {letter}: ").strip()
        if opt_text.lower() == 'cancel': return
        if not opt_text:
            print("Option text cannot be empty.")
            return
        options[letter] = opt_text

    while True:
        correct_ans = input("Enter correct answer letter (A, B, C, or D): ").strip().upper()
        if correct_ans.lower() == 'cancel': return
        if correct_ans in ["A", "B", "C", "D"]:
            break
        print("Invalid option. Must be A, B, C, or D.")

    explanation = input("Enter explanation: ").strip()
    if explanation.lower() == 'cancel': return
    if not explanation:
        print("Explanation cannot be empty.")
        return

    # Calculate next ID
    next_id = max([q["id"] for q in quizzes], default=0) + 1

    new_q = {
        "id": next_id,
        "category": category,
        "difficulty": difficulty,
        "question": question_text,
        "options": options,
        "answer": correct_ans,
        "explanation": explanation
    }

    quizzes.append(new_q)
    save_quizzes(quizzes)
    print(f"\n[Success] Question added successfully with ID: {next_id}!")

def delete_question(quizzes):
    print("\n--- DELETE A QUESTION ---")
    print("(Type 'cancel' to go back)")

    id_str = input("Enter the ID of the question to delete: ").strip()
    if id_str.lower() == 'cancel':
        return
    if not id_str.isdigit():
        print("Invalid ID. ID must be an integer.")
        return

    q_id = int(id_str)
    
    # Find question
    matched_q = None
    for q in quizzes:
        if q["id"] == q_id:
            matched_q = q
            break

    if not matched_q:
        print(f"No question found with ID: {q_id}.")
        return

    # Confirm delete
    print(f"\nFound Question [ID: {q_id}]: '{matched_q['question']}'")
    confirm = input("Are you sure you want to delete this question? (yes/no): ").strip().lower()
    if confirm == 'yes':
        quizzes.remove(matched_q)
        save_quizzes(quizzes)
        print(f"\n[Success] Question ID {q_id} deleted successfully.")
    else:
        print("Deletion cancelled.")

def reset_stats(users):
    print("\n" + "!" * 40)
    print(" WARNING: RESET ALL USER SCORES & STATS")
    print(" This will clear high scores, total scores,")
    print(" and category records for all registered users.")
    print(" This operation cannot be undone!")
    print("!" * 40)
    
    confirm = input("Type 'RESET' to confirm or anything else to cancel: ").strip()
    if confirm == 'RESET':
        for u in users:
            u["quizzes_played"] = 0
            u["total_score"] = 0
            u["high_score"] = 0
            u["category_stats"] = {}
        save_users(users)
        print("\n[Success] All user statistics and leaderboards have been reset.")
    else:
        print("\nReset operation cancelled.")
