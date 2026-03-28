while True:
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Spending")
    print("4. Exit")

    task = int(input("Enter your choice: "))

    # Safe read
    with open("expense.txt") as f:
        data = f.read()

    if task == 1:
        category = input("Enter Category: ")
        amount = int(input("Enter Amount Spent: "))
        New_data = f"{category}-{amount}\n"

        with open("expense.txt", "a") as f:
            f.write(New_data)
        with open("expense.txt", "r") as f:
            print(f.read())

        

    elif task == 2:
        if data.strip() == "":
            print("No expenses added yet.")
        else:
            print(data)

    elif task == 3:
        with open("expense.txt") as f:
            datas=f.readlines()
        total_amount = 0
        for item in datas:
            category, amount = item.strip().split("-")
            total_amount += int(amount)
        print("Total Spending:", total_amount)

    elif task == 4:
        print("Exiting...")
        break

    else:
        print("Invalid choice")
