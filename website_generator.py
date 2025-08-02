#!/usr/bin/env python3
"""
Static Website Generator for SpydirWebz Puzzles

This script converts JSON puzzle files into a static website that can be hosted
on GitHub Pages or any static hosting service. No authentication required.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
import shutil

# Set console encoding for Windows
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())


class WebsiteGenerator:
    """Generates a static website from puzzle JSON files."""
    
    def __init__(self, puzzles_dir: str = "puzzles", output_dir: str = "website"):
        self.puzzles_dir = Path(puzzles_dir)
        self.output_dir = Path(output_dir)
        self.puzzles = []
        
    def load_puzzles(self) -> None:
        """Load all puzzle files from the puzzles directory."""
        if not self.puzzles_dir.exists():
            print(f"Puzzles directory {self.puzzles_dir} not found!")
            return
            
        for puzzle_file in self.puzzles_dir.glob("web_*_draft.json"):
            try:
                with open(puzzle_file, 'r') as f:
                    puzzle_data = json.load(f)
                    puzzle_number = puzzle_file.stem.split('_')[1]  # Extract number from filename
                    puzzle_data['puzzle_number'] = int(puzzle_number)
                    self.puzzles.append(puzzle_data)
                    print(f"Loaded puzzle {puzzle_number}")
            except Exception as e:
                print(f"Error loading {puzzle_file}: {e}")
                
        self.puzzles.sort(key=lambda x: x['puzzle_number'])
        print(f"Loaded {len(self.puzzles)} puzzles")
    
    def generate_index_html(self) -> str:
        """Generate the main index.html page."""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🕷️ SpydirWebz - Cybersecurity Logic Puzzles</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header>
            <h1>🕷️ SpydirWebz</h1>
            <p class="subtitle">Cybersecurity Logic Puzzles</p>
        </header>
        
        <main>
            <section class="intro">
                <h2>Welcome to SpydirWebz</h2>
                <p>Test your cybersecurity knowledge with these logic puzzles. Each puzzle presents a scenario where you need to determine:</p>
                <ul>
                    <li><strong>WHO?</strong> - Which threat actor performed the attack</li>
                    <li><strong>HOW?</strong> - What attack vector was used</li>
                    <li><strong>WHERE?</strong> - Which asset was compromised</li>
                    <li><strong>WHY?</strong> - What data was stolen</li>
                </ul>
                <p>Use the interactive logic grid and clues to solve each puzzle!</p>
            </section>
            
            <section class="puzzle-grid">
                <h2>Available Puzzles</h2>
                <div class="puzzle-cards">
                    {self._generate_puzzle_cards()}
                </div>
            </section>
        </main>
        
        <footer>
            <p>&copy; {datetime.now().year} SpydirWebz - Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </footer>
    </div>
    
    <script src="script.js"></script>
</body>
</html>"""
    
    def _generate_puzzle_cards(self) -> str:
        """Generate HTML for puzzle cards."""
        cards = []
        for puzzle in self.puzzles:
            difficulty_class = puzzle.get('difficulty', 'medium').lower()
            cards.append(f"""
                <div class="puzzle-card {difficulty_class}">
                    <h3>Puzzle #{puzzle['puzzle_number']}</h3>
                    <div class="difficulty-badge {difficulty_class}">{puzzle.get('difficulty', 'medium').title()}</div>
                    <p class="author">by {puzzle.get('author', 'Unknown')}</p>
                    <div class="puzzle-stats">
                        <span>🎭 {len(puzzle.get('actors', []))} Actors</span>
                        <span>⚔️ {len(puzzle.get('vectors', []))} Vectors</span>
                        <span>🏢 {len(puzzle.get('assets', []))} Assets</span>
                        <span>🔍 {len(puzzle.get('clues', []))} Clues</span>
                    </div>
                    <a href="puzzle_{puzzle['puzzle_number']}.html" class="play-button">Play Puzzle</a>
                </div>
            """)
        return '\n'.join(cards)
    
    def generate_puzzle_page(self, puzzle: Dict[str, Any]) -> str:
        """Generate an individual puzzle page with Murdle-inspired design."""
        puzzle_num = puzzle['puzzle_number']
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Puzzle #{puzzle_num} - SpydirWebz</title>
    <link rel="stylesheet" href="styles.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
