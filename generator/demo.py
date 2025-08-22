#!/usr/bin/env python3
"""
Interactive Table Highlighting Tool - Usage Examples
==================================================

This script demonstrates how to use the interactive highlighting tool.

Features:
- Works with any markdown file containing tables
- Interactive prompts for each table found
- Configurable highlighting thresholds (default 20% for low/high)
- Option to clear all existing highlighting
- Column selection for targeted highlighting
- Automatic backup creation before saving changes

Usage Examples:
1. python interactive_highlight_calculator.py path/to/file.md
2. python interactive_highlight_calculator.py (will prompt for file path)
3. Drag and drop a file onto the script

Options for each table:
1. Process with highlighting (default)
   - Select which columns to highlight
   - Configure threshold percentages (default: 20% low, 20% high)
   - Red = worst values, Green = best values
2. Clear all highlighting
   - Removes all existing color highlighting from the table
3. Skip this table
   - Leave the table unchanged

The tool automatically:
- Creates a backup file (.backup extension) before making changes
- Identifies numeric columns that can be highlighted
- Shows table preview and column information
- Handles various numeric formats (integers, floats, with commas)
- Preserves table structure and formatting
"""

import os
import sys

def show_usage():
    """Display usage information."""
    print(__doc__)

def main():
    print("Interactive Table Highlighting Tool - Demo")
    print("=" * 50)
    
    # Show usage information
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', 'help']:
        show_usage()
        return
    
    # Get the path to the interactive script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    interactive_script = os.path.join(script_dir, 'interactive_highlight_calculator.py')
    test_file = os.path.join(script_dir, 'test_table.md')
    
    if not os.path.exists(interactive_script):
        print(f"Error: Interactive script not found at {interactive_script}")
        return
    
    print("Demo Files Available:")
    print(f"- Interactive Script: {os.path.basename(interactive_script)}")
    print(f"- Test File: {os.path.basename(test_file)}")
    
    if os.path.exists(test_file):
        print(f"\nTo test with the sample file, run:")
        print(f"python {os.path.basename(interactive_script)} {os.path.basename(test_file)}")
    
    print(f"\nTo use with any file:")
    print(f"python {os.path.basename(interactive_script)} your_file.md")
    print(f"or simply run:")
    print(f"python {os.path.basename(interactive_script)}")
    print("and enter the file path when prompted.")

if __name__ == '__main__':
    main()
