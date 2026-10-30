#!/usr/bin/env python3
import subprocess
import json
import sys
import os

print("=== Hermes Price Radar Manual Job Trigger ===")

# Get the absolute path
base_dir = '/c/Users/Administrator/hermes-price-radar'
products_path = f'{base_dir}/data/products.json'
add_products_path = f'{base_dir}/add_products.py'

# Check add_products.py
if os.path.exists(add_products_path):
    print("\nAttempting to run add_products.py...")
    try:
        result = subprocess.run(['python', add_products_path], capture_output=True, text=True, timeout=60)
        print(f"Return code: {result.returncode}")
        print(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            print(f"STDERR:\n{result.stderr}")
    except subprocess.TimeoutExpired:
        print("ERROR: add_products.py timed out after 60 seconds")
    except Exception as e:
        print(f"ERROR: {e}")
else:
    print("✗ add_products.py not found")

# Check Hermes availability
try:
    result = subprocess.run(['which', 'hermes'], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Hermes not found in PATH")
        sys.exit(1)
    print(f"Hermes found at: {result.stdout.strip()}")
except Exception as e:
    print(f"Error checking Hermes: {e}")
    sys.exit(1)

# Try to run the price radar cron job
print(f"\nAttempting to run job: price-radar-daily-research-71882589")
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
    else:
        print(f"\n✗ FAILURE: Cron job failed with return code {result.returncode}")
        
except subprocess.TimeoutExpired:
    print(f"\n✗ TIMEOUT: Cron job timed out after 60 seconds")
except Exception as e:
    print(f"\n✗ ERROR running cron job: {e}")

print("\n=== Manual Job Trigger Complete ===")