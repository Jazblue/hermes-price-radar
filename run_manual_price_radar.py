#!/usr/bin/env python3
import subprocess
import json
import sys
import os

print("=== Hermes Price Radar Manual Job Trigger ===")
print(f"Working directory: {os.getcwd()}")

# Change to the hermes-price-radar directory
os.chdir('/c/Users/Administrator/hermes-price-radar')

# Check if products.json exists
if not os.path.exists('data/products.json'):
    print("ERROR: data/products.json not found")
    sys.exit(1)

print("✓ products.json exists")

# Check if products_cleaned.json exists
cleaned_path = 'data/products_cleaned.json'
if os.path.exists(cleaned_path):
    print(f"✓ {cleaned_path} exists")
else:
    print(f"✗ {cleaned_path} does not exist")

# Check for the main price radar skill
if os.path.exists('SKILL.md'):
    print("✓ SKILL.md exists")
    
    # Try to run a simple test
    print("\nAttempting to run price radar skill...")
    
    # Try to read the skill
    with open('SKILL.md', 'r') as f:
        skill_content = f.read()
    
    if 'price-radar' in skill_content.lower():
        print("✓ SKILL.md mentions price-radar")
    else:
        print("✗ SKILL.md does not mention price-radar")
        
else:
    print("✗ SKILL.md not found")

# Check if add_products.py exists
if os.path.exists('add_products.py'):
    print("✓ add_products.py exists")
    
    # Try to run it
    print("\nAttempting to run add_products.py...")
    try:
        result = subprocess.run(['python', 'add_products.py'], capture_output=True, text=True, timeout=30)
        print(f"Return code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
    except subprocess.TimeoutExpired:
        print("ERROR: add_products.py timed out after 30 seconds")
    except Exception as e:
        print(f"ERROR: {e}")
else:
    print("✗ add_products.py not found")

# Try to run Hermes cron job directly
print("\n=== Attempting to run Hermes cron job directly ===")
job_name = "price-radar-daily-research-71882589"

# Check if hermes is available
try:
    result = subprocess.run(['which', 'hermes'], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Hermes not found in PATH")
        sys.exit(1)
    print(f"Hermes found at: {result.stdout.strip()}")
except Exception as e:
    print(f"Error checking Hermes: {e}")
    sys.exit(1)

# Try to run the cron job
print(f"\nRunning cron job: {job_name}")
cmd = ['hermes', 'cron', 'run', job_name]

# Set a timeout
try:
    print(f"Command: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    print(f"\nReturn code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
        
    if result.returncode == 0:
        print(f"\n✓ SUCCESS: Cron job '{job_name}' completed successfully")
    else:
        print(f"\n✗ FAILURE: Cron job '{job_name}' failed with return code {result.returncode}")
        
except subprocess.TimeoutExpired:
    print(f"\n✗ TIMEOUT: Cron job '{job_name}' timed out after 60 seconds")
except Exception as e:
    print(f"\n✗ ERROR running cron job '{job_name}': {e}")

print("\n=== Manual Job Trigger Complete ===")