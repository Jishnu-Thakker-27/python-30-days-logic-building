expenses = []

while True:
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Spending")
    print("4. Exit")

    task = int(input("Enter your choice: "))

    if task == 1:
        category = input("Enter Category: ")
        amount = int(input("Enter Amount Spent: "))
        expenses.append({"category": category, "amount": amount})

    elif task == 2:
        if not expenses:
            print("No expenses added yet.")
        else:
            for item in expenses:
                print(item["category"], "-", item["amount"])

    elif task == 3:
        total_amount = 0
        for item in expenses:
            total_amount += item["amount"]
        print("Total Spending:", total_amount)

    elif task == 4:
        print("Exiting...")
        break

    else:
        print("Invalid choice")
