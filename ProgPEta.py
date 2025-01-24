import random
import time


class_names = ["Mage", "Dex Build", "Strength Build", "Luck Build"]
class_difficulties = ["Easy", "Medium", "Hard", "Grief"]
class_attacks = [(20, 100), (12, 75), (12, 60), (5, 30)]
class_heavy_attacks = [(20, 200), (15, 110), (10, 100), (10, 65)]
class_status = ["Burn", "Bleed", "Stagger", "Random Effect"]
class_weapon_skills = ["Firestorm", "Shadow Strike", "Earthquake", "Fate's Gamble"]


boss_names = ["Deanfaya", "Wrakaphas", "Barnibole", "Deep Wrench"]
boss_health = [1000, 1200, 1300, 1500]
boss_damage = [(10, 60), (10, 67), (10, 56), (1, 75)]
final_boss_name = "Akceptika"
final_boss_health = 2000
final_boss_damage = (20, 100)


def choose_class():
    print("\nChoose your starting class:")
    print("[1] Mage (Easy)")
    print("[2] Dex Build (Medium)")
    print("[3] Strength Build (Hard)")
    print("[4] Luck Build (Grief)")

    while True:
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            index = int(choice) - 1
            print("You have chosen", class_names[index] + ".")
            return index
        else:
            print("Invalid choice. Please choose again.")


def open_inventory(anti_greifa_flask, player_hp, max_hp):
    while True:
        print("\nInventory:")
        print("[1] Anti-Greifa Flask:", anti_greifa_flask)

        use_item = input("Enter item number to use (0 to exit): ").strip()

        if use_item == "0":
            return player_hp, anti_greifa_flask  
        elif use_item == "1" and anti_greifa_flask > 0:
            player_hp = max_hp
            anti_greifa_flask -= 1
            print("You drank the Anti-Greifa Flask and fully restored your HP!")
            return player_hp, anti_greifa_flask
        else:
            print("Invalid choice or no flasks left!")

# Function for battle
def battle(player_index, boss_name, boss_hp, boss_damage_range, player_hp, anti_greifa_flask):
    max_hp = 500

    print("\nYou have entered battle with", boss_name + "!\n")

    while player_hp > 0 and boss_hp > 0:
        print("\n", boss_name, "HP:", boss_hp, "| Your HP:", player_hp)
        print("[1] Light Attack  [2] Heavy Attack  [3] Status Effect  [4] Weapon Skill  [5] Dodge  [6] Open Inventory")

        move = input("Your move: ").strip()
        if move == "1":
            damage = random.randint(*class_attacks[player_index])
            boss_hp -= damage
            print("You dealt", damage, "damage with a Light Attack!")

        elif move == "2":
            damage = random.randint(*class_heavy_attacks[player_index])
            boss_hp -= damage
            print("You dealt", damage, "damage with a Heavy Attack!")

        elif move == "3":
            print("You cast", class_status[player_index], "on", boss_name + "!")

        elif move == "4":
            print("You used your weapon skill:", class_weapon_skills[player_index] + "!")

        elif move == "5":
            if random.random() <= 0.75:
                print("You dodged the attack!")
                continue
            else:
                print("Dodge failed!")

        elif move == "6":
            player_hp, anti_greifa_flask = open_inventory(anti_greifa_flask, player_hp, max_hp)
            continue

        else:
            print("Invalid move, try again.")
            continue

        
        if boss_hp > 0:
            boss_damage = random.randint(*boss_damage_range)
            player_hp -= boss_damage
            print(boss_name, "attacks and deals", boss_damage, "damage!")

        time.sleep(1)

    if player_hp > 0:
        print("\nYou have defeated", boss_name + "!")
        return player_hp, anti_greifa_flask
    else:
        print("\nYou have been defeated...")
        return 0, anti_greifa_flask


def game_loop():
    while True:
        print("\nWelcome to the world of Greifa!")
        start_game = input("Would you like to invade this world? (Y/N): ").strip().upper()

        if start_game == "N":
            print("Goodbye, coward.")
            break
        elif start_game == "Y":
            player_index = choose_class()
            player_hp = 500
            anti_greifa_flask = 15
            remaining_bosses = [0, 1, 2, 3]  

            while remaining_bosses and player_hp > 0:
                print("\nChoose a boss to fight:")
                for i in remaining_bosses:
                    print("[" + str(i + 1) + "]", boss_names[i])

                choice = input("Enter the number of the boss: ").strip()
                if choice in ["1", "2", "3", "4"]:
                    boss_index = int(choice) - 1
                    if boss_index in remaining_bosses:
                        remaining_bosses.remove(boss_index)

                        print("\nBefore the fight, would you like to use an item?")
                        player_hp, anti_greifa_flask = open_inventory(anti_greifa_flask, player_hp, 500)

                        player_hp, anti_greifa_flask = battle(player_index, boss_names[boss_index], boss_health[boss_index], boss_damage[boss_index], player_hp, anti_greifa_flask)
                        if player_hp == 0:
                            print("Game Over.")
                            return
                    else:
                        print("You already defeated that boss!")
                else:
                    print("Invalid choice. Try again.")

            if player_hp > 0:
                print("\nThe final battle awaits!")
                player_hp, anti_greifa_flask = open_inventory(anti_greifa_flask, player_hp, 500)
                player_hp, anti_greifa_flask = battle(player_index, final_boss_name, final_boss_health, final_boss_damage, player_hp, anti_greifa_flask)

            if player_hp > 0:
                print("\nCongratulations! You have conquered the world of Greifa!")

            replay = input("\nWould you like to play again? (Y/N): ").strip().upper()
            if replay != "Y":
                print("Thanks for playing!")
                break
        else:
            print("Invalid choice. Enter Y or N.")

game_loop()
