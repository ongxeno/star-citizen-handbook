import re
import pandas as pd
from io import StringIO
import os
import sys

def parse_value(v_str):
    """Cleans and parses a string from the table into a numeric value or tuple."""
    v_str = str(v_str).strip()
    # Remove any HTML tags (like <span>) to get the raw value
    v_str = re.sub(r'<[^>]+>', '', v_str)
    if v_str == 'N/A':
        return None
    
    # Regex for 'Value<br>(Boosted Value)' format
    br_match = re.search(r'([\d,.]+)\s*<br>\s*\(([\d,.]+)\)', v_str)
    if br_match:
        base = float(br_match.group(1).replace(',', ''))
        boost = float(br_match.group(2).replace(',', ''))
        return (base, boost)
    
    # Regex for 'Value(Boosted Value)' format (without <br>)
    paren_match = re.search(r'([\d,.]+)\s*\(([\d,.]+)\)', v_str)
    if paren_match:
        base = float(paren_match.group(1).replace(',', ''))
        boost = float(paren_match.group(2).replace(',', ''))
        return (base, boost)
        
    # Regex for 'P/Y/R<br>(Boosted P/Y/R)' format
    pyr_br_match = re.search(r'([\d,.]+)/([\d,.]+)/([\d,.]+)\s*<br>\s*\(([\d,.]+)/([\d,.]+)/([\d,.]+)\)', v_str)
    if pyr_br_match:
        base = tuple(float(g.replace(',', '')) for g in pyr_br_match.groups()[:3])
        boost = tuple(float(g.replace(',', '')) for g in pyr_br_match.groups()[3:])
        return (base, boost)
    
    # Regex for 'P/Y/R(Boosted P/Y/R)' format (without <br>)
    pyr_paren_match = re.search(r'([\d,.]+)/([\d,.]+)/([\d,.]+)\s*\(([\d,.]+)/([\d,.]+)/([\d,.]+)\)', v_str)
    if pyr_paren_match:
        base = tuple(float(g.replace(',', '')) for g in pyr_paren_match.groups()[:3])
        boost = tuple(float(g.replace(',', '')) for g in pyr_paren_match.groups()[3:])
        return (base, boost)

    # Regex for a simple number (with or without commas)
    simple_match = re.match(r'^[\d,.]+$', v_str)
    if simple_match:
        return float(v_str.replace(',', ''))
        
    # Return the original string if no numeric pattern is matched
    return v_str

def is_higher_better(column_name):
    """
    Determine if higher values are better for a given column.
    
    Args:
        column_name: The name of the column
        
    Returns:
        bool: True if higher values are better (is_bad_low=False), False if lower values are better (is_bad_low=True)
    """
    column_lower = column_name.lower()
    
    # Columns where higher values are better
    higher_better_keywords = [
        'speed', 'velocity', 'acceleration', 'range', 'health', 'shield', 
        'armor', 'damage', 'dps', 'fire rate', 'capacity', 'storage', 
        'power', 'thrust', 'quantum fuel', 'hydrogen fuel'
    ]
    
    # Columns where lower values are better  
    lower_better_keywords = [
        'time to empty', 'charge time', 'overheat time', 'signature', 
        'em signature', 'ir signature', 'cross section'
    ]
    
    # Check for higher is better keywords
    for keyword in higher_better_keywords:
        if keyword in column_lower:
            return True
            
    # Check for lower is better keywords  
    for keyword in lower_better_keywords:
        if keyword in column_lower:
            return False
    
    # Default: assume higher is better
    return True

def highlight(val, min_v, max_v, low_threshold=0.2, high_threshold=0.2, is_bad_low=True):
    """Applies a color-coded <span> tag to a value based on its position within a range."""
    if val is None or pd.isna(val) or min_v is None or max_v is None:
        return ''
        
    range_v = max_v - min_v
    if range_v == 0:
        # Format as integer if it's a whole number, otherwise as a float
        return f"{val:,.0f}" if val == int(val) else f"{val:,.1f}"

    # Set the thresholds for highlighting based on user input
    low_thresh = min_v + range_v * low_threshold
    high_thresh = max_v - range_v * high_threshold

    # Format the number with commas
    str_val = f"{val:,.0f}" if val == int(val) else f"{val:,.1f}"

    # Apply color based on whether a low value is good or bad
    if is_bad_low: # Higher is better
        if val <= low_thresh:
            return f'<span style="color:#FF6B6B">{str_val}</span>'
        if val >= high_thresh:
            return f'<span style="color:#4ECDC4">{str_val}</span>'
    else: # Lower is better
        if val <= low_thresh:
            return f'<span style="color:#4ECDC4">{str_val}</span>'
        if val >= high_thresh:
            return f'<span style="color:#FF6B6B">{str_val}</span>'
            
    return str_val

