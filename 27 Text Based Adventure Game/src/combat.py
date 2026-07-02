import random
from src.models import SPELLS_DB, ITEMS_DB
from src.utils import type_print, red, green, yellow, blue, magenta, cyan, bold, health_bar, mana_bar, prompt_input

def start_combat(player, enemy_template):
    """
    Runs the combat loop between player and enemy.
    Returns:
        True if player won
        False if player died
        None if player fled
    """
    enemy = enemy_template.copy()
    type_print(red(f"\n*** BATTLE START: {bold(enemy.name)} appears! ***", True))
    type_print(f"{enemy.description}\n")

    # Track special combat effects
    troll_regenerated = False
    ignited_this_turn = False

    # Who goes first?
    player_turn = player.agility >= enemy.speed

    while player.hp > 0 and enemy.hp > 0:
        # Reset turn-based flags
        ignited_this_turn = False

        # Display Battle HUD
        type_print(f"\n--- {bold(enemy.name.upper())} ---")
        type_print(f"HP: {health_bar(enemy.hp, enemy.max_hp, length=20)}")
        if enemy.weakness != "none":
            type_print(cyan(f"Weakness: {enemy.weakness.capitalize()}"))
        if enemy.resistance != "none":
            type_print(magenta(f"Resistance: {enemy.resistance.capitalize()}"))

        type_print(f"\n--- {bold('YOU')} ---")
        type_print(f"HP: {health_bar(player.hp, player.max_hp, length=20)}")
        type_print(f"MP: {mana_bar(player.mp, player.max_mp, length=20)}")
        type_print("-" * 30)

        if player_turn:
            # Player's Turn
            action = prompt_input(
                f"What will you do? ({green('attack')}/{blue('spell')}/{cyan('item')}/{yellow('flee')})",
                ["attack", "spell", "item", "flee"]
            )

            if action == "attack":
                # Standard Attack
                base_dmg = player.attack_power - enemy.defense
                variance = random.uniform(0.85, 1.15)
                dmg = max(1, int(base_dmg * variance))
                
                # Check for special phantom resistance (slashed by normal weapons)
                if enemy.id == "shadow_phantom":
                    dmg = max(1, dmg // 4)
                    type_print(magenta("Your physical blade passes harmlessly through the phantom's misty form!"))
                
                enemy.hp -= dmg
                type_print(green(f"You slash {enemy.name} for {dmg} physical damage!"))

            elif action == "spell":
                # Spells selection
                if not player.spells:
                    type_print("You do not know any spells!")
                    player_turn = True  # don't waste turn
                    continue

                type_print("\nChoose a spell:")
                choices = []
                for idx, spell_id in enumerate(player.spells, 1):
                    spell = SPELLS_DB[spell_id]
                    type_print(f"  {idx}. {spell.name} ({blue(str(spell.mana_cost) + ' MP')}) - {spell.description}")
                    choices.append(str(idx))
                choices.append("cancel")
                type_print("  Enter 'cancel' to go back.")

                spell_choice = prompt_input("Select spell number:", choices)
                if spell_choice == "cancel":
                    continue

                spell_id = player.spells[int(spell_choice) - 1]
                spell = SPELLS_DB[spell_id]

                if player.mp < spell.mana_cost:
                    type_print(red("Not enough MP!"))
                    continue

                player.mp -= spell.mana_cost

                if spell.target == "self":
                    # Heal spell
                    heal_amt = spell.power + player.magic_power
                    actual_heal = min(heal_amt, player.max_hp - player.hp)
                    player.hp += actual_heal
                    type_print(green(f"You cast {spell.name}! Restored {actual_heal} HP!"))
                else:
                    # Offense spells
                    # Spells ignore half of enemy's defense
                    base_dmg = (spell.power + player.magic_power) - (enemy.defense // 2)
                    variance = random.uniform(0.9, 1.1)
                    dmg = max(1, int(base_dmg * variance))

                    # Element check
                    if enemy.weakness == spell.element:
                        dmg = int(dmg * 1.5)
                        type_print(yellow(f"CRITICAL WEAKNESS! {spell.element.capitalize()} deals 1.5x damage!"))
                    elif enemy.resistance == spell.element:
                        dmg = int(dmg * 0.5)
                        type_print(magenta(f"RESISTED! {enemy.name} is resistant to {spell.element}."))

                    # Special Spell Modifiers
                    if spell.id == "divine_smite" and enemy.type == "undead":
                        dmg = int(dmg * 2.0)
                        type_print(yellow("HOLY SMITE! Massive damage dealt to undead creature!"))

                    if spell.element == "fire":
                        ignited_this_turn = True

                    enemy.hp -= dmg
                    type_print(blue(f"You cast {spell.name}! Dealt {dmg} {spell.element} damage to {enemy.name}!"))

            elif action == "item":
                # Consumables selection
                consumables = [item_id for item_id in player.inventory if ITEMS_DB[item_id].type == "consumable"]
                if not consumables:
                    type_print("You have no usable items in your inventory!")
                    continue

                type_print("\nChoose an item:")
                counts = {}
                for item_id in consumables:
                    counts[item_id] = counts.get(item_id, 0) + 1

                choices = []
                for idx, (item_id, count) in enumerate(counts.items(), 1):
                    item = ITEMS_DB[item_id]
                    type_print(f"  {idx}. {item.name} (x{count}) - {item.description}")
                    choices.append(str(idx))
                choices.append("cancel")
                type_print("  Enter 'cancel' to go back.")

                item_choice = prompt_input("Select item number:", choices)
                if item_choice == "cancel":
                    continue

                selected_item_id = list(counts.keys())[int(item_choice) - 1]
                player.use_consumable(selected_item_id)

            elif action == "flee":
                # Escape calculation
                escape_chance = 0.45 + (player.agility - enemy.speed) * 0.04
                if enemy.id == "red_dragon":
                    type_print(red("There is no escape from the Dragon's Sanctum! The gates are sealed by fire!"))
                    continue

                if random.random() < escape_chance:
                    type_print(yellow("You managed to escape from combat!"))
                    return None
                else:
                    type_print(red("You failed to escape! The enemy cuts off your path!"))

            player_turn = False  # pass turn to enemy

        else:
            # Enemy's Turn
            type_print(red(f"\n{enemy.name}'s turn..."))
            
            # Enemy Special Attacks
            if enemy.id == "red_dragon" and random.random() < 0.35:
                # Fire breath
                dmg = 24 - player.defense_power // 2
                dmg = max(5, dmg)
                player.hp -= dmg
                type_print(red(f"{enemy.name} breathes a torrent of molten fire! You take {dmg} fire damage!"))
            elif enemy.id == "shadow_phantom" and random.random() < 0.3:
                # Soul drain
                dmg = 12
                player.hp -= dmg
                # Heal phantom slightly
                enemy.hp = min(enemy.max_hp, enemy.hp + 6)
                type_print(magenta(f"{enemy.name} touches your chest, draining your life energy! You take {dmg} shadow damage, and the phantom heals!"))
            else:
                # Basic Attack
                base_dmg = enemy.attack - player.defense_power
                variance = random.uniform(0.85, 1.15)
                dmg = max(1, int(base_dmg * variance))
                player.hp -= dmg
                type_print(red(f"{enemy.name} attacks you for {dmg} damage!"))

            # Cave Troll Regeneration Mechanic
            if enemy.id == "cave_troll" and enemy.hp < enemy.max_hp:
                if ignited_this_turn:
                    type_print(yellow(f"{enemy.name}'s wounds are cauterized! Regeneration is blocked this turn."))
                else:
                    regen = 5
                    enemy.hp = min(enemy.max_hp, enemy.hp + regen)
                    type_print(green(f"{enemy.name} regenerates {regen} HP!"))

            player_turn = True  # pass turn to player

    # Battle End Check
    if player.hp <= 0:
        type_print(red(f"\n=== YOU HAVE BEEN SLAIN BY {enemy.name.upper()} ==="))
        return False
    else:
        type_print(green(f"\n=== VICTORY! You defeated {enemy.name}! ===", True))
        player.add_xp(enemy.xp_reward)
        player.gold += enemy.gold_reward
        type_print(yellow(f"Looted: {enemy.gold_reward} Gold Pieces."))

        # Roll Drops
        for drop in enemy.drops:
            item_id = drop["item_id"]
            chance = drop["chance"]
            if random.random() < chance:
                player.add_item(item_id)
        
        # Specific Quest/Item drops
        if enemy.id == "goblin_scout" and "rusty_key" not in player.inventory:
            # Make sure keys/quest items drop if the quest is active
            if "slay_goblin" in player.active_quests:
                player.add_item("rusty_key")
        elif enemy.id == "shadow_phantom" and "shadow_crystal" not in player.inventory:
            if "retrieve_crystal" in player.active_quests:
                player.add_item("shadow_crystal")

        # Update Player kills
        player.check_quests_on_kill(enemy.id)

        return True
