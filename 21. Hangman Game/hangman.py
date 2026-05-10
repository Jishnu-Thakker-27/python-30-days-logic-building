import random

words = ["Python", "Java", "Machine", "JavaScript", "Animal", "Movie", "Theater"]

word = random.choice(words).lower()
blanks_letters = ["_"] * len(word)
lives = 5
guessed_letters = []


print("Welcome to the Hangman Game:\n")
print("Game Rules:\n")
print(
    "- Guess the hidden word one letter at a time.\n"
    "- Correct guesses reveal letters in the word.\n"
    "- Wrong guesses reduce your lives.\n"
    "- You will have total 5 lives.\n"
    "- Repeated guesses do not help.\n"
    "- Guess the full word before your lives run out to win."
)

while True:
    try:
        press = int(input('\nPress "0" to start the game: '))

        if press != 0:
            print("Invalid Input!!")
            

    except ValueError:
        print("Invalid Input!!")
        
        
    else:
        if press==0:
            break
        


while lives > 0 and "_" in blanks_letters:
    print("\nWord: ", end="")

    for char in blanks_letters:
        print(char, end=" ")

    user_input = input("\nGuess the letter: ").lower()

    if len(user_input) != 1:
        print("Enter only one letter as your guess.")
        continue

    if not user_input.isalpha():
        print("Enter only alphabet letters.")
        continue

    if user_input in guessed_letters:
        print("You already guessed this letter.")
        continue

    guessed_letters.append(user_input)

    if user_input in word:
        print("You guessed the correct letter!")

        for index, letter in enumerate(word):
            if letter == user_input:
                blanks_letters[index] = user_input

    else:
        lives -= 1
        print("No such letter in the word.")
        print(f"You have {lives} lives left.")


if "_" not in blanks_letters:
    print("\nCongratulations! You guessed the word.")

    print("The word was:", word)

else:
    print("\nGame Over! You lost.")
    print("The word was:", word)
