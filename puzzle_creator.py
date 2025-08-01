"""
SpydirWebz Puzzle Creator

A tool for creating cybersecurity logic puzzles with automated validation.
"""

import json
import random
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime

from logic_validator import validate_puzzle


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    IMPOSSIBLE = "impossible"


class ClueType(Enum):
    NEGATION = "negation"
    AFFIRMATIVE = "affirmative"
    RELATIONAL = "relational"
    CONDITIONAL = "conditional"
    DATA_INFERENCE = "data_inference"


@dataclass
class PuzzleSolution:
    actor: str
    vector: str
    asset: str
    stolen_data: str


@dataclass
class Clue:
    text: str
    type: ClueType


@dataclass
class Puzzle:
    author: str
    difficulty: Difficulty
    actors: List[str]
    vectors: List[str]
    assets: List[str]
    stolen_data: List[str]
    solution: PuzzleSolution
    clues: List[Clue]


class PuzzleConfig:
    """Configuration constants for the puzzle creator."""
    MIN_ITEMS = 3
    MAX_ITEMS = 6
    PUZZLES_DIR = "puzzles"
    PUZZLE_FILE_PATTERN = "web_*_draft.json"
    DATA_DIR = "data"
    THREAT_ACTORS_FILE = "data_threat_actors.json"
    ATTACK_VECTORS_FILE = "data_attack_vectors.json"
    ASSETS_FILE = "data_assets.json"
    DATATYPES_FILE = "data_datatypes.json"
    AUTO_ITEMS_PER_CATEGORY = 3
    AUTO_CLUES_COUNT = 10  # 2 of each type


