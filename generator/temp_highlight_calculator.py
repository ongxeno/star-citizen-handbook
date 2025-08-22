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

def highlight(val, min_v, max_v, low_threshold=0.05, high_threshold=0.05, is_bad_low=True):
    """Applies a color-coded <span> tag to a value based on its position within a range."""
    if val is None or pd.isna(val) or min_v is None or max_v is None:
        return ''
        
    range_v = max_v - min_v
    if range_v == 0:
        # Format as integer if it's a whole number, otherwise as a float
        return f"{val:,.0f}" if val == int(val) else f"{val:,.1f}"

    # Set the thresholds for highlighting (configurable)
    low_thresh = min_v + range_v * low_threshold
    high_thresh = max_v - range_v * high_threshold

    # Format the number with commas
    str_val = f"{val:,.0f}" if val == int(val) else f"{val:,.1f}"

    # Apply color based on whether a low value is good or bad
    if is_bad_low: # Higher is better
        if val < low_thresh:
            return f'<span style="color:#FF6B6B">{str_val}</span>'
        if val > high_thresh:
            return f'<span style="color:#4ECDC4">{str_val}</span>'
    else: # Lower is better
        if val < low_thresh:
            return f'<span style="color:#4ECDC4">{str_val}</span>'
        if val > high_thresh:
            return f'<span style="color:#FF6B6B">{str_val}</span>'
            
    return str_val

