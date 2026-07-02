import json
import os
import datetime
from src.models import ROOMS_DB, NPCS_DB, Quest, Puzzle, load_databases
from src.utils import type_print, green, red, yellow

SAVES_DIR = "saves"

def ensure_saves_dir():
    if not os.path.exists(SAVES_DIR):
        os.makedirs(SAVES_DIR)

def get_save_path(slot):
    return os.path.join(SAVES_DIR, f"save_slot_{slot}.json")

def save_game(player, slot=1):
    """Saves player stats, inventory, active quests, and room states to a JSON file."""
    ensure_saves_dir()
    save_path = get_save_path(slot)

    # 1. Compile player state
    player_state = {
        "level": player.level,
        "xp": player.xp,
        "xp_to_next": player.xp_to_next,
        "max_hp": player.max_hp,
        "hp": player.hp,
        "max_mp": player.max_mp,
        "mp": player.mp,
        "base_attack": player.base_attack,
        "base_defense": player.base_defense,
        "base_magic": player.base_magic,
        "agility": player.agility,
        "gold": player.gold,
        "weapon_id": player.weapon_id,
        "armor_id": player.armor_id,
        "inventory": player.inventory,
        "spells": player.spells,
        "completed_quests": player.completed_quests,
        "kills": player.kills,
        "current_room_id": player.current_room_id,
        "active_quests": [
            {"id": q.id, "current_count": q.current_count}
            for q in player.active_quests.values()
        ]
    }

    # 2. Compile world (rooms) state
    # We only save changes: items, enemies, solved status of puzzles, exits (which might have unlocked)
    rooms_state = {}
    for room_id, room in ROOMS_DB.items():
        rooms_state[room_id] = {
            "items": room.items,
            "enemies": room.enemies,
            "exits": room.exits,
            "puzzles": [p.to_dict() for p in room.puzzles]
        }

    save_data = {
        "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "player": player_state,
        "rooms": rooms_state
    }

    try:
        with open(save_path, "w") as f:
            json.dump(save_data, f, indent=2)
        type_print(green(f"Game successfully saved to Slot {slot}! ({save_data['timestamp']})"))
        return True
    except Exception as e:
        type_print(red(f"Error saving game: {e}"))
        return False

def load_game(player, slot=1, data_dir="data"):
    """Loads player stats, inventory, active quests, and room states from a JSON file."""
    save_path = get_save_path(slot)
    if not os.path.exists(save_path):
        type_print(red(f"No save file found in Slot {slot}."))
        return False

    try:
        with open(save_path, "r") as f:
            save_data = json.load(f)

        # Re-initialize original databases to clean start state before applying changes
        load_databases(data_dir)

        # 1. Restore Player state
        p_data = save_data["player"]
        player.level = p_data["level"]
        player.xp = p_data["xp"]
        player.xp_to_next = p_data["xp_to_next"]
        player.max_hp = p_data["max_hp"]
        player.hp = p_data["hp"]
        player.max_mp = p_data["max_mp"]
        player.mp = p_data["mp"]
        player.base_attack = p_data["base_attack"]
        player.base_defense = p_data["base_defense"]
        player.base_magic = p_data["base_magic"]
        player.agility = p_data["agility"]
        player.gold = p_data["gold"]
        player.weapon_id = p_data["weapon_id"]
        player.armor_id = p_data["armor_id"]
        player.inventory = p_data["inventory"]
        player.spells = p_data["spells"]
        player.completed_quests = p_data["completed_quests"]
        player.kills = p_data["kills"]
        player.current_room_id = p_data["current_room_id"]

        # Restore active quests
        player.active_quests.clear()
        for q_saved in p_data.get("active_quests", []):
            q_id = q_saved["id"]
            # Look up quest in npcs.json database
            quest_template = None
            for npc in NPCS_DB.values():
                if npc.quest and npc.quest.id == q_id:
                    quest_template = npc.quest
                    break
            
            if quest_template:
                # Create a fresh copy
                new_q = Quest(
                    quest_id=quest_template.id,
                    name=quest_template.name,
                    description=quest_template.description,
                    objective_type=quest_template.type,
                    target=quest_template.target,
                    required_count=quest_template.required_count,
                    reward_xp=quest_template.reward_xp,
                    reward_gold=quest_template.reward_gold,
                    reward_items=quest_template.reward_items,
                    reward_spells=quest_template.reward_spells
                )
                new_q.current_count = q_saved["current_count"]
                player.active_quests[q_id] = new_q

        # 2. Restore World (rooms) state
        r_data = save_data["rooms"]
        for room_id, r_state in r_data.items():
            if room_id in ROOMS_DB:
                room = ROOMS_DB[room_id]
                room.items = r_state["items"]
                room.enemies = r_state["enemies"]
                room.exits = r_state["exits"]
                
                # Reconstruct puzzles
                room.puzzles.clear()
                for p_d in r_state.get("puzzles", []):
                    room.puzzles.append(Puzzle.from_dict(p_d))

        type_print(green(f"Game loaded successfully from Slot {slot}! Saved on {save_data['timestamp']}"))
        return True
    except Exception as e:
        type_print(red(f"Error loading game: {e}"))
        return False

def list_save_slots():
    """Returns a list of tuples (slot_number, details_string)."""
    ensure_saves_dir()
    slots = []
    for slot in range(1, 4):
        path = get_save_path(slot)
        if os.path.exists(path):
            try:
                with open(path, "r") as f:
                    data = json.load(f)
                p = data["player"]
                details = f"Slot {slot}: Level {p['level']} Adventurer in {ROOMS_DB[p['current_room_id']].name} (Saved: {data['timestamp']})"
                slots.append((slot, details))
            except:
                slots.append((slot, f"Slot {slot}: [Corrupted Save Data]"))
        else:
            slots.append((slot, f"Slot {slot}: [Empty]"))
    return slots