</head>
<body>
    <div class="container">
        <header>
            <a href="index.html" class="back-link">← Back to Puzzles</a>
            <h1>Puzzle #{puzzle_num}</h1>
            <div class="puzzle-meta">
                <span class="difficulty-badge {puzzle.get('difficulty', 'medium').lower()}">{puzzle.get('difficulty', 'medium').title()}</span>
                <span class="author">by {puzzle.get('author', 'Unknown')}</span>
            </div>
        </header>
        
        <main class="puzzle-content">
            <!-- Logic Grid Section -->
            <div class="logic-grid-section">
                <h2>Logic Grid</h2>
                <div class="logic-grid-container">
                    <!-- Murdle-style connected elbow grid -->
                    <div class="murdle-elbow-grid">
                        <!-- Top section with shared actor headers -->
                        <div class="grid-top-row">
                            <!-- Top-left: Vectors vs Actors -->
                            <div class="grid-section top-left">
                                <div class="grid-header-row">
                                    <div class="corner-cell"></div>
                                    <div class="header-cell actor-header">{self._get_element_letter(puzzle.get('actors', [])[0]) if len(puzzle.get('actors', [])) > 0 else 'A'}</div>
                                    <div class="header-cell actor-header">{self._get_element_letter(puzzle.get('actors', [])[1]) if len(puzzle.get('actors', [])) > 1 else 'B'}</div>
                                    <div class="header-cell actor-header">{self._get_element_letter(puzzle.get('actors', [])[2]) if len(puzzle.get('actors', [])) > 2 else 'C'}</div>
                                </div>
                                <div class="grid-row">
                                    <div class="header-cell vector-header">{self._get_element_letter(puzzle.get('vectors', [])[0]) if len(puzzle.get('vectors', [])) > 0 else 'X'}</div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[0]}" data-vector="{puzzle.get('vectors', [])[0]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[1]}" data-vector="{puzzle.get('vectors', [])[0]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[2]}" data-vector="{puzzle.get('vectors', [])[0]}"></div>
                                </div>
                                <div class="grid-row">
                                    <div class="header-cell vector-header">{self._get_element_letter(puzzle.get('vectors', [])[1]) if len(puzzle.get('vectors', [])) > 1 else 'Y'}</div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[0]}" data-vector="{puzzle.get('vectors', [])[1]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[1]}" data-vector="{puzzle.get('vectors', [])[1]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[2]}" data-vector="{puzzle.get('vectors', [])[1]}"></div>
                                </div>
                                <div class="grid-row">
                                    <div class="header-cell vector-header">{self._get_element_letter(puzzle.get('vectors', [])[2]) if len(puzzle.get('vectors', [])) > 2 else 'Z'}</div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[0]}" data-vector="{puzzle.get('vectors', [])[2]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[1]}" data-vector="{puzzle.get('vectors', [])[2]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[2]}" data-vector="{puzzle.get('vectors', [])[2]}"></div>
                                </div>
                            </div>
                            
                            <!-- Top-right: Assets vs Actors -->
                            <div class="grid-section top-right">
                                <div class="grid-header-row">
                                    <div class="header-cell actor-header">{self._get_element_letter(puzzle.get('actors', [])[0]) if len(puzzle.get('actors', [])) > 0 else 'A'}</div>
                                    <div class="header-cell actor-header">{self._get_element_letter(puzzle.get('actors', [])[1]) if len(puzzle.get('actors', [])) > 1 else 'B'}</div>
                                    <div class="header-cell actor-header">{self._get_element_letter(puzzle.get('actors', [])[2]) if len(puzzle.get('actors', [])) > 2 else 'C'}</div>
                                </div>
                                <div class="grid-row">
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[0]}" data-asset="{puzzle.get('assets', [])[0]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[1]}" data-asset="{puzzle.get('assets', [])[0]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[2]}" data-asset="{puzzle.get('assets', [])[0]}"></div>
                                </div>
                                <div class="grid-row">
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[0]}" data-asset="{puzzle.get('assets', [])[1]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[1]}" data-asset="{puzzle.get('assets', [])[1]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[2]}" data-asset="{puzzle.get('assets', [])[1]}"></div>
                                </div>
                                <div class="grid-row">
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[0]}" data-asset="{puzzle.get('assets', [])[2]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[1]}" data-asset="{puzzle.get('assets', [])[2]}"></div>
                                    <div class="grid-cell" data-actor="{puzzle.get('actors', [])[2]}" data-asset="{puzzle.get('assets', [])[2]}"></div>
                                </div>
                            </div>
                        </div>
                        
                        <!-- Bottom: Assets vs Vectors -->
                        <div class="grid-section bottom">
                            <div class="grid-row">
                                <div class="header-cell asset-header">{self._get_element_letter(puzzle.get('assets', [])[0]) if len(puzzle.get('assets', [])) > 0 else 'P'}</div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[0]}" data-asset="{puzzle.get('assets', [])[0]}"></div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[1]}" data-asset="{puzzle.get('assets', [])[0]}"></div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[2]}" data-asset="{puzzle.get('assets', [])[0]}"></div>
                            </div>
                            <div class="grid-row">
                                <div class="header-cell asset-header">{self._get_element_letter(puzzle.get('assets', [])[1]) if len(puzzle.get('assets', [])) > 1 else 'Q'}</div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[0]}" data-asset="{puzzle.get('assets', [])[1]}"></div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[1]}" data-asset="{puzzle.get('assets', [])[1]}"></div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[2]}" data-asset="{puzzle.get('assets', [])[1]}"></div>
                            </div>
                            <div class="grid-row">
                                <div class="header-cell asset-header">{self._get_element_letter(puzzle.get('assets', [])[2]) if len(puzzle.get('assets', [])) > 2 else 'R'}</div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[0]}" data-asset="{puzzle.get('assets', [])[2]}"></div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[1]}" data-asset="{puzzle.get('assets', [])[2]}"></div>
                                <div class="grid-cell" data-vector="{puzzle.get('vectors', [])[2]}" data-asset="{puzzle.get('assets', [])[2]}"></div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Elements Section -->
            <div class="elements-section">
                <div class="element-category">
                    <h3>WHO?</h3>
                    <div class="element-list">
                        {self._generate_element_list(puzzle.get('actors', []))}
                    </div>
                </div>
                
                <div class="element-category">
                    <h3>HOW?</h3>
                    <div class="element-list">
                        {self._generate_element_list(puzzle.get('vectors', []))}
                    </div>
                </div>
                
                <div class="element-category">
                    <h3>WHERE?</h3>
                    <div class="element-list">
                        {self._generate_element_list(puzzle.get('assets', []))}
                    </div>
                </div>
                
                <div class="element-category">
                    <h3>WHY?</h3>
                    <div class="element-list">
                        {self._generate_element_list(puzzle.get('stolen_data', []))}
                    </div>
                </div>
            </div>
            
            <!-- Clues Section -->
            <div class="clues-section">
                <h2>Clues</h2>
                <div class="clues-list">
                    {self._generate_clues_list(puzzle.get('clues', []))}
                </div>
            </div>
            
            <!-- Solution Section -->
            <div class="solution-section">
                <h2>Your Solution</h2>
                <div class="solution-form">
                    <div class="solution-row">
                        <label>WHO?</label>
                        <select id="solution-actor">
                            <option value="">Select actor...</option>
                            {self._generate_select_options(puzzle.get('actors', []))}
                        </select>
                    </div>
                    <div class="solution-row">
                        <label>HOW?</label>
                        <select id="solution-vector">
                            <option value="">Select vector...</option>
                            {self._generate_select_options(puzzle.get('vectors', []))}
                        </select>
                    </div>
                    <div class="solution-row">
                        <label>WHERE?</label>
                        <select id="solution-asset">
                            <option value="">Select asset...</option>
                            {self._generate_select_options(puzzle.get('assets', []))}
                        </select>
                    </div>
                    <div class="solution-row">
                        <label>WHY?</label>
                        <select id="solution-data">
                            <option value="">Select data...</option>
                            {self._generate_select_options(puzzle.get('stolen_data', []))}
                        </select>
                    </div>
                    <button id="check-solution" class="check-button">Check Solution</button>
                </div>
                <div id="solution-result" class="solution-result"></div>
            </div>
        </main>
        
        <footer>
            <p>&copy; {datetime.now().year} SpydirWebz</p>
        </footer>
    </div>
    
    <script>
        // Embed puzzle data for JavaScript
        const puzzleData = {json.dumps(puzzle)};
    </script>
    <script src="puzzle-script.js"></script>
