class EffectStrategy:
    def apply_effect(self, character):
        raise NotImplementedError

class HealEffect(EffectStrategy):
    def __init__(self, value):
        self.value = value

    def apply_effect(self, character):
        character.health += self.value
        if character.health > character.max_health:
            character.health = character.max_health

class BuffAttackEffect(EffectStrategy):
    def __init__(self, value):
        self.value = value

    def apply_effect(self, character):
        character.attack += self.value

class Item:
    def __init__(self, name, effect_strategy):
        self.name = name
        self.effect_strategy = effect_strategy

    def apply_effect(self, character):
        self.effect_strategy.apply_effect(character)

class Character:
    def __init__(self, name, health, attack, defense, magic, speed, max_health, level=1, experience=0):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.magic = magic
        self.speed = speed
        self.max_health = max_health
        self.level = level
        self.experience = experience
        self.inventory = []
        self.equipment = {"weapon": None, "armor": None}

    def use_item(self, item_name):
        found = False
        for item in self.inventory:
            if item.name == item_name:
                found = True
                item.apply_effect(self)
                self.inventory.remove(item)  # Assuming consumable items
                break
        if not found:
            print(f"Item {item_name} not found in inventory.")

class CombatScreen(Screen):
    def on_pre_enter(self, *args):
        # Prepare combat UI and display enemy info
        # This is a placeholder for actual implementation
        print("Entering combat...")

    def attack_enemy(self):
        # Placeholder for player attack logic
        print("Player attacks!")

# Ensure smooth transitions in ScreenManagement
class ScreenManagement(ScreenManager):
    pass

kv = """
ScreenManagement:
    InventoryScreen:
    GameScreen:
    CombatScreen:

<InventoryScreen>:
    name: 'inventory'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Inventory'
        Button:
            text: 'Back to game'
            on_press: app.root.current = 'game'

<GameScreen>:
    name: 'game'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Game Screen'
        Button:
            text: 'Go to inventory'
            on_press: app.root.current = 'inventory'
        Button:
            text: 'Enter Combat'
            on_press: app.root.current = 'combat'

<CombatScreen>:
    name: 'combat'
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Prepare for battle!'
        Button:
            text: 'Attack'
            on_press: root.attack_enemy()
"""