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

    return v_str

# Test data from the file - let me extract some Pitch/Yaw/Roll values
pitch_yaw_roll_data = [
    "52/43/148<br>(62.4/51.6/177.6)",  # F7C Hornet Mk II
    "52/43/148<br>(62.4/51.6/177.6)",  # Hornet Tracker Mk II
    "50/40/140<br>(60/48/168)",        # Super Hornet Mk II
    "50/40/140<br>(60/48/168)",        # Hornet Heartseeker Mk II
    "51/42/147<br>(61.2/50.4/176.4)",  # Hornet Ghost Mk II
    "58/58/160<br>(69.6/69.6/192)",    # San'tok.yāi
    "60/43/155<br>(72/51.6/186)",      # Glaive
    "46/38/155<br>(55.2/45.6/186)",    # Meteor
    "56/52/147<br>(67.2/62.4/176.4)"   # Scythe
]

print("Analyzing Pitch/Yaw/Roll data ranges:")
print("=" * 60)

# Parse all values and separate into 6 categories
pitch_values = []
yaw_values = []
roll_values = []
pitch_boost_values = []
yaw_boost_values = []
roll_boost_values = []

for data in pitch_yaw_roll_data:
    parsed = parse_value(data)
    if isinstance(parsed, tuple) and len(parsed) == 2:
        base_tuple, boost_tuple = parsed
        if isinstance(base_tuple, tuple) and isinstance(boost_tuple, tuple):
            pitch_values.append(base_tuple[0])
            yaw_values.append(base_tuple[1])
            roll_values.append(base_tuple[2])
            pitch_boost_values.append(boost_tuple[0])
            yaw_boost_values.append(boost_tuple[1])
            roll_boost_values.append(boost_tuple[2])

# Calculate statistics for each category
categories = {
    'Pitch': pitch_values,
    'Yaw': yaw_values, 
    'Roll': roll_values,
    'Pitch Boost': pitch_boost_values,
    'Yaw Boost': yaw_boost_values,
    'Roll Boost': roll_boost_values
}

print(f"{'Category':<15} {'Min':<8} {'Max':<8} {'Range':<8} {'Values'}")
print("-" * 70)

all_values = []
for category, values in categories.items():
    if values:
        min_val = min(values)
        max_val = max(values)
        range_val = max_val - min_val
        all_values.extend(values)
        print(f"{category:<15} {min_val:<8.1f} {max_val:<8.1f} {range_val:<8.1f} {values}")

print("\n" + "=" * 60)
print("CURRENT IMPLEMENTATION TEST:")
print("=" * 60)

# Test what the current implementation would do (combine all values)
print(f"All combined values: {sorted(all_values)}")
print(f"Combined Min: {min(all_values):.1f}")
print(f"Combined Max: {max(all_values):.1f}")
print(f"Combined Range: {max(all_values) - min(all_values):.1f}")

# Test thresholds with 10% (as used in the test)
combined_min = min(all_values)
combined_max = max(all_values)
combined_range = combined_max - combined_min
low_threshold_10 = combined_min + combined_range * 0.1
high_threshold_10 = combined_max - combined_range * 0.1

print(f"\nWith 10% thresholds:")
print(f"Low threshold (red): {low_threshold_10:.1f}")
print(f"High threshold (green): {high_threshold_10:.1f}")

print("\nValues that should be RED (≤ low threshold):")
red_values = [v for v in all_values if v <= low_threshold_10]
print(sorted(set(red_values)))

print("\nValues that should be GREEN (≥ high threshold):")
green_values = [v for v in all_values if v >= high_threshold_10]
print(sorted(set(green_values)))

print("\n" + "=" * 60)
print("SEPARATE RANGE ANALYSIS:")
print("=" * 60)

print("If we calculated separate ranges for each category:")
for category, values in categories.items():
    if values:
        cat_min = min(values)
        cat_max = max(values)
        cat_range = cat_max - cat_min
        cat_low_10 = cat_min + cat_range * 0.1
        cat_high_10 = cat_max - cat_range * 0.1
        
        print(f"\n{category}:")
        print(f"  Range: {cat_min:.1f} - {cat_max:.1f}")
        print(f"  Low threshold (10%): {cat_low_10:.1f}")
        print(f"  High threshold (10%): {cat_high_10:.1f}")
        print(f"  Red values: {[v for v in values if v <= cat_low_10]}")
        print(f"  Green values: {[v for v in values if v >= cat_high_10]}")
