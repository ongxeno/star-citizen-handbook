#!/usr/bin/env python3
"""Debug script to check SCM Speed highlighting calculations."""

def highlight(val, min_v, max_v, low_threshold=0.2, high_threshold=0.2, is_bad_low=True):
    """Applies a color-coded <span> tag to a value based on its position within a range."""
    if val is None or min_v is None or max_v is None:
        return ''
        
    range_v = max_v - min_v
    if range_v == 0:
        return f"{val:,.0f}" if val == int(val) else f"{val:,.1f}"

    # Set the thresholds for highlighting based on user input
    low_thresh = min_v + range_v * low_threshold
    high_thresh = max_v - range_v * high_threshold

    # Format the number with commas
    str_val = f"{val:,.0f}" if val == int(val) else f"{val:,.1f}"

    print(f"Value: {val}, Min: {min_v}, Max: {max_v}")
    print(f"Range: {range_v}, Low threshold: {low_thresh}, High threshold: {high_thresh}")
    print(f"is_bad_low: {is_bad_low}")

    # Apply color based on whether a low value is good or bad
    if is_bad_low: # Higher is better
        if val <= low_thresh:
            print(f"→ RED (val {val} <= low_thresh {low_thresh})")
            return f'<span style="color:#FF6B6B">{str_val}</span>'
        if val >= high_thresh:
            print(f"→ GREEN (val {val} >= high_thresh {high_thresh})")
            return f'<span style="color:#4ECDC4">{str_val}</span>'
        print(f"→ NORMAL (val {val} between thresholds)")
    else: # Lower is better
        if val <= low_thresh:
            print(f"→ GREEN (val {val} <= low_thresh {low_thresh})")
            return f'<span style="color:#4ECDC4">{str_val}</span>'
        if val >= high_thresh:
            print(f"→ RED (val {val} >= high_thresh {high_thresh})")
            return f'<span style="color:#FF6B6B">{str_val}</span>'
        print(f"→ NORMAL (val {val} between thresholds)")
            
    return str_val

# Test SCM Speed values from the first table
scm_speeds = [220, 220, 220, 215, 215, 220, 227, 218, 229, 222]
min_speed = min(scm_speeds)
max_speed = max(scm_speeds)

print(f"SCM Speed range: {min_speed} - {max_speed}")
print(f"Values: {scm_speeds}")
print("\nTesting each value:")

for speed in scm_speeds:
    print(f"\n--- Testing {speed} ---")
    result = highlight(speed, min_speed, max_speed, 0.2, 0.2, True)
    print(f"Result: {result}\n")
