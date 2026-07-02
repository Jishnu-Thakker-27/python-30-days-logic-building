import os
import sys

# Add current directory to path so we can import src modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.models import (
    load_databases,
    ITEMS_DB,
    SPELLS_DB,
    ENEMIES_DB,
    NPCS_DB,
    ROOMS_DB
)

def run_verification():
    print("=== STARTING DATA REFERENTIAL INTEGRITY VERIFICATION ===")
    
    # 1. Load database
    try:
        load_databases("data")
        print("[PASS] Successfully loaded database JSON files.")
    except Exception as e:
        print(f"[FAIL] Failed to load databases: {e}")
        return False

    errors = 0

    # 2. Verify items database
    print("\nVerifying items database...")
    for item_id, item in ITEMS_DB.items():
        if not item.name:
            print(f"[ERROR] Item '{item_id}' is missing a name.")
            errors += 1
        if item.type not in ["weapon", "armor", "consumable", "key", "quest", "misc"]:
            print(f"[ERROR] Item '{item_id}' has invalid type: {item.type}")
            errors += 1

    # 3. Verify spells database
    print("Verifying spells database...")
    for spell_id, spell in SPELLS_DB.items():
        if not spell.name:
            print(f"[ERROR] Spell '{spell_id}' is missing a name.")
            errors += 1
        if spell.element not in ["fire", "ice", "holy", "lightning", "none"]:
            print(f"[ERROR] Spell '{spell_id}' has invalid element: {spell.element}")
            errors += 1

    # 4. Verify enemies database
    print("Verifying enemies database...")
    for enemy_id, enemy in ENEMIES_DB.items():
        if not enemy.name:
            print(f"[ERROR] Enemy '{enemy_id}' is missing a name.")
            errors += 1
        # Check enemy drops
        for drop in enemy.drops:
            drop_item = drop.get("item_id")
            if drop_item not in ITEMS_DB:
                print(f"[ERROR] Enemy '{enemy_id}' drops non-existent item: '{drop_item}'")
                errors += 1

    # 5. Verify NPCs database
    print("Verifying NPCs database...")
    for npc_id, npc in NPCS_DB.items():
        if not npc.name:
            print(f"[ERROR] NPC '{npc_id}' is missing a name.")
            errors += 1
        # Verify shop inventory
        for entry in npc.shop_inventory:
            shop_item = entry.get("item_id")
            if shop_item not in ITEMS_DB:
                print(f"[ERROR] NPC '{npc_id}' shop contains non-existent item: '{shop_item}'")
                errors += 1
        # Verify NPC Quest details
        if npc.quest:
            quest = npc.quest
            if quest.type == "kill":
                if quest.target not in ENEMIES_DB:
                    print(f"[ERROR] NPC '{npc_id}' quest target enemy '{quest.target}' does not exist in enemies database.")
                    errors += 1
            elif quest.type == "fetch":
                if quest.target not in ITEMS_DB:
                    print(f"[ERROR] NPC '{npc_id}' quest target item '{quest.target}' does not exist in items database.")
                    errors += 1
            else:
                print(f"[ERROR] NPC '{npc_id}' quest has invalid type: {quest.type}")
                errors += 1
            # Check quest rewards
            for rew_item in quest.reward_items:
                if rew_item not in ITEMS_DB:
                    print(f"[ERROR] NPC '{npc_id}' quest rewards non-existent item: '{rew_item}'")
                    errors += 1
            for rew_spell in quest.reward_spells:
                if rew_spell not in SPELLS_DB:
                    print(f"[ERROR] NPC '{npc_id}' quest rewards non-existent spell: '{rew_spell}'")
                    errors += 1

    # 6. Verify rooms database
    print("Verifying rooms database...")
    for room_id, room in ROOMS_DB.items():
        if not room.name:
            print(f"[ERROR] Room '{room_id}' is missing a name.")
            errors += 1
        
        # Verify room items
        for item_id in room.items:
            if item_id not in ITEMS_DB:
                print(f"[ERROR] Room '{room_id}' contains non-existent item: '{item_id}'")
                errors += 1
                
        # Verify room NPCs
        for npc_id in room.npcs:
            if npc_id not in NPCS_DB:
                print(f"[ERROR] Room '{room_id}' contains non-existent NPC: '{npc_id}'")
                errors += 1
                
        # Verify room enemies
        for enemy_id in room.enemies:
            if enemy_id not in ENEMIES_DB:
                print(f"[ERROR] Room '{room_id}' contains non-existent enemy: '{enemy_id}'")
                errors += 1

        # Verify room puzzles
        for puzzle in room.puzzles:
            for rew_item in puzzle.reward_items:
                if rew_item not in ITEMS_DB:
                    print(f"[ERROR] Room '{room_id}' puzzle '{puzzle.id}' rewards non-existent item: '{rew_item}'")
                    errors += 1

        # Verify exits
        for direction, exit_info in room.exits.items():
            if isinstance(exit_info, dict):
                target_room = exit_info.get("target")
                key_item = exit_info.get("key_item")
                if target_room not in ROOMS_DB:
                    print(f"[ERROR] Room '{room_id}' locked exit '{direction}' points to non-existent room: '{target_room}'")
                    errors += 1
                if key_item not in ITEMS_DB:
                    print(f"[ERROR] Room '{room_id}' locked exit '{direction}' requires non-existent key: '{key_item}'")
                    errors += 1
            else:
                if exit_info not in ROOMS_DB:
                    print(f"[ERROR] Room '{room_id}' exit '{direction}' points to non-existent room: '{exit_info}'")
                    errors += 1

    print("\n=== VERIFICATION SUMMARY ===")
    if errors == 0:
        print("[SUCCESS] All data referential integrity checks passed! 0 errors found.")
        return True
    else:
        print(f"[FAILED] Data verification completed with {errors} errors.")
        return False

if __name__ == "__main__":
    success = run_verification()
    sys.exit(0 if success else 1)
