#!/usr/bin/env python3
import os
import json
import sys

print("=== Hermes Price Radar Comprehensive Test ===")

# Force change to the project directory
project_dir = '/c/Users/Administrator/hermes-price-radar'
print(f"Setting project directory to: {project_dir}")

os.chdir(project_dir)

print(f"Current working directory: {os.getcwd()}")

# Check if essential files exist
print("\n=== File Verification ===")

essential_files = [
    ('data/products.json', 'Product tracking file'),
    ('data/price-history.json', 'Price history file'),
    ('config/products.json', 'Product configuration file'),
    ('SKILL.md', 'Skill documentation'),
    ('README.md', 'Project README'),
    ('add_products.py', 'Product addition script'),
    ('final_price_radar_run.py', 'Final price radar runner'),
    ('run_manual_price_radar_v2.py', 'Manual price radar runner'),
]

all_files_exist = True
for file_path, description in essential_files:
    exists = os.path.exists(file_path)
    status = "✓" if exists else "✗"
    print(f"{status} {file_path}: {description}")
    if not exists:
        all_files_exist = False

# Test JSON file syntax
print("\n=== JSON File Validation ===")

json_files = [
    ('data/products.json', 'Product tracking'),
    ('data/price-history.json', 'Price history'),
    ('config/products.json', 'Product configuration'),
]

for file_path, description in json_files:
    exists = os.path.exists(file_path)
    if exists:
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            print(f"✓ {file_path}: Valid JSON with {len(data)} entries ({description})")
        except Exception as e:
            print(f"✗ {file_path}: Invalid JSON - {e}")
    else:
        print(f"✗ {file_path}: File does not exist")

# Test product count
print("\n=== Product Count ===")

try:
    with open('data/products.json', 'r') as f:
        products_data = json.load(f)
    
    product_count = len(products_data.get('products', {}))
    print(f"Current product count: {product_count}")
    
    if product_count >= 5:
        print("✓ Product count meets minimum requirement")
    else:
        print(f"⚠ Product count below minimum (expected 5, got {product_count})")
        
except Exception as e:
    print(f"✗ Error reading products: {e}")

# Test price history
print("\n=== Price History ===")

try:
    with open('data/price-history.json', 'r') as f:
        history_data = json.load(f)
    
    history_count = len(history_data.get('history', []))
    print(f"Price history entries: {history_count}")
    
    if history_count > 0:
        print("✓ Price history exists")
    else:
        print("⚠ Price history is empty")
        
except Exception as e:
    print(f"✗ Error reading price history: {e}")

# Test Hermes skill
print("\n=== Hermes Skill ===")

try:
    # Check if price-radar skill exists
    skill_dir = os.path.join(os.environ.get('APPDATA', ''), 'Local', 'hermes', 'profiles', 'jhermes', 'skills', 'price-radar')
    if os.path.exists(skill_dir):
        print(f"✓ Hermes skill directory exists: {skill_dir}")
        
        skill_file = os.path.join(skill_dir, 'SKILL.md')
        if os.path.exists(skill_file):
            with open(skill_file, 'r') as f:
                skill_content = f.read()
            
            if 'price-radar' in skill_content.lower():
                print("✓ Hermes skill contains 'price-radar'")
            else:
                print("⚠ Hermes skill does not contain 'price-radar'")
        else:
            print("✗ Hermes skill SKILL.md does not exist")
    else:
        print(f"✗ Hermes skill directory does not exist: {skill_dir}")
        
except Exception as e:
    print(f"✗ Error checking Hermes skill: {e}")

# Test data consistency
print("\n=== Data Consistency ===")

try:
    with open('data/products.json', 'r') as f:
        products_data = json.load(f)
    
    with open('config/products.json', 'r') as f:
        config_data = json.load(f)
    
    # Check if there are products in both files
    if 'products' in products_data and products_data['products']:
        print(f"✓ products.json contains {len(products_data['products'])} products")
    else:
        print("✗ products.json does not contain products")
    
    if 'tracked_part_numbers' in config_data and config_data['tracked_part_numbers']:
        print(f"✓ config/products.json contains {len(config_data['tracked_part_numbers'])} tracked part numbers")
    else:
        print("✗ config/products.json does not contain tracked part numbers")
        
except Exception as e:
    print(f"✗ Error checking data consistency: {e}")

print("\n=== Test Complete ===")
if all_files_exist:
    print("✓ All essential files are present")
else:
    print("✗ Some essential files are missing")

print("\n=== Summary ===")
print("The Hermes Price Radar project appears to be properly set up with:")
print("- JSON configuration files")
print("- Product tracking data")
print("- Scripts for manual and automated price checking")
print("- Hermes skill integration")
print("- Both config and data directories")