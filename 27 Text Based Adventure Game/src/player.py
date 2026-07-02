from src.models import ITEMS_DB, SPELLS_DB, Quest
from src.utils import type_print, green, yellow, blue, magenta, cyan, bold, health_bar, mana_bar, xp_bar

class Player:
    def __init__(self):
        # Stats
        self.level = 1
        self.xp = 0
        self.xp_to_next = 100
        
        self.max_hp = 50
        self.hp = 50
        
        self.max_mp = 20
        self.mp = 20
        
        self.base_attack = 5
        self.base_defense = 2
        self.base_magic = 3
        self.agility = 10
        
        self.gold = 50
        
        # Equipment & Inventories
        self.weapon_id = None  # item_id of equipped weapon
        self.armor_id = None   # item_id of equipped armor
        self.inventory = ["rusty_dagger", "health_potion"]  # list of item_ids
        
        # Spells known (by spell_id)
        self.spells = ["fireball"]
        
        # Quest state
        self.active_quests = {}  # quest_id -> Quest object
        self.completed_quests = []  # list of quest_ids
        
        # Stats tracking for quests/achievements
        self.kills = {}  # enemy_id -> count
        
        self.current_room_id = "starting_cell"

    # Property helpers
    @property
    def weapon(self):
        return ITEMS_DB.get(self.weapon_id) if self.weapon_id else None

    @property
    def armor(self):
        return ITEMS_DB.get(self.armor_id) if self.armor_id else None

    @property
    def attack_power(self):
        atk = self.base_attack
        if self.weapon:
            atk += self.weapon.attack
        if self.armor:
            atk += self.armor.attack
        return atk

    @property
    def defense_power(self):
        df = self.base_defense
        if self.weapon:
            df += self.weapon.defense
        if self.armor:
            df += self.armor.defense
        return df

    @property
    def magic_power(self):
        mag = self.base_magic
        if self.weapon:
            mag += self.weapon.magic_power
        if self.armor:
            mag += self.armor.magic_power
        return mag

    def show_stats(self):
        """Displays player sheet."""
        stats = [
            f"=== {bold(yellow('PLAYER PROFILE'))} ===",
            f"Level: {self.level} | XP: {self.xp}/{self.xp_to_next}",
            xp_bar(self.xp, self.xp_to_next, length=25),
            f"HP: {health_bar(self.hp, self.max_hp, length=25)}",
            f"MP: {mana_bar(self.mp, self.max_mp, length=25)}",
            f"Gold: {yellow(str(self.gold))} G",
            "",
            f"Attack: {self.attack_power} (Base: {self.base_attack} + Eq: {self.attack_power - self.base_attack})",
            f"Defense: {self.defense_power} (Base: {self.base_defense} + Eq: {self.defense_power - self.base_defense})",
            f"Magic Power: {self.magic_power} (Base: {self.base_magic} + Eq: {self.magic_power - self.base_magic})",
            f"Agility: {self.agility}",
            "",
            f"Weapon: {cyan(self.weapon.name) if self.weapon else 'Bare Hands'}",
            f"Armor: {cyan(self.armor.name) if self.armor else 'Ragged Clothes'}",
            ""
        ]
        for line in stats:
            type_print(line)

    def show_inventory(self):
        """Displays player inventory."""
        if not self.inventory:
            type_print("Your inventory is empty.")
            return

        type_print(f"=== {bold(cyan('INVENTORY'))} ===")
        # Count identical items
        counts = {}
        for item_id in self.inventory:
            counts[item_id] = counts.get(item_id, 0) + 1

        for item_id, count in counts.items():
            item = ITEMS_DB.get(item_id)
            if not item:
                continue
            equip_tag = ""
            if self.weapon_id == item_id:
                equip_tag = yellow(" [Equipped Weapon]")
            elif self.armor_id == item_id:
                equip_tag = yellow(" [Equipped Armor]")

            qty = f" x{count}" if count > 1 else ""
            desc = f"- {bold(item.name)}{qty} ({item.type}): {item.description}{equip_tag}"
            type_print(desc)
        type_print("")

    def show_spells(self):
        """Displays player spells."""
        if not self.spells:
            type_print("You don't know any spells.")
            return

        type_print(f"=== {bold(blue('SPELLBOOK'))} ===")
        for spell_id in self.spells:
            spell = SPELLS_DB.get(spell_id)
            if spell:
                type_print(f"- {bold(spell.name)} (Cost: {blue(str(spell.mana_cost) + ' MP')}, Power: {spell.power}): {spell.description}")
        type_print("")

    def add_item(self, item_id):
        if item_id in ITEMS_DB:
            self.inventory.append(item_id)
            item = ITEMS_DB[item_id]
            type_print(green(f"Acquired: {bold(item.name)}!"))
            self.check_quests_on_fetch(item_id)
            return True
        return False

    def remove_item(self, item_id):
        if item_id in self.inventory:
            # If removing equipped item, unequip first
            if self.weapon_id == item_id:
                self.weapon_id = None
            elif self.armor_id == item_id:
                self.armor_id = None
            self.inventory.remove(item_id)
            return True
        return False

    def equip(self, item_id):
        if item_id not in self.inventory:
            type_print(f"You don't have that item.")
            return

        item = ITEMS_DB.get(item_id)
        if not item:
            return

        if item.type == "weapon":
            self.weapon_id = item_id
            type_print(green(f"Equipped {bold(item.name)} as your weapon."))
        elif item.type == "armor":
            self.armor_id = item_id
            type_print(green(f"Equipped {bold(item.name)} as your armor."))
        else:
            type_print(f"{item.name} cannot be equipped.")

    def unequip(self, slot):
        if slot == "weapon":
            if self.weapon_id:
                name = ITEMS_DB[self.weapon_id].name
                self.weapon_id = None
                type_print(yellow(f"Unequipped {bold(name)}."))
            else:
                type_print("You don't have a weapon equipped.")
        elif slot == "armor":
            if self.armor_id:
                name = ITEMS_DB[self.armor_id].name
                self.armor_id = None
                type_print(yellow(f"Unequipped {bold(name)}."))
            else:
                type_print("You don't have armor equipped.")
        else:
            type_print("Invalid slot. Choose 'weapon' or 'armor'.")

    def use_consumable(self, item_id):
        if item_id not in self.inventory:
            type_print(f"You don't have a {item_id}.")
            return False

        item = ITEMS_DB.get(item_id)
        if not item or item.type != "consumable":
            type_print(f"You cannot consume {item.name if item else item_id}.")
            return False

        if item.effect == "heal_hp":
            actual_heal = min(item.amount, self.max_hp - self.hp)
            self.hp += actual_heal
            type_print(green(f"You consumed {bold(item.name)} and restored {actual_heal} HP!"))
        elif item.effect == "heal_mp":
            actual_heal = min(item.amount, self.max_mp - self.mp)
            self.mp += actual_heal
            type_print(green(f"You consumed {bold(item.name)} and restored {actual_heal} MP!"))
        elif item.effect == "restore_all":
            heal_hp = self.max_hp - self.hp
            heal_mp = self.max_mp - self.mp
            self.hp = self.max_hp
            self.mp = self.max_mp
            type_print(green(f"You consumed {bold(item.name)}! Restored {heal_hp} HP and {heal_mp} MP completely!"))
        
        self.inventory.remove(item_id)
        return True

    def add_xp(self, amount):
        self.xp += amount
        type_print(magenta(f"Gained {amount} XP!"))
        if self.xp >= self.xp_to_next:
            self.level_up()

    def level_up(self):
        self.level += 1
        self.xp -= self.xp_to_next
        self.xp_to_next = int(self.xp_to_next * 1.5)
        
        # Increase stats
        self.max_hp += 12
        self.max_mp += 5
        self.base_attack += 2
        self.base_defense += 1
        self.base_magic += 2
        self.agility += 1
        
        # Refill pools
        self.hp = self.max_hp
        self.mp = self.max_mp
        
        type_print(yellow("*" * 40, True))
        type_print(yellow(f" LEVEL UP! You reached LEVEL {self.level}! ".center(40), True))
        type_print(yellow("*" * 40, True))
        type_print(green(f"Max HP increased to {self.max_hp}"))
        type_print(blue(f"Max MP increased to {self.max_mp}"))
        type_print(f"Base Attack increased to {self.base_attack}")
        type_print(f"Base Defense increased to {self.base_defense}")
        type_print(f"Base Magic increased to {self.base_magic}")
        
        # Unlock spells
        new_spells = {
            2: "ice_shard",
            3: "thunderbolt"
        }
        if self.level in new_spells:
            spell_id = new_spells[self.level]
            spell = SPELLS_DB.get(spell_id)
            if spell and spell_id not in self.spells:
                self.spells.append(spell_id)
                type_print(magenta(f"Unlocked new spell: {bold(spell.name)}!"))

    def check_quests_on_kill(self, enemy_id):
        """Update active quests with kill objectives."""
        self.kills[enemy_id] = self.kills.get(enemy_id, 0) + 1
        for quest in self.active_quests.values():
            if quest.type == "kill" and quest.target == enemy_id:
                quest.current_count = min(quest.required_count, self.kills.get(enemy_id, 0))
                type_print(yellow(f"Quest Progress [{quest.name}]: Slayed {enemy_id} ({quest.current_count}/{quest.required_count})"))

    def check_quests_on_fetch(self, item_id):
        """Update active quests with fetch objectives."""
        for quest in self.active_quests.values():
            if quest.type == "fetch" and quest.target == item_id:
                count = self.inventory.count(item_id)
                quest.current_count = min(quest.required_count, count)
                type_print(yellow(f"Quest Progress [{quest.name}]: Collected {ITEMS_DB[item_id].name} ({quest.current_count}/{quest.required_count})"))

    def check_quest_ready_to_complete(self, quest_id):
        """Verify if a quest is ready to be turned in."""
        quest = self.active_quests.get(quest_id)
        if not quest:
            return False
        
        if quest.type == "kill":
            return quest.current_count >= quest.required_count
        elif quest.type == "fetch":
            # Recalculate based on inventory to be accurate
            count = self.inventory.count(quest.target)
            quest.current_count = min(quest.required_count, count)
            return quest.current_count >= quest.required_count
        return False

    def show_quests(self):
        """Prints quest log."""
        if not self.active_quests and not self.completed_quests:
            type_print("You have no quests.")
            return

        if self.active_quests:
            type_print(f"=== {bold(yellow('ACTIVE QUESTS'))} ===")
            for quest in self.active_quests.values():
                type_print(f"- {bold(quest.name)}: {quest.description}")
                type_print(f"  Progress: {quest.current_count}/{quest.required_count}")
            type_print("")

        if self.completed_quests:
            type_print(f"=== {bold(green('COMPLETED QUESTS'))} ===")
            for q_id in self.completed_quests:
                # Retrieve from npcs database quest definitions since we don't have a quests.json database
                # Alternatively just print quest ID or look it up in NPC quests.
                # Let's search NPCs DB
                q_name = q_id
                from src.models import NPCS_DB
                for npc in NPCS_DB.values():
                    if npc.quest and npc.quest.id == q_id:
                        q_name = npc.quest.name
                        break
                type_print(f"- {green(q_name)} (Completed)")
            type_print("")