def process_table(md_table):
    """Reads a markdown table, recalculates stats, and returns a new markdown table with updated highlighting."""
    lines = md_table.strip().split('\n')
    header_line = lines[0]
    divider = lines[1]
    data_lines = lines[2:]

    # A more robust way to read markdown tables into pandas
    # Process lines to ensure consistent column count for pandas
    processed_lines = []
    num_columns = header_line.count('|') - 1
    for line in data_lines:
        # Ensure each data row has the correct number of columns
        processed_lines.append('|'.join(line.strip().split('|', num_columns)))

    csv_io = StringIO('\n'.join(processed_lines))
    df = pd.read_csv(csv_io, sep='|', header=None, skipinitialspace=True)
    
    # Drop empty columns created by leading/trailing '|'
    df = df.drop(columns=[df.columns[0], df.columns[-1]])

    # Clean and assign header names - remove HTML tags
    header_names_raw = [h.strip() for h in header_line.strip().split('|')[1:-1]]
    header_names = [re.sub(r'<[^>]+>', '', h).strip() for h in header_names_raw]
    
    # Map raw headers to clean headers for later reference
    raw_to_clean = dict(zip(header_names_raw, header_names))
    
    df.columns = header_names_raw  # Keep raw headers for DataFrame columns
    
    # Set the first column ('Ship') as the index
    ship_column_name = header_names_raw[0]
    df = df.set_index(ship_column_name)
    df.index.name = 'Ship'

    df_original = df.copy()

    # --- Calculate min/max for each stat column ---
    stats = {
        'Hull HP': {'data': df[header_names_raw[1]].apply(parse_value).dropna()},
        'Stock DPS': {'data': df[header_names_raw[5]].apply(parse_value).dropna()},
        'Nav Speed (m/s)': {'data': df[header_names_raw[7]].apply(parse_value).dropna()},
    }
    
    # Add Stock Shield HP if the column exists and contains numeric data
    shield_hp_column = None
    for i, col_name in enumerate(header_names):
        if 'Shield HP' in col_name or 'Stock Shield HP' in col_name:
            shield_hp_column = header_names_raw[i]  # Use raw header name
            shield_hp_data = df[shield_hp_column].apply(parse_value).dropna()
            if not shield_hp_data.empty and all(isinstance(x, (int, float)) for x in shield_hp_data):
                stats['Stock Shield HP'] = {'data': shield_hp_data}
            break
    
    # Handle SCM Speed (base/boost) parsing
    scm_data = df[header_names_raw[8]].apply(parse_value)
    scm_base_data = []
    scm_boost_data = []
    for val in scm_data:
        if isinstance(val, tuple) and len(val) == 2:
            scm_base_data.append(val[0])
            scm_boost_data.append(val[1])
    
    if scm_base_data:
        stats['SCM Speed'] = {'data': pd.Series(scm_base_data).dropna()}
    if scm_boost_data:
        stats['SCM Boost'] = {'data': pd.Series(scm_boost_data).dropna()}
    
    # Handle Pitch/Yaw/Roll parsing
    pyr_data = df[header_names_raw[9]].apply(parse_value)
    pitch_data, yaw_data, roll_data = [], [], []
    pitch_boost_data, yaw_boost_data, roll_boost_data = [], [], []
    
    for val in pyr_data:
        if isinstance(val, tuple) and len(val) == 2 and isinstance(val[0], tuple) and isinstance(val[1], tuple):
            base_pyr, boost_pyr = val
            if len(base_pyr) == 3 and len(boost_pyr) == 3:
                pitch_data.append(base_pyr[0])
                yaw_data.append(base_pyr[1])
                roll_data.append(base_pyr[2])
                pitch_boost_data.append(boost_pyr[0])
                yaw_boost_data.append(boost_pyr[1])
                roll_boost_data.append(boost_pyr[2])
    
    if pitch_data:
        stats['Pitch'] = {'data': pd.Series(pitch_data).dropna()}
    if yaw_data:
        stats['Yaw'] = {'data': pd.Series(yaw_data).dropna()}
    if roll_data:
        stats['Roll'] = {'data': pd.Series(roll_data).dropna()}
    if pitch_boost_data:
        stats['Pitch Boost'] = {'data': pd.Series(pitch_boost_data).dropna()}
    if yaw_boost_data:
        stats['Yaw Boost'] = {'data': pd.Series(yaw_boost_data).dropna()}
    if roll_boost_data:
        stats['Roll Boost'] = {'data': pd.Series(roll_boost_data).dropna()}

    for key, value in stats.items():
        if not value['data'].empty:
            value['min'] = value['data'].min()
            value['max'] = value['data'].max()

    # --- Apply highlighting to a copy of the dataframe ---
    df_highlighted = df_original.copy()

    for ship_name, row in df_original.iterrows():
        # Hull HP
        val = parse_value(row[header_names_raw[1]])
        if val is not None and 'Hull HP' in stats and not stats['Hull HP']['data'].empty:
            df_highlighted.loc[ship_name, header_names_raw[1]] = highlight(val, stats['Hull HP']['min'], stats['Hull HP']['max'])
        
        # Stock Shield HP (if column exists)
        if shield_hp_column and 'Stock Shield HP' in stats and not stats['Stock Shield HP']['data'].empty:
            val = parse_value(row[shield_hp_column])
            if val is not None:
                df_highlighted.loc[ship_name, shield_hp_column] = highlight(val, stats['Stock Shield HP']['min'], stats['Stock Shield HP']['max'])
        
        # Stock DPS
        val = parse_value(row[header_names_raw[5]])
        if val is not None and 'Stock DPS' in stats and not stats['Stock DPS']['data'].empty:
            df_highlighted.loc[ship_name, header_names_raw[5]] = highlight(val, stats['Stock DPS']['min'], stats['Stock DPS']['max'])

        # Nav Speed
        val = parse_value(row[header_names_raw[7]])
        if val is not None and 'Nav Speed (m/s)' in stats and not stats['Nav Speed (m/s)']['data'].empty:
            df_highlighted.loc[ship_name, header_names_raw[7]] = highlight(val, stats['Nav Speed (m/s)']['min'], stats['Nav Speed (m/s)']['max'])

        # SCM Speed (Boost)
        try:
            vals = parse_value(row[header_names_raw[8]])
        except Exception as e:
            print(f"Error parsing SCM Speed for {ship_name}: {e}")
            print(f"Row data: {row[header_names_raw[8]]}")
            print(f"Column name: {header_names_raw[8]}")
            raise
        if isinstance(vals, tuple) and len(vals) == 2:
            base, boost = vals
            h_base = highlight(base, stats['SCM Speed'].get('min'), stats['SCM Speed'].get('max')) if 'SCM Speed' in stats and 'min' in stats['SCM Speed'] and 'max' in stats['SCM Speed'] else str(base)
            h_boost = highlight(boost, stats['SCM Boost'].get('min'), stats['SCM Boost'].get('max')) if 'SCM Boost' in stats and 'min' in stats['SCM Boost'] and 'max' in stats['SCM Boost'] else str(boost)
            df_highlighted.loc[ship_name, header_names_raw[8]] = f"{h_base}<br>({h_boost})"

        # Pitch/Yaw/Roll
        vals = parse_value(row[header_names_raw[9]])
        if isinstance(vals, tuple) and len(vals) == 2 and isinstance(vals[0], tuple):
            (p, y, r), (pb, yb, rb) = vals
            
            # Check if stats are available and have min/max values before highlighting
            hp = highlight(p, stats['Pitch'].get('min'), stats['Pitch'].get('max')) if 'Pitch' in stats and 'min' in stats['Pitch'] and 'max' in stats['Pitch'] else str(p)
            hy = highlight(y, stats['Yaw'].get('min'), stats['Yaw'].get('max')) if 'Yaw' in stats and 'min' in stats['Yaw'] and 'max' in stats['Yaw'] else str(y)
            hr = highlight(r, stats['Roll'].get('min'), stats['Roll'].get('max')) if 'Roll' in stats and 'min' in stats['Roll'] and 'max' in stats['Roll'] else str(r)
            hpb = highlight(pb, stats['Pitch Boost'].get('min'), stats['Pitch Boost'].get('max')) if 'Pitch Boost' in stats and 'min' in stats['Pitch Boost'] and 'max' in stats['Pitch Boost'] else str(pb)
            hyb = highlight(yb, stats['Yaw Boost'].get('min'), stats['Yaw Boost'].get('max')) if 'Yaw Boost' in stats and 'min' in stats['Yaw Boost'] and 'max' in stats['Yaw Boost'] else str(yb)
            hrb = highlight(rb, stats['Roll Boost'].get('min'), stats['Roll Boost'].get('max')) if 'Roll Boost' in stats and 'min' in stats['Roll Boost'] and 'max' in stats['Roll Boost'] else str(rb)
            
            df_highlighted.loc[ship_name, header_names_raw[9]] = f"{hp}/{hy}/{hr}<br>({hpb}/{hyb}/{hrb})"

    # --- Reconstruct the Markdown Table ---
    new_md_lines = [header_line, divider]
    for ship_name, row in df_highlighted.iterrows():
        clean_ship_name = re.sub(r'<[^>]+>', '', ship_name).strip()
        cols = [f" {clean_ship_name} "] + [f" {str(c).strip()} " for c in row.values]
        new_md_lines.append('|' + '|'.join(cols) + '|')
        
    return '\n'.join(new_md_lines)


