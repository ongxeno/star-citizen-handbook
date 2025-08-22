#!/usr/bin/env python3
"""
Table Highlighting Tools - Complete Feature Set
==============================================

This module provides comprehensive table highlighting functionality for markdown files.

NEW INTERACTIVE FEATURES:
✅ Works with any markdown file containing tables
✅ Interactive prompts for user choices per table
✅ Configurable highlighting thresholds (20% default)
✅ Column selection with preview
✅ Clear highlighting option
✅ Automatic backup creation
✅ Smart numeric column detection

ENHANCED ORIGINAL FEATURES:
✅ Command line argument support
✅ Flexible file processing
✅ Improved error handling
✅ Support for various table structures
"""

import os
import sys

def main():
    print("Table Highlighting Tools - Feature Summary")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists('interactive_highlight_calculator.py'):
        print("Error: Please run this script from the generator directory.")
        return
    
    print("\n🔧 AVAILABLE TOOLS:")
    print("\n1. INTERACTIVE TOOL (NEW)")
    print("   File: interactive_highlight_calculator.py")
    print("   ✨ Interactive mode with user prompts")
    print("   ✨ Works with any markdown file")
    print("   ✨ Configurable thresholds and column selection")
    print("   ✨ Clear highlighting option")
    print("   ✨ Automatic backup creation")
    
    print("\n2. AUTOMATED TOOL (ENHANCED)")
    print("   File: temp_highlight_calculator.py")  
    print("   ⚡ Fast automated processing")
    print("   ⚡ Specialized for ship comparison data")
    print("   ⚡ Command line argument support")
    print("   ⚡ Batch processing capability")
    
    print("\n📋 USAGE EXAMPLES:")
    print("\n# Interactive mode (any file)")
    print("python interactive_highlight_calculator.py")
    print("python interactive_highlight_calculator.py your_file.md")
    
    print("\n# Automated mode (ship data)")
    print("python temp_highlight_calculator.py")
    print("python temp_highlight_calculator.py custom_file.md")
    
    print("\n# Test with sample data")
    print("python interactive_highlight_calculator.py test_table.md")
    
    print("\n🎨 COLOR CODING:")
    print("🔴 Red (#FF6B6B): Worst performing values")
    print("🟢 Green (#4ECDC4): Best performing values")
    print("⚪ No highlight: Middle range values")
    
    print("\n📊 SUPPORTED FORMATS:")
    print("• Simple numbers: 1000, 1,500, 15.5")
    print("• Base/boost: 220<br>(480)")
    print("• Multi-axis: 52/43/148<br>(62.4/51.6/177.6)")
    print("• HTML tagged: Strips existing <span> tags")
    
    print("\n🔍 FEATURES COMPARISON:")
    print(f"{'Feature':<25} {'Interactive':<12} {'Automated':<10}")
    print("-" * 47)
    print(f"{'User prompts':<25} {'✅':<12} {'❌':<10}")
    print(f"{'Any file support':<25} {'✅':<12} {'✅':<10}")
    print(f"{'Column selection':<25} {'✅':<12} {'❌':<10}")
    print(f"{'Threshold config':<25} {'✅':<12} {'❌':<10}")
    print(f"{'Clear highlighting':<25} {'✅':<12} {'❌':<10}")
    print(f"{'Auto backup':<25} {'✅':<12} {'❌':<10}")
    print(f"{'Ship data optimized':<25} {'❌':<12} {'✅':<10}")
    print(f"{'Speed':<25} {'Medium':<12} {'Fast':<10}")
    
    print(f"\n📁 FILES CREATED:")
    files = [
        'interactive_highlight_calculator.py',
        'temp_highlight_calculator.py (updated)',
        'test_table.md',
        'demo.py',
        'README.md'
    ]
    for file in files:
        status = "✅" if os.path.exists(file.split(' ')[0]) else "❌"
        print(f"   {status} {file}")
    
    print(f"\n🚀 QUICK START:")
    print("1. Try interactive mode: python interactive_highlight_calculator.py test_table.md")
    print("2. Check README.md for detailed documentation")
    print("3. Use demo.py for usage examples")

if __name__ == '__main__':
    main()
