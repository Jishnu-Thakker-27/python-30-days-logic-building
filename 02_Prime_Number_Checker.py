a=int(input("Enter Your Nunber:- "))

for i in range(2,a):
    if(a%i==0):
        print("It Is A Composite Number.")
        break
else:
    print("It Is A Prime Number.")