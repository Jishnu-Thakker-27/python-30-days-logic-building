import random
guesses=5
words=["Python","Java","Machine","JavaScript","Animal","Movie","Theater"]
# process(blanks,i,guesses)
    
def process(blanks,i,guesses):
    blanks_letters=[]
    user_input=input("Guess the letter. ").lower()
    if len(user_input)>1 or len(user_input)==0:
        print("Enter any one letter as your guess. ")
    else:
        if user_input in i:
            for char in blanks:
                blanks_letters.append(char)
            for index,letter in enumerate(i):
                if letter==user_input :
                    blanks_letters[index]=user_input
                    print("You guessed the correct letter")
                    for char in blanks_letters:
                        print(char+" ",end="")
        else:
            print("No such letter in the word.")
            guesses-=1
            print(f"You have {guesses} guesses left.")
        
        
print("Welcome to the Hangman Game: \n")
print("Game Rules: \n")
print("-Guess the hidden word one letter at a time.\n-Correct guesses reveal letters in the word.\n-Wrong guesses reduce your lives.\n-You will have total 5 lives.\n-Repeated guesses do not help.\n-Guess the full word before your lives run out to win.")

try:
    press=int(input("\nPress \"0\" to start the game. "))
    
    if press==0:
        # game()
        pass
    else:
        print("Invalid Input!!")
        
except ValueError:
    
    print("Invalid Input!!")
    
i=random.choice(words).lower()
blanks="_ "*len(i)
print(blanks)

while guesses==5:
    process(blanks,i,guesses)
    
