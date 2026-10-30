#!/usr/bin/env python3
import os
import json
import sys

print("=== Hermes Price Radar Verification ===")

# Get the current working directory
project_dir = os.getcwd()
print(f"Project directory: {project_dir}")

# Print the current working directory
cwd = os.getcwd()
print(f"Current working directory: {cwd}")

# Print the absolute path of the current directory
abs_path = os.path.abspath(project_dir)
print(f"Absolute path: {abs_path}")

# Check if data directory exists
data_dir = os.path.join(project_dir, 'data')
print(f"Data directory exists: {os.path.exists(data_dir)}")

if os.path.exists(data_dir):
    print(f"Files in data directory:")
    for file in os.listdir(data_dir):
        print(f"  {file}")
else:
    print("data directory does not exist")

# Check if config directory exists
config_dir = os.path.join(project_dir, 'config')
print(f"Config directory exists: {os.path.exists(config_dir)}")

if os.path.exists(config_dir):
    print(f"Files in config directory:")
    for file in os.listdir(config_dir):
        print(f"  {file}")
else:
    print("config directory does not exist")

# Try to read the JSON files
print("\nTrying to read JSON files:")

if os.path.exists(os.path.join(data_dir, 'products.json')):
    try:
        with open(os.path.join(data_dir, 'products.json'), 'r') as f:
            data = json.load(f)
        print(f"✓ data/products.json is valid JSON with {len(data)} entries")
    except Exception as e:
        print(f"✗ data/products.json is invalid: {e}")
else:
    print("✗ data/products.json does not exist")

if os.path.exists(os.path.join(data_dir, 'price-history.json')):
    try:
        with open(os.path.join(data_dir, 'price-history.json'), 'r') as f:
            data = json.load(f)
        print(f"✓ data/price-history.json is valid JSON with {len(data)} entries")
    except Exception as e:
        print(f"✗ data/price-history.json is invalid: {e}")
else:
    print("✗ data/price-history.json does not exist")

if os.path.exists(os.path.join(config_dir, 'products.json')):
    try:
        with open(os.path.join(config_dir, 'products.json'), 'r') as f:
            data = json.load(f)
        print(f"✓ config/products.json is valid JSON")
    except Exception as e:
        print(f"✗ config/products.json is invalid: {e}")
else:
    print("✗ config/products.json does not exist")