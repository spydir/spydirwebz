# 🕷️ SpydirWebz Puzzle Creator & Validator

A comprehensive tool for automatically generating and validating cybersecurity logic puzzles. This project provides an automated puzzle generation system using Z3 theorem prover to ensure puzzles are logically consistent and uniquely solvable.

## ✨ Features

- **Automatic Puzzle Generation**: Generates complete cybersecurity puzzles without user interaction
- **Automated Validation**: Z3-based logic validation ensuring puzzles are:
  - Logically consistent
  - Uniquely solvable (exactly one Actor/Vector/Asset triplet)
  - Permits inference of stolen data via clues
- **Multiple Clue Types**: Automatically generates two clues of each type:
  - Negation clues
  - Affirmative clues
  - Relational clues
  - Conditional clues
  - Data inference clues
- **Structured Data**: Clean, type-safe data structures using Python dataclasses
- **Error Handling**: Robust error handling and validation
- **File Management**: Automatic puzzle numbering and JSON file generation
- **Data Integrity**: Automatic duplicate detection and removal from data sources
- **Uniqueness Validation**: Ensures all puzzle elements (actors, vectors, assets, data) are unique

## 🏗️ Architecture

The project is organized into several key components:

### Core Classes

- **`PuzzleCreator`**: Main orchestration class for puzzle creation
- **`AutomaticPuzzleGenerator`**: Generates puzzles automatically
- **`PuzzleManager`**: Manages file operations and puzzle storage
- **`PuzzleConfig`**: Centralized configuration management
- **`DataManager`**: Handles data loading and caching

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

The tool will automatically:

1. **Prompt for Basic Information**:
   - Author name/alias
   - Puzzle difficulty (easy/medium/impossible)

2. **Generate Puzzle Elements** (3 items each):
   - Threat Actors (e.g., "GhostShell", "ZeroShadow")
   - Attack Vectors (e.g., "SQL Injection", "Phishing")
   - Compromised Assets (e.g., "Email Server", "HR Portal")
   - Stolen Data (e.g., "Source Code", "Customer Data")

3. **Create Solution**:
   - Randomly select the correct actor, vector, asset, and stolen data

4. **Generate Clues**:
   - Automatically create 10 clues (2 of each type)
   - Ensure logical consistency and unique solution

5. **Validation & Saving**:
   - Automatic validation using Z3 theorem prover
   - Save to JSON file if valid

### Generating a Website

Create a static website from your puzzles:

```bash
python website_generator.py
```

This generates a complete static website in the `website/` directory that can be deployed to:
- **GitHub Pages** (recommended - free and secure)
- **Netlify** 
- **Vercel**
- **Any static hosting service**

The website includes:
- Interactive puzzle interface
- No authentication required
- Responsive design
- Client-side solution validation

## 🌐 Website Deployment

### Quick GitHub Pages Deployment

1. **Generate the website**:
   ```bash
   python website_generator.py
   ```

2. **Create a new GitHub repository** for the website

3. **Push the website files**:
   ```bash
   cd website
   git init
   git add .
   git commit -m "Initial website deployment"
   git remote add origin https://github.com/yourusername/spydirwebz-website.git
   git push -u origin main
   ```

4. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

Your website will be available at: `https://yourusername.github.io/spydirwebz-website/`

### Updating the Website

When you create new puzzles, regenerate the website:

```bash
python website_generator.py
git add .
git commit -m "Add new puzzles"
git push
```

GitHub Pages will automatically rebuild with the new puzzles.

### Example Session

