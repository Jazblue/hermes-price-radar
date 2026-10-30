#!/usr/bin/env python3
import json

# Read the corrupted products.json file
with open('data/products.json', 'r') as f:
    content = f.read()

print("First 50 characters of original content:")
print(repr(content[:50]))
print()

# Check if we have line numbers
lines = content.split('\n')
print("First 5 lines of original content:")
for i, line in enumerate(lines[:5]):
    print(f"{i+1}: {repr(line)}")
print()

# Try to parse the original JSON directly
try:
    data_original = json.loads(content)
    print("Successfully parsed original JSON")
except json.JSONDecodeError as e:
    print(f"Failed to parse original JSON: {e}")
    print(f"Position: {e.pos}")
    print(f"Content around position {e.pos}: {repr(content[max(0, e.pos-50):e.pos+50])}")

# Now try with line number stripping
print("\nTrying line number stripping...")
import re
cleaned_content = re.sub(r'^\s*\d+\|', '', content, flags=re.MULTILINE)

# Check first 50 characters of cleaned content
print("First 50 characters of cleaned content:")
print(repr(cleaned_content[:50]))
print()

# Try to parse the cleaned JSON
try:
    data_cleaned = json.loads(cleaned_content)
    print(f"Successfully parsed cleaned JSON with {len(data_cleaned['products'])} products")
    
    # Save the cleaned version
    with open('data/products_cleaned.json', 'w') as f:
        json.dump(data_cleaned, f, indent=2)
    print("Saved cleaned JSON to products_cleaned.json")
    
except json.JSONDecodeError as e:
    print(f"Failed to parse cleaned JSON: {e}")
    print(f"Position: {e.pos}")
    print(f"Content around position {e.pos}: {repr(cleaned_content[max(0, e.pos-50):e.pos+50])}")