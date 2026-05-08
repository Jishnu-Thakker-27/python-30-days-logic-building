def triangle(n):
    for i in range(1,n+1):
        print(i * "*")

def pyramid(n):
    for i in range(1,n+1):
        print(" "*(n-i),end="")
        for j in range(1,i+1):
            print("* ",end="")
        print()

def diamond(n):
    for i in range(1,n+1):
        print(" "*(n-i),end="")
        for j in range(1,i+1):
            print("* ",end="")
        print()
    for i in range(1,n):   
        print(" "*(i),end="")
        for j in range(n-i,0,-1):#for  i in range(Start, stop, step)
            print("* ",end="")
        print()
        
    
def increasing(n):
    for i in range(1,n+1):
        for j in range(1,i+1):
            print(j,end="")
        print()
def repeating(n):
    for i in range(1,n+1):
        for j in range(1,i+1):
            print(i,end="")
        print()
        
def reverse(n):
    for i in range(n,0,-1):
        for j in range(1,i+1):
            print(j,end="")
        print()

    print("Menu: ")
    print("1.Star pattern: ")
    print("2.Number Pattern: ")
    try:
        Pattern=int(input("Choose the index number of pattern you want to see: - "))
    except ValueError:
        print("Enter the integer value")
    else:
        match(Pattern):
            case 1:
                print("1. Triangle Pattern")
                print("2. Pyramid Pattern")
                print("3. Diamond Pattern")
                try:
                    Star=int(input("Choose the index number of star  pattern you want to see: - "))
                except ValueError:
                    print("Enter the integer value")
                else:
                    match(Star):
                        case 1:
                            try:
                                n=int(input("Enter The Number of iterations up to which you want to see pattern: "))
                                triangle(n)
                            except ValueError:
                                print("Enter the integer value")
                        
                        case 2:
                            try:
                                n=int(input("Enter The Number of iterations up to which you want to see pattern: "))
                                pyramid(n)
                            except ValueError:
                                print("Enter the integer value")
                        
                        case 3:
                            try:
                                n=int(input("Enter The Number of iterations up to which you want to see pattern: "))
                                diamond(n)
                            except ValueError:
                                print("Enter the integer value")
                        
                        case _:
                            print("Invalid choice")
     
            case 2:
                print("1.Increasing numbers")
                print("2.Repeating numbers")
                print("3.Reverse order")
                try:
                    number=int(input("Choose the index number of number  pattern you want to see: - "))
                except ValueError:
                    print("Enter the integer value")
                else:
                
                    match number:
                        case 1:
                            try:
                                n=int(input("Enter The Number of iterations up to which you want to see pattern: "))
                                increasing(n)
                            except ValueError:
                                print("Enter the integer value")
                        case 2:
                            try:
                                n=int(input("Enter The Number of iterations up to which you want to see pattern: "))
                                repeating(n)
                            except ValueError:
                                print("Enter the integer value")
                    
                        case 3:
                            try:
                                n=int(input("Enter The Number of iterations up to which you want to see pattern: "))
                                reverse(n)
                            except ValueError:
                                print("Enter the integer value")
                            
                        case _:
                            print("Invalid choice")
            case _:
                print("Invalid choice")
                    
