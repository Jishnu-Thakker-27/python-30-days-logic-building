import sys
from src.models import load_databases, ROOMS_DB
from src.player import Player
from src.engine import execute_command, look_room
from src.save_manager import load_game, list_save_slots
from src.utils import type_print, clear_screen, red, green, yellow, blue, cyan, magenta, bold, prompt_input

def show_title_screen():
    clear_screen()
    title = f"""
{red("  _______ _            ", True)}{yellow("_____                                 ", True)}
{red(" |__   __| |          ", True)}{yellow("/ ____|                                ", True)}
{red("    | |  | |__   ___ ", True)}{yellow("| |     __ ___   _____ _ __ _ __  ___   ", True)}
{red("    | |  | '_ \\ / _ \\", True)}{yellow("| |    / _` \\ \\ / / _ \\ '__| '_ \\/ __|  ", True)}
{red("    | |  | | | |  __/", True)}{yellow("| |___| (_| |\\ V /  __/ |  | | | \\__ \\  ", True)}
{red("    |_|  |_| |_|\\___|", True)}{yellow(" \\_____\\__,_| \\_/ \\___|_|  |_| |_|___/  ", True)}
"""
    print(title)
    type_print(bold(cyan("     --- An Advanced Text-Based RPG Adventure Game ---     ").center(60)))
    print()

def show_main_menu():
    while True:
        show_title_screen()
        type_print(bold("MAIN MENU"))
        type_print(f"  1. {green('New Game')}")
        type_print(f"  2. {blue('Load Game')}")
        type_print(f"  3. {red('Exit')}")
        
        choice = prompt_input("Select an option (1-3):", ["1", "2", "3"])
        
        if choice == "1":
            start_new_game()
        elif choice == "2":
            load_saved_game()
        elif choice == "3":
            type_print(yellow("\nThank you for playing! Goodbye."))
            sys.exit(0)

def play_game(player):
    """Primary game loop once state is set."""
    clear_screen()
    # Initial room inspection
    room = ROOMS_DB.get(player.current_room_id)
    if room:
        look_room(room)
    
    while True:
        cmd_str = prompt_input(">")
        if not cmd_str:
            continue
            
        execute_command(player, cmd_str)
        
        # Check death
        if player.hp <= 0:
            type_print(red("\n=================== GAME OVER ===================", True))
            type_print(red("Your vision fades to black. The caverns claim another soul..."))
            type_print(red("=================================================", True))
            input("\nPress Enter to return to the Main Menu...")
            break
            
        # Check victory (red dragon defeated)
        if player.current_room_id == "dragon_sanctum" and not ROOMS_DB["dragon_sanctum"].enemies:
            clear_screen()
            type_print(yellow("\n" + "=" * 60))
            type_print(green("                  CONGRATULATIONS!", True))
            type_print(yellow("=" * 60))
            type_print("With a final mighty blow, the dragon Ignis falls, letting out a deafening roar.")
            type_print("The volcanic cavern shakes as the golden portal behind him flares with blinding light.")
            type_print("You step through the portal, leaving the subterranean darkness behind you.")
            type_print("Fresh surface breeze hits your face, and you see the rising sun.")
            type_print("You have escaped, and your name will be remembered forever as the Hero of the Caverns!")
            type_print(yellow("=" * 60))
            input("\nPress Enter to return to the Main Menu...")
            break

def start_new_game():
    clear_screen()
    type_print(bold(cyan("=== STARTING NEW JOURNEY ===")))
    
    # Initialize fresh databases
    load_databases("data")
    player = Player()
    
    # Story Intro
    type_print("\nInitializing world...")
    type_print("\nYou wake up on a cold stone floor. Your head throbs painfully.")
    type_print("The smell of wet stone, moss, and ancient decay fills your nostrils.")
    type_print("Looking around, you realize you are locked in an ancient subterranean dungeon cell.")
    type_print("Your only possessions are a rusty dagger and a single health potion.")
    type_print(yellow("Goal: Navigate deep into the caverns, defeat the dragon Ignis, and escape through the golden portal."))
    
    input("\nPress Enter to begin your adventure...")
    play_game(player)

def load_saved_game():
    clear_screen()
    type_print(bold(blue("=== LOAD SAVED GAME ===")))
    
    # Display slots
    slots = list_save_slots()
    for idx, details in slots:
        type_print(f"  {details}")
        
    choice = prompt_input("Select Slot Number (1-3) or type 'cancel' to go back:", ["1", "2", "3", "cancel"])
    if choice == "cancel":
        return
        
    player = Player()
    if load_game(player, int(choice), "data"):
        input("\nPress Enter to resume your adventure...")
        play_game(player)
    else:
        input("\nPress Enter to return to the Main Menu...")

if __name__ == "__main__":
    show_main_menu()