def process_file(file_path):
    """Main function to read a file, process all tables, and write the changes back."""
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' not found.")
        return False
        
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all markdown tables in the file
    tables = re.findall(r'(\|(?:[^\n]+\|)+\n\|(?::?-+:?\|)+[\s\S]*?(?=\n\n|\n---|\Z))', content)
    
    if len(tables) < 3:
        print(f"Warning: Found {len(tables)} tables, expected 3 for the ship comparison file.")
        if len(tables) == 0:
            print("No tables found in the file.")
            return False

    # For the original ship comparison file, use specific table names
    if 'alpha-4.3-medium-fighter-compare' in file_path and len(tables) >= 3:
        original_tables = {
            'main': tables[0],
            'mk1': tables[1],
            'cutlass': tables[2]
        }
    else:
        # For other files, process all tables found
        original_tables = {f'table_{i+1}': table for i, table in enumerate(tables)}

    new_content = content
    tables_processed = 0
    
    for key, table_md in original_tables.items():
        try:
            print(f"Processing table: {key}")
            processed_table = process_table(table_md)
            new_content = new_content.replace(table_md, processed_table)
            tables_processed += 1
        except Exception as e:
            print(f"Error processing table '{key}': {e}")
            import traceback
            traceback.print_exc()
            
    # Overwrite the original file with the new, updated content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print(f"File '{file_path}' has been updated. {tables_processed} table(s) processed.")
    return True


if __name__ == '__main__':
    # Allow file path to be passed as command line argument
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        # Default to the ship comparison file
        file_path = 'c:/Users/ppong/VSCodeProject/star-citizen-handbook/content/ships/alpha-4.3-medium-fighter-compare/index.md'
    
    process_file(file_path)
