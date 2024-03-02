from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# Ensure other necessary imports are here

class Character:
    def __init__(self, name, health, attack, defense, max_health, level=1, experience=0):
        """Initialize a new character with extended attributes."""
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.max_health = max_health
        self.level = level
        self.experience = experience
        self.inventory = []

    def gain_experience(self, amount):
        """Increase character's experience and handle leveling up."""
        self.experience += amount
        while self.experience >= 100:  # Allows for multiple level-ups if experience > 100
            self.level_up()
            self.experience -= 100  # Keeps excess experience

    def level_up(self):
        """Increase character's level and improve stats."""
        self.level += 1
        self.attack += 5
        self.defense += 5
        self.max_health += 20
        self.health = self.max_health
        print(f"{self.name} has reached level {self.level}!")

    def add_item_to_inventory(self, item):
        """Add an item to the character's inventory."""
        self.inventory.append(item)

    def use_item(self, item_name):
        """Use an item from the inventory, affecting character stats or health."""
        for item in self.inventory:
            if item.name == item_name:
                if item.effect == "health":
                    self.health += item.magnitude
                    if self.health > self.max_health:
                        self.health = self.max_health
                # Add other effects as needed
                self.inventory.remove(item)
                break

class Item:
    def __init__(self, name, effect, magnitude, item_type="consumable"):
        """Initialize a new item with type."""
        self.name = name
        self.effect = effect
        self.magnitude = magnitude
        self.item_type = item_type

class InventoryScreen(Screen):
    def on_pre_enter(self, *args):
        # Example of updating inventory display
        inventory_info = self.ids.inventory_info
        inventory_info.text = '\n'.join([item.name for item in player_character.inventory])  # Assuming 'player_character' is your character instance

# Ensure GameScreen class is defined, even if unchanged
class GameScreen(Screen):
    pass

# Kivy layout string remains unchanged, ensure it's correctly integrated with the Python code