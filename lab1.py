class Weapon:
    def __init__(self, name, damage):
        self.name = name
        self.damage = damage

class Armor:
    def __init__(self, name, defense):
        self.name = name
        self.defense = defense

class Player:
    def __init__(self, name, level, hp, weapon, armor, guild=None):
        self.name = name
        self.level = level
        self.hp = hp
        self.weapon = weapon
        self.armor = armor
        self.guild = guild

class Guild:
    def __init__(self, name, leader):
        self.name = name
        self.leader = leader
        self.members = [leader]

    def add(self, player):
        self.members.append(player)
        player.guild = self

weapon1 = Weapon("Iron Sword", 10)
weapon2 = Weapon("Wooden Bow", 8)
weapon3 = Weapon("Magic Staff", 12)

armor1 = Armor("Iron Armor", 5)
armor2 = Armor("Diamond Armor", 10)
armor3 = Armor("Netherite Armomr", 30)

player1 = Player("Arm", 1, 100, weapon1, armor1)
player2 = Player("Jim", 2, 120, weapon2, armor2)
player3 = Player("Bright", 3, 80, weapon3, armor3)

guild = Guild("CEI", player1)
guild.add(player1)
guild.add(player2)
guild.add(player3)

def show_infoma(player):
    print(f"=== {player.name} ===")
    print(f"Level: {player.level}")
    print(f"HP: {player.hp}")
    print(f"Weapon: {player.weapon.name} (Damage: {player.weapon.damage})")
    print(f"Armor: {player.armor.name} (Defense: {player.armor.defense})")
    if player.guild:
        leader_tag = " (Leader)" if player.guild.leader == player else ""
        print(f"Guild: {player.guild.name}{leader_tag}")
    print()

if guild:
    for member in guild.members:
        show_infoma(member)