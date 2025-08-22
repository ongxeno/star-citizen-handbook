import re
import pandas as pd
from io import StringIO
import traceback

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

def test_single_table():
    # Load the file and extract just the first table
    file_path = 'c:/Users/ppong/VSCodeProject/star-citizen-handbook/content/ships/alpha-4.3-medium-fighter-compare/index.md'
    
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all markdown tables in the file
    tables = re.findall(r'(\|(?:[^\n]+\|)+\n\|(?::?-+:?\|)+[\s\S]*?(?=\n\n|\n---|\Z))', content)
    
    if not tables:
        print("No tables found")
        return
    
    print(f"Found {len(tables)} tables")
    
    # Test the first table
    table_md = tables[0]
    print(f"First table:\n{table_md[:500]}...")
    
    try:
        lines = table_md.strip().split('\n')
        
        # Find the header line (contains 'Ship')
        header_line = None
        for i, line in enumerate(lines):
            if 'Ship' in line:
                header_line = line
                break
        
        if not header_line:
            print("No header line found")
            return
            
        # Get all data rows (skip header and separator)
        data_lines = []
        in_data = False
        for line in lines:
            if '---' in line or ':---:' in line:
                in_data = True
                continue
            if in_data and line.strip():
                data_lines.append(line)
        
        print(f"Found {len(data_lines)} data rows")
        
        # Create DataFrame from the data
        table_data = []
        for line in data_lines:
            row_data = [cell.strip() for cell in line.strip().split('|')[1:-1]]
            table_data.append(row_data)
        
        # Clean and assign header names
        header_names = [h.strip() for h in header_line.strip().split('|')[1:-1]]
        
        print("Headers:")
        for i, h in enumerate(header_names):
            print(f"  {i}: {h}")
        
        df = pd.DataFrame(table_data, columns=header_names)
        df = df.set_index(header_names[0])
        
        print("\nDataFrame shape:", df.shape)
        print("DataFrame:")
        print(df)
        
        # Test specific columns
        print("\nTesting Shield HP column:")
        shield_hp_column = None
        for i, col_name in enumerate(header_names):
            if 'Shield HP' in col_name or 'Stock Shield HP' in col_name:
                shield_hp_column = col_name
                print(f"Found Shield HP column: {col_name}")
                break
        
        if shield_hp_column:
            shield_hp_data = df[shield_hp_column].apply(parse_value)
            print("Parsed Shield HP data:")
            for ship, val in shield_hp_data.items():
                print(f"  {ship}: {val} (type: {type(val)})")
                
            # Calculate stats
            numeric_data = shield_hp_data.dropna()
            numeric_only = [x for x in numeric_data if isinstance(x, (int, float))]
            print(f"Numeric Shield HP values: {numeric_only}")
            if numeric_only:
                print(f"Min: {min(numeric_only)}, Max: {max(numeric_only)}")
        
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

if __name__ == '__main__':
    test_single_table()
