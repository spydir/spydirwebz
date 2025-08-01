"""
SpydirWebz Puzzle Creator

A tool for creating cybersecurity logic puzzles with automated validation.
"""

import json
import os
import re
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
    PUZZLE_FILE_PATTERN = r'web_(\d+)\.json'
    
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


class UserInterface:
    """Handles all user interaction and input validation."""
    
    @staticmethod
    def prompt_list(name: str, min_count: int = PuzzleConfig.MIN_ITEMS, 
                   max_count: int = PuzzleConfig.MAX_ITEMS) -> List[str]:
        """Prompt user for a list of items with validation."""
        print(f"Enter {name} ({min_count}-{max_count} items, comma-separated):")
        
        while True:
            try:
                user_input = input(f"{name}: ").strip()
                if not user_input:
                    print(f"❌ Please enter at least {min_count} items.")
                    continue
                
                items = [item.strip() for item in user_input.split(",") if item.strip()]
                
                if len(items) < min_count:
                    print(f"❌ Please enter at least {min_count} items.")
                    continue
                    
                if len(items) > max_count:
                    print(f"❌ Please enter no more than {max_count} items.")
                    continue
                
                return items
                
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                raise
            except Exception as e:
                print(f"❌ Error processing input: {e}")
    
    @staticmethod
    def prompt_choice(name: str, options: List[str]) -> str:
        """Prompt user to select from a list of options."""
        if not options:
            raise ValueError("No options provided for selection")
        
        print(f"Select {name}:")
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
    
    @staticmethod
    def prompt_clue(actors: List[str], vectors: List[str], 
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
                    return UserInterface._create_clue_by_type(
                        clue_type, actors, vectors, assets
                    )
                else:
                    print(f"❌ Please enter a number between 1 and {len(clue_options)}.")
                    
            except ValueError:
                print("❌ Please enter a valid number.")
            except KeyboardInterrupt:
                print("\n\nOperation cancelled by user.")
                raise
    
    @staticmethod
    def _create_clue_by_type(clue_type: ClueType, actors: List[str], 
                           vectors: List[str], assets: List[str]) -> Clue:
        """Create a clue based on the specified type."""
        if clue_type == ClueType.NEGATION:
            actor = UserInterface.prompt_choice("Actor", actors)
            vector = UserInterface.prompt_choice("Vector", vectors)
            text = f"{actor} did not use {vector}."
            
        elif clue_type == ClueType.AFFIRMATIVE:
            vector = UserInterface.prompt_choice("Vector", vectors)
            asset = UserInterface.prompt_choice("Asset", assets)
            text = f"{vector} was used against the {asset}."
            
        elif clue_type == ClueType.RELATIONAL:
            vector = UserInterface.prompt_choice("Vector", vectors)
            asset = UserInterface.prompt_choice("Asset", assets)
            text = f"The actor that used {vector} did not access the {asset}."
            
        elif clue_type == ClueType.CONDITIONAL:
            actor = UserInterface.prompt_choice("Actor", actors)
            vector = UserInterface.prompt_choice("Vector", vectors)
            asset = UserInterface.prompt_choice("Asset", assets)
            text = f"If {actor} used {vector}, then they accessed the {asset}."
            
        elif clue_type == ClueType.DATA_INFERENCE:
            vector = UserInterface.prompt_choice("Vector", vectors)
            data = input("Enter stolen data (e.g., Source Code): ").strip()
            if not data:
                data = "Unknown Data"
            text = f"Only attacks using {vector} resulted in theft of {data}."
            
        else:
            raise ValueError(f"Unknown clue type: {clue_type}")
        
        return Clue(text=text, type=clue_type)
    
    @staticmethod
    def prompt_continue() -> bool:
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
        self.ui = UserInterface()
        self.manager = PuzzleManager()
    
    def create_puzzle(self) -> Optional[Puzzle]:
        """Create a new puzzle through user interaction."""
        try:
            print("\n🕷️ Welcome to the SpydirWebz Puzzle Creator")
            
            # Get basic puzzle information
            author = self._get_author()
            difficulty = self._get_difficulty()
            
            # Get puzzle elements
            actors = self.ui.prompt_list("Threat Actors")
            vectors = self.ui.prompt_list("Attack Vectors")
            assets = self.ui.prompt_list("Compromised Assets")
            data_types = self.ui.prompt_list("Stolen Data")
            
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
            
        except KeyboardInterrupt:
            print("\n\nPuzzle creation cancelled.")
            return None
        except Exception as e:
            print(f"\n❌ Error creating puzzle: {e}")
            return None
    
    def _get_author(self) -> str:
        """Get puzzle author name."""
        while True:
            author = input("Enter your name or alias: ").strip()
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
            
            puzzle_number = self.manager.get_next_puzzle_number()
            filename = self.manager.save_puzzle(puzzle, puzzle_number)
            
            print(f"📁 Puzzle saved to {filename}")
            return True
        else:
            print(f"❌ Puzzle validation failed: {result['status']}")
            print(result)
            return False


def main():
    """Main entry point for the puzzle creator."""
    creator = PuzzleCreator()
    
    puzzle = creator.create_puzzle()
    if puzzle:
        creator.validate_and_save(puzzle)


if __name__ == "__main__":
    main()