class PuzzleManager:
    """Manages file operations for puzzles."""
    
    @staticmethod
    def get_next_puzzle_number() -> int:
        """Get the next available puzzle number."""
        puzzles_dir = Path(PuzzleConfig.PUZZLES_DIR)
        if not puzzles_dir.exists():
            return 1
        
        existing_files = list(puzzles_dir.glob(PuzzleConfig.PUZZLE_FILE_PATTERN))
        if not existing_files:
            return 1
        
        numbers = []
        for file in existing_files:
            try:
                # Extract number from filename like "web_1.json"
                number = int(file.stem.split('_')[1])
                numbers.append(number)
            except (ValueError, IndexError):
                continue
        
        return max(numbers) + 1 if numbers else 1
    
    @staticmethod
    def save_puzzle(puzzle: Puzzle, puzzle_number: int) -> str:
        """Save puzzle to JSON file."""
        puzzles_dir = Path(PuzzleConfig.PUZZLES_DIR)
        puzzles_dir.mkdir(exist_ok=True)
        
        filename = f"web_{puzzle_number}_draft.json"
        filepath = puzzles_dir / filename
        
        # Convert puzzle to dict, handling enums
        puzzle_dict = asdict(puzzle)
        puzzle_dict['difficulty'] = puzzle.difficulty.value
        puzzle_dict['clues'] = [{'text': clue.text, 'type': clue.type.value} for clue in puzzle.clues]
        
        with open(filepath, 'w') as f:
            json.dump(puzzle_dict, f, indent=2)
        
        return str(filepath)
    
    @staticmethod
    def save_validation_results(puzzle_number: int, validation_result: Dict[str, Any]) -> str:
        """Save validation results to JSON file."""
        puzzles_dir = Path(PuzzleConfig.PUZZLES_DIR)
        puzzles_dir.mkdir(exist_ok=True)
        
        filename = f"web_{puzzle_number}_review.json"
        filepath = puzzles_dir / filename
        
        validation_output = {
            "puzzle_number": puzzle_number,
            "validation_timestamp": datetime.now().isoformat(),
            "validation_result": validation_result,
            "summary": {
                "status": validation_result.get("status", "unknown"),
                "valid": validation_result.get("status") == "valid",
                "has_explanation": "explanation" in validation_result,
                "has_suggestions": "suggestions" in validation_result
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(validation_output, f, indent=2)
        
        return str(filepath)


class DataManager:
    """Manages loading and caching of data from JSON files."""
    
    def __init__(self):
        self._actors_cache = None
        self._vectors_cache = None
        self._assets_cache = None
        self._datatypes_cache = None
    
    def _load_json_file(self, filename: str) -> List[str]:
        """Load data from JSON file with duplicate removal."""
        filepath = Path(PuzzleConfig.DATA_DIR) / filename
        
        if not filepath.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            raise ValueError(f"Invalid data format in {filename}: expected list")
        
        # Remove duplicates while preserving order
        unique_data = []
        for item in data:
            if item not in unique_data:
                unique_data.append(item)
        
        # Warn if duplicates were found
        if len(unique_data) < len(data):
            print(f"⚠️  Warning: Removed {len(data) - len(unique_data)} duplicate entries from {filename}")
        
        return unique_data
    
    def get_actors(self) -> List[str]:
        """Get threat actors from cache or file."""
        if self._actors_cache is None:
            self._actors_cache = self._load_json_file(PuzzleConfig.THREAT_ACTORS_FILE)
        return self._actors_cache
    
    def get_vectors(self) -> List[str]:
        """Get attack vectors from cache or file."""
        if self._vectors_cache is None:
            self._vectors_cache = self._load_json_file(PuzzleConfig.ATTACK_VECTORS_FILE)
        return self._vectors_cache
    
    def get_assets(self) -> List[str]:
        """Get assets from cache or file."""
        if self._assets_cache is None:
            self._assets_cache = self._load_json_file(PuzzleConfig.ASSETS_FILE)
        return self._assets_cache
    
    def get_datatypes(self) -> List[str]:
        """Get data types from cache or file."""
        if self._datatypes_cache is None:
            self._datatypes_cache = self._load_json_file(PuzzleConfig.DATATYPES_FILE)
        return self._datatypes_cache
    
    def select_random_subset(self, data: List[str], count: int) -> List[str]:
        """Select a random subset of data."""
        if count > len(data):
            raise ValueError(f"Requested {count} items but only {len(data)} available")
        
        return random.sample(data, count)


class AutomaticPuzzleGenerator:
    """Generates puzzles automatically without user interaction."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def generate_puzzle(self, author: str, difficulty: Difficulty) -> Puzzle:
        """Generate a complete puzzle automatically."""
        print("🤖 Generating automatic puzzle...")
        
        # Select random elements
        actors = self.data_manager.select_random_subset(
            self.data_manager.get_actors(), 
            PuzzleConfig.AUTO_ITEMS_PER_CATEGORY
        )
        vectors = self.data_manager.select_random_subset(
            self.data_manager.get_vectors(), 
            PuzzleConfig.AUTO_ITEMS_PER_CATEGORY
        )
        assets = self.data_manager.select_random_subset(
            self.data_manager.get_assets(), 
            PuzzleConfig.AUTO_ITEMS_PER_CATEGORY
        )
        datatypes = self.data_manager.select_random_subset(
            self.data_manager.get_datatypes(), 
            1
        )
        
        print(f"✅ Selected {len(actors)} actors: {', '.join(actors)}")
        print(f"✅ Selected {len(vectors)} vectors: {', '.join(vectors)}")
        print(f"✅ Selected {len(assets)} assets: {', '.join(assets)}")
        print(f"✅ Selected data type: {datatypes[0]}")
        
        # Validate uniqueness
        self._validate_uniqueness(actors, vectors, assets, datatypes)
        
        # Create solution
        solution = PuzzleSolution(
            actor=random.choice(actors),
            vector=random.choice(vectors),
            asset=random.choice(assets),
            stolen_data=datatypes[0]
        )
        
        print(f"🎯 Solution: {solution.actor} used {solution.vector} against {solution.asset}")
        
        # Generate clues
        clues = self._generate_random_clues(actors, vectors, assets, solution)
        
        return Puzzle(
            author=author,
            difficulty=difficulty,
            actors=actors,
            vectors=vectors,
            assets=assets,
            stolen_data=datatypes,
            solution=solution,
            clues=clues
        )
    
    def _validate_uniqueness(self, actors: List[str], vectors: List[str], 
                           assets: List[str], datatypes: List[str]) -> None:
        """Validate that all puzzle elements contain only unique items."""
        # Check each category for duplicates
        if len(actors) != len(set(actors)):
            duplicates = [actor for actor in actors if actors.count(actor) > 1]
            raise ValueError(f"Duplicate actors found: {duplicates}")
        
        if len(vectors) != len(set(vectors)):
            duplicates = [vector for vector in vectors if vectors.count(vector) > 1]
            raise ValueError(f"Duplicate vectors found: {duplicates}")
        
        if len(assets) != len(set(assets)):
            duplicates = [asset for asset in assets if assets.count(asset) > 1]
            raise ValueError(f"Duplicate assets found: {duplicates}")
        
        if len(datatypes) != len(set(datatypes)):
            duplicates = [data_type for data_type in datatypes if datatypes.count(data_type) > 1]
            raise ValueError(f"Duplicate data types found: {duplicates}")
        
        print("✅ All puzzle elements are unique")
    
    def _generate_random_clues(self, actors: List[str], vectors: List[str], 
                             assets: List[str], solution: PuzzleSolution) -> List[Clue]:
        """Generate two clues of each type for the puzzle."""
        clues = []
        used_clues = set()
        clue_types = list(ClueType)
        random.shuffle(clue_types)  # Shuffle to vary clue order

        # Helper to avoid duplicate clues
        def add_clue(text, clue_type):
            key = (clue_type, text)
            if key not in used_clues:
                clues.append(Clue(text=text, type=clue_type))
                used_clues.add(key)
                print(f"🔍 Generated clue {len(clues)}: {text}")

        # Negation clues (2)
        negation_options = []
        for a in actors:
            for v in vectors:
                if not (a == solution.actor and v == solution.vector):
                    negation_options.append((a, v))
        random.shuffle(negation_options)
        for a, v in negation_options[:2]:
            add_clue(f"{a} did not use {v}.", ClueType.NEGATION)

        # Affirmative clues (2)
        affirmative_options = []
        for v in vectors:
            for asset in assets:
                if not (v == solution.vector and asset == solution.asset):
                    affirmative_options.append((v, asset))
        random.shuffle(affirmative_options)
        for v, asset in affirmative_options[:2]:
            add_clue(f"{v} was used against the {asset}.", ClueType.AFFIRMATIVE)

        # Relational clues (2)
        relational_options = []
        for v in vectors:
            for asset in assets:
                if not (v == solution.vector and asset == solution.asset):
                    relational_options.append((v, asset))
        random.shuffle(relational_options)
        for v, asset in relational_options[:2]:
            add_clue(f"The actor that used {v} did not access the {asset}.", ClueType.RELATIONAL)

        # Conditional clues (2)
        conditional_options = []
        for a in actors:
            for v in vectors:
                for asset in assets:
                    if not (a == solution.actor and v == solution.vector and asset == solution.asset):
                        conditional_options.append((a, v, asset))
        random.shuffle(conditional_options)
        for a, v, asset in conditional_options[:2]:
            add_clue(f"If {a} used {v}, then they accessed the {asset}.", ClueType.CONDITIONAL)

        # Data Inference clues (2)
        data_inference_options = []
        for v in vectors:
            data_inference_options.append((v, solution.stolen_data))
        random.shuffle(data_inference_options)
        for v, d in data_inference_options[:2]:
            add_clue(f"Only attacks using {v} resulted in theft of {d}.", ClueType.DATA_INFERENCE)

        return clues


class PuzzleCreator:
    """Main class for creating puzzles."""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.puzzle_generator = AutomaticPuzzleGenerator(self.data_manager)
    
    def create_puzzle(self) -> Puzzle:
        """Create a puzzle automatically."""
        print("🕷️ Welcome to the SpydirWebz Puzzle Creator")
        print("🤖 Automatic Mode - Generating puzzle...")
        
        # Get basic information
        author = input("Enter your name or alias: ").strip()
        if not author:
            author = "Anonymous"
        
        # Select difficulty
        print("Select Difficulty:")
        print("1) easy")
        print("2) medium")
        print("3) impossible")
        
        while True:
            try:
                difficulty_choice = int(input("Difficulty (1-3): "))
                if difficulty_choice in [1, 2, 3]:
                    break
                print("❌ Please enter 1, 2, or 3.")
            except ValueError:
                print("❌ Please enter a valid number.")
        
        difficulty_map = {1: Difficulty.EASY, 2: Difficulty.MEDIUM, 3: Difficulty.IMPOSSIBLE}
        difficulty = difficulty_map[difficulty_choice]
        
        # Generate puzzle automatically
        return self.puzzle_generator.generate_puzzle(author, difficulty)
    
    def validate_and_save(self, puzzle: Puzzle) -> bool:
        """Validate puzzle and save to file."""
        print("\n🧪 Validating puzzle...")
        
        # Get next puzzle number
        puzzle_number = PuzzleManager.get_next_puzzle_number()
        
        # Save puzzle before validation
        puzzle_file = PuzzleManager.save_puzzle(puzzle, puzzle_number)
        print(f"📁 Puzzle saved to {puzzle_file}")
        
        # Convert puzzle to dictionary for validation
        puzzle_dict = asdict(puzzle)
        puzzle_dict['difficulty'] = puzzle.difficulty.value
        puzzle_dict['clues'] = [{'text': clue.text, 'type': clue.type.value} for clue in puzzle.clues]
        
        # Validate puzzle
        validation_result = validate_puzzle(puzzle_dict)
        
        # Save validation results
        validation_file = PuzzleManager.save_validation_results(puzzle_number, validation_result)
        print(f"📁 Validation results saved to {validation_file}")
        
        # Display results
        if validation_result["status"] == "valid":
            print("✅ Puzzle is valid and uniquely solvable.")
            return True
        else:
            print(f"❌ Puzzle validation failed: {validation_result['status']}")
            if "explanation" in validation_result:
                print(f"📝 {validation_result['explanation']}")
            if "suggestions" in validation_result:
                print("💡 Suggestions:")
                for suggestion in validation_result["suggestions"]:
                    print(f"   • {suggestion}")
            return False


def main():
    """Main function to run the puzzle creator."""
    try:
        creator = PuzzleCreator()
        puzzle = creator.create_puzzle()
        creator.validate_and_save(puzzle)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()