def remove_all_highlighting(text):
    """Remove all HTML span tags with color styling from text."""
    # Pattern to match span tags with color styling
    pattern = r'<span\s+style="color:[^"]*"[^>]*>(.*?)</span>'
    return re.sub(pattern, r'\1', text)

def get_numeric_columns(df, header_names_raw, header_names):
    """Identify which columns contain numeric data that can be highlighted."""
    numeric_columns = []
    
    for i, (raw_name, clean_name) in enumerate(zip(header_names_raw, header_names)):
        # Skip the first column (ship names)
        if i == 0:
            continue
            
        # Test if this column has numeric data
        test_data = df[raw_name].apply(parse_value)
        numeric_data = []
        for val in test_data:
            if isinstance(val, (int, float)):
                numeric_data.append(val)
            elif isinstance(val, tuple) and len(val) == 2 and all(isinstance(x, (int, float)) for x in val):
                numeric_data.extend(val)
            elif isinstance(val, tuple) and len(val) == 2:
                # Handle nested tuples like pitch/yaw/roll data: ((base1, base2, base3), (boost1, boost2, boost3))
                for sub_tuple in val:
                    if isinstance(sub_tuple, tuple) and all(isinstance(x, (int, float)) for x in sub_tuple):
                        numeric_data.extend(sub_tuple)
        
        if len(numeric_data) > 1:  # Need at least 2 values for comparison
            numeric_columns.append({
                'index': i,
                'raw_name': raw_name,
                'clean_name': clean_name,
                'sample_values': numeric_data[:3]  # Show first 3 values as examples
            })
    
    return numeric_columns

def display_table_info(table_md, table_index):
    """Display information about a table for user review."""
    lines = table_md.strip().split('\n')
    header_line = lines[0] if lines else ""
    data_lines = lines[2:] if len(lines) > 2 else []
    
    print(f"\n{'='*60}")
    print(f"TABLE {table_index + 1} FOUND")
    print(f"{'='*60}")
    print(f"Rows: {len(data_lines)} data rows")
    
    # Show header
    if header_line:
        headers = [h.strip() for h in header_line.split('|')[1:-1]]
        clean_headers = [re.sub(r'<[^>]+>', '', h).strip() for h in headers]
        print(f"Columns: {', '.join(clean_headers)}")
    
    # Show first few rows as preview
    print(f"\nPreview (first 2 rows):")
    for i, line in enumerate(data_lines[:2]):
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        if cells:
            clean_cells = [re.sub(r'<[^>]+>', '', cell).strip()[:20] + ('...' if len(re.sub(r'<[^>]+>', '', cell).strip()) > 20 else '') for cell in cells]
            print(f"  Row {i+1}: {clean_cells[0]} | {' | '.join(clean_cells[1:3])}...")

def get_user_choice():
    """Get user's choice for what to do with the table."""
    print(f"\nWhat would you like to do with this table?")
    print("1. Process with highlighting (default)")
    print("2. Clear all highlighting")
    print("3. Skip this table")
    
    while True:
        choice = input("Enter choice (1-3, or press Enter for default): ").strip()
        if choice == "" or choice == "1":
            return "process"
        elif choice == "2":
            return "clear"
        elif choice == "3":
            return "skip"
        else:
            print("Invalid choice. Please enter 1, 2, 3, or press Enter for default.")

def get_threshold_settings():
    """Get threshold settings from user."""
    print(f"\nHighlighting Settings:")
    print("- Red color: worst performing values")
    print("- Green color: best performing values")
    print("- Default: bottom 20% = red, top 20% = green")
    
    try:
        low_input = input("Low threshold percentage (default 20): ").strip()
        low_threshold = float(low_input) / 100 if low_input else 0.2
        
        high_input = input("High threshold percentage (default 20): ").strip()
        high_threshold = float(high_input) / 100 if high_input else 0.2
        
        # Validate thresholds
        if low_threshold < 0 or low_threshold > 0.5:
            low_threshold = 0.2
        if high_threshold < 0 or high_threshold > 0.5:
            high_threshold = 0.2
            
        return low_threshold, high_threshold
    except ValueError:
        return 0.2, 0.2