```
🕷️ Welcome to the SpydirWebz Puzzle Creator
🤖 Automatic Mode - Generating puzzle...

Enter your name or alias: CyberPuzzleMaster
Select Difficulty:
1) easy
2) medium
3) impossible
Difficulty (1-3): 2

🤖 Generating automatic puzzle...
✅ Selected 3 actors: GhostShell, ZeroShadow, DarkPhantom
✅ Selected 3 vectors: SQL Injection, Phishing, RDP Exploit
✅ Selected 3 assets: Email Server, HR Portal, Finance Database
✅ Selected data type: Source Code
✅ All puzzle elements are unique
🎯 Solution: GhostShell used SQL Injection against Email Server

🔍 Generated clue 1: ZeroShadow did not use SQL Injection.
🔍 Generated clue 2: DarkPhantom did not use Phishing.
🔍 Generated clue 3: SQL Injection was used against the HR Portal.
🔍 Generated clue 4: RDP Exploit was used against the Finance Database.
🔍 Generated clue 5: The actor that used SQL Injection did not access the Finance Database.
🔍 Generated clue 6: The actor that used Phishing did not access the Email Server.
🔍 Generated clue 7: If ZeroShadow used SQL Injection, then they accessed the HR Portal.
🔍 Generated clue 8: If DarkPhantom used RDP Exploit, then they accessed the Finance Database.
🔍 Generated clue 9: Only attacks using SQL Injection resulted in theft of Source Code.
🔍 Generated clue 10: Only attacks using Phishing resulted in theft of Source Code.

🧪 Validating puzzle...
✅ Puzzle is valid and uniquely solvable.
📁 Puzzle saved to puzzles/web_1_draft.json
📁 Validation results saved to puzzles/web_1_review.json
```

## 📁 File Structure

```
spydirwebz/
├── puzzle_creator.py      # Main puzzle creation tool
├── logic_validator.py     # Z3-based validation logic
├── website_generator.py   # Static website generator
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── .gitignore           # Git ignore rules
├── tests/               # Test files
│   ├── tests_easy.py
│   └── tests_impossible.py
├── data/                # Data source files
│   ├── data_threat_actors.json
│   ├── data_attack_vectors.json
│   ├── data_assets.json
│   └── data_datatypes.json
├── puzzles/             # Generated puzzle files
│   ├── web_1_draft.json       # Puzzle JSON files
│   ├── web_1_review.json      # Validation results
│   ├── web_2_draft.json
│   ├── web_2_review.json
│   └── ...
└── website/             # Generated static website
    ├── index.html            # Main page
    ├── puzzle_*.html         # Individual puzzle pages
    ├── styles.css            # Website styling
    ├── script.js             # Main JavaScript
    ├── puzzle-script.js      # Puzzle interaction logic
    └── README.md             # Deployment guide
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

### Validation Output

The system now provides comprehensive validation feedback:

- **Human-readable explanations** of validation issues
- **Specific suggestions** for fixing problems
- **Detailed analysis** of logical vs declared solutions
- **Automatic file saving** of both puzzles and validation results

### File Output Structure

For each puzzle created, two files are generated:

1. **`web_N.json`** - The puzzle definition
2. **`validation_web_N.json`** - Validation results with metadata

Example validation output:
```json
{
  "puzzle_number": 1,
  "validation_timestamp": "2024-01-15T10:30:45.123456",
  "validation_result": {
    "status": "valid",
    "explanation": "The puzzle is logically consistent and has exactly one solution...",
    "solution": {...},
    "validation_summary": {...}
  },
  "summary": {
    "status": "valid",
    "valid": true,
    "has_explanation": true,
    "has_suggestions": false
  }
}
```

### Clue Type Logic

- **Negation**: `Actor A did not use Vector V`
- **Affirmative**: `Vector V was used against Asset S`
- **Relational**: `Actor using Vector V did not access Asset S`
- **Conditional**: `If Actor A used Vector V, then they accessed Asset S`
- **Data Inference**: `Only attacks using Vector V resulted in theft of Data D`

## 🔒 Data Integrity

The system ensures data integrity through multiple validation layers:

### Uniqueness Enforcement
- **Data Sources**: Automatically removes duplicates from JSON data files
- **Automatic Generation**: Ensures unique items in automatically generated puzzles
- **Validation**: Runtime checks verify all puzzle elements are unique

### Duplicate Detection
- **Warning Messages**: Alerts users when duplicates are found and removed
- **Error Prevention**: Stops puzzle creation if duplicates are detected
- **Data Cleaning**: Automatically cleans data sources on load

### Example Validation
```
⚠️  Warning: Removed 2 duplicate entries from data_threat_actors.json
✅ All puzzle elements are unique
```

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
- `PUZZLE_FILE_PATTERN`: File naming pattern (default: "web_*_draft.json")
- `AUTO_ITEMS_PER_CATEGORY`: Items per category in automatic mode (default: 3)
- `AUTO_CLUES_COUNT`: Number of clues in automatic mode (default: 10)

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