import time
import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow(text):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(0.02)
    print()

# GAME DATA
suspects = {
    "1": {"name": "Mr. Verma", "alibi": "I was at the office late night...", "clue": "His watch is broken at 10:15"},
    "2": {"name": "Mrs. Verma", "alibi": "I was sleeping...", "clue": "She has mud on her shoes"},
    "3": {"name": "Rohit (Friend)", "alibi": "I was out of town...", "clue": "His phone location shows he was nearby"}
}

killer = "2"  # Change this to randomize later

found_clues = []
visited = []

def intro():
    clear()
    slow("🕵️ CASE FILE: MIDNIGHT MURDER")
    slow("A wealthy man was found dead at midnight...")
    slow("You are the detective assigned to solve this case.")
    input("\nPress ENTER to begin investigation...")

def show_menu():
    print("\n📌 What would you like to do?")
    print("1. Interrogate a suspect")
    print("2. View collected clues")
    print("3. Accuse someone")
    print("4. Exit game")

def interrogate():
    print("\n👥 Suspects:")
    for key, val in suspects.items():
        print(f"{key}. {val['name']}")

    choice = input("Choose a suspect: ")

    if choice in suspects:
        suspect = suspects[choice]

        slow(f"\n🗣️ Interrogating {suspect['name']}...")
        slow(f"💬 {suspect['alibi']}")

        if choice not in visited:
            slow(f"🔍 Clue found: {suspect['clue']}")
            found_clues.append(suspect['clue'])
            visited.append(choice)
        else:
            slow("⚠️ You already interrogated this suspect.")

    else:
        print("❌ Invalid choice")

def show_clues():
    print("\n📂 Collected Clues:")
    if not found_clues:
        print("No clues yet...")
    else:
        for clue in found_clues:
            print(f"- {clue}")

def accuse():
    print("\n⚖️ Who do you accuse?")
    for key, val in suspects.items():
        print(f"{key}. {val['name']}")

    choice = input("Your accusation: ")

    if choice == killer:
        slow("\n🎉 Correct! You solved the case!")
        slow("Justice has been served.")
    else:
        slow("\n❌ Wrong accusation!")
        slow("The real killer escaped...")
    
    slow("\n🏁 CASE CLOSED")
    return False  # end game

def game():
    intro()
    running = True

    while running:
        show_menu()
        choice = input("Enter your choice: ")

        if choice == "1":
            interrogate()
        elif choice == "2":
            show_clues()
        elif choice == "3":
            running = accuse()
        elif choice == "4":
            print("👋 Exiting game...")
            break
        else:
            print("❌ Invalid option")

def main():
    while True:
        game()
        again = input("\n🔁 Play again? (y/n): ").lower()
        if again != 'y':
            break

if __name__ == "__main__":
    main()