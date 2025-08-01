#!/usr/bin/env python3
"""
Test script for the AI Blog Generator

This script runs basic tests to ensure the generator is working correctly.
"""

import os
import sys
from pathlib import Path
import tempfile
import shutil

# Add the generator directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test if all required modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        import google.generativeai as genai
        print("✅ google.generativeai imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import google.generativeai: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import python-dotenv: {e}")
        return False
    
    try:
        from blog_generator import HugoBlogGenerator
        print("✅ blog_generator module imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import blog_generator: {e}")
        return False
    
    return True

def test_env_file():
    """Test if .env file exists and has API key configured"""
    print("🧪 Testing environment configuration...")
    
    env_file = Path(".env")
    if not env_file.exists():
        print("❌ .env file not found")
        return False
    
    print("✅ .env file exists")
    
    with open(env_file, 'r') as f:
        content = f.read()
    
    if "GEMINI_API_KEY=" not in content:
        print("❌ GEMINI_API_KEY not found in .env")
        return False
    
    if "your_gemini_api_key_here" in content:
        print("⚠️  GEMINI_API_KEY still has placeholder value")
        return False
    
    print("✅ GEMINI_API_KEY appears to be configured")
    return True

def test_generator_initialization():
    """Test if the generator can be initialized"""
    print("🧪 Testing generator initialization...")
    
    try:
        from blog_generator import HugoBlogGenerator
        generator = HugoBlogGenerator()
        print("✅ Generator initialized successfully")
        
        # Test basic methods
        slug = generator.slugify("Test Blog Post Title")
        if slug == "test-blog-post-title":
            print("✅ Slugify function working correctly")
        else:
            print(f"⚠️  Slugify function returned unexpected result: {slug}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to initialize generator: {e}")
        return False

def test_project_structure():
    """Test if Hugo project structure is accessible"""
    print("🧪 Testing Hugo project structure...")
    
    try:
        from blog_generator import HugoBlogGenerator
        generator = HugoBlogGenerator()
        
        # Check if content directory exists
        if not generator.content_dir.exists():
            print(f"❌ Content directory not found: {generator.content_dir}")
            return False
        
        print(f"✅ Content directory found: {generator.content_dir}")
        
        # Check categories
        for category in generator.categories.keys():
            category_dir = generator.content_dir / category
            if category_dir.exists():
                print(f"✅ Category directory found: {category}")
            else:
                print(f"⚠️  Category directory missing: {category}")
        
        return True
    except Exception as e:
        print(f"❌ Failed to check project structure: {e}")
        return False

def test_api_connection():
    """Test if API connection works"""
    print("🧪 Testing API connection...")
    
    try:
        from blog_generator import HugoBlogGenerator
        generator = HugoBlogGenerator()
        
        # Try a simple API call
        test_prompt = "Say 'API connection test successful' in Thai."
        response = generator.cost_effective_model.generate_content(test_prompt)
        
        if response and response.text:
            print("✅ API connection successful")
            print(f"   Response: {response.text.strip()[:100]}...")
            return True
        else:
            print("❌ API returned empty response")
            return False
    except Exception as e:
        print(f"❌ API connection failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Running AI Blog Generator Tests")
    print("=" * 50)
    
    tests = [
        ("Imports", test_imports),
        ("Environment", test_env_file),
        ("Generator Init", test_generator_initialization),
        ("Project Structure", test_project_structure),
        ("API Connection", test_api_connection),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n📋 {test_name}:")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"💥 Test {test_name} crashed: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTests passed: {passed}/{len(results)}")
    
    if passed == len(results):
        print("🎉 All tests passed! Generator is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the configuration.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
