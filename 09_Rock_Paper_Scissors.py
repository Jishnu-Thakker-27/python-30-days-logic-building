import random
print("=================================================================================")
print("                             GAME STARTS                                         ")
print("=================================================================================")


def game_rule(Move,Computer,U_move,C_move):
    if(Move==Computer):
        print(f"You chose {U_move} and Computer chose {C_move}\n")
        print("It's a draw!\n")
        print("Type '0' to play again! \n")
    elif(Move==1 and Computer==2):
        print(f"You chose {U_move} and Computer chose {C_move}\n")
        print("Congratulations.You Won!!!\n")
        print("Type '0' to play again!\n ")
    elif(Move==2 and Computer==3):
        print(f"You chose {U_move} and Computer chose {C_move}\n")
        print("Congratulations.You Won!!!\n")
        print("Type '0' to play again!\n ")
    elif(Move==3 and Computer==1):
        print(f"You chose {U_move} and Computer chose {C_move}\n")
        print("Congratulations.You Won!!!\n")
        print("Type '0' to play again!\n ")
    elif(Move==2 and Computer==1):
        print(f"You chose {U_move} and Computer chose {C_move}\n")
        print("You Lost!!\n")
        print("Type '0' to play again! \n")
    elif(Move==3 and Computer==2):
        print(f"You chose {U_move} and Computer chose {C_move}\n")
        print("You Lost!!")
        print("Type '0' to play again! \n")
    elif(Move==1 and Computer==3):
        print(f"You chose {U_move} and Computer chose {C_move}\n")
        print("You Lost!!\n")
        print("Type '0' to play again!\n ")
    elif(move is not 1 and not 2 and not 3):
        print("Invalid Input.\n")
        print("Make Your Move\n")


print("Welcome To The Game.\n")


print("Snake Water Gun!")
print("Type 'R' for Rock")
print("Type 'P' for Paper")
print("Type 'S' for Scissor\n")

def computer_game():
    Computer=random.choice([1,2,3])
    User=(input("Enter Your Move: \n")).lower()
    game_dict={
    "r":1,
    "p":2,
    "s":3
}
    U_dict={
    "r":"Rock",
    "p":"Paper",
    "s":"Scissors"
}
    C_dict={
    1:"Rock",
    2:"Paper",
    3:"Scissors"
}
    Move=game_dict[User]
    U_move=U_dict[User]
    C_move=C_dict[Computer]
    game_rule(Move,Computer,U_move,C_move)
    



print("=================================================================================")
print("                              GAME ENDS                                          ")
print("=================================================================================")

