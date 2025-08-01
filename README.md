# 🕷️ SpydirWebz Puzzle Creator & Validator

A comprehensive tool for creating and validating cybersecurity logic puzzles. This project provides both a puzzle creation interface and an automated validation system using Z3 theorem prover to ensure puzzles are logically consistent and uniquely solvable.

## ✨ Features

- **Interactive Puzzle Creation**: User-friendly CLI interface for creating cybersecurity puzzles
- **Automated Validation**: Z3-based logic validation ensuring puzzles are:
  - Logically consistent
  - Uniquely solvable (exactly one Actor/Vector/Asset triplet)
  - Permits inference of stolen data via clues
- **Multiple Clue Types**: Support for various clue types:
  - Negation clues
  - Affirmative clues
  - Relational clues
  - Conditional clues
  - Data inference clues
- **Structured Data**: Clean, type-safe data structures using Python dataclasses
- **Error Handling**: Robust error handling and user input validation
- **File Management**: Automatic puzzle numbering and JSON file generation

## 🏗️ Architecture

The project is organized into several key components:

### Core Classes

- **`PuzzleCreator`**: Main orchestration class for puzzle creation
- **`UserInterface`**: Handles all user interaction and input validation
- **`PuzzleManager`**: Manages file operations and puzzle storage
- **`PuzzleConfig`**: Centralized configuration management

### Data Structures

- **`Puzzle`**: Complete puzzle representation
- **`Clue`**: Individual clue with type and text
- **`PuzzleSolution`**: Solution components (actor, vector, asset, stolen data)
- **`Difficulty`**: Enum for puzzle difficulty levels
- **`ClueType`**: Enum for different clue types

## 🔧 Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-repo/spydirwebz.git
   cd spydirwebz
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify installation**:
   ```bash
   python puzzle_creator.py --help
   ```

## 🚀 Usage

### Creating a New Puzzle

Run the puzzle creator:

```bash
python puzzle_creator.py
```

The tool will guide you through:

1. **Basic Information**:
   - Author name/alias
   - Puzzle difficulty (easy/medium/impossible)

2. **Puzzle Elements** (3-6 items each):
   - Threat Actors (e.g., "GhostShell", "ZeroShadow")
   - Attack Vectors (e.g., "SQL Injection", "Phishing")
   - Compromised Assets (e.g., "Email Server", "HR Portal")
   - Stolen Data (e.g., "Source Code", "Customer Data")

3. **Solution Definition**:
   - Select the correct actor, vector, asset, and stolen data

4. **Clue Creation**:
   - Add multiple clues using different types
   - Each clue type has specific logic patterns

5. **Validation & Saving**:
   - Automatic validation using Z3 theorem prover
   - Save to JSON file if valid

### Example Session

```
🕷️ Welcome to the SpydirWebz Puzzle Creator

Enter your name or alias: CyberPuzzleMaster
Select Difficulty:
1) easy
2) medium
3) impossible
Difficulty (1-3): 2

Enter Threat Actors (3-6 items, comma-separated):
Threat Actors: GhostShell, ZeroShadow, DarkPhantom, CyberNinja

Enter Attack Vectors (3-6 items, comma-separated):
Attack Vectors: SQL Injection, Phishing, RDP Exploit, XSS

Enter Compromised Assets (3-6 items, comma-separated):
Compromised Assets: Email Server, HR Portal, Finance Database, Web Server

Enter Stolen Data (3-6 items, comma-separated):
Stolen Data: Source Code, Customer Data, Employee Records, Financial Data

Now choose the correct solution:
Select Actor:
1) GhostShell
2) ZeroShadow
3) DarkPhantom
4) CyberNinja
Actor (1-4): 2

Select Vector:
1) SQL Injection
2) Phishing
3) RDP Exploit
4) XSS
Vector (1-4): 3

Select Asset:
1) Email Server
2) HR Portal
3) Finance Database
4) Web Server
Asset (1-4): 3

Select Stolen Data:
1) Source Code
2) Customer Data
3) Employee Records
4) Financial Data
Stolen Data (1-4): 4

Add a clue (select type):
 1) Negation
 2) Affirmative
 3) Relational
 4) Conditional
 5) Data Inference
Type (1-5): 1

Select Actor:
1) GhostShell
2) ZeroShadow
3) DarkPhantom
4) CyberNinja
Actor (1-4): 1

Select Vector:
1) SQL Injection
2) Phishing
3) RDP Exploit
4) XSS
Vector (1-4): 1

Add another clue? (y/n): n

🧪 Validating puzzle...
✅ Puzzle is valid and uniquely solvable.
📁 Puzzle saved to puzzles/web_1.json
```

## 📁 File Structure

```
spydirwebz/
├── puzzle_creator.py      # Main puzzle creation tool
├── logic_validator.py     # Z3-based validation logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── tests/               # Test files
│   ├── tests_easy.py
│   └── tests_impossible.py
└── puzzles/             # Generated puzzle files
    └── web_*.json       # Puzzle JSON files
```

## 🧪 Validation Logic

The validation system uses Z3 theorem prover to:

1. **Create Boolean variables** for each possible (Actor, Vector, Asset) triplet
2. **Enforce constraints**:
   - Exactly one triplet must be true
   - No two triplets can be true simultaneously
3. **Encode clues** as logical constraints
4. **Solve the system** to check:
   - Satisfiability (at least one solution exists)
   - Uniqueness (exactly one solution exists)
   - Solution correctness (matches declared solution)

### Clue Type Logic

- **Negation**: `Actor A did not use Vector V`
- **Affirmative**: `Vector V was used against Asset S`
- **Relational**: `Actor using Vector V did not access Asset S`
- **Conditional**: `If Actor A used Vector V, then they accessed Asset S`
- **Data Inference**: `Only attacks using Vector V resulted in theft of Data D`

## 🧪 Testing

Run the test suite:

```bash
python -m pytest tests/
```

Or run individual test files:

```bash
python tests/tests_easy.py
python tests/tests_impossible.py
```

## 🔧 Configuration

Key configuration options in `PuzzleConfig`:

- `MIN_ITEMS`: Minimum items per category (default: 3)
- `MAX_ITEMS`: Maximum items per category (default: 6)
- `PUZZLES_DIR`: Directory for storing puzzles (default: "puzzles")
- `PUZZLE_FILE_PATTERN`: File naming pattern (default: "web_*.json")

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run linting
python -m flake8 puzzle_creator.py logic_validator.py

# Run tests
python -m pytest tests/
```

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Z3 Theorem Prover**: Microsoft Research's Z3 solver for logic validation
- **Python Community**: For excellent tooling and libraries
- **Cybersecurity Community**: For inspiration and puzzle concepts

## 📞 Support

For questions, issues, or contributions:

- Open an issue on GitHub
- Contact the maintainers
- Check the documentation

---

**Happy Puzzle Creating! 🕷️🧩**
