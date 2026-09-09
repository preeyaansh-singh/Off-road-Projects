import random

print("🎰 Welcome to BLAVIA CASINO 🎰")

balance = 500

while True:
    print(f"\n💰 Current Balance: ₹{balance}")

    if balance <= 0:
        print("💀 You're broke... Game Over!")
        break

    choice = input("\nDo you want to play? (yes/no): ").lower()
    if choice == "no":
        print("👋 Thanks for playing!")
        break

    # Bet validation
    while True:
        try:
            bet = int(input("💸 Enter your bet amount: "))
            if 0 < bet <= balance:
                break
            else:
                print("❌ Invalid bet amount.")
        except:
            print("⚠️ Enter a valid number.")

    # Difficulty selection
    print("\n🎯 Choose Difficulty:")
    print("1. Easy (1-50)")
    print("2. Medium (1-100)")
    print("3. Hard (1-200)")

    difficulty_map = {
        "1": (50, 1.5),
        "2": (100, 2),
        "3": (200, 3)
    }

    while True:
        diff = input("Select (1/2/3): ")
        if diff in difficulty_map:
            max_range, multiplier = difficulty_map[diff]
            break
        else:
            print("❌ Invalid choice.")

    # 🔥 Generate 10 random numbers (pool)
    winning_numbers = random.sample(range(1, max_range + 1), 10)

    # User guess
    while True:
        try:
            guess = int(input(f"🔢 Guess a number (1-{max_range}): "))
            if 1 <= guess <= max_range:
                break
            else:
                print("❌ Out of range.")
        except:
            print("⚠️ Enter a valid number.")

    # ✅ Updated result logic
    if guess in winning_numbers:
        winnings = int(bet * multiplier)
        balance += winnings
        print(f"\n🎉 JACKPOT! Your number matched!")
        print(f"💸 You won ₹{winnings}")
    else:
        balance -= bet
        print(f"\n😢 You lost ₹{bet}")

    print(f"🎲 Winning pool: {sorted(winning_numbers)}")
    print(f"🔢 Your guess: {guess}")
    print(f"💰 New Balance: ₹{balance}")

print("\n🏁 Game Ended")