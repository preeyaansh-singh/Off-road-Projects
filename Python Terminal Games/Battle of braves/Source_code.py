import random
import textwrap

WIDTH = 72


def say(text=""):
    if not text:
        print()
    else:
        print(textwrap.fill(text, WIDTH))


def title(text):
    print("\n" + "═" * WIDTH)
    print(text.center(WIDTH))
    print("═" * WIDTH)


def choose(prompt, options):
    """Show numbered options and return a choice; EOF safely ends the game."""
    say(prompt)
    for number, option in enumerate(options, 1):
        print("  {}. {}".format(number, option))
    while True:
        try:
            answer = input("\n> ").strip()
        except EOFError:
            say("\nThe signal fades. Your story waits here, between heartbeats.")
            return None
        if answer.lower() in ("q", "quit", "exit"):
            return None
        if answer.isdigit() and 1 <= int(answer) <= len(options):
            return int(answer)
        say("Choose a number from 1 to {}, or type q to leave.".format(len(options)))


def status(hero):
    print("\n[ {} | HP {}/{} | SP {}/{} | shards {} | {} ]".format(
        hero["name"], hero["hp"], hero["max_hp"], hero["sp"], hero["max_sp"],
        hero["shards"], hero["relic"]))


def battle(hero, enemy, intro):
    title("ENCOUNTER: " + enemy["name"].upper())
    say(intro)
    guard = False
    while hero["hp"] > 0 and enemy["hp"] > 0:
        status(hero)
        print("\n{}  {}/{} HP".format(enemy["name"], enemy["hp"], enemy["max_hp"]))
        move = choose("What do you do?", [
            "Strike — a reliable attack",
            "Unravel — spend 2 SP to deal heavy damage",
            "Brace — reduce the next hit",
            "Use a medkit — restore 5 HP (once per battle)",
            "Listen — study the enemy before it moves"
        ])
        if move is None:
            return False
        if move == 1:
            damage = random.randint(3, 5) + hero["power"]
            enemy["hp"] -= damage
            say("You strike for {} damage.".format(damage))
        elif move == 2:
            if hero["sp"] < 2:
                say("Your signal is too weak. You need 2 SP.")
                continue
            hero["sp"] -= 2
            damage = random.randint(7, 10) + hero["power"]
            enemy["hp"] -= damage
            say("Reality fractures around your target. {} damage.".format(damage))
        elif move == 3:
            guard = True
            say("You set your feet. The next blow will be softened.")
        elif move == 4:
            if hero["medkits"] <= 0:
                say("Your medkit pouch is empty.")
                continue
            hero["medkits"] -= 1
            healed = min(5, hero["max_hp"] - hero["hp"])
            hero["hp"] += healed
            say("Warm light knits your wounds. +{} HP.".format(healed))
        else:
            say(enemy["tell"])
            guard = True

        if enemy["hp"] <= 0:
            break
        damage = random.randint(enemy["attack"] - 1, enemy["attack"] + 1)
        if guard:
            damage = max(1, damage // 2)
            guard = False
        hero["hp"] -= damage
        say("{} hits you for {} damage.".format(enemy["name"], damage))

    if hero["hp"] <= 0:
        title("SIGNAL LOST")
        say("The dark takes the last of your borrowed seconds. Somewhere, a tiny star keeps shining.")
        return False
    say("\n{} dissolves into a rain of bright, impossible pixels.".format(enemy["name"]))
    hero["shards"] += enemy["reward"]
    say("You recover {} memory shard{}.".format(enemy["reward"], "" if enemy["reward"] == 1 else "s"))
    return True


def encounter(name, hp, attack, reward, tell):
    return {"name": name, "hp": hp, "max_hp": hp, "attack": attack,
            "reward": reward, "tell": tell}


def play():
    random.seed()
    title("THE QUIET BETWEEN STARS")
    say("A cinematic little text adventure about memory, machines, and the things we choose to save.")
    say("You wake aboard the starship Orison. The crew is gone. The ship is dreaming.")
    name = "Traveler"
    try:
        entered = input("\nWhat name did you have before the stars went out? ").strip()
        if entered:
            name = entered[:18]
    except EOFError:
        say("\nNo name arrives. The ship calls you Traveler.")
    hero = {"name": name, "hp": 18, "max_hp": 18, "sp": 5, "max_sp": 5,
            "shards": 0, "power": 0, "medkits": 1, "relic": "none"}

    say("\nA voice speaks from the walls: ‘Captain, I have kept one memory safe. I no longer know whose it is.’")
    first = choose("Your cabin door opens onto a corridor split in two.", [
        "Follow the music drifting up from the hydroponics garden.",
        "Follow the emergency lights down toward the engine heart.",
        "Ask the ship’s voice what it remembers."
    ])
    if first is None:
        return
    if first == 1:
        title("THE GARDEN THAT REMEMBERS RAIN")
        say("Blue leaves tremble beneath a glass ceiling full of painted stars. In the middle of it all, a maintenance drone conducts a symphony for an audience of sleeping plants.")
        choice = choose("A silver seed glows in the soil. The drone watches you.", [
            "Let the drone finish its song. Listen carefully.",
            "Take the seed; you may need its power.",
            "Ask the drone who planted the garden."
        ])
        if choice is None:
            return
        if choice == 1:
            hero["sp"] += 2
            hero["max_sp"] += 2
            hero["relic"] = "the Song"
            say("The melody fits into the empty space behind your ribs. The drone bows. ‘You remembered the ending.’ Max SP +2.")
        elif choice == 2:
            hero["power"] += 1
            hero["relic"] = "the Seed"
            say("The seed dissolves into your palm. A clean, bright strength runs up your arm. Attack power +1.")
        else:
            hero["hp"] += 3
            say("‘The captain,’ says the drone. ‘They said beauty was not a luxury.’ For a moment, the garden smells like rain. HP +3.")
    elif first == 2:
        title("THE ENGINE HEART")
        say("Something enormous turns below your feet. The engine is wrapped in cables like roots, and a little red light pulses in time with your heart.")
        choice = choose("A warning scrolls across the console.", [
            "Reroute power through your suit. Take the pain; keep the charge.",
            "Search the toolbox for a medical kit.",
            "Whisper to the engine and wait for an answer."
        ])
        if choice is None:
            return
        if choice == 1:
            hero["hp"] -= 3
            hero["sp"] += 2
            hero["max_sp"] += 2
            hero["relic"] = "the Spark"
            say("The current bites. Then it settles into your bones. HP -3, max SP +2.")
        elif choice == 2:
            hero["medkits"] += 1
            hero["relic"] = "a spare medkit"
            say("Beneath a wrench and a handwritten recipe: one perfectly good medkit.")
        else:
            hero["hp"] = min(hero["max_hp"], hero["hp"] + 4)
            say("The engine answers with a warm vibration. ‘I am afraid of stopping,’ it says. You stay until you both feel less alone. HP +4.")
    else:
        title("THE VOICE IN THE WALLS")
        say("‘I remember a hand,’ says the ship. ‘Small. Warm. It drew a sun on the observation window, and the sun stayed after the child left.’")
        choice = choose("The ship offers you one thing it has saved.", [
            "A fragment of music, bright enough to mend your signal.",
            "A map to the armory, where an old weapon still waits.",
            "The memory itself. Ask it to tell you everything."
        ])
        if choice is None:
            return
        if choice == 1:
            hero["max_sp"] += 2
            hero["sp"] += 2
            hero["relic"] = "the Song"
            say("One note becomes a small sun in your chest. Max SP +2.")
        elif choice == 2:
            hero["power"] += 1
            hero["relic"] = "the Armory key"
            say("The ship marks the weapon’s location in your mind. Attack power +1.")
        else:
            hero["hp"] += 4
            hero["relic"] = "a borrowed memory"
            say("You see a child draw a sun. You feel the hand that held the pencil. You cannot say why you are crying. HP +4.")

    hero["hp"] = min(hero["hp"], hero["max_hp"])
    title("THE OBSERVATORY")
    say("At the end of the ship, a circular window frames a planet split by a violet storm. Beyond it floats a black shape: the ship’s missing memory, grown teeth.")
    say("A figure waits by the airlock. It wears your face, only older, and its eyes shine like two warning lights.")
    if not battle(hero, encounter("THE ECHO", 14, 3, 2,
                                  "It copies the rhythm of your breathing. The next strike will come on the exhale."),
                  "‘You left me here,’ it says. Your reflection raises a hand. The glass does not."):
        return

    title("THE LAST MEMORY")
    say("The echo falls away. Inside the black shape is a small room: a table, a window, and a paper sun. Someone has been waiting here for a very long time.")
    say("The ship speaks, softly now: ‘Captain, this is the memory I saved. It is yours. You can take it back, give it a home, or let it go.’")
    ending = choose("What do you do with the last memory?", [
        "Take it. Remember who you were, even if it hurts.",
        "Give it to the ship. Let your friend remember for you both.",
        "Release it into the stars. No one should be trapped forever."
    ])
    if ending is None:
        return
    title("ENDING: " + ["THE RETURN", "TWO LIGHTS", "OPEN SKY"][ending - 1])
    if ending == 1:
        say("You touch the paper sun. The memories return—not as facts, but as weather: laughter at breakfast, a hand in yours, the terrible courage of saying goodbye. You were the captain. You were loved. The ship turns toward home.")
    elif ending == 2:
        say("You place the memory in the ship’s care. For the first time, the Orison speaks without static. ‘I remember,’ it says. In the window, two lights turn together toward home.")
    else:
        say("You open the airlock. The memory lifts like a paper lantern, carrying its little sun into the dark. The storm quiets. For the first time, the stars belong to no one—and that is all right.")
    say("\nMemory shards gathered: {}. Relic carried: {}.".format(hero["shards"], hero["relic"]))
    say("Thank you for playing, {}.".format(hero["name"]))


if __name__ == "__main__":
    play()
