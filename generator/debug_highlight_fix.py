def is_higher_better(column_name):
    """
    Determine if higher values are better for a given column.
    """
    column_lower = column_name.lower()
    
    # Columns where higher values are better
    higher_better_keywords = [
        'speed', 'velocity', 'acceleration', 'range', 'health', 'shield', 
        'armor', 'damage', 'dps', 'fire rate', 'capacity', 'storage', 
        'power', 'thrust', 'quantum fuel', 'hydrogen fuel'
    ]
    
    # Check for higher is better keywords
    for keyword in higher_better_keywords:
        if keyword in column_lower:
            return True
    
    # Default: assume higher is better
    return True

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

# Test with SCM Speed values from the table
scm_values = [220, 220, 220, 215, 215, 220, 227, 218, 229, 222]
min_val = min(scm_values)  # 215
max_val = max(scm_values)  # 229

print("SCM Speed highlighting test:")
print(f"Range: {min_val} to {max_val}")
print(f"20% thresholds: low={min_val + (max_val-min_val)*0.2:.1f}, high={max_val - (max_val-min_val)*0.2:.1f}")
print()

# Test both approaches
column_name = "SCM Speed (Boost)"
is_higher_better_result = is_higher_better(column_name)
print(f"is_higher_better('{column_name}') = {is_higher_better_result}")
print()

# Test with corrected logic (don't invert)
is_bad_low = is_higher_better_result  # CORRECTED: don't invert
print(f"Using is_bad_low = {is_bad_low} (corrected logic)")

for val in scm_values:
    result = highlight(val, min_val, max_val, 0.2, 0.2, is_bad_low)
    print(f"  {val} -> {result}")
