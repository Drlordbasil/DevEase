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

    def level_up(self):
        self.level += 1
        self.health += 10
        self.attack += 5
        self.defense += 2

    def take_damage(self, damage):
        self.health -= damage

    def attack_enemy(self, enemy):
        damage = self.attack - enemy.defense
        if damage < 0:
            damage = 0
        enemy.take_damage(damage)

# Define the enemy class
class Enemy:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense

    def take_damage(self, damage):
        self.health -= damage

    def attack_player(self, player):
        damage = self.attack - player.defense
        if damage < 0:
            damage = 0
        player.take_damage(damage)

# Define a function to simulate a battle between the player and an enemy
def battle(player, enemy):
    print(f"A wild {enemy.name} appears!")
    while player.health > 0 and enemy.health > 0:
        print(f"{player.name}: {player.health} HP")
        print(f"{enemy.name}: {enemy.health} HP")
        print("1. Attack")
        print("2. Run")
        choice = input("Enter your choice: ")
        if choice == "1":
            player.attack_enemy(enemy)
            enemy.attack_player(player)
        elif choice == "2":
            print("You managed to escape!")
            return
        else:
            print("Invalid choice. Try again.")
    if player.health <= 0:
        print("You were defeated. Game over.")
    else:
        print(f"You defeated the {enemy.name}!")

# Define the main function
def main():
    print("Welcome to Mystic Quest!")
    name = input("Enter your name: ")
    player_class = input("Choose your class (warrior/mage/rogue): ")
    player = Player(name, player_class)
    print(f"Welcome, {player.name} the {player.player_class}!")
    print("Let the adventure begin!")
    enemy = Enemy("Goblin", 50, 8, 2)
    battle(player, enemy)

# Run the main function
if __name__ == "__main__":
    main()