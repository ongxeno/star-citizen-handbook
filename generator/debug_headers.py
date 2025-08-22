import re
import pandas as pd
from io import StringIO

file_path = 'c:/Users/ppong/VSCodeProject/star-citizen-handbook/content/ships/alpha-4.3-medium-fighter-compare/index.md'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Find all markdown tables in the file
tables = re.findall(r'(\|(?:[^\n]+\|)+\n\|(?::?-+:?\|)+[\s\S]*?(?=\n\n|\n---|\Z))', content)

if tables:
    table_md = tables[0]  # First table
    lines = table_md.strip().split('\n')
    
    # Find the header line
    header_line = None
    for line in lines:
        if 'Ship' in line:
            header_line = line
            break
    
    if header_line:
        # Get raw header names
        header_names_raw = [h.strip() for h in header_line.strip().split('|')[1:-1]]
        print("Raw header names:")
        for i, h in enumerate(header_names_raw):
            print(f"  {i}: '{h}'")
        
        # Get clean header names
        header_names = [re.sub(r'<[^>]+>', '', h).strip() for h in header_names_raw]
        print("\nClean header names:")
        for i, h in enumerate(header_names):
            print(f"  {i}: '{h}'")
        
        # Check specifically for SCM column
        print(f"\nSCM column raw: '{header_names_raw[7]}'")
        print(f"SCM column clean: '{header_names[7]}'")
        
        # Check array bounds
        print(f"Total headers: {len(header_names_raw)}")
        if len(header_names_raw) > 7:
            print(f"Index 7 is valid")
        else:
            print(f"Index 7 is OUT OF BOUNDS")
