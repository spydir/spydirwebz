"""
SpydirWebz Puzzle Creator

A tool for creating cybersecurity logic puzzles with automated validation.
"""

import json
import os
import re
import random
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum
from pathlib import Path

from logic_validator import validate_puzzle


class Difficulty(Enum):
    """Puzzle difficulty levels."""
    EASY = "easy"
    MEDIUM = "medium"
    IMPOSSIBLE = "impossible"


class ClueType(Enum):
    """Types of clues that can be added to puzzles."""
    NEGATION = "negation"
    AFFIRMATIVE = "affirmative"
    RELATIONAL = "relational"
    CONDITIONAL = "conditional"
    DATA_INFERENCE = "data-inference"


@dataclass
class PuzzleSolution:
    """Represents the solution to a puzzle."""
    actor: str
    vector: str
    asset: str
    stolen_data: str


@dataclass
class Clue:
    """Represents a clue in the puzzle."""
    text: str
    type: ClueType


@dataclass
class Puzzle:
    """Represents a complete puzzle."""
    title: str
    difficulty: Difficulty
    author: str
    actors: List[str]
    vectors: List[str]
    assets: List[str]
    stolen_data: List[str]
    solution: PuzzleSolution
    clues: List[Clue]


class PuzzleConfig:
    """Configuration for puzzle creation."""
    
    MIN_ITEMS = 3
    MAX_ITEMS = 6
    PUZZLES_DIR = "puzzles"
    DATA_DIR = "data"
    PUZZLE_FILE_PATTERN = r'web_(\d+)\.json'
    
    # Data source file names
    THREAT_ACTORS_FILE = "data_threat_actors.json"
    ATTACK_VECTORS_FILE = "data_attack_vectors.json"
    ASSETS_FILE = "data_assets.json"
    DATATYPES_FILE = "data_datatypes.json"
    
    # Automatic mode settings
    AUTO_ITEMS_PER_CATEGORY = 3
    AUTO_CLUES_COUNT = 3
    
    @classmethod
    def get_clue_type_options(cls) -> List[Tuple[str, ClueType]]:
        """Get available clue type options for user selection."""
        return [
            ("Negation", ClueType.NEGATION),
            ("Affirmative", ClueType.AFFIRMATIVE),
            ("Relational", ClueType.RELATIONAL),
            ("Conditional", ClueType.CONDITIONAL),
            ("Data Inference", ClueType.DATA_INFERENCE),
        ]


class DataManager:
    """Manages loading and selection of puzzle data from JSON files."""
    
    def __init__(self, data_dir: str = PuzzleConfig.DATA_DIR):
        self.data_dir = Path(data_dir)
        self._threat_actors: Optional[List[str]] = None
        self._attack_vectors: Optional[List[str]] = None
        self._assets: Optional[List[str]] = None
        self._datatypes: Optional[List[str]] = None
    
    def load_all_data(self) -> Dict[str, List[str]]:
        """Load all data sources and return as a dictionary."""
        return {
            'threat_actors': self.get_threat_actors(),
            'attack_vectors': self.get_attack_vectors(),
            'assets': self.get_assets(),
            'datatypes': self.get_datatypes()
        }
    
    def get_threat_actors(self) -> List[str]:
        """Load threat actors from JSON file."""
        if self._threat_actors is None:
            self._threat_actors = self._load_json_file(PuzzleConfig.THREAT_ACTORS_FILE)
        return self._threat_actors
    
    def get_attack_vectors(self) -> List[str]:
        """Load attack vectors from JSON file."""
        if self._attack_vectors is None:
            self._attack_vectors = self._load_json_file(PuzzleConfig.ATTACK_VECTORS_FILE)
        return self._attack_vectors
    
    def get_assets(self) -> List[str]:
        """Load assets from JSON file."""
        if self._assets is None:
            self._assets = self._load_json_file(PuzzleConfig.ASSETS_FILE)
        return self._assets
    
    def get_datatypes(self) -> List[str]:
        """Load datatypes from JSON file."""
        if self._datatypes is None:
            self._datatypes = self._load_json_file(PuzzleConfig.DATATYPES_FILE)
        return self._datatypes
    
    def _load_json_file(self, filename: str) -> List[str]:
        """Load and parse a JSON file containing a list of strings."""
        file_path = self.data_dir / filename
        
        if not file_path.exists():
            raise FileNotFoundError(f"Data file not found: {file_path}")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            if not isinstance(data, list):
                raise ValueError(f"Expected list in {filename}, got {type(data)}")
            
            # Validate that all items are strings
            if not all(isinstance(item, str) for item in data):
                raise ValueError(f"All items in {filename} must be strings")
            
            return data
            
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {filename}: {e}")
        except Exception as e:
            raise RuntimeError(f"Error loading {filename}: {e}")
    
    def select_random_subset(self, data: List[str], count: int = None) -> List[str]:
        """Select a random subset of data items."""
        if count is None:
            count = PuzzleConfig.AUTO_ITEMS_PER_CATEGORY
        
        # Ensure we don't try to select more items than available
        count = min(count, len(data))
        
        # Return random subset
        return random.sample(data, count)


