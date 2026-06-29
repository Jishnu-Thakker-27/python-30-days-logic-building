import datetime
from storage import banking_load, banking_save, transactions_load, transactions_save

def verify_pin(logged_user):
    attempts = 3
    while attempts > 0:
        pin = input("Enter your 4-digit PIN: ").strip()
        if pin == logged_user["transaction_pin"]:
            return True
        attempts -= 1
        print(f"Incorrect PIN. {attempts} attempt(s) remaining.")
    print("Verification failed. Access denied.")
    return False

def balance(logged_user):
    if not verify_pin(logged_user):
        return
    
    banking_data = banking_load()
    acc_num = logged_user["account_number"]
    if acc_num in banking_data:
        bal = banking_data[acc_num]["balance"]
        print(f"\nAccount Balance: ${bal:,.2f}")
    else:
        print("Error: Account details not found in banking records.")

def deposit(logged_user):
    acc_num = logged_user["account_number"]
    print("\n--- DEPOSIT FUNDS ---")
    
    while True:
        amount_str = input("Enter amount to deposit: ").strip()
        if amount_str.lower() == 'cancel':
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Deposit amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    banking_data = banking_load()
    if acc_num not in banking_data:
        print("Error: Account details not found in banking records.")
        return

    current_balance = banking_data[acc_num]["balance"]
    new_balance = current_balance + amount
    banking_data[acc_num]["balance"] = new_balance
    banking_save(banking_data)

    # Log transaction
    transactions = transactions_load()
    if acc_num not in transactions:
        transactions[acc_num] = []
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions[acc_num].append({
        "timestamp": timestamp,
        "type": "Deposit",
        "amount": amount,
        "description": "Deposit via self-service",
        "balance_after": new_balance
    })
    transactions_save(transactions)

    print(f"\nSuccessfully deposited ${amount:,.2f}. New Balance: ${new_balance:,.2f}")

def withdraw(logged_user):
    acc_num = logged_user["account_number"]
    print("\n--- WITHDRAW FUNDS ---")
    
    while True:
        amount_str = input("Enter amount to withdraw: ").strip()
        if amount_str.lower() == 'cancel':
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Withdrawal amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    if not verify_pin(logged_user):
        return

    banking_data = banking_load()
    if acc_num not in banking_data:
        print("Error: Account details not found in banking records.")
        return

    current_balance = banking_data[acc_num]["balance"]
    if amount > current_balance:
        print(f"Insufficient funds. Your current balance is ${current_balance:,.2f}")
        return

    new_balance = current_balance - amount
    banking_data[acc_num]["balance"] = new_balance
    banking_save(banking_data)

    # Log transaction
    transactions = transactions_load()
    if acc_num not in transactions:
        transactions[acc_num] = []
        
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    transactions[acc_num].append({
        "timestamp": timestamp,
        "type": "Withdrawal",
        "amount": amount,
        "description": "Withdrawal via self-service",
        "balance_after": new_balance
    })
    transactions_save(transactions)

    print(f"\nSuccessfully withdrew ${amount:,.2f}. Remaining Balance: ${new_balance:,.2f}")

def transfer(logged_user):
    sender_acc = logged_user["account_number"]
    print("\n--- TRANSFER FUNDS ---")
    
    # Recipient verification
    banking_data = banking_load()
    while True:
        receiver_acc = input("Enter recipient's 4-digit account number: ").strip()
        if receiver_acc.lower() == 'cancel':
            return
        if receiver_acc == sender_acc:
            print("You cannot transfer money to your own account.")
            continue
        if receiver_acc not in banking_data:
            print("Recipient account number not found. Please try again.")
            continue
        break

    recipient_name = banking_data[receiver_acc]["name"]
    print(f"Recipient Found: {recipient_name}")

    while True:
        amount_str = input(f"Enter amount to transfer to {recipient_name}: ").strip()
        if amount_str.lower() == 'cancel':
            return
        try:
            amount = float(amount_str)
            if amount <= 0:
                print("Transfer amount must be greater than zero.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    if not verify_pin(logged_user):
        return

    # Check sufficient funds
    sender_balance = banking_data[sender_acc]["balance"]
    if amount > sender_balance:
        print(f"Insufficient funds. Your current balance is ${sender_balance:,.2f}")
        return

    # Perform transfer
    receiver_balance = banking_data[receiver_acc]["balance"]
    
    new_sender_bal = sender_balance - amount
    new_receiver_bal = receiver_balance + amount

    banking_data[sender_acc]["balance"] = new_sender_bal
    banking_data[receiver_acc]["balance"] = new_receiver_bal
    banking_save(banking_data)

    # Log transaction for sender and receiver
    transactions = transactions_load()
    if sender_acc not in transactions:
        transactions[sender_acc] = []
    if receiver_acc not in transactions:
        transactions[receiver_acc] = []

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Sender log (Debit)
    transactions[sender_acc].append({
        "timestamp": timestamp,
        "type": "Transfer Out",
        "amount": amount,
        "description": f"Transfer to Acc: {receiver_acc} ({recipient_name})",
        "balance_after": new_sender_bal
    })
    
    # Receiver log (Credit)
    transactions[receiver_acc].append({
        "timestamp": timestamp,
        "type": "Transfer In",
        "amount": amount,
        "description": f"Transfer from Acc: {sender_acc} ({logged_user['username']})",
        "balance_after": new_receiver_bal
    })
    
    transactions_save(transactions)

    print(f"\nSuccessfully transferred ${amount:,.2f} to {recipient_name}.")
    print(f"Your remaining balance is ${new_sender_bal:,.2f}")

def transaction_history(logged_user):
    acc_num = logged_user["account_number"]
    transactions = transactions_load()
    
    user_txs = transactions.get(acc_num, [])
    
    if not user_txs:
        print("\nNo transaction history found for this account.")
        return
        
    print(f"\n===== TRANSACTION HISTORY FOR ACC: {acc_num} =====")
    print(f"{'Date & Time':<20} | {'Type':<12} | {'Amount':<10} | {'Balance':<10} | {'Description'}")
    print("-" * 85)
    for tx in user_txs:
        t_time = tx.get("timestamp", "N/A")
        t_type = tx.get("type", "N/A")
        t_amount = tx.get("amount", 0.0)
        t_bal = tx.get("balance_after", 0.0)
        t_desc = tx.get("description", "N/A")
        
        sign = "+" if t_type in ["Deposit", "Transfer In"] else "-"
        print(f"{t_time:<20} | {t_type:<12} | {sign}${t_amount:<9,.2f} | ${t_bal:<9,.2f} | {t_desc}")
    print("-" * 85)