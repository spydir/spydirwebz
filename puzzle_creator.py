import json
import os
import re
from logic_validator import validate_puzzle

def prompt_list(name, min_count=3, max_count=6):
    print(f"Enter {name} ({min_count}-{max_count} items, comma-separated):")
    while True:
        items = input(f"{name}: ").strip().split(",")
        items = [x.strip() for x in items if x.strip()]
        if min_count <= len(items) <= max_count:
            return items
        print(f"❌ Please enter between {min_count} and {max_count} items.")

def prompt_choice(name, options):
    print(f"Select {name}:")
    for i, option in enumerate(options, 1):
        print(f"{i}) {option}")
    while True:
        try:
            i = int(input(f"{name} (1-{len(options)}): "))
            return options[i-1]
        except:
            print("❌ Invalid choice.")

def prompt_clue(actors, vectors, assets):
    print("\nAdd a clue (select type):")
    print(" 1) Negation")
    print(" 2) Affirmative")
    print(" 3) Relational")
    print(" 4) Conditional")
    print(" 5) Data Inference")
    choice = input("Type (1-5): ").strip()
    if choice == "1":
        a = prompt_choice("Actor", actors)
        v = prompt_choice("Vector", vectors)
        return {"text": f"{a} did not use {v}.", "type": "negation"}
    elif choice == "2":
        v = prompt_choice("Vector", vectors)
        s = prompt_choice("Asset", assets)
        return {"text": f"{v} was used against the {s}.", "type": "affirmative"}
    elif choice == "3":
        v = prompt_choice("Vector", vectors)
        s = prompt_choice("Asset", assets)
        return {"text": f"The actor that used {v} did not access the {s}.", "type": "relational"}
    elif choice == "4":
        a = prompt_choice("Actor", actors)
        v = prompt_choice("Vector", vectors)
        s = prompt_choice("Asset", assets)
        return {"text": f"If {a} used {v}, then they accessed the {s}.", "type": "conditional"}
    elif choice == "5":
        v = prompt_choice("Vector", vectors)
        d = input("Enter stolen data (e.g., Source Code): ").strip()
        return {"text": f"Only attacks using {v} resulted in theft of {d}.", "type": "data-inference"}
    else:
        print("❌ Invalid choice.")
        return None

def get_next_puzzle_number():
    os.makedirs("puzzles", exist_ok=True)
    existing = [f for f in os.listdir("puzzles") if re.match(r'web_\d+\.json', f)]
    numbers = [int(re.findall(r'\d+', f)[0]) for f in existing] if existing else [0]
    return max(numbers) + 1

def main():
    print("\n🕷️ Welcome to the SpydirWebz Puzzle Creator")

    author = input("Enter your name or alias: ").strip()
    difficulty = prompt_choice("Difficulty", ["easy", "medium", "impossible"])

    actors = prompt_list("Threat Actors")
    vectors = prompt_list("Attack Vectors")
    assets = prompt_list("Compromised Assets")
    data_types = prompt_list("Stolen Data")

    print("\nNow choose the correct solution:")
    sol_actor = prompt_choice("Actor", actors)
    sol_vector = prompt_choice("Vector", vectors)
    sol_asset = prompt_choice("Asset", assets)
    sol_data = prompt_choice("Stolen Data", data_types)

    clues = []
    while True:
        clue = prompt_clue(actors, vectors, assets)
        if clue:
            clues.append(clue)
        more = input("Add another clue? (y/n): ").strip().lower()
        if more != 'y':
            break

    puzzle = {
        "title": f"Web {get_next_puzzle_number()} - {sol_actor} breach",
        "difficulty": difficulty,
        "author": author,
        "actors": actors,
        "vectors": vectors,
        "assets": assets,
        "stolen_data": data_types,
        "solution": {
            "actor": sol_actor,
            "vector": sol_vector,
            "asset": sol_asset,
            "stolen_data": sol_data
        },
        "clues": clues
    }

    print("\n🧪 Validating puzzle...")
    result = validate_puzzle(puzzle)

    if result['status'] == 'valid':
        print("✅ Puzzle is valid and uniquely solvable.")
        num = get_next_puzzle_number()
        filename = f"puzzles/web_{num}.json"
        with open(filename, "w") as f:
            json.dump(puzzle, f, indent=2)
        print(f"📁 Puzzle saved to {filename}")
    else:
        print(f"❌ Puzzle validation failed: {result['status']}")
        print(result)

if __name__ == "__main__":
    main()
