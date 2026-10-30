#!/usr/bin/env python3
import os
import json
import sys

print("=== Hermes Price Radar Status Test ===")

# Print the current working directory
print(f"Current working directory: {os.getcwd()}")

# Print the absolute path of the project directory
project_dir = os.path.abspath('/c/Users/Administrator/hermes-price-radar')
print(f"Project directory: {project_dir}")

# Change to the project directory
os.chdir(project_dir)

print(f"Changed working directory to: {os.getcwd()}")

# List files in the current directory
print("\nFiles in current directory:")
for file in os.listdir('.'):
    print(f"  {file}")

# Check for data directory
if os.path.exists('data'):
    print("\nFiles in data directory:")
    for file in os.listdir('data'):
        print(f"  data/{file}")
else:
    print("\ndata directory does not exist")

# Check for specific files
print("\nChecking specific files:")
specific_files = ['data/products.json', 'data/price-history.json', 'config/products.json']
for file_path in specific_files:
    full_path = os.path.abspath(file_path)
    print(f"{file_path}: exists={os.path.exists(file_path)}, full_path={full_path}")

# Try to read the JSON files if they exist
print("\nTrying to read JSON files:")
if os.path.exists('data/products.json'):
    try:
        with open('data/products.json', 'r') as f:
            data = json.load(f)
        print(f"✓ data/products.json is valid JSON with {len(data)} entries")
    except Exception as e:
        print(f"✗ data/products.json is invalid: {e}")
else:
    print("✗ data/products.json does not exist")

if os.path.exists('data/price-history.json'):
    try:
        with open('data/price-history.json', 'r') as f:
            data = json.load(f)
        print(f"✓ data/price-history.json is valid JSON with {len(data)} entries")
    except Exception as e:
        print(f"✗ data/price-history.json is invalid: {e}")
else:
    print("✗ data/price-history.json does not exist")

if os.path.exists('config/products.json'):
    try:
        with open('config/products.json', 'r') as f:
            data = json.load(f)
        print(f"✓ config/products.json is valid JSON")
    except Exception as e:
        print(f"✗ config/products.json is invalid: {e}")
else:
    print("✗ config/products.json does not exist")