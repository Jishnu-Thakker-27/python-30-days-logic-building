import json
import os

# Global database registries
ITEMS_DB = {}
SPELLS_DB = {}
ENEMIES_DB = {}
NPCS_DB = {}
ROOMS_DB = {}

class Item:
    def __init__(self, item_id, name, item_type, description, attack=0, defense=0, magic_power=0, value=0, effect=None, amount=0):
        self.id = item_id
        self.name = name
        self.type = item_type  # "weapon", "armor", "consumable", "key", "quest"
        self.description = description
        self.attack = attack
        self.defense = defense
        self.magic_power = magic_power
        self.value = value
        self.effect = effect   # e.g., "heal_hp", "heal_mp", "restore_all"
        self.amount = amount   # amount healed/restored

    @classmethod
    def from_dict(cls, item_id, d):
        return cls(
            item_id=item_id,
            name=d.get("name", "Unknown Item"),
            item_type=d.get("type", "misc"),
            description=d.get("description", ""),
            attack=d.get("attack", 0),
            defense=d.get("defense", 0),
            magic_power=d.get("magic_power", 0),
            value=d.get("value", 0),
            effect=d.get("effect", None),
            amount=d.get("amount", 0)
        )

class Spell:
    def __init__(self, spell_id, name, mana_cost, power, element, description, target="enemy"):
        self.id = spell_id
        self.name = name
        self.mana_cost = mana_cost
        self.power = power
        self.element = element  # "fire", "ice", "holy", "lightning", "none"
        self.description = description
        self.target = target    # "enemy" or "self"

    @classmethod
    def from_dict(cls, spell_id, d):
        return cls(
            spell_id=spell_id,
            name=d.get("name", "Unknown Spell"),
            mana_cost=d.get("mana_cost", 0),
            power=d.get("power", 0),
            element=d.get("element", "none"),
            description=d.get("description", ""),
            target=d.get("target", "enemy")
        )

class Enemy:
    def __init__(self, enemy_id, name, hp, max_hp, attack, defense, speed, xp_reward, gold_reward, description, enemy_type="beast", weakness="none", resistance="none", drops=None):
        self.id = enemy_id
        self.name = name
        self.hp = hp
        self.max_hp = max_hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.xp_reward = xp_reward
        self.gold_reward = gold_reward
        self.description = description
        self.type = enemy_type
        self.weakness = weakness
        self.resistance = resistance
        self.drops = drops if drops is not None else []  # List of {"item_id": str, "chance": float}

    def copy(self):
        return Enemy(
            enemy_id=self.id,
            name=self.name,
            hp=self.hp,
            max_hp=self.max_hp,
            attack=self.attack,
            defense=self.defense,
            speed=self.speed,
            xp_reward=self.xp_reward,
            gold_reward=self.gold_reward,
            description=self.description,
            enemy_type=self.type,
            weakness=self.weakness,
            resistance=self.resistance,
            drops=list(self.drops)
        )

    @classmethod
    def from_dict(cls, enemy_id, d):
        return cls(
            enemy_id=enemy_id,
            name=d.get("name", "Unknown Enemy"),
            hp=d.get("hp", 10),
            max_hp=d.get("max_hp", 10),
            attack=d.get("attack", 2),
            defense=d.get("defense", 0),
            speed=d.get("speed", 5),
            xp_reward=d.get("xp_reward", 5),
            gold_reward=d.get("gold_reward", 2),
            description=d.get("description", ""),
            enemy_type=d.get("type", "beast"),
            weakness=d.get("weakness", "none"),
            resistance=d.get("resistance", "none"),
            drops=d.get("drops", [])
        )

class Quest:
    def __init__(self, quest_id, name, description, objective_type, target, required_count, reward_xp, reward_gold, reward_items=None, reward_spells=None):
        self.id = quest_id
        self.name = name
        self.description = description
        self.type = objective_type  # "kill" or "fetch"
        self.target = target        # enemy_id for "kill", item_id for "fetch"
        self.required_count = required_count
        self.current_count = 0
        self.reward_xp = reward_xp
        self.reward_gold = reward_gold
        self.reward_items = reward_items if reward_items is not None else []
        self.reward_spells = reward_spells if reward_spells is not None else []

    @classmethod
    def from_dict(cls, d):
        if not d:
            return None
        return cls(
            quest_id=d.get("id"),
            name=d.get("name", "Unnamed Quest"),
            description=d.get("description", ""),
            objective_type=d.get("type", "fetch"),
            target=d.get("target"),
            required_count=d.get("required_count", 1),
            reward_xp=d.get("reward_xp", 0),
            reward_gold=d.get("reward_gold", 0),
            reward_items=d.get("reward_items", []),
            reward_spells=d.get("reward_spells", [])
        )

