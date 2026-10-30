#!/usr/bin/env python3
import subprocess
import json
import sys
import os

print("=== Hermes Price Radar Direct Verification ===")

# Get the absolute path
base_dir = '/c/Users/Administrator/hermes-price-radar'
products_path = os.path.join(base_dir, 'data', 'products.json')

print(f"Base directory: {base_dir}")
print(f"Products path: {products_path}")
print(f"Products path exists: {os.path.exists(products_path)}")

# List directory contents
print("\nDirectory contents:")
if os.path.exists(base_dir):
    for item in os.listdir(base_dir):
        print(f"  {item}")

# Check data directory
if os.path.exists(os.path.join(base_dir, 'data')):
    print(f"\nData directory contents:")
    for item in os.listdir(os.path.join(base_dir, 'data')):
        print(f"  {item}")

# Try to run Hermes cron job
print("\n=== Running Hermes cron job ===")
job_name = "price-radar-daily-research-71882589"

run_cmd = ['hermes', 'cron', 'run', job_name]

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

print("\n=== Verification Complete ===")