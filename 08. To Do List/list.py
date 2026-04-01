print("To-do Tasks!")
print("1.View Tasks.")
print("2.Add Tasks.")
print("3.Remove Tasks.")
print("4.Exit.")
while True:
    a=int(input("Choose Your Action. "))
    if a==1 :
       with open("Task.txt") as f:
           data=f.read()
           if data.strip()=="" :
               print("You don't have any pending tasks.")
           else:
               print(data)
               continue
    
    elif a==2 :
        Task=input("Enter Your Task:-")
        with open("Task.txt","a") as f:
            f.write(Task+"\n")
            continue
    elif a==3:
        with open("Task.txt") as f:
            Data=f.readlines()
            for i in range(1,len(Data)+1):
                print(f"{i}.{Data[i-1]}") 
            
            Remove=int(input("Enter The Task Number You Want To Remove."))
            
            if Remove in range(1,len(Data)+1):
                Data.pop((Remove-1))
            else:
                print("Invalid Number.")
        with open("Task.txt","w") as f:
            print("Your Updated Tasks:-")
            for i in Data:
                f.write(i)
    elif a==4 :
        print("Your Tasks Have Been Updated.")
        break
        
    
