import sys
from src.models import ROOMS_DB, ITEMS_DB, NPCS_DB, ENEMIES_DB
from src.combat import start_combat
from src.save_manager import save_game, list_save_slots
from src.utils import type_print, red, green, yellow, blue, magenta, cyan, bold, prompt_input, print_header

def find_match_by_name(input_str, list_of_ids, db):
    """Finds a database key matching the input name or substring."""
    input_str = input_str.lower().strip()
    if input_str in list_of_ids:
        return input_str
    
    # Match by exact name
    for item_id in list_of_ids:
        obj = db.get(item_id)
        if obj and obj.name.lower() == input_str:
            return item_id
            
    # Match by substring
    for item_id in list_of_ids:
        obj = db.get(item_id)
        if obj and input_str in obj.name.lower():
            return item_id
            
    return None

def find_puzzle_match(input_str, puzzles):
    """Finds an active puzzle matching input string."""
    input_str = input_str.lower().strip()
    for puzzle in puzzles:
        if input_str in puzzle.id.lower() or input_str in "chest" or input_str in "riddle":
            return puzzle
    return None

def open_shop(player, npc):
    """Runs a buy/sell trade loop with a merchant NPC."""
    type_print(f"\n=== {bold(npc.name + ' - Shop')} ===")
    type_print(f"Your Gold: {yellow(str(player.gold))} G")
    
    while True:
        action = prompt_input(
            f"Would you like to {green('buy')}, {cyan('sell')}, or {yellow('leave')}?",
            ["buy", "sell", "leave"]
        )
        if action == "leave":
            type_print(yellow(f"{npc.name} says: 'Come back soon!'"))
            break
            
        elif action == "buy":
            if not npc.shop_inventory:
                type_print("The shop is completely out of stock.")
                continue
                
            type_print("\nWares for Sale:")
            choices = []
            for idx, entry in enumerate(npc.shop_inventory, 1):
                item_id = entry["item_id"]
                price = entry["price"]
                item = ITEMS_DB.get(item_id)
                if item:
                    type_print(f"  {idx}. {bold(item.name)} - {yellow(str(price) + ' G')} | {item.description}")
                    choices.append(str(idx))
            choices.append("cancel")
            type_print("  Enter 'cancel' to go back.")
            
            buy_choice = prompt_input("Select item to buy:", choices)
            if buy_choice == "cancel":
                continue
                
            selected_entry = npc.shop_inventory[int(buy_choice) - 1]
            item_id = selected_entry["item_id"]
            price = selected_entry["price"]
            
            if player.gold < price:
                type_print(red("You do not have enough gold!"))
            else:
                player.gold -= price
                player.add_item(item_id)
                type_print(green(f"Bought {ITEMS_DB[item_id].name} for {price} G. Remaining gold: {player.gold} G"))
                
        elif action == "sell":
            # Filter player items (excluding equipped and quest)
            sellable_ids = [item_id for item_id in player.inventory if item_id != player.weapon_id and item_id != player.armor_id]
            if not sellable_ids:
                type_print("You have no sellable items in your inventory.")
                continue
                
            type_print("\nYour Wares to Sell:")
            counts = {}
            for item_id in sellable_ids:
                counts[item_id] = counts.get(item_id, 0) + 1
                
            choices = []
            sellable_keys = list(counts.keys())
            for idx, item_id in enumerate(sellable_keys, 1):
                item = ITEMS_DB[item_id]
                sell_val = max(1, item.value // 2)
                type_print(f"  {idx}. {bold(item.name)} (x{counts[item_id]}) - Value: {yellow(str(sell_val) + ' G')}")
                choices.append(str(idx))
            choices.append("cancel")
            type_print("  Enter 'cancel' to go back.")
            
            sell_choice = prompt_input("Select item to sell:", choices)
            if sell_choice == "cancel":
                continue
                
            item_id = sellable_keys[int(sell_choice) - 1]
            item = ITEMS_DB[item_id]
            sell_val = max(1, item.value // 2)
            
            player.remove_item(item_id)
            player.gold += sell_val
            type_print(green(f"Sold {item.name} for {sell_val} G! Current gold: {player.gold} G"))

def run_dialogue(player, npc):
    """Processes branching dialogue for NPCs, managing quest updates and shop triggers."""
    node_id = "start"
    type_print(yellow(f"\n--- Dialogue with {npc.name} ---"))

    while node_id != "exit":
        # Check special virtual nodes first
        if node_id == "check_quest":
            if not npc.quest:
                node_id = "start"
                continue
                
            q_id = npc.quest.id
            if q_id not in player.active_quests and q_id not in player.completed_quests:
                node_id = "quest_offer"
            elif q_id in player.active_quests:
                if player.check_quest_ready_to_complete(q_id):
                    node_id = "quest_finish"
                else:
                    node_id = "quest_active"
            else:
                node_id = "quest_done"
            continue

        if node_id == "accept_quest":
            # Add quest to player active quests
            q = npc.quest
            # Copy template to player
            from src.models import Quest
            player.active_quests[q.id] = Quest(
                quest_id=q.id,
                name=q.name,
                description=q.description,
                objective_type=q.type,
                target=q.target,
                required_count=q.required_count,
                reward_xp=q.reward_xp,
                reward_gold=q.reward_gold,
                reward_items=q.reward_items,
                reward_spells=q.reward_spells
            )
            # Fetch initialization
            if q.type == "fetch":
                player.check_quests_on_fetch(q.target)
            type_print(green(f"\nQuest Accepted: {bold(q.name)}!"))
            node_id = "quest_accepted"
            continue

        if node_id == "complete_quest":
            q_id = npc.quest.id
            quest = player.active_quests[q_id]
            
            # Remove from active, add to completed
            del player.active_quests[q_id]
            player.completed_quests.append(q_id)
            
            type_print(green(f"\nQuest Completed: {bold(quest.name)}!"))
            
            # Remove required quest item if it was a fetch quest
            if quest.type == "fetch":
                for _ in range(quest.required_count):
                    player.remove_item(quest.target)
                    
            # Rewards
            player.gold += quest.reward_gold
            type_print(yellow(f"Rewarded: {quest.reward_gold} G"))
            player.add_xp(quest.reward_xp)
            
            for item_id in quest.reward_items:
                player.add_item(item_id)
                
            for spell_id in quest.reward_spells:
                if spell_id not in player.spells:
                    player.spells.append(spell_id)
                    from src.models import SPELLS_DB
                    type_print(magenta(f"Learned spell: {bold(SPELLS_DB[spell_id].name)}!"))
                    
            node_id = "quest_done"
            continue

        if node_id == "shop":
            open_shop(player, npc)
            node_id = "start"
            continue

        # Get dialog node text
        node = npc.dialogue.get(node_id)
        if not node:
            type_print(red(f"Error: Dialog node '{node_id}' not found!"))
            break

        type_print(f"\n{bold(npc.name)}: \"{node['text']}\"")
        
        options = node.get("options", [])
        if not options:
            break

        # Present options
        choices = []
        for idx, opt in enumerate(options, 1):
            type_print(f"  {idx}. {opt['text']}")
            choices.append(str(idx))

        choice_idx = prompt_input("Select an option:", choices)
        selected_option = options[int(choice_idx) - 1]
        node_id = selected_option["next"]

    type_print(yellow(f"Dialogue with {npc.name} ended."))

def look_room(room):
    """Prints the room name, description, and list of contents."""
    print_header(room.name, cyan)
    type_print(room.description)
    
    # 1. Print Exits
    exits_desc = []
    for direction, exit_info in room.exits.items():
        if isinstance(exit_info, dict):
            exits_desc.append(f"{direction} (locked)")
        else:
            exits_desc.append(direction)
            
    if exits_desc:
        type_print(f"Exits: {', '.join(exits_desc)}")
    else:
        type_print("Exits: None")
        
    # 2. Print NPCs
    if room.npcs:
        npc_names = [bold(NPCS_DB[npc_id].name) for npc_id in room.npcs if npc_id in NPCS_DB]
        type_print(yellow(f"People here: {', '.join(npc_names)}"))
        
    # 3. Print Items on Floor
    if room.items:
        item_names = [cyan(ITEMS_DB[item_id].name) for item_id in room.items if item_id in ITEMS_DB]
        type_print(green(f"Items on ground: {', '.join(item_names)}"))
        
    # 4. Print Puzzles
    active_puzzles = [p for p in room.puzzles if not p.solved]
    if active_puzzles:
        puzzle_descs = [yellow(f"[{p.id.replace('_', ' ').title()}]") for p in active_puzzles]
        type_print(f"Objects to inspect: {', '.join(puzzle_descs)}")
        
    # 5. Print Enemies
    if room.enemies:
        enemy_names = [red(ENEMIES_DB[enemy_id].name) for enemy_id in room.enemies if enemy_id in ENEMIES_DB]
        type_print(red(f"Hostile enemies block your path: {', '.join(enemy_names)}!"))

def solve_puzzle(player, puzzle):
    """Asks the puzzle question and handles the reward on correct answer."""
    type_print(yellow(f"\n--- Solving Riddle: {puzzle.id.replace('_', ' ').title()} ---"))
    type_print(f"Question: {bold(puzzle.question)}")
    
    answer_input = prompt_input("Your Answer (or type 'cancel' to exit):")
    if answer_input.lower() == "cancel":
        type_print("You stepped away from the puzzle.")
        return

    if answer_input.lower().strip() == puzzle.answer.lower().strip():
        puzzle.solved = True
        type_print(green(puzzle.solved_message))
        # Hand rewards
        for item_id in puzzle.reward_items:
            player.add_item(item_id)
    else:
        type_print(red("Incorrect! The lock remains shut. You can try again."))

def move_player(player, room, direction):
    """Handles room transitions and locked doors."""
    if direction not in room.exits:
        type_print(red("You cannot go that way."))
        return
        
    exit_info = room.exits[direction]
    
    if isinstance(exit_info, dict):
        # Locked door!
        target_room = exit_info["target"]
        key_item = exit_info["key_item"]
        locked_msg = exit_info["locked_message"]
        
        # Check player inventory
        if key_item in player.inventory:
            # Unlock!
            type_print(green(f"You unlocked the door using the {ITEMS_DB[key_item].name}!"))
            room.exits[direction] = target_room  # permanently unlock in this session
            player.current_room_id = target_room
            # Display new room
            new_room = ROOMS_DB[target_room]
            look_room(new_room)
            trigger_room_encounters(player, new_room)
        else:
            type_print(red(locked_msg))
    else:
        # Open door
        player.current_room_id = exit_info
        new_room = ROOMS_DB[exit_info]
        look_room(new_room)
        trigger_room_encounters(player, new_room)

def trigger_room_encounters(player, room):
    """Triggers combat if an enemy is in the room."""
    if room.enemies:
        enemy_id = room.enemies[0]
        enemy_template = ENEMIES_DB.get(enemy_id)
        if enemy_template:
            result = start_combat(player, enemy_template)
            if result is True:
                # Slayed enemy, remove from room list
                room.enemies.remove(enemy_id)
            elif result is None:
                # Fled, move back to starting_cell or safe_haven depending on room
                # For safety, return player to 'safe_haven' if in crypt_hall, otherwise starting_cell
                fallback = "starting_cell"
                if room.id in ["old_armory", "crypt_hall", "shadow_caverns"]:
                    fallback = "safe_haven"
                elif room.id == "dragon_sanctum":
                    fallback = "crypt_hall"
                
                type_print(yellow(f"Retreating back to {ROOMS_DB[fallback].name}..."))
                player.current_room_id = fallback
                look_room(ROOMS_DB[fallback])
            else:
                # Player died! Handled in game loop
                pass

def execute_command(player, command_str):
    """Parses and executes a player text command."""
    room = ROOMS_DB.get(player.current_room_id)
    if not room:
        type_print(red("Error: Player is out of bounds!"))
        return True

    # Check for active combat blocks first
    if room.enemies and command_str.lower().strip() not in ["look", "stats", "inventory", "spells", "quests", "help", "save"]:
        type_print(red(f"You cannot do that while enemies are near! Defeat the {ENEMIES_DB[room.enemies[0]].name} first."))
        trigger_room_encounters(player, room)
        return True

    tokens = command_str.lower().strip().split()
    if not tokens:
        return True

    cmd = tokens[0]
    
    if cmd == "help":
        type_print(bold("\n=== AVAILABLE COMMANDS ==="))
        type_print("  look                        - Inspect your surroundings")
        type_print("  go <north/south/east/west>  - Move to a connecting room")
        type_print("  take/loot <item name>       - Pick up an item from the floor")
        type_print("  talk <person name>          - Talk to an NPC in the room")
        type_print("  inspect <object name>       - Solve a puzzle or open chests")
        type_print("  equip <item name>           - Equip a weapon or armor")
        type_print("  unequip <weapon/armor>      - Unequip slot")
        type_print("  use <potion name>           - Drink a healing or mana potion")
        type_print("  stats                       - View player level, stats, and equipment")
        type_print("  inventory / inv             - Display items in your backpack")
        type_print("  spells                      - View your spellbook and mana costs")
        type_print("  quests                      - Display active and completed quests")
        type_print("  save                        - Save your game state")
        type_print("  exit / quit                 - Quit the game (unsaved progress will be lost)")
        
    elif cmd == "look":
        look_room(room)
        
    elif cmd == "go":
        if len(tokens) < 2:
            type_print("Go where? (E.g. 'go east')")
        else:
            move_player(player, room, tokens[1])
            
    elif cmd in ["take", "loot", "pickup"]:
        if len(tokens) < 2:
            type_print("Take what? (E.g. 'take sword')")
        else:
            target_str = " ".join(tokens[1:])
            item_id = find_match_by_name(target_str, room.items, ITEMS_DB)
            if item_id:
                room.items.remove(item_id)
                player.add_item(item_id)
            else:
                type_print(red(f"There is no '{target_str}' on the floor here."))
                
    elif cmd in ["talk", "speak"]:
        if len(tokens) < 2:
            type_print("Talk to whom? (E.g. 'talk eldrin')")
        else:
            target_str = " ".join(tokens[1:])
            # Filter talk target
            if "to" in tokens[1]:
                target_str = " ".join(tokens[2:])
            npc_id = find_match_by_name(target_str, room.npcs, NPCS_DB)
            if npc_id:
                run_dialogue(player, NPCS_DB[npc_id])
            else:
                type_print(red(f"There is no one named '{target_str}' here."))
                
    elif cmd in ["inspect", "solve", "open"]:
        if len(tokens) < 2:
            type_print("Inspect what? (E.g. 'inspect chest')")
        else:
            target_str = " ".join(tokens[1:])
            puzzle = find_puzzle_match(target_str, room.puzzles)
            if puzzle:
                if puzzle.solved:
                    type_print(yellow("This puzzle has already been solved."))
                else:
                    solve_puzzle(player, puzzle)
            else:
                type_print(red(f"There is no '{target_str}' to inspect here."))
                
    elif cmd == "equip":
        if len(tokens) < 2:
            type_print("Equip what? (E.g. 'equip iron sword')")
        else:
            target_str = " ".join(tokens[1:])
            item_id = find_match_by_name(target_str, player.inventory, ITEMS_DB)
            if item_id:
                player.equip(item_id)
            else:
                type_print(red(f"You don't have '{target_str}' in your inventory."))
                
    elif cmd == "unequip":
        if len(tokens) < 2:
            type_print("Unequip what? ('weapon' or 'armor')")
        else:
            player.unequip(tokens[1])
            
    elif cmd == "use":
        if len(tokens) < 2:
            type_print("Use what? (E.g. 'use health potion')")
        else:
            target_str = " ".join(tokens[1:])
            item_id = find_match_by_name(target_str, player.inventory, ITEMS_DB)
            if item_id:
                player.use_consumable(item_id)
            else:
                type_print(red(f"You don't have '{target_str}' in your inventory."))
                
    elif cmd == "stats":
        player.show_stats()
        
    elif cmd in ["inventory", "inv"]:
        player.show_inventory()
        
    elif cmd == "spells":
        player.show_spells()
        
    elif cmd == "quests":
        player.show_quests()
        
    elif cmd == "save":
        type_print("\nChoose a Save Slot (1-3):")
        slots = list_save_slots()
        for idx, details in slots:
            type_print(f"  {details}")
        slot_choice = prompt_input("Select Slot Number (1-3) or 'cancel':", ["1", "2", "3", "cancel"])
        if slot_choice != "cancel":
            save_game(player, int(slot_choice))
            
    elif cmd in ["exit", "quit"]:
        confirm = prompt_input("Are you sure you want to quit? Unsaved progress will be lost. (y/n)", ["y", "n"])
        if confirm == "y":
            type_print(yellow("Thank you for playing! Goodbye."))
            sys.exit(0)
            
    else:
        type_print(red("Unknown command. Type 'help' to see available commands."))
        
    return True