class AutomaticPuzzleGenerator:
    """Generates puzzles automatically without human interaction."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def generate_puzzle(self, author: str = "AutoGenerator") -> Puzzle:
        """Generate a complete puzzle automatically."""
        print("🤖 Generating automatic puzzle...")
        
        # Load all data
        all_data = self.data_manager.load_all_data()
        
        # Randomly select items for each category
        actors = self.data_manager.select_random_subset(all_data['threat_actors'])
        vectors = self.data_manager.select_random_subset(all_data['attack_vectors'])
        assets = self.data_manager.select_random_subset(all_data['assets'])
        datatypes = self.data_manager.select_random_subset(all_data['datatypes'], 1)  # Only 1 data type
        
        print(f"✅ Selected {len(actors)} actors: {', '.join(actors)}")
        print(f"✅ Selected {len(vectors)} vectors: {', '.join(vectors)}")
        print(f"✅ Selected {len(assets)} assets: {', '.join(assets)}")
        print(f"✅ Selected data type: {datatypes[0]}")
        
        # Randomly select solution
        solution = PuzzleSolution(
            actor=random.choice(actors),
            vector=random.choice(vectors),
            asset=random.choice(assets),
            stolen_data=datatypes[0]
        )
        
        print(f"🎯 Solution: {solution.actor} used {solution.vector} against {solution.asset}")
        
        # Generate random clues
        clues = self._generate_random_clues(actors, vectors, assets, solution)
        
        # Create puzzle
        puzzle_number = PuzzleManager.get_next_puzzle_number()
        title = f"Web {puzzle_number} - {solution.actor} breach"
        
        return Puzzle(
            title=title,
            difficulty=Difficulty.EASY,
            author=author,
            actors=actors,
            vectors=vectors,
            assets=assets,
            stolen_data=datatypes,
            solution=solution,
            clues=clues
        )
    
    def _generate_random_clues(self, actors: List[str], vectors: List[str], 
                             assets: List[str], solution: PuzzleSolution) -> List[Clue]:
        """Generate random clues that help solve the puzzle."""
        clues = []
        
        # Strategy: Create clues that eliminate ALL other possibilities
        # We need to ensure only the solution remains as a valid option
        
        # Clue 1: Eliminate ALL other actors from using the solution vector
        other_actors = [a for a in actors if a != solution.actor]
        for actor in other_actors:
            text = f"{actor} did not use {solution.vector}."
            clues.append(Clue(text=text, type=ClueType.NEGATION))
            print(f"🔍 Generated clue {len(clues)}: {text}")
        
        # Clue 2: Eliminate ALL other vectors for the solution actor
        other_vectors = [v for v in vectors if v != solution.vector]
        for vector in other_vectors:
            text = f"{solution.actor} did not use {vector}."
            clues.append(Clue(text=text, type=ClueType.NEGATION))
            print(f"🔍 Generated clue {len(clues)}: {text}")
        
        # Clue 3: Eliminate ALL other assets for the solution vector
        other_assets = [a for a in assets if a != solution.asset]
        for asset in other_assets:
            text = f"The actor that used {solution.vector} did not access the {asset}."
            clues.append(Clue(text=text, type=ClueType.RELATIONAL))
            print(f"🔍 Generated clue {len(clues)}: {text}")
        
        return clues
    
    def _create_clue_by_type(self, clue_type: ClueType, actors: List[str], 
                           vectors: List[str], assets: List[str], 
                           solution: PuzzleSolution) -> Optional[Clue]:
        """Create a clue based on the specified type."""
        try:
            if clue_type == ClueType.NEGATION:
                # Create a negation clue about a different actor-vector combination
                other_actors = [a for a in actors if a != solution.actor]
                other_vectors = [v for v in vectors if v != solution.vector]
                
                if other_actors and other_vectors:
                    actor = random.choice(other_actors)
                    vector = random.choice(other_vectors)
                    text = f"{actor} did not use {vector}."
                    return Clue(text=text, type=clue_type)
            
            elif clue_type == ClueType.AFFIRMATIVE:
                # Create an affirmative clue about the solution vector and a different asset
                other_assets = [a for a in assets if a != solution.asset]
                
                if other_assets:
                    asset = random.choice(other_assets)
                    text = f"{solution.vector} was used against the {asset}."
                    return Clue(text=text, type=clue_type)
            
            elif clue_type == ClueType.RELATIONAL:
                # Create a relational clue about the solution vector and a different asset
                other_assets = [a for a in assets if a != solution.asset]
                
                if other_assets:
                    asset = random.choice(other_assets)
                    text = f"The actor that used {solution.vector} did not access the {asset}."
                    return Clue(text=text, type=clue_type)
            
            elif clue_type == ClueType.CONDITIONAL:
                # Create a conditional clue about the solution
                text = f"If {solution.actor} used {solution.vector}, then they accessed the {solution.asset}."
                return Clue(text=text, type=clue_type)
            
            elif clue_type == ClueType.DATA_INFERENCE:
                # Create a data inference clue about the solution
                text = f"Only attacks using {solution.vector} resulted in theft of {solution.stolen_data}."
                return Clue(text=text, type=clue_type)
            
        except Exception as e:
            print(f"Warning: Could not create clue of type {clue_type}: {e}")
        
        return None


class UserInterface:
    """Handles all user interaction and input validation."""
    
    def __init__(self, data_manager: DataManager):
        self.data_manager = data_manager
    
    def prompt_mode_selection(self) -> str:
        """Prompt user to select between manual and automatic modes."""
        print("\n🕷️ Welcome to the SpydirWebz Puzzle Creator")
        print("Select creation mode:")
        print("1) Manual Mode - Create puzzle with user interaction")
        print("2) Automatic Mode - Generate easy puzzle automatically")
        
        while True:
            try:
                choice = input("Mode (1-2): ").strip()
                if choice == "1":
                    return "manual"
                elif choice == "2":
                    return "automatic"
                else:
                    print("❌ Please enter 1 or 2.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                raise
    
    def prompt_list_selection(self, name: str, data: List[str], 
                            min_count: int = PuzzleConfig.MIN_ITEMS, 
                            max_count: int = PuzzleConfig.MAX_ITEMS) -> List[str]:
        """Prompt user to select items from a predefined list."""
        print(f"\nSelect {name} ({min_count}-{max_count} items):")
        print("Available options:")
        
        for i, item in enumerate(data, 1):
            print(f"{i:2d}) {item}")
        
        print(f"\nEnter numbers (1-{len(data)}) separated by commas:")
        
        while True:
            try:
                user_input = input(f"{name}: ").strip()
                if not user_input:
                    print(f"❌ Please select at least {min_count} items.")
                    continue
                
                # Parse selected indices
                selected_indices = []
                for part in user_input.split(','):
                    part = part.strip()
                    if not part:
                        continue
                    
                    try:
                        index = int(part)
                        if 1 <= index <= len(data):
                            selected_indices.append(index - 1)  # Convert to 0-based
                        else:
                            print(f"❌ Invalid selection: {index}. Must be between 1 and {len(data)}.")
                            break
                    except ValueError:
                        print(f"❌ Invalid input: {part}. Please enter numbers only.")
                        break
                else:
                    # All indices were valid
                    selected_items = [data[i] for i in selected_indices]
                    
                    # Remove duplicates while preserving order
                    unique_items = []
                    for item in selected_items:
                        if item not in unique_items:
                            unique_items.append(item)
                    
                    if len(unique_items) < min_count:
                        print(f"❌ Please select at least {min_count} items.")
                        continue
                    
                    if len(unique_items) > max_count:
                        print(f"❌ Please select no more than {max_count} items.")
                        continue
                    
                    print(f"✅ Selected {len(unique_items)} {name}: {', '.join(unique_items)}")
                    return unique_items
                    
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                raise
            except Exception as e:
                print(f"❌ Error processing input: {e}")
    
    def prompt_choice(self, name: str, options: List[str]) -> str:
        """Prompt user to select from a list of options."""
        if not options:
            raise ValueError("No options provided for selection")
        
        print(f"\nSelect {name}:")
        for i, option in enumerate(options, 1):
            print(f"{i}) {option}")
        
        while True:
            try:
                user_input = input(f"{name} (1-{len(options)}): ").strip()
                if not user_input:
                    print("❌ Please enter a valid choice.")
                    continue
                
                choice = int(user_input)
                if 1 <= choice <= len(options):
                    return options[choice - 1]
                else:
                    print(f"❌ Please enter a number between 1 and {len(options)}.")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                raise
    
    def prompt_clue(self, actors: List[str], vectors: List[str], 
                   assets: List[str]) -> Optional[Clue]:
        """Prompt user to create a clue."""
        print("\nAdd a clue (select type):")
        
        clue_options = PuzzleConfig.get_clue_type_options()
        for i, (name, _) in enumerate(clue_options, 1):
            print(f" {i}) {name}")
        
        while True:
            try:
                choice = input("Type (1-5): ").strip()
                if not choice:
                    print("❌ Please enter a valid choice.")
                    continue
                
                choice_num = int(choice)
                if 1 <= choice_num <= len(clue_options):
                    _, clue_type = clue_options[choice_num - 1]
                    return self._create_clue_by_type(
                        clue_type, actors, vectors, assets
                    )
                else:
                    print(f"❌ Please enter a number between 1 and {len(clue_options)}.")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                raise
    
    def _create_clue_by_type(self, clue_type: ClueType, actors: List[str], 
                           vectors: List[str], assets: List[str]) -> Clue:
        """Create a clue based on the specified type."""
        if clue_type == ClueType.NEGATION:
            actor = self.prompt_choice("Actor", actors)
            vector = self.prompt_choice("Vector", vectors)
            text = f"{actor} did not use {vector}."
            
        elif clue_type == ClueType.AFFIRMATIVE:
            vector = self.prompt_choice("Vector", vectors)
            asset = self.prompt_choice("Asset", assets)
            text = f"{vector} was used against the {asset}."
            
        elif clue_type == ClueType.RELATIONAL:
            vector = self.prompt_choice("Vector", vectors)
            asset = self.prompt_choice("Asset", assets)
            text = f"The actor that used {vector} did not access the {asset}."
            
        elif clue_type == ClueType.CONDITIONAL:
            actor = self.prompt_choice("Actor", actors)
            vector = self.prompt_choice("Vector", vectors)
            asset = self.prompt_choice("Asset", assets)
            text = f"If {actor} used {vector}, then they accessed the {asset}."
            
        elif clue_type == ClueType.DATA_INFERENCE:
            vector = self.prompt_choice("Vector", vectors)
            data = input("Enter stolen data (e.g., Source Code): ").strip()
            if not data:
                data = "Unknown Data"
            text = f"Only attacks using {vector} resulted in theft of {data}."
            
        else:
            raise ValueError(f"Unknown clue type: {clue_type}")
        
        return Clue(text=text, type=clue_type)
    
    def prompt_continue(self) -> bool:
        """Ask user if they want to continue adding clues."""
        while True:
            try:
                response = input("Add another clue? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    return True
                elif response in ['n', 'no']:
                    return False
                else:
                    print("❌ Please enter 'y' or 'n'.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                raise


class PuzzleManager:
    """Handles puzzle file operations and management."""
    
    @staticmethod
    def get_next_puzzle_number() -> int:
        """Get the next available puzzle number."""
        puzzles_dir = Path(PuzzleConfig.PUZZLES_DIR)
        puzzles_dir.mkdir(exist_ok=True)
        
        existing_files = [
            f for f in puzzles_dir.iterdir() 
            if f.is_file() and re.match(PuzzleConfig.PUZZLE_FILE_PATTERN, f.name)
        ]
        
        if not existing_files:
            return 1
        
        numbers = [
            int(re.search(PuzzleConfig.PUZZLE_FILE_PATTERN, f.name).group(1))
            for f in existing_files
        ]
        
        return max(numbers) + 1
    
    @staticmethod
    def save_puzzle(puzzle: Puzzle, puzzle_number: int) -> Path:
        """Save puzzle to file."""
        puzzles_dir = Path(PuzzleConfig.PUZZLES_DIR)
        puzzles_dir.mkdir(exist_ok=True)
        
        filename = puzzles_dir / f"web_{puzzle_number}.json"
        
        # Convert puzzle to dictionary for JSON serialization
        puzzle_dict = {
            "title": puzzle.title,
            "difficulty": puzzle.difficulty.value,
            "author": puzzle.author,
            "actors": puzzle.actors,
            "vectors": puzzle.vectors,
            "assets": puzzle.assets,
            "stolen_data": puzzle.stolen_data,
            "solution": {
                "actor": puzzle.solution.actor,
                "vector": puzzle.solution.vector,
                "asset": puzzle.solution.asset,
                "stolen_data": puzzle.solution.stolen_data
            },
            "clues": [
                {"text": clue.text, "type": clue.type.value}
                for clue in puzzle.clues
            ]
        }
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(puzzle_dict, f, indent=2, ensure_ascii=False)
        
        return filename


class PuzzleCreator:
    """Main class for creating puzzles."""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.ui = UserInterface(self.data_manager)
        self.auto_generator = AutomaticPuzzleGenerator(self.data_manager)
        self.manager = PuzzleManager()
    
    def create_puzzle(self) -> Optional[Puzzle]:
        """Create a new puzzle through user interaction or automatic generation."""
        try:
            # Prompt for mode selection
            mode = self.ui.prompt_mode_selection()
            
            if mode == "automatic":
                return self._create_automatic_puzzle()
            else:
                return self._create_manual_puzzle()
                
        except KeyboardInterrupt:
            print("\n\nPuzzle creation cancelled.")
            return None
        except Exception as e:
            print(f"\n❌ Error creating puzzle: {e}")
            return None
    
    def _create_automatic_puzzle(self) -> Puzzle:
        """Create a puzzle automatically."""
        return self.auto_generator.generate_puzzle()
    
    def _create_manual_puzzle(self) -> Optional[Puzzle]:
        """Create a puzzle through manual user interaction."""
        print("📁 Loading data sources...")
        
        # Load all data sources
        all_data = self.data_manager.load_all_data()
        print("✅ Data sources loaded successfully!")
        
        # Get basic puzzle information
        author = self._get_author()
        difficulty = self._get_difficulty()
        
        # Get puzzle elements from data sources
        actors = self.ui.prompt_list_selection("Threat Actors", all_data['threat_actors'])
        vectors = self.ui.prompt_list_selection("Attack Vectors", all_data['attack_vectors'])
        assets = self.ui.prompt_list_selection("Compromised Assets", all_data['assets'])
        data_types = self.ui.prompt_list_selection("Stolen Data", all_data['datatypes'])
        
        # Get solution
        solution = self._get_solution(actors, vectors, assets, data_types)
        
        # Get clues
        clues = self._get_clues(actors, vectors, assets)
        
        # Create puzzle
        puzzle_number = self.manager.get_next_puzzle_number()
        title = f"Web {puzzle_number} - {solution.actor} breach"
        
        return Puzzle(
            title=title,
            difficulty=difficulty,
            author=author,
            actors=actors,
            vectors=vectors,
            assets=assets,
            stolen_data=data_types,
            solution=solution,
            clues=clues
        )
    
    def _get_author(self) -> str:
        """Get puzzle author name."""
        while True:
            author = input("\nEnter your name or alias: ").strip()
            if author:
                return author
            print("❌ Please enter a valid name.")
    
    def _get_difficulty(self) -> Difficulty:
        """Get puzzle difficulty."""
        difficulty_name = self.ui.prompt_choice(
            "Difficulty", 
            [diff.value for diff in Difficulty]
        )
        return Difficulty(difficulty_name)
    
    def _get_solution(self, actors: List[str], vectors: List[str], 
                     assets: List[str], data_types: List[str]) -> PuzzleSolution:
        """Get the correct solution from user."""
        print("\nNow choose the correct solution:")
        
        actor = self.ui.prompt_choice("Actor", actors)
        vector = self.ui.prompt_choice("Vector", vectors)
        asset = self.ui.prompt_choice("Asset", assets)
        stolen_data = self.ui.prompt_choice("Stolen Data", data_types)
        
        return PuzzleSolution(
            actor=actor,
            vector=vector,
            asset=asset,
            stolen_data=stolen_data
        )
    
    def _get_clues(self, actors: List[str], vectors: List[str], 
                  assets: List[str]) -> List[Clue]:
        """Get clues from user."""
        clues = []
        
        while True:
            clue = self.ui.prompt_clue(actors, vectors, assets)
            if clue:
                clues.append(clue)
            
            if not self.ui.prompt_continue():
                break
        
        return clues
    
    def validate_and_save(self, puzzle: Puzzle) -> bool:
        """Validate puzzle and save if valid."""
        print("\n🧪 Validating puzzle...")
        
        # Convert puzzle to dictionary for validation
        puzzle_dict = {
            "title": puzzle.title,
            "difficulty": puzzle.difficulty.value,
            "author": puzzle.author,
            "actors": puzzle.actors,
            "vectors": puzzle.vectors,
            "assets": puzzle.assets,
            "stolen_data": puzzle.stolen_data,
            "solution": {
                "actor": puzzle.solution.actor,
                "vector": puzzle.solution.vector,
                "asset": puzzle.solution.asset,
                "stolen_data": puzzle.solution.stolen_data
            },
            "clues": [
                {"text": clue.text, "type": clue.type.value}
                for clue in puzzle.clues
            ]
        }
        
        result = validate_puzzle(puzzle_dict)
        
        if result['status'] == 'valid':
            print("✅ Puzzle is valid and uniquely solvable.")
            print(f"📋 {result['explanation']}")
            
            puzzle_number = self.manager.get_next_puzzle_number()
            filename = self.manager.save_puzzle(puzzle, puzzle_number)
            
            print(f"📁 Puzzle saved to {filename}")
            return True
        else:
            print(f"❌ Puzzle validation failed: {result['status']}")
            print(f"\n🔍 {result['explanation']}")
            
            # Display specific details based on the error type
            if result['status'] == 'mismatch':
                print(f"\n📊 Analysis:")
                print(f"   Logical solution: {result['analysis']['logical_solution']}")
                print(f"   Declared solution: {result['analysis']['declared_solution']}")
                print(f"   Issue: {result['analysis']['issue']}")
            
            elif result['status'] == 'ambiguous':
                print(f"\n🔍 Found {len(result['found_solutions'])} possible solutions:")
                for i, solution in enumerate(result['found_solutions'], 1):
                    print(f"   {i}. {solution}")
            
            elif result['status'] == 'invalid':
                if 'reason' in result:
                    print(f"\n🚫 Reason: {result['reason']}")
            
            # Display suggestions for fixing the puzzle
            if 'suggestions' in result:
                print(f"\n💡 Suggestions to fix the puzzle:")
                for i, suggestion in enumerate(result['suggestions'], 1):
                    print(f"   {i}. {suggestion}")
            
            return False


def main():
    """Main entry point for the puzzle creator."""
    creator = PuzzleCreator()
    
    puzzle = creator.create_puzzle()
    if puzzle:
        creator.validate_and_save(puzzle)


if __name__ == "__main__":
    main()
