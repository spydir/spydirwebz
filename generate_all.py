#!/usr/bin/env python3
"""
SpydirWebz All-in-One Generator

This script creates a new puzzle and then generates the website in one command.
Perfect for quickly creating and deploying new puzzles.
"""

import subprocess
import sys
from pathlib import Path


def run_command(command, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print(f"Error: {e.stderr}")
        return False


def main():
    """Main function to generate puzzle and website."""
    print("🕷️ SpydirWebz All-in-One Generator")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("puzzle_creator.py").exists():
        print("❌ Error: puzzle_creator.py not found!")
        print("Please run this script from the spydirwebz directory.")
        sys.exit(1)
    
    # Step 1: Generate a new puzzle
    if not run_command("python puzzle_creator.py", "Creating new puzzle"):
        print("\n❌ Puzzle creation failed. Stopping.")
        sys.exit(1)
    
    # Step 2: Generate the website
    if not run_command("python website_generator.py", "Generating website"):
        print("\n❌ Website generation failed.")
        sys.exit(1)
    
    print("\n🎉 All done! Your puzzle and website are ready.")
    print("\n📁 Files created:")
    print("   - New puzzle in puzzles/ directory")
    print("   - Updated website in website/ directory")
    print("\n🚀 Next steps:")
    print("   1. Review the generated puzzle")
    print("   2. Test the website locally by opening website/index.html")
    print("   3. Deploy to GitHub Pages or your preferred hosting service")
    print("\n💡 To deploy to GitHub Pages:")
    print("   cd website")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Add new puzzle'")
    print("   git remote add origin https://github.com/yourusername/repo.git")
    print("   git push -u origin main")


if __name__ == "__main__":
    main() 