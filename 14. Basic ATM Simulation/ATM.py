def check_balance():
    with open("ATM.txt","r") as f:
        data=f.read()
        if data.strip()=="":
            balance=10000
            print(balance)
        else:
            balance=data
            print(balance)
            with open("ATM.txt","w") as f:
                f.write(balance)
        


def withdraw():
    
    withdrawal=int(input("Enter The money you want to withdraw."))
    with open("ATM.txt","r") as f:
        data=f.read()
        if data.strip()=="":
            balance=10000 - withdrawal
            if balance<0:
                    print("Insufficient balance for withdrawing this much amount. Please Check Balance.")
            else:
                print(balance)
                with open("ATM.txt","w") as f:
                    f.write(str(balance))
        else:
            if int(data)==0:
                print("Insufficient Balance for withdrawing money.")
            else:
                balance=int(data)- withdrawal
                if balance<0:
                    print("Insufficient balance for withdrawing this much amount. Please Check Balance.")
                else:
                    print(balance)
                    with open("ATM.txt","w") as f:
                        f.write(str(balance))

def deposit():
    depositing=int(input("Enter The money you want to deposit."))
    with open("ATM.txt","r") as f:
        data=f.read()
        if data.strip()=="":
            balance=10000 + depositing
            print(balance)
            with open("ATM.txt","w") as f:
                f.write(str(balance))
        else:
            balance=int(data)+ depositing
            print(balance)
            with open("ATM.txt","w") as f:
                f.write(str(balance))

while True: 
    print("Welcome to City Bank ATM. ")
    print("1. Check Balance.")
    print("2. Withdraw Money.")
    print("3. Deposit Money.")
    print("4. Exit.")
    Task=int(input("Choose Your Task:- "))


    if Task==1:
        check_balance()

    elif Task==2:
        check=int(input("Do you want to check your balance? Type 1 for Yes and 0 for No."))
        if check==1:
            check_balance()
            withdraw()
        elif check==0:
            withdraw()

    elif Task==3:
        check=int(input("Do you want to check your balance? Type 1 for Yes and 0 for No."))
        if check==1:
            check_balance()
            deposit()
        elif check==0:
            deposit()

    elif Task==4:
        print("Thanks for visiting!!!")
        break