def select_columns_to_highlight(numeric_columns):
    """Let user select which columns to highlight."""
    if not numeric_columns:
        print("No numeric columns found in this table.")
        return []
    
    print(f"\nFound {len(numeric_columns)} numeric columns:")
    for i, col in enumerate(numeric_columns):
        sample_str = ', '.join(str(v) for v in col['sample_values'])
        print(f"{i+1}. {col['clean_name']} (sample: {sample_str})")
    
    print(f"\nWhich columns would you like to highlight?")
    print(f"Enter column numbers separated by commas (e.g., 1,3,5)")
    print(f"Or press Enter to highlight all numeric columns")
    
    while True:
        selection = input("Columns to highlight: ").strip()
        if selection == "":
            return numeric_columns
        
        try:
            indices = [int(x.strip()) - 1 for x in selection.split(',')]
            if all(0 <= i < len(numeric_columns) for i in indices):
                return [numeric_columns[i] for i in indices]
            else:
                print("Invalid column numbers. Please try again.")
        except ValueError:
            print("Invalid input format. Please enter numbers separated by commas.")

def process_table_interactive(table_md):
    """Process a table with user interaction."""
    lines = table_md.strip().split('\n')
    header_line = lines[0]
    divider = lines[1]
    data_lines = lines[2:]

    # Parse table into DataFrame
    processed_lines = []
    num_columns = header_line.count('|') - 1
    for line in data_lines:
        processed_lines.append('|'.join(line.strip().split('|', num_columns)))

    csv_io = StringIO('\n'.join(processed_lines))
    df = pd.read_csv(csv_io, sep='|', header=None, skipinitialspace=True)
    df = df.drop(columns=[df.columns[0], df.columns[-1]])

    # Get header names
    header_names_raw = [h.strip() for h in header_line.strip().split('|')[1:-1]]
    header_names = [re.sub(r'<[^>]+>', '', h).strip() for h in header_names_raw]
    
    df.columns = header_names_raw
    ship_column_name = header_names_raw[0]
    df = df.set_index(ship_column_name)
    df_original = df.copy()

    # Get user choice
    choice = get_user_choice()
    
    if choice == "skip":
        return table_md
    elif choice == "clear":
        # Remove all highlighting from the table
        clear_table = remove_all_highlighting(table_md)
        print("✓ All highlighting cleared from this table.")
        return clear_table
    elif choice == "process":
        # Get numeric columns
        numeric_columns = get_numeric_columns(df, header_names_raw, header_names)
        selected_columns = select_columns_to_highlight(numeric_columns)
        
        if not selected_columns:
            print("No columns selected for highlighting.")
            return table_md
        
        # Get threshold settings
        low_threshold, high_threshold = get_threshold_settings()
        
        # Process highlighting
        df_highlighted = df_original.copy()
        stats = {}
        
        for col_info in selected_columns:
            raw_name = col_info['raw_name']
            clean_name = col_info['clean_name']
            
            # Calculate stats for this column
            data = df[raw_name].apply(parse_value).dropna()
            
            # Check if this is a Pitch/Yaw/Roll column (nested tuples)
            is_pitch_yaw_roll = False
            first_val = data.iloc[0] if len(data) > 0 else None
            if (isinstance(first_val, tuple) and len(first_val) == 2 and 
                isinstance(first_val[0], tuple) and isinstance(first_val[1], tuple)):
                is_pitch_yaw_roll = True
            
            if is_pitch_yaw_roll:
                # Handle Pitch/Yaw/Roll column - calculate separate stats for each component
                pitch_values = []
                yaw_values = []
                roll_values = []
                pitch_boost_values = []
                yaw_boost_values = []
                roll_boost_values = []
                
                for val in data:
                    if isinstance(val, tuple) and len(val) == 2:
                        base_tuple, boost_tuple = val
                        if (isinstance(base_tuple, tuple) and isinstance(boost_tuple, tuple) and
                            len(base_tuple) == 3 and len(boost_tuple) == 3):
                            pitch_values.append(base_tuple[0])
                            yaw_values.append(base_tuple[1])
                            roll_values.append(base_tuple[2])
                            pitch_boost_values.append(boost_tuple[0])
                            yaw_boost_values.append(boost_tuple[1])
                            roll_boost_values.append(boost_tuple[2])
                
                # Store separate stats for each component
                stats[clean_name] = {
                    'type': 'pitch_yaw_roll',
                    'pitch': {'min': min(pitch_values), 'max': max(pitch_values)} if pitch_values else None,
                    'yaw': {'min': min(yaw_values), 'max': max(yaw_values)} if yaw_values else None,
                    'roll': {'min': min(roll_values), 'max': max(roll_values)} if roll_values else None,
                    'pitch_boost': {'min': min(pitch_boost_values), 'max': max(pitch_boost_values)} if pitch_boost_values else None,
                    'yaw_boost': {'min': min(yaw_boost_values), 'max': max(yaw_boost_values)} if yaw_boost_values else None,
                    'roll_boost': {'min': min(roll_boost_values), 'max': max(roll_boost_values)} if roll_boost_values else None,
                }
            else:
                # Check if this is a base/boost pair column (like SCM Speed (Boost))
                is_base_boost = False
                base_values = []
                boost_values = []
                single_values = []
                
                for val in data:
                    if isinstance(val, (int, float)):
                        single_values.append(val)
                    elif isinstance(val, tuple) and len(val) == 2 and all(isinstance(x, (int, float)) for x in val):
                        is_base_boost = True
                        base_values.append(val[0])
                        boost_values.append(val[1])
                
                if is_base_boost and base_values and boost_values:
                    # Handle base/boost pairs with separate ranges
                    stats[clean_name] = {
                        'type': 'base_boost',
                        'base': {'min': min(base_values), 'max': max(base_values)},
                        'boost': {'min': min(boost_values), 'max': max(boost_values)},
                    }
                elif single_values:
                    # Handle regular single values
                    stats[clean_name] = {
                        'type': 'single',
                        'min': min(single_values),
                        'max': max(single_values),
                        'data': single_values
                    }
        
        # Apply highlighting
        for ship_name, row in df_original.iterrows():
            for col_info in selected_columns:
                raw_name = col_info['raw_name']
                clean_name = col_info['clean_name']
                
                if clean_name not in stats:
                    continue
                    
                val = parse_value(row[raw_name])
                
                # Check what type of column this is
                col_stats = stats[clean_name]
                
                if col_stats.get('type') == 'pitch_yaw_roll':
                    # Handle Pitch/Yaw/Roll format with separate stats for each component
                    if isinstance(val, tuple) and len(val) == 2:
                        base_tuple, boost_tuple = val
                        if (isinstance(base_tuple, tuple) and isinstance(boost_tuple, tuple) and
                            len(base_tuple) == 3 and len(boost_tuple) == 3):
                            
                            # Highlight each component with its own range
                            components = ['pitch', 'yaw', 'roll']
                            boost_components = ['pitch_boost', 'yaw_boost', 'roll_boost']
                            
                            base_values = []
                            boost_values = []
                            
                            # Process base values (pitch, yaw, roll)
                            for i, component in enumerate(components):
                                if col_stats[component]:
                                    is_bad_low = is_higher_better(clean_name)  # Fixed: don't invert
                                    highlighted = highlight(
                                        base_tuple[i], 
                                        col_stats[component]['min'], 
                                        col_stats[component]['max'], 
                                        low_threshold, high_threshold, is_bad_low
                                    )
                                    base_values.append(highlighted)
                                else:
                                    base_values.append(str(base_tuple[i]))
                            
                            # Process boosted values (pitch_boost, yaw_boost, roll_boost)
                            for i, component in enumerate(boost_components):
                                if col_stats[component]:
                                    is_bad_low = is_higher_better(clean_name)  # Fixed: don't invert
                                    highlighted = highlight(
                                        boost_tuple[i], 
                                        col_stats[component]['min'], 
                                        col_stats[component]['max'], 
                                        low_threshold, high_threshold, is_bad_low
                                    )
                                    boost_values.append(highlighted)
                                else:
                                    boost_values.append(str(boost_tuple[i]))
                            
                            base_str = '/'.join(base_values)
                            boost_str = '/'.join(boost_values)
                            df_highlighted.loc[ship_name, raw_name] = f"{base_str}<br>({boost_str})"
                            
                elif col_stats.get('type') == 'base_boost':
                    # Handle base/boost format with separate ranges
                    if isinstance(val, tuple) and len(val) == 2:
                        base, boost = val
                        is_bad_low = is_higher_better(clean_name)  # Fixed: don't invert
                        h_base = highlight(
                            base, 
                            col_stats['base']['min'], 
                            col_stats['base']['max'], 
                            low_threshold, high_threshold, is_bad_low
                        )
                        h_boost = highlight(
                            boost, 
                            col_stats['boost']['min'], 
                            col_stats['boost']['max'], 
                            low_threshold, high_threshold, is_bad_low
                        )
                        df_highlighted.loc[ship_name, raw_name] = f"{h_base}<br>({h_boost})"
                elif isinstance(val, (int, float)):
                    # Handle regular single values
                    is_bad_low = is_higher_better(clean_name)  # Fixed: don't invert
                    df_highlighted.loc[ship_name, raw_name] = highlight(
                        val, col_stats['min'], col_stats['max'], 
                        low_threshold, high_threshold, is_bad_low
                    )
                elif isinstance(val, tuple) and len(val) == 2:
                    # Handle simple base/boost format (fallback for any missed cases)
                    base, boost = val
                    is_bad_low = is_higher_better(clean_name)  # Fixed: don't invert
                    h_base = highlight(base, col_stats['min'], col_stats['max'], low_threshold, high_threshold, is_bad_low)
                    h_boost = highlight(boost, col_stats['min'], col_stats['max'], low_threshold, high_threshold, is_bad_low)
                    df_highlighted.loc[ship_name, raw_name] = f"{h_base}<br>({h_boost})"
        
        # Reconstruct markdown table
        new_md_lines = [header_line, divider]
        for ship_name, row in df_highlighted.iterrows():
            clean_ship_name = re.sub(r'<[^>]+>', '', ship_name).strip()
            cols = [f" {clean_ship_name} "] + [f" {str(c).strip()} " for c in row.values]
            new_md_lines.append('|' + '|'.join(cols) + '|')
        
        processed_cols = [col['clean_name'] for col in selected_columns]
        print(f"✓ Applied highlighting to columns: {', '.join(processed_cols)}")
        print(f"✓ Thresholds: {low_threshold*100:.0f}% low, {high_threshold*100:.0f}% high")
        
        return '\n'.join(new_md_lines)

