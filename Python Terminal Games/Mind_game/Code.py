import os
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def get_user_input():
    while True:
        choice = input("👉 Is your number (h) Higher, (l) Lower, or (c) Correct? : ").lower()
        if choice in ['h', 'l', 'c']:
            return choice
        else:
            print("❌ Invalid input. Use h / l / c")

def play_game():
    clear()
    slow_print("🧠 Welcome to the Mind Reader Game!")
    slow_print("Think of a number between 1 and 100...")
    input("Press ENTER when you're ready...")

    low = 1
    high = 100
    attempts = 0
    max_attempts = 7  # Binary search max steps

    while low <= high:
        attempts += 1
        guess = (low + high) // 2

        print(f"\n🤖 My guess is: {guess}")
        choice = get_user_input()

        if choice == 'c':
            slow_print(f"\n🎉 I guessed it in {attempts} attempts!")
            break

        elif choice == 'h':
            low = guess + 1

        elif choice == 'l':
            high = guess - 1

        if attempts >= max_attempts:
            slow_print("\n😵 Hmm... something feels off...")
            slow_print("👉 Did you change your number? 😏")
            break

    print("\n📊 Game Over")

def main():
    while True:
        play_game()

        again = input("\n🔁 Play again? (y/n): ").lower()
        if again != 'y':
            print("\n👋 Thanks for playing Mind Reader!")
            break

if __name__ == "__main__":
    main()