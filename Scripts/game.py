# Import necessary modules
import random

# Define the player class
class Player:
    def __init__(self, name, player_class):
        self.name = name
        self.player_class = player_class
        self.level = 1
        self.health = 100
        self.attack = 10
        self.defense = 5
        self.experience = 0

    def level_up(self):
        self.level += 1
        self.health += 10
        self.attack += 5
        self.defense += 2

    def gain_experience(self, exp):
        self.experience += exp
        if self.experience >= 100:
            self.level_up()
            self.experience = 0

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.game_over()

    def game_over(self):
        print("Game Over")
        # Add more feedback or options to restart the game

# Define the enemy class
class Enemy:
    def __init__(self, name, health, attack):
        self.name = name
        self.health = health
        self.attack = attack

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            print(f"You defeated the {self.name}!")

# Define the game class
class Game:
    def __init__(self):
        self.player = None
        self.enemies = [
            Enemy("Goblin", 20, 5),
            Enemy("Orc", 30, 10),
            Enemy("Dragon", 50, 15)
        ]

    def start(self):
        print("Welcome to Mystic Quest!")
        name = input("Enter your name: ")
        player_class = input("Choose your class (warrior/mage/rogue): ")
        self.player = Player(name, player_class)
        print(f"Welcome, {self.player.name} the {self.player.player_class}!")

    def explore(self):
        print("You are exploring the mystical land...")
        enemy = random.choice(self.enemies)
        print(f"An enemy {enemy.name} appears!")
        while self.player.health > 0 and enemy.health > 0:
            action = input("What do you want to do? (attack/run): ")
            if action == "attack":
                damage = self.player.attack - enemy.attack
                if damage > 0:
                    enemy.take_damage(damage)
                else:
                    print("Your attack is too weak to damage the enemy.")
                if enemy.health > 0:
                    damage = enemy.attack - self.player.defense
                    if damage > 0:
                        self.player.take_damage(damage)
                    else:
                        print("The enemy's attack is too weak to damage you.")
            elif action == "run":
                print("You managed to escape!")
                break
            else:
                print("Invalid action!")

    def play(self):
        self.start()
        while self.player.health > 0:
            self.explore()

# Create an instance of the game and start playing
game = Game()
game.play()