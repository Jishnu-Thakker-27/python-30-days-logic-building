
def add():
    with open("contacts.txt","a") as f:

        Name=input("Enter The Name: ")

        Number=(input("Enter The Number: "))

        New_Contact=f"{Name}\t{Number}\n"

        f.write((New_Contact))

        print("Saved Contacts:- ")

    with open("contacts.txt","r") as f:

        read=f.readlines()

        for i in read:

            print(i)

def view():
    with open("contacts.txt","r") as f:
        read=f.readlines()

        for i in read:

            print(i)

def search():
    search=input("Search The Name:")

    with open("contacts.txt","r") as f:

        read=f.readlines()
        found=False
        for i in read:
            if search.lower() in i.split("\t")[0].lower():
                found=True
                print(i)
        if not found:
            print("Name Not Found.")
    
def update():
    with open("contacts.txt", "r") as f:
        read = f.readlines()

    for index, contact in enumerate(read, start=1):
        print(f"{index}. {contact}")

    Update = int(input("Enter the index number of the contact you want to update: "))

    name, number = read[Update - 1].strip().split("\t")

    Task = int(input("What you want to do?\n1. Update Name\n2. Update Number\n3. Both\n"))

    if Task == 1:
        name = input("Enter the updated name: ")

    elif Task == 2:
        number = input("Enter the updated number: ")

    elif Task == 3:
        name = input("Enter the updated name: ")
        number = input("Enter the updated number: ")
    
    read[Update - 1] = f"{name}\t{number}\n"

    with open("contacts.txt", "w") as f:
        f.writelines(read)

    print("Contact updated successfully!\n")

def delete():
    with open("contacts.txt") as f:
        read=f.readlines()
        for i in range(1,len(read)+1):
            print(f"{i}.{read[i-1]}")
        a=int(input("Choose the index number if contact you want to delete."))
        read.pop(a-1)
        for i in range(1,len(read)+1):
            print(f"{i}.{read[i-1]}")

    with open("contacts.txt", "w") as f:
            f.writelines(read)
     
     

while True: 
    print("Menu:-")

    print("1.Add contacts")

    print("2.View saved contacts")

    print("3.Search for a contact")

    print("4.Update a contact")

    print("5.Delete a contact")

    print("6.Exit.")
    Action=int(input("Enter the number assigned for action you want to do:- "))

    if Action==1:
        add()

    elif Action==2:
        view()

    elif Action==3:
         search()


    elif Action==4:   
        update()
        
        
    elif Action==5:
         delete()   
    
    elif Action==6:
        print("Your Contacts have been updated.")
        break