</body>
</html>"""
    
    def _generate_element_list(self, elements: List[str]) -> str:
        """Generate HTML for element lists."""
        return '\n'.join([f'<div class="element">{element}</div>' for element in elements])
    
    def _generate_select_options(self, elements: List[str]) -> str:
        """Generate HTML for select options."""
        return '\n'.join([f'<option value="{element}">{element}</option>' for element in elements])
    
    def _generate_clues_list(self, clues: List[Dict[str, str]]) -> str:
        """Generate HTML for clues list."""
        clues_html = []
        for i, clue in enumerate(clues, 1):
            clue_type = clue.get('type', 'unknown').title()
            clues_html.append(f"""
                <div class="clue">
                    <div class="clue-header">
                        <span class="clue-number">#{i}</span>
                        <span class="clue-type">{clue_type}</span>
                    </div>
                    <div class="clue-text">{clue.get('text', '')}</div>
                </div>
            """)
        return '\n'.join(clues_html)
    
    def _get_element_letter(self, element: str) -> str:
        """Get the first letter of an element for grid display."""
        if not element:
            return '?'
        return element[0].upper()
    
    def generate_css(self) -> str:
        """Generate the CSS styles with Murdle-inspired design."""
        return """/* SpydirWebz Website Styles - Dark Mode Cybersecurity Theme */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    line-height: 1.6;
    color: #e2e8f0;
    background: #0f172a;
    min-height: 100vh;
}