class NPC:
    def __init__(self, npc_id, name, role, dialogue, quest=None, shop_inventory=None):
        self.id = npc_id
        self.name = name
        self.role = role  # "quest_giver", "merchant", "citizen"
        self.dialogue = dialogue  # raw dialogue dictionary
        self.quest = quest        # Quest object (or None)
        self.shop_inventory = shop_inventory if shop_inventory is not None else []  # List of {"item_id": str, "price": int}

    @classmethod
    def from_dict(cls, npc_id, d):
        quest_data = d.get("quest")
        quest_obj = Quest.from_dict(quest_data) if quest_data else None
        return cls(
            npc_id=npc_id,
            name=d.get("name", "Unknown NPC"),
            role=d.get("role", "citizen"),
            dialogue=d.get("dialogue", {}),
            quest=quest_obj,
            shop_inventory=d.get("shop_inventory", [])
        )

class Puzzle:
    def __init__(self, puzzle_id, puzzle_type, question, answer, solved=False, reward_items=None, solved_message=""):
        self.id = puzzle_id
        self.type = puzzle_type  # e.g., "riddle"
        self.question = question
        self.answer = answer
        self.solved = solved
        self.reward_items = reward_items if reward_items is not None else []
        self.solved_message = solved_message

    def to_dict(self):
        return {
            "id": self.id,
            "type": self.type,
            "question": self.question,
            "answer": self.answer,
            "solved": self.solved,
            "reward_items": self.reward_items,
            "solved_message": self.solved_message
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            puzzle_id=d.get("id"),
            puzzle_type=d.get("type", "riddle"),
            question=d.get("question", ""),
            answer=d.get("answer", ""),
            solved=d.get("solved", False),
            reward_items=d.get("reward_items", []),
            solved_message=d.get("solved_message", "")
        )

class Room:
    def __init__(self, room_id, name, description, exits, items=None, enemies=None, npcs=None, puzzles=None):
        self.id = room_id
        self.name = name
        self.description = description
        self.exits = exits  # dict: direction -> target_room_id or dict for locks
        self.items = items if items is not None else []        # list of item_ids
        self.enemies = enemies if enemies is not None else []  # list of enemy_ids
        self.npcs = npcs if npcs is not None else []          # list of npc_ids
        self.puzzles = puzzles if puzzles is not None else []  # list of Puzzle objects

    @classmethod
    def from_dict(cls, room_id, d):
        puzzles_list = [Puzzle.from_dict(p) for p in d.get("puzzles", [])]
        return cls(
            room_id=room_id,
            name=d.get("name", "Unknown Room"),
            description=d.get("description", ""),
            exits=d.get("exits", {}),
            items=d.get("items", []),
            enemies=d.get("enemies", []),
            npcs=d.get("npcs", []),
            puzzles=puzzles_list
        )

def load_databases(data_dir):
    """Loads all JSON files into memory, compiling them as python objects."""
    global ITEMS_DB, SPELLS_DB, ENEMIES_DB, NPCS_DB, ROOMS_DB
    
    # Reset
    ITEMS_DB.clear()
    SPELLS_DB.clear()
    ENEMIES_DB.clear()
    NPCS_DB.clear()
    ROOMS_DB.clear()

    # Load Items
    with open(os.path.join(data_dir, "items.json"), "r") as f:
        data = json.load(f)
        for item_id, item_d in data.items():
            ITEMS_DB[item_id] = Item.from_dict(item_id, item_d)

    # Load Spells
    with open(os.path.join(data_dir, "spells.json"), "r") as f:
        data = json.load(f)
        for spell_id, spell_d in data.items():
            SPELLS_DB[spell_id] = Spell.from_dict(spell_id, spell_d)

    # Load Enemies
    with open(os.path.join(data_dir, "enemies.json"), "r") as f:
        data = json.load(f)
        for enemy_id, enemy_d in data.items():
            ENEMIES_DB[enemy_id] = Enemy.from_dict(enemy_id, enemy_d)

    # Load NPCs
    with open(os.path.join(data_dir, "npcs.json"), "r") as f:
        data = json.load(f)
        for npc_id, npc_d in data.items():
            NPCS_DB[npc_id] = NPC.from_dict(npc_id, npc_d)

    # Load Rooms
    with open(os.path.join(data_dir, "rooms.json"), "r") as f:
        data = json.load(f)
        for room_id, room_d in data.items():
            ROOMS_DB[room_id] = Room.from_dict(room_id, room_d)
