#!/usr/bin/env python3
import subprocess
import json
import sys
import os
import time

print("=== Hermes Price Radar Final Verification ===")

# Get the absolute path to the hermes-price-radar directory
base_dir = '/c/Users/Administrator/hermes-price-radar'
print(f"Base directory: {base_dir}")

# Check if products.json exists
products_path = os.path.join(base_dir, 'data', 'products.json')
if not os.path.exists(products_path):
    print(f"ERROR: products.json not found at {products_path}")
    sys.exit(1)

print("✓ products.json exists")

# Check if SKILL.md exists
skill_path = os.path.join(base_dir, 'SKILL.md')
if not os.path.exists(skill_path):
    print(f"ERROR: SKILL.md not found at {skill_path}")
    sys.exit(1)

print("✓ SKILL.md exists")

# Check if Hermes is available
print("\n=== Checking Hermes availability ===")
try:
    result = subprocess.run(['which', 'hermes'], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Hermes not found in PATH")
        sys.exit(1)
    print(f"✓ Hermes found at: {result.stdout.strip()}")
except Exception as e:
    print(f"✗ Error checking Hermes: {e}")
    sys.exit(1)

# Try to run the Hermes cron job
print("\n=== Attempting to run Hermes cron job ===")
run_cmd = ['hermes', 'cron', 'run', 'price-radar-daily-research-71882589']

try:
    print(f"Command: {' '.join(run_cmd)}")
    result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=60)
    
    print(f"\nReturn code: {result.returncode}")
    print(f"STDOUT:\n{result.stdout}")
    if result.stderr:
        print(f"STDERR:\n{result.stderr}")
        
    if result.returncode == 0:
        print(f"\n✓ SUCCESS: Cron job completed successfully")
        
        if 'not run again' in result.stdout or 'already being fired' in result.stdout:
            print("  (Note: Job may already be running or scheduled)")
        else:
            print("  (Job appears to have run)")
    else:
        print(f"\n✗ FAILURE: Cron job failed with return code {result.returncode}")
        
except subprocess.TimeoutExpired:
    print(f"\n✗ TIMEOUT: Cron job timed out after 60 seconds")
except Exception as e:
    print(f"\n✗ ERROR running cron job: {e}")

# Check if products.json was modified
try:
    print("\n=== Checking products.json file ===")
    print(f"Path: {products_path}")
    print(f"Exists: {os.path.exists(products_path)}")
    
    if os.path.exists(products_path):
        stat = os.stat(products_path)
        print(f"Size: {stat.st_size} bytes")
        print(f"Modified: {time.ctime(stat.st_mtime)}")
        
        with open(products_path, 'r') as f:
            data = json.load(f)
        
        print(f"✓ Valid JSON with {len(data['products'])} products")
        
except Exception as e:
    print(f"✗ Error: {e}")

print("\n=== Verification Complete ===")