.container {
    max-width: 1000px;
    margin: 0 auto;
    padding: 20px;
    background: #1e293b;
    min-height: 100vh;
    box-shadow: 0 2px 20px rgba(0,0,0,0.3);
    border: 1px solid #334155;
}

header {
    text-align: center;
    margin-bottom: 40px;
    padding-bottom: 20px;
    border-bottom: 2px solid #475569;
}

header h1 {
    font-size: 3rem;
    color: #f1f5f9;
    margin-bottom: 10px;
    text-shadow: 0 0 10px rgba(59, 130, 246, 0.5);
}

.subtitle {
    font-size: 1.2rem;
    color: #94a3b8;
}

.back-link {
    display: inline-block;
    margin-bottom: 20px;
    color: #60a5fa;
    text-decoration: none;
    font-weight: 600;
}

.back-link:hover {
    color: #3b82f6;
    text-decoration: underline;
}

.intro {
    background: #334155;
    padding: 30px;
    border-radius: 8px;
    margin-bottom: 40px;
    border: 1px solid #475569;
}

.intro h2 {
    color: #f1f5f9;
    margin-bottom: 20px;
    text-align: center;
    font-size: 1.8rem;
}

.intro ul {
    margin: 20px 0;
    padding-left: 20px;
}

.intro li {
    margin: 12px 0;
    color: #cbd5e1;
}

.puzzle-grid h2 {
    text-align: center;
    margin-bottom: 30px;
    color: #f1f5f9;
}

.puzzle-cards {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.puzzle-card {
    background: #334155;
    border: 2px solid #475569;
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: all 0.3s ease;
    position: relative;
}

.puzzle-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(0,0,0,0.3);
    border-color: #60a5fa;
}

.puzzle-card.easy {
    border-color: #10b981;
}

.puzzle-card.medium {
    border-color: #f59e0b;
}

.puzzle-card.impossible {
    border-color: #ef4444;
}

.puzzle-card h3 {
    color: #f1f5f9;
    margin-bottom: 10px;
}

.difficulty-badge {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 10px;
}

.difficulty-badge.easy {
    background: #c6f6d5;
    color: #22543d;
}

.difficulty-badge.medium {
    background: #fed7d7;
    color: #742a2a;
}

.difficulty-badge.impossible {
    background: #fed7d7;
    color: #742a2a;
}

.author {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-bottom: 15px;
}

.puzzle-stats {
    display: flex;
    justify-content: space-around;
    margin: 15px 0;
    font-size: 0.8rem;
    color: #94a3b8;
}

.play-button {
    display: inline-block;
    background: #3b82f6;
    color: white;
    padding: 10px 20px;
    border-radius: 5px;
    text-decoration: none;
    font-weight: 600;
    transition: background 0.3s ease;
}