def process_file_interactive(file_path):
    """Main function to interactively process all tables in a file."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all markdown tables
    tables = re.findall(r'(\|(?:[^\n]+\|)+\n\|(?::?-+:?\|)+[\s\S]*?(?=\n\n|\n---|\Z))', content)
    
    if not tables:
        print("No markdown tables found in the file.")
        return False
    
    print(f"Found {len(tables)} table(s) in '{os.path.basename(file_path)}'")
    
    new_content = content
    tables_processed = 0
    
    for i, table_md in enumerate(tables):
        display_table_info(table_md, i)
        
        try:
            processed_table = process_table_interactive(table_md)
            if processed_table != table_md:
                new_content = new_content.replace(table_md, processed_table)
                tables_processed += 1
        except Exception as e:
            print(f"Error processing table {i+1}: {e}")
            print("Skipping this table...")
            continue
    
    # Ask user if they want to save changes
    if tables_processed > 0:
        print(f"\n{tables_processed} table(s) were modified.")
        save = input("Save changes to file? (y/N): ").strip().lower()
        if save in ['y', 'yes']:
            # Create backup
            backup_path = file_path + '.backup'
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Backup saved to '{backup_path}'")
            
            # Save modified file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"✓ Changes saved to '{file_path}'")
            return True
        else:
            print("Changes discarded.")
            return False
    else:
        print("No changes were made.")
        return False

def main():
    """Main entry point for the interactive highlighting tool."""
    print("Interactive Table Highlighting Tool")
    print("=" * 40)
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        file_path = input("Enter file path (or drag & drop file here): ").strip().strip('"')
    
    if not file_path:
        print("No file specified.")
        return
    
    # Convert to absolute path
    file_path = os.path.abspath(file_path)
    
    process_file_interactive(file_path)
    
    print("\nDone!")

if __name__ == '__main__':
    main()
