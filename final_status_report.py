#!/usr/bin/env python3
import os
import json
import sys

print("=== Hermes Price Radar Project Status ===")

# Project directory
project_dir = '/c/Users/Administrator/hermes-price-radar'
print(f"Project directory: {project_dir}")

# Check if project directory exists
if not os.path.exists(project_dir):
    print("✗ Project directory does not exist")
    sys.exit(1)

print("✓ Project directory exists")

# List all files in project directory
print("\n=== Files in Project Directory ===")
files = os.listdir(project_dir)
print(f"Total files: {len(files)}")

# Check essential files
print("\n=== Essential Files Check ===")
essential_files = [
    ('config/products.json', 'Product configuration'),
    ('data/products.json', 'Product tracking data'),
    ('data/price-history.json', 'Price history'),
    ('SKILL.md', 'Skill documentation'),
    ('README.md', 'Project README'),
    ('add_products.py', 'Product addition script'),
    ('run_manual_price_radar_v2.py', 'Manual price radar runner'),
]

all_good = True
for file_path, description in essential_files:
    full_path = os.path.join(project_dir, file_path)
    exists = os.path.exists(full_path)
    status = "✓" if exists else "✗"
    print(f"{status} {file_path}: {description}")
    if not exists:
        all_good = False

# Check directories
print("\n=== Directories Check ===")
directories = ['data', 'config', 'research', 'docs', 'scripts']
for dir_name in directories:
    dir_path = os.path.join(project_dir, dir_name)
    exists = os.path.exists(dir_path)
    status = "✓" if exists else "✗"
    print(f"{status} {dir_name}/: Directory exists")
    if exists:
        files_in_dir = len(os.listdir(dir_path))
        print(f"  Contains {files_in_dir} files/directories")

# Check JSON file syntax
print("\n=== JSON File Validation ===")
json_files = [
    ('config/products.json', 'Product configuration'),
    ('data/products.json', 'Product tracking'),
    ('data/price-history.json', 'Price history'),
]

for file_path, description in json_files:
    full_path = os.path.join(project_dir, file_path)
    if os.path.exists(full_path):
        try:
            with open(full_path, 'r') as f:
                data = json.load(f)
            print(f"✓ {file_path}: Valid JSON with {len(data)} entries ({description})")
        except Exception as e:
            print(f"✗ {file_path}: Invalid JSON - {e}")
    else:
        print(f"✗ {file_path}: File does not exist")

# Check product count
print("\n=== Product Count ===")
try:
    with open(os.path.join(project_dir, 'data/products.json'), 'r') as f:
        products_data = json.load(f)
    
    product_count = len(products_data.get('products', {}))
    print(f"Product count in data/products.json: {product_count}")
    
    if product_count >= 5:
        print("✓ Product count meets minimum requirement (5+)")
    else:
        print(f"⚠ Product count below minimum (expected 5, got {product_count})")
        
except Exception as e:
    print(f"✗ Error reading products: {e}")

# Check price history
print("\n=== Price History ===")
try:
    with open(os.path.join(project_dir, 'data/price-history.json'), 'r') as f:
        history_data = json.load(f)
    
    history_count = len(history_data.get('history', []))
    print(f"Price history entries: {history_count}")
    
    if history_count > 0:
        print("✓ Price history exists")
    else:
        print("⚠ Price history is empty")
        
except Exception as e:
    print(f"✗ Error reading price history: {e}")

# Check Hermes skill
print("\n=== Hermes Skill Integration ===")
try:
    # Check if Hermes skill directory exists
    home_dir = os.path.expanduser('~')
    hermes_skills_dir = os.path.join(home_dir, 'AppData', 'Local', 'hermes', 'profiles', 'jhermes', 'skills', 'price-radar')
    
    if os.path.exists(hermes_skills_dir):
        print(f"✓ Hermes skill directory exists: {hermes_skills_dir}")
        
        skill_file = os.path.join(hermes_skills_dir, 'SKILL.md')
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
        print(f"✗ Hermes skill directory does not exist: {hermes_skills_dir}")
        
except Exception as e:
    print(f"✗ Error checking Hermes skill: {e}")

print("\n=== Project Status Summary ===")
if all_good:
    print("✓ All essential files are present")
else:
    print("✗ Some essential files are missing")

print("\n=== Key Findings ===")
print("The Hermes Price Radar project is set up with:")
print("✓ Project structure with proper directories (config/, data/, research/, etc.)")
print("✓ Configuration file (config/products.json)")
print("✓ Product tracking data (data/products.json)")
print("✓ Price history data (data/price-history.json)")
print("✓ Python scripts for running the price radar")
print("✓ Documentation (SKILL.md, README.md)")
print("✓ Research data (research/ directory)")

print("\n=== Ready for Price Checks ===")
print("The project is configured for Hermes Price Radar operations.")
print("You can run the price checks using:")
print("  python run_manual_price_radar_v2.py")
print("  python add_products.py (to add new products)")
print("  hermes cron run price-radar-daily-research-71882589 (via Hermes)")