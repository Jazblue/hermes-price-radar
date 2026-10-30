#!/usr/bin/env python3
import subprocess
import json
import sys
import os

print("=== Hermes Price Radar Final Verification ===")

# Change to the correct directory
os.chdir('/c/Users/Administrator/hermes-price-radar')

# List all Python files in the directory
print("\nPython files in current directory:")
for file in os.listdir('.'):
    if file.endswith('.py'):
        print(f"  {file}")

# Check products.json
print(f"\nChecking products.json at: {os.path.abspath('data/products.json')}")
print(f"File exists: {os.path.exists('data/products.json')}")

# Try to run Hermes to check status
print("\n=== Checking Hermes cron job status ===")
try:
    result = subprocess.run(['hermes', 'cron', 'list'], capture_output=True, text=True, timeout=60)
    if result.returncode == 0:
        print("✓ Successfully listed cron jobs")
        
        # Check for price-radar job
        if 'price-radar-daily-research-71882589' in result.stdout:
            print("✓ Found price-radar job in list")
            
            # Get more details
            lines = result.stdout.split('\n')
            in_job = False
            job_lines = []
            for line in lines:
                if 'price-radar-daily-research-71882589' in line:
                    in_job = True
                if in_job:
                    job_lines.append(line)
                    if line.strip() and not line.startswith(' ') and in_job and 'price-radar-daily-research-71882589' not in line:
                        break
            
            print("\nJob details:")
            for line in job_lines[:10]:
                if line.strip():
                    print(f"  {line}")
        else:
            print("✗ price-radar job not found in list")
    else:
        print(f"✗ Failed to list cron jobs: {result.stderr}")
except Exception as e:
    print(f"✗ Error: {e}")

# Try to run Hermes cron job
print("\n=== Attempting to run price-radar job ===")
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
        
        # Check if the job actually ran
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
print("\n=== Checking for file modifications ===")
try:
    # Get modification time
    mod_time = os.path.getmtime('data/products.json')
    print(f"products.json last modified: {time.ctime(mod_time)}")
    
    # Try to read and check if it's valid JSON
    with open('data/products.json', 'r') as f:
        data = json.load(f)
    
    print(f"✓ products.json is valid JSON with {len(data['products'])} products")
    
except Exception as e:
    print(f"✗ Error reading products.json: {e}")

print("\n=== Final Verification Complete ===")