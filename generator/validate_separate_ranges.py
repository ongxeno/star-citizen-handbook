import re

def parse_value(v_str):
    """Parse Pitch/Yaw/Roll values from the markdown."""
    v_str = str(v_str).strip()
    v_str = re.sub(r'<[^>]+>', '', v_str)  # Remove HTML tags
    
    # Regex for 'P/Y/R<br>(Boosted P/Y/R)' format
    pyr_br_match = re.search(r'([\d,.]+)/([\d,.]+)/([\d,.]+)\s*<br>\s*\(([\d,.]+)/([\d,.]+)/([\d,.]+)\)', v_str)
    if pyr_br_match:
        base = tuple(float(g.replace(',', '')) for g in pyr_br_match.groups()[:3])
        boost = tuple(float(g.replace(',', '')) for g in pyr_br_match.groups()[3:])
        return (base, boost)
    return None

# Current highlighted data from the file
highlighted_data = [
    "52/43/148<br>(62.4/51.6/177.6)",          # F7C Hornet Mk II - no highlighting  
    "52/43/148<br>(62.4/51.6/177.6)",          # Hornet Tracker Mk II - no highlighting
    "50/40/140<br>(60/48/168)",                # Super Hornet Mk II - yaw=red, roll=red, yaw_boost=red, roll_boost=red
    "50/40/140<br>(60/48/168)",                # Hornet Heartseeker Mk II - same as above
    "51/42/147<br>(61.2/50.4/176.4)",         # Hornet Ghost Mk II - yaw=red, yaw_boost=red
    "58/58/160<br>(69.6/69.6/192)",           # San'tok.yāi - ALL GREEN
    "60/43/155<br>(72/51.6/186)",             # Glaive - pitch=green, pitch_boost=green
    "46/38/155<br>(55.2/45.6/186)",           # Meteor - pitch=red, yaw=red, pitch_boost=red, yaw_boost=red
    "56/52/147<br>(67.2/62.4/176.4)"          # Scythe - no highlighting
]

# Parse and collect all values
all_data = []
for item in highlighted_data:
    parsed = parse_value(item)
    print(f"'{item}' -> {parsed}")
    if parsed:
        all_data.append(parsed)

print(f"\nTotal parsed data: {len(all_data)}")
print(f"All data: {all_data}")

if not all_data:
    print("ERROR: No data was parsed!")
    exit(1)

# Separate into 6 categories
pitch_values = [d[0][0] for d in all_data]
yaw_values = [d[0][1] for d in all_data]
roll_values = [d[0][2] for d in all_data]
pitch_boost_values = [d[1][0] for d in all_data]
yaw_boost_values = [d[1][1] for d in all_data]
roll_boost_values = [d[1][2] for d in all_data]

categories = {
    'Pitch': pitch_values,
    'Yaw': yaw_values,
    'Roll': roll_values,
    'Pitch Boost': pitch_boost_values,
    'Yaw Boost': yaw_boost_values,
    'Roll Boost': roll_boost_values
}

print("VALIDATION: Separate Range Calculation (20% thresholds)")
print("=" * 65)

for category, values in categories.items():
    if not values:
        continue
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val
    
    # 20% thresholds
    low_threshold = min_val + range_val * 0.2
    high_threshold = max_val - range_val * 0.2
    
    red_values = [v for v in values if v <= low_threshold]
    green_values = [v for v in values if v >= high_threshold]
    
    print(f"{category}:")
    print(f"  Range: {min_val} - {max_val} (span: {range_val})")
    print(f"  Red threshold: ≤ {low_threshold:.1f}")
    print(f"  Green threshold: ≥ {high_threshold:.1f}")
    print(f"  RED values: {red_values}")
    print(f"  GREEN values: {green_values}")
    print()

print("Ship-by-ship expected highlighting:")
print("-" * 40)
ships = ["F7C Hornet Mk II", "Hornet Tracker Mk II", "Super Hornet Mk II", "Hornet Heartseeker Mk II", 
         "Hornet Ghost Mk II", "San'tok.yāi", "Glaive", "Meteor", "Scythe"]

for i, ship in enumerate(ships):
    data = all_data[i]
    base_values = data[0]  # (pitch, yaw, roll)
    boost_values = data[1]  # (pitch_boost, yaw_boost, roll_boost)
    
    print(f"{ship}:")
    print(f"  Pitch: {base_values[0]} -> {'RED' if base_values[0] in [v for v in pitch_values if v <= min(pitch_values) + (max(pitch_values) - min(pitch_values)) * 0.2] else 'GREEN' if base_values[0] in [v for v in pitch_values if v >= max(pitch_values) - (max(pitch_values) - min(pitch_values)) * 0.2] else 'normal'}")
    print(f"  Yaw: {base_values[1]} -> {'RED' if base_values[1] in [v for v in yaw_values if v <= min(yaw_values) + (max(yaw_values) - min(yaw_values)) * 0.2] else 'GREEN' if base_values[1] in [v for v in yaw_values if v >= max(yaw_values) - (max(yaw_values) - min(yaw_values)) * 0.2] else 'normal'}")
    print(f"  Roll: {base_values[2]} -> {'RED' if base_values[2] in [v for v in roll_values if v <= min(roll_values) + (max(roll_values) - min(roll_values)) * 0.2] else 'GREEN' if base_values[2] in [v for v in roll_values if v >= max(roll_values) - (max(roll_values) - min(roll_values)) * 0.2] else 'normal'}")
    print()