.play-button:hover {
    background: #2563eb;
}

/* Puzzle Page Styles - Murdle Inspired */
.puzzle-meta {
    display: flex;
    justify-content: center;
    gap: 20px;
    margin-top: 10px;
}

.puzzle-content {
    display: flex;
    flex-direction: column;
    gap: 30px;
    margin-bottom: 40px;
}

/* Logic Grid Styles - Murdle-inspired elbow layout */
.logic-grid-section {
    background: #334155;
    padding: 20px;
    border-radius: 8px;
    border: 2px solid #475569;
}

.logic-grid-section h2 {
    text-align: center;
    margin-bottom: 20px;
    color: #f1f5f9;
    font-size: 1.5rem;
}

.logic-grid-container {
    display: flex;
    justify-content: center;
    overflow-x: auto;
}

/* Murdle-style elbow grid */
.murdle-elbow-grid {
    display: inline-block;
    background: #1e293b;
    border: 1px solid #475569;
}

/* Grid sections layout */
.grid-top-row {
    display: flex;
}

.grid-section {
    border-collapse: collapse;
}

.grid-section.top-left {
    border-right: none;
    border-bottom: none;
}

.grid-section.top-right {
    border-left: 1px solid #475569;
    border-bottom: none;
}

.grid-section.bottom {
    border-top: 1px solid #475569;
    width: 100%;
}

/* Grid rows and cells */
.grid-header-row, .grid-row {
    display: flex;
}

.corner-cell {
    background: #475569;
    width: 80px;
    height: 30px;
    border: 1px solid #64748b;
}

/* Header cells */
.header-cell {
    color: white;
    font-weight: 600;
    font-size: 0.75rem;
    padding: 8px 5px;
    text-align: center;
    border: 1px solid #475569;
    width: 80px;
    height: 30px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    display: flex;
    align-items: center;
    justify-content: center;
}

.actor-header {
    background: #475569;
}

.vector-header {
    background: #64748b;
}

.asset-header {
    background: #64748b;
}

/* Grid cells */
.grid-cell {
    width: 80px;
    height: 45px;
    border: 1px solid #64748b;
    cursor: pointer;
    transition: background-color 0.2s;
    position: relative;
    background: #1e293b;
    display: flex;
    align-items: center;
    justify-content: center;
}

.grid-cell:hover {
    background: #334155;
}

.grid-cell.marked {
    background: #10b981;
    color: white;
}

.grid-cell.eliminated {
    background: #ef4444;
    color: white;
}

.grid-cell.marked::after {
    content: "✓";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.2rem;
    font-weight: bold;
}

.grid-cell.eliminated::after {
    content: "✗";
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    font-size: 1.2rem;
    font-weight: bold;
}

/* Elements Section */
.elements-section {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
}

.element-category {
    background: #334155;
    padding: 15px;
    border-radius: 8px;
    border: 1px solid #475569;
}

.element-category h3 {
    color: #f1f5f9;
    margin-bottom: 15px;
    text-align: center;
    font-size: 1.2rem;
    font-weight: 600;
}

.element-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.element {
    background: #1e293b;
    padding: 8px 12px;
    border-radius: 4px;
    border: 1px solid #475569;
    font-size: 0.85rem;
    text-align: center;
    color: #e2e8f0;
}

.clues-section {
    background: #334155;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #475569;
}

.clues-section h2 {
    color: #f1f5f9;
    margin-bottom: 20px;
    text-align: center;
    font-size: 1.5rem;
}

.clues-list {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.clue {
    background: #1e293b;
    padding: 15px;
    border-radius: 6px;
    border-left: 4px solid #3b82f6;
    border: 1px solid #475569;
}

.clue-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 8px;
}

.clue-number {
    background: #3b82f6;
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: 600;
}

.clue-type {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
}

.clue-text {
    color: #e2e8f0;
    line-height: 1.4;
    font-size: 0.9rem;
}

.solution-section {
    background: #334155;
    padding: 20px;
    border-radius: 8px;
    border: 1px solid #475569;
}

.solution-section h2 {
    color: #f1f5f9;
    margin-bottom: 20px;
    text-align: center;
    font-size: 1.5rem;
}

.solution-form {
    max-width: 400px;
    margin: 0 auto;
}

