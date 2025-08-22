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

# Test the function
test_columns = [
    "SCM Speed (Boost)",
    "Nav Speed (m/s)", 
    "Hull HP",
    "Stock DPS"
]

print("Testing is_higher_better function:")
for col in test_columns:
    result = is_higher_better(col)
    is_bad_low = not result
    print(f"Column: '{col}'")
    print(f"  is_higher_better() = {result}")
    print(f"  is_bad_low = {is_bad_low}")
    print(f"  Meaning: {'Higher values are better (green=high, red=low)' if result else 'Lower values are better (green=low, red=high)'}")
    print()
