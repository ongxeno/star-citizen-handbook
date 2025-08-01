#!/usr/bin/env python3
"""
Quick validation script to check if the blog generator is ready to use.
Run this after setup to ensure everything is working.
"""

import os
import sys
from pathlib import Path

def main():
    """Quick validation check"""
    print("🔍 Quick Blog Generator Validation")
    print("=" * 40)
    
    issues = []
    
    # Check Python version
    if sys.version_info < (3, 8):
        issues.append(f"Python 3.8+ required (current: {sys.version.split()[0]})")
    else:
        print("✅ Python version OK")
    
    # Check .env file
    env_file = Path(".env")
    if not env_file.exists():
        issues.append(".env file missing")
    elif "your_gemini_api_key_here" in env_file.read_text():
        issues.append("GEMINI_API_KEY not configured in .env")
    else:
        print("✅ .env file configured")
    
    # Check dependencies
    try:
        import google.generativeai
        import dotenv
        print("✅ Dependencies installed")
    except ImportError as e:
        issues.append(f"Missing dependency: {e}")
    
    # Check Hugo structure
    content_dir = Path("..") / "content"
    if not content_dir.exists():
        issues.append("Hugo content directory not found")
    else:
        print("✅ Hugo structure found")
    
    # Check required categories
    for category in ["ships", "concepts", "guides"]:
        if not (content_dir / category).exists():
            issues.append(f"Missing category: {category}")
    
    if not issues:
        print("✅ All categories found")
    
    print("=" * 40)
    
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"   • {issue}")
        print("\nRun 'python setup.py' to fix these issues.")
        return False
    else:
        print("🎉 Generator is ready to use!")
        print("\nExample usage:")
        print('python blog_generator.py "Drake Cutlass Red medical ship"')
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
