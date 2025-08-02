#!/usr/bin/env python3
"""
SpydirWebz Deployment Script

This script generates the website and prepares it for deployment to GitHub Pages.
It creates a deployment-ready directory that can be easily pushed to GitHub.
"""

import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime


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
    """Main deployment function."""
    print("🚀 SpydirWebz Deployment Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("puzzle_creator.py").exists():
        print("❌ Error: puzzle_creator.py not found!")
        print("Please run this script from the spydirwebz directory.")
        sys.exit(1)
    
    # Step 1: Generate the website
    if not run_command("python website_generator.py", "Generating website"):
        print("\n❌ Website generation failed. Stopping.")
        sys.exit(1)
    
    # Step 2: Create deployment directory
    deploy_dir = Path("deploy")
    if deploy_dir.exists():
        shutil.rmtree(deploy_dir)
    deploy_dir.mkdir()
    
    # Step 3: Copy website files to deployment directory
    website_dir = Path("website")
    if website_dir.exists():
        for item in website_dir.iterdir():
            if item.is_file():
                shutil.copy2(item, deploy_dir)
            elif item.is_dir():
                shutil.copytree(item, deploy_dir / item.name)
        print("✅ Copied website files to deploy/ directory")
    else:
        print("❌ Website directory not found!")
        sys.exit(1)
    
    # Step 4: Create deployment README
    deploy_readme = f"""# SpydirWebz - Deploy to GitHub Pages

This directory contains the generated website ready for deployment.

## 🚀 Quick Deployment

1. **Create a new GitHub repository** (e.g., `spydirwebz-website`)

2. **Push this directory to GitHub**:
   ```bash
   git init
   git add .
   git commit -m "Initial SpydirWebz website deployment"
   git remote add origin https://github.com/YOUR_USERNAME/spydirwebz-website.git
   git push -u origin main
   ```

3. **Enable GitHub Pages**:
   - Go to repository Settings → Pages
   - Select "Deploy from a branch"
   - Choose "main" branch and "/ (root)" folder
   - Click "Save"

Your website will be available at: `https://YOUR_USERNAME.github.io/spydirwebz-website/`

## 🔄 Updating

To update the website with new puzzles:
1. Run `python deploy.py` in the main spydirwebz directory
2. Push the updated deploy/ directory to your repository

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    with open(deploy_dir / "README.md", 'w', encoding='utf-8') as f:
        f.write(deploy_readme)
    
    print("✅ Created deployment README")
    
    print(f"\n🎉 Deployment package ready in {deploy_dir}/")
    print("\n📁 Files ready for deployment:")
    for item in deploy_dir.iterdir():
        if item.is_file():
            print(f"   📄 {item.name}")
        elif item.is_dir():
            print(f"   📁 {item.name}/")
    
    print("\n🚀 Next steps:")
    print("   1. Create a new GitHub repository")
    print("   2. Copy the contents of deploy/ to your repository")
    print("   3. Enable GitHub Pages in repository settings")
    print("   4. Your site will be live!")
    
    print("\n💡 Quick commands:")
    print("   cd deploy")
    print("   git init")
    print("   git add .")
    print("   git commit -m 'Initial SpydirWebz website'")
    print("   git remote add origin https://github.com/YOUR_USERNAME/repo.git")
    print("   git push -u origin main")


if __name__ == "__main__":
    main() 