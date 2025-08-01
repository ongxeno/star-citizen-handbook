#!/usr/bin/env python3
"""
Setup script for the AI Blog Generator

This script helps set up the blog generator environment.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False

def setup_env_file():
    """Create .env file from template if it doesn't exist"""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if not env_example.exists():
        print("❌ .env.example file not found")
        return False
    
    # Copy example to .env
    with open(env_example, 'r') as src, open(env_file, 'w') as dst:
        dst.write(src.read())
    
    print("✅ Created .env file from template")
    print("⚠️  Please edit .env and add your GEMINI_API_KEY")
    return True

def check_api_key():
    """Check if API key is configured"""
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    if "your_gemini_api_key_here" in content:
        print("⚠️  Please update GEMINI_API_KEY in .env file")
        print("   Get your API key from: https://makersuite.google.com/app/apikey")
        return False
    
    if "GEMINI_API_KEY=" in content and len(content.split("GEMINI_API_KEY=")[1].split()[0]) > 10:
        print("✅ API key appears to be configured")
        return True
    
    print("⚠️  API key may not be properly configured in .env")
    return False

def check_hugo_structure():
    """Check if Hugo project structure exists"""
    project_root = Path("..").resolve()
    content_dir = project_root / "content"
    
    if not content_dir.exists():
        print(f"❌ Hugo content directory not found: {content_dir}")
        return False
    
    print("✅ Hugo project structure found")
    
    # Check required categories
    required_categories = ["ships", "concepts", "guides"]
    missing_categories = []
    
    for category in required_categories:
        category_dir = content_dir / category
        if not category_dir.exists():
            missing_categories.append(category)
    
    if missing_categories:
        print(f"⚠️  Missing category directories: {missing_categories}")
        return False
    
    print("✅ All required categories found")
    return True

def main():
    """Main setup process"""
    print("🚀 Setting up AI Blog Generator for Star Citizen Handbook")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed: Could not install dependencies")
        sys.exit(1)
    
    # Setup .env file
    if not setup_env_file():
        print("❌ Setup failed: Could not create .env file")
        sys.exit(1)
    
    # Check Hugo structure
    if not check_hugo_structure():
        print("❌ Setup failed: Hugo project structure issues")
        sys.exit(1)
    
    # Check API key
    api_key_ok = check_api_key()
    
    print("=" * 60)
    if api_key_ok:
        print("🎉 Setup completed successfully!")
        print("\nYou can now run the blog generator:")
        print('python blog_generator.py "your blog topic here"')
    else:
        print("⚠️  Setup mostly complete, but please configure your API key")
        print("\n1. Edit the .env file")
        print("2. Replace 'your_gemini_api_key_here' with your actual API key")
        print("3. Get your API key from: https://makersuite.google.com/app/apikey")
        print("\nThen you can run:")
        print('python blog_generator.py "your blog topic here"')

if __name__ == "__main__":
    main()
