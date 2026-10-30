#!/usr/bin/env python3
import subprocess
import json
import sys
import os

print("=== Hermes Price Radar Manual Job Trigger ===")

# Get the absolute path
base_dir = '/c/Users/Administrator/hermes-price-radar'
products_path = f'{base_dir}/data/products.json'

print(f"Checking products.json at: {products_path}")
print(f"File exists: {os.path.exists(products_path)}")

# Check add_products.py
add_products_path = f'{base_dir}/add_products.py'
print(f"\nChecking add_products.py at: {add_products_path}")
print(f"File exists: {os.path.exists(add_products_path)}")

# Try to run add_products.py directly
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
print("\n=== Checking Hermes availability ===")
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
print("\n=== Attempting to run Hermes price radar cron job ===")
job_name = "price-radar-daily-research-71882589"

# Try to run Hermes directly to check status first
print(f"\nChecking status of job: {job_name}")
cmd = ['hermes', 'cron', 'list']
try:
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        print("✓ Successfully listed cron jobs")
        if job_name in result.stdout:
            print(f"✓ Found job: {job_name}")
        else:
            print(f"✗ Job '{job_name}' not found in list")
    else:
        print(f"✗ Failed to list cron jobs: {result.stderr}")
except Exception as e:
    print(f"✗ Error listing cron jobs: {e}")

# Try to run the cron job directly
print(f"\nAttempting to run job: {job_name}")
run_cmd = ['hermes', 'cron', 'run', job_name]

try:
    print(f"Command: {' '.join(run_cmd)}")
    result = subprocess.run(run_cmd, capture_output=True, text=True, timeout=60)
    
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