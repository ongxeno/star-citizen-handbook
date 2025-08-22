import re
import pandas as pd
from io import StringIO

def parse_value(v_str):
    """Cleans and parses a string from the table into a numeric value or tuple."""
    v_str = str(v_str).strip()
    # Remove any HTML tags (like <span>) to get the raw value
    v_str = re.sub(r'<[^>]+>', '', v_str)
    if v_str == 'N/A':
        return None
    
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

    # Regex for a simple number (with or without commas)
    simple_match = re.match(r'^[\d,.]+$', v_str)
    if simple_match:
        return float(v_str.replace(',', ''))
        
    # Return the original string if no numeric pattern is matched
    return v_str

# Test the Pitch/Yaw/Roll values
test_values = [
    "52/43/148<br>(62.4/51.6/177.6)",
    "50/40/140<br>(60/48/168)",
    "58/58/160<br>(69.6/69.6/192)",
    "60/43/155<br>(72/51.6/186)"
]

print("Testing Pitch/Yaw/Roll parsing:")
for val in test_values:
    parsed = parse_value(val)
    print(f"'{val}' -> {parsed}")
    print(f"  Type: {type(parsed)}")
    if isinstance(parsed, tuple):
        print(f"  Base values: {parsed[0]}")
        print(f"  Boosted values: {parsed[1]}")
    print()

# Test if we can extract numeric data
print("Testing numeric extraction:")
numeric_data = []
for val in test_values:
    parsed = parse_value(val)
    if isinstance(parsed, tuple) and len(parsed) == 2:
        if isinstance(parsed[0], tuple) and isinstance(parsed[1], tuple):
            # This is pitch/yaw/roll data
            numeric_data.extend(parsed[0])  # Add base values
            numeric_data.extend(parsed[1])  # Add boosted values
        elif all(isinstance(x, (int, float)) for x in parsed):
            numeric_data.extend(parsed)

print(f"Extracted numeric values: {numeric_data}")
print(f"Number of numeric values: {len(numeric_data)}")
