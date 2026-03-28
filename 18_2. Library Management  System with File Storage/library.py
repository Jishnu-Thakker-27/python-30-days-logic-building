while True:
    print("\nExpense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Total Spending")
    print("4. Exit")

    task = int(input("Enter your choice: "))
    with open("expense.txt") as f:
        data=f.read()
    if task == 1:
        with open("expense.txt","w") as f:
            category = input("Enter Category: ")
            amount = int(input("Enter Amount Spent: "))
            New_data=f"{category}-{amount}"
            data+=New_data
            f.write(data)
        print(data)

    elif task == 2:
        if data.strip()=""
            print("No expenses added yet.")
        else:
            for item in expenses:
                print(data)

    elif task == 3:
        with open("expense.txt") as f:
            datas=f.readlines()
        total_amount = 0
        for item in datas:
            total_amount += item[2]
        print("Total Spending:", total_amount)

    elif task == 4:
        print("Exiting...")
        break

    else:
        print("Invalid choice")