.solution-row {
    display: flex;
    flex-direction: column;
    margin-bottom: 15px;
}

.solution-row label {
    font-weight: 600;
    margin-bottom: 5px;
    color: #e2e8f0;
    font-size: 0.9rem;
}

.solution-row select {
    padding: 10px;
    border: 2px solid #475569;
    border-radius: 4px;
    font-size: 1rem;
    background: #1e293b;
    color: #e2e8f0;
}

.solution-row select:focus {
    outline: none;
    border-color: #3b82f6;
    box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.2);
}

.check-button {
    width: 100%;
    background: #3b82f6;
    color: white;
    padding: 12px;
    border: none;
    border-radius: 4px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.3s ease;
}

.check-button:hover {
    background: #2563eb;
}

.solution-result {
    margin-top: 20px;
    padding: 15px;
    border-radius: 5px;
    text-align: center;
    font-weight: 600;
}

.solution-result.correct {
    background: #c6f6d5;
    color: #22543d;
    border: 1px solid #9ae6b4;
}

.solution-result.incorrect {
    background: #fed7d7;
    color: #742a2a;
    border: 1px solid #feb2b2;
}

footer {
    text-align: center;
    padding: 20px 0;
    color: #94a3b8;
    border-top: 2px solid #475569;
}

/* Responsive Design */
@media (max-width: 768px) {
    .elements-section {
        grid-template-columns: repeat(2, 1fr);
    }
    
    .logic-grid-container {
        transform: scale(0.7);
        transform-origin: top center;
    }
    
    .puzzle-cards {
        grid-template-columns: 1fr;
    }
    
    header h1 {
        font-size: 2rem;
    }
    
    .sub-grid-header {
        grid-template-columns: 50px repeat(3, 70px);
    }
    
    .sub-grid-row {
        grid-template-columns: 50px repeat(3, 70px);
    }
    
    .sub-grid-category, .sub-grid-label {
        font-size: 0.7rem;
    }
    
    .grid-cell {
        height: 35px;
    }
}"""
    
    def generate_js(self) -> str:
        """Generate the main JavaScript file."""
        return """// SpydirWebz Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    console.log('🕷️ SpydirWebz website loaded');
    
    // Add any main page interactions here
    const puzzleCards = document.querySelectorAll('.puzzle-card');
    puzzleCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (!e.target.classList.contains('play-button')) {
                const link = this.querySelector('.play-button');
                if (link) {
                    window.location.href = link.href;
                }
            }
        });
    });
});"""
    
    def generate_puzzle_js(self) -> str:
        """Generate the puzzle page JavaScript with interactive logic grid."""
        return """// SpydirWebz Puzzle JavaScript - Murdle Inspired
