a=int(input("Enter Number 1:- "))
b=int(input("Enter Number 2:- "))

print("1.Addition")
print("2.Subtraction")
print("3.Multiply")
print("4.Division")
c=int(input("Choose the Operations from above."))

if c == 1 :
    print(f"The Addition Of Two Numbers Is {a+b}" )
elif c == 2 :
    print(f"The Subtraction Of Two Numbers Is {a-b}")
elif c == 3 :
    print(f"The Multiplication Of Two Numbers Is {a*b}")
elif c == 4 :
    if b == 0 :
        print("Division Not Possible.")
    else:
        print(f"The Division Of Two Numbers Is {a/b}")
else:
    print("Invalid Input.")