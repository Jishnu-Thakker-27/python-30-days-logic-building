
import random
while True: 
    target_number=random.randint(1,50)
    number_of_attempts=0
    guess_number=-1
    attempts=10
    print(f"\nYou Have {attempts} Attempts!!")
    while(guess_number!=target_number):
        guess_number=int(input("Guess The Number."))
        if(guess_number>target_number):
            print("Guess Lower Number.")
            number_of_attempts+=1
        elif(guess_number<target_number):
            print("Guess Higher Number")
            number_of_attempts+=1
        if(number_of_attempts>=attempts):
            print(f"Your Maximum Attempts Are Over.The correct number was {target_number}.")
            break
    if(guess_number==target_number):
        number_of_attempts+=1
        print(f"Congratulations. You Guess the number {target_number} in {number_of_attempts} guesses.")
        Next_game=int(input("Want To Play Again?. Type 1 for Yes and 0 for No.")) 
    elif(number_of_attempts>=attempts):
        Next_game=int(input("Want To Play Again?. Type 1 for Yes and 0 for No.")) 
    if(Next_game==0):
        print("Thanks For Playing!")
        break
    else:
        print("\nYour Game Restarts")
        
        