document.addEventListener('DOMContentLoaded', function() {
    const checkButton = document.getElementById('check-solution');
    const resultDiv = document.getElementById('solution-result');
    const gridCells = document.querySelectorAll('.grid-cell');
    
    if (checkButton && resultDiv) {
        checkButton.addEventListener('click', checkSolution);
    }
    
    // Interactive Logic Grid
    gridCells.forEach(cell => {
        cell.addEventListener('click', function() {
            const currentState = this.className;
            
            // Cycle through states: empty -> marked -> eliminated -> empty
            if (currentState.includes('marked')) {
                this.className = 'grid-cell eliminated';
            } else if (currentState.includes('eliminated')) {
                this.className = 'grid-cell';
            } else {
                this.className = 'grid-cell marked';
            }
        });
        
        // Right click to eliminate
        cell.addEventListener('contextmenu', function(e) {
            e.preventDefault();
            if (!this.className.includes('marked')) {
                this.className = 'grid-cell eliminated';
            }
        });
    });
    
    function checkSolution() {
        const actor = document.getElementById('solution-actor').value;
        const vector = document.getElementById('solution-vector').value;
        const asset = document.getElementById('solution-asset').value;
        const data = document.getElementById('solution-data').value;
        
        if (!actor || !vector || !asset || !data) {
            showResult('Please select all solution components.', 'incorrect');
            return;
        }
        
        // Get the correct solution from embedded puzzle data
        const solution = puzzleData.solution;
        const isCorrect = 
            actor === solution.actor &&
            vector === solution.vector &&
            asset === solution.asset &&
            data === solution.stolen_data;
        
        if (isCorrect) {
            showResult('🎉 Correct! You solved the puzzle!', 'correct');
        } else {
            const correctAnswer = `${solution.actor} used ${solution.vector} against ${solution.asset} to steal ${solution.stolen_data}`;
            showResult(`❌ Incorrect. The correct answer is: ${correctAnswer}`, 'incorrect');
        }
    }
    
    function showResult(message, type) {
        resultDiv.textContent = message;
        resultDiv.className = `solution-result ${type}`;
        resultDiv.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && checkButton) {
            checkSolution();
        }
    });
});"""
    
    def generate_website(self) -> None:
        """Generate the complete website."""
        print("Generating SpydirWebz website...")
        
        # Load puzzles
        self.load_puzzles()
        
        if not self.puzzles:
            print("No puzzles found to generate website!")
            return
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Generate main index page
        index_html = self.generate_index_html()
        with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
            f.write(index_html)
        print("Generated index.html")
        
        # Generate individual puzzle pages
        for puzzle in self.puzzles:
            puzzle_html = self.generate_puzzle_page(puzzle)
            puzzle_filename = f"puzzle_{puzzle['puzzle_number']}.html"
            with open(self.output_dir / puzzle_filename, 'w', encoding='utf-8') as f:
                f.write(puzzle_html)
            print(f"Generated {puzzle_filename}")
        
        # Generate CSS
        css_content = self.generate_css()
        with open(self.output_dir / "styles.css", 'w', encoding='utf-8') as f:
            f.write(css_content)
        print("Generated styles.css")
        
        # Generate JavaScript files
        js_content = self.generate_js()
        with open(self.output_dir / "script.js", 'w', encoding='utf-8') as f:
            f.write(js_content)
        print("Generated script.js")
        
        puzzle_js_content = self.generate_puzzle_js()
        with open(self.output_dir / "puzzle-script.js", 'w', encoding='utf-8') as f:
            f.write(puzzle_js_content)
        print("Generated puzzle-script.js")
        
        # Generate README for the website
        readme_content = self.generate_website_readme()
        with open(self.output_dir / "README.md", 'w', encoding='utf-8') as f:
            f.write(readme_content)
        print("Generated README.md")
        
        print(f"\nWebsite generated successfully in {self.output_dir}/")
        print("Files created:")
        print(f"   - index.html (main page)")
        print(f"   - puzzle_*.html ({len(self.puzzles)} puzzle pages)")
        print(f"   - styles.css (styling)")
        print(f"   - script.js (main JavaScript)")
        print(f"   - puzzle-script.js (puzzle logic)")
        print(f"   - README.md (deployment guide)")
        print("\nTo deploy:")
        print("   1. Push the website/ directory to GitHub")
        print("   2. Enable GitHub Pages in repository settings")
        print("   3. Your site will be available at: https://yourusername.github.io/reponame/")
    
    def generate_website_readme(self) -> str:
        """Generate a README for the website directory."""
        return f"""# SpydirWebz Website

This is a static website generated from SpydirWebz puzzle files.

## 🚀 Deployment

### GitHub Pages (Recommended)

1. **Create a new repository** on GitHub
2. **Push this website directory** to the repository
3. **Enable GitHub Pages**:
   - Go to repository Settings
   - Scroll to "Pages" section
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

Your website will be available at: `https://yourusername.github.io/reponame/`

### Other Static Hosting

This website can be deployed to any static hosting service:
- Netlify
- Vercel
- AWS S3
- Firebase Hosting
- Any web server

## 📁 Files

- `index.html` - Main page with puzzle list
- `puzzle_*.html` - Individual puzzle pages
- `styles.css` - Website styling
- `script.js` - Main JavaScript functionality
- `puzzle-script.js` - Puzzle interaction logic

## 🔄 Updating

To update the website with new puzzles:

1. Run the website generator again:
   ```bash
   python website_generator.py
   ```
2. Push the updated files to your repository
3. GitHub Pages will automatically rebuild

## 🔒 Security

This is a static website with:
- ✅ No server-side code
- ✅ No authentication required
- ✅ No database
- ✅ No user data collection
- ✅ Client-side puzzle validation only

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""


def main():
    """Main function to generate the website."""
    generator = WebsiteGenerator()
    generator.generate_website()


if __name__ == "__main__":
    main() 