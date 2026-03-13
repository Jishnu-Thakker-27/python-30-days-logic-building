
# Student Record System (Work in Progress)
# Day 9 Python Project
# Features completed:
# - Add student record
# - View records
# Remaining:
# - Fix search function
# - Add average calculation

print("How may I help you?")
print("1.Add Student Record")
print("2.View All Records")
print("3.Search Student")
print("4.Calculate Avearge")
print("5.Exit")
while True:
    
    user=int(input("Choose Your Task."))

    if user ==1 :
        with open("Data.txt","a") as f:
            name=input("Enter The Name Of The Student.")
            maths_marks=int(input("Enter Marks Of Maths."))
            science_marks=int(input("Enter Marks Of Science."))
            english_marks=int(input("Enter Marks Of English."))
            
            f.write(f"Name={name}\n Maths={maths_marks}\n Science={science_marks}\n English={english_marks}\n")
    if user==2:
        with open("Data.txt",) as f:
            read=f.readlines()
            print(read)
    if user==3:
        with open("Data.txt") as f:
            search=input("Search The Name Of The Student.")
            read=f.readlines()
            found=False
            
            for line in read:
                if search.lower() in line.lower():
                    print(line.strip())
                    found=True

            if not found:
                print("Student Not Found.")
    if user==4:
        with open("Data.txt") as f:
            search=input("Search The Name Of The Student: ")
            read=f.readlines()
            found=False
        
            for i in range(len(read)):
                if search.lower() in read[i].lower():
                
                    maths = int(read[i+1].split("=")[1])
                    science = int(read[i+2].split("=")[1])
                    english = int(read[i+3].split("=")[1])
                
                    avg = (maths + science + english) / 3
                
                    print(f"Average Marks = {avg}")
                    found=True
        
            if not found:
                print("Student Not Found.")
        
        
    if user==5:
        break
