# Table Highlighting Tools

This directory contains tools for automatically highlighting numerical values in markdown tables with color coding to indicate best/worst performing values.

## Files

### `interactive_highlight_calculator.py` ✨ NEW
**Interactive tool for any markdown file with tables**

- **Interactive mode**: Prompts for each table found in any file
- **Flexible file input**: Works with any markdown file containing tables  
- **User choices per table**:
  - Process with highlighting (configurable thresholds)
  - Clear all existing highlighting
  - Skip table unchanged
- **Column selection**: Choose which numeric columns to highlight
- **Configurable thresholds**: Set custom percentages for low/high highlighting (default 20%)
- **Automatic backup**: Creates `.backup` file before making changes
- **Smart detection**: Automatically identifies numeric columns

**Usage:**
```bash
# Interactive mode (prompts for file path)
python interactive_highlight_calculator.py

# Direct file input
python interactive_highlight_calculator.py path/to/your/file.md

# Help
python demo.py --help
```

### `temp_highlight_calculator.py`
**Original automated tool for ship comparison file**

- **Automated processing**: No user interaction required
- **Specialized for ship data**: Designed for the alpha-4.3-medium-fighter-compare file
- **Fixed columns**: Highlights predefined columns (Hull HP, Shield HP, DPS, etc.)
- **Command line support**: Can now accept file path as argument

**Usage:**
```bash
# Default ship comparison file
python temp_highlight_calculator.py

# Custom file
python temp_highlight_calculator.py path/to/file.md
```

### `test_table.md`
Sample markdown file with tables for testing the interactive tool.

### `demo.py`
Usage examples and documentation for the interactive tool.

## Color Coding

- 🔴 **Red (#FF6B6B)**: Worst performing values (bottom threshold %)
- 🟢 **Green (#4ECDC4)**: Best performing values (top threshold %)
- ⚪ **No highlight**: Middle range values

## Supported Number Formats

- Simple integers: `1000`, `1,500`
- Decimals: `15.5`, `1,234.56`
- Base/boost format: `220<br>(480)` or `220(480)`
- Pitch/Yaw/Roll: `52/43/148<br>(62.4/51.6/177.6)`
- HTML tagged values: Automatically strips existing `<span>` tags

## Features

### Interactive Tool Features
- ✅ Works with any markdown file
- ✅ Table preview and information display
- ✅ Column selection with sample data preview
- ✅ Configurable highlighting thresholds
- ✅ Clear highlighting option
- ✅ Automatic file backup
- ✅ Error handling and validation

### Original Tool Features  
- ✅ Specialized for ship comparison data
- ✅ Automated processing of specific columns
- ✅ Support for complex data formats (base/boost, pitch/yaw/roll)
- ✅ Command line argument support
- ✅ Batch processing of multiple tables

## Installation

No additional dependencies required beyond the standard Python libraries:
- `pandas` (for data processing)
- `re` (for regular expressions)
- Built-in modules: `os`, `sys`, `io`

## Examples

### Using Interactive Tool
```bash
# Start interactive mode
python interactive_highlight_calculator.py

# Process the test file
python interactive_highlight_calculator.py test_table.md
```

### Using Original Tool
```bash
# Process ship comparison file (default)
python temp_highlight_calculator.py

# Process any file
python temp_highlight_calculator.py custom_file.md
```

## Tips

1. **Backup Safety**: The interactive tool automatically creates backups - look for `.backup` files
2. **Column Selection**: Preview sample values to understand what will be highlighted
3. **Threshold Tuning**: Start with default 20% and adjust based on your data distribution
4. **Clear Highlighting**: Use the clear option to remove all highlighting and start fresh
5. **File Formats**: Ensure tables follow standard markdown format with proper `|` separators

## Troubleshooting

- **No tables found**: Verify your markdown tables have proper header/separator rows
- **No numeric columns**: Tool only highlights columns with numeric data
- **File encoding**: Ensure files are saved in UTF-8 encoding
- **Permission errors**: Check file write permissions and that files aren't open in other programs
