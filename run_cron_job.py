#!/usr/bin/env python3
import subprocess
import time
import sys
import os

print("=== Hermes Price Radar Cron Job Runner ===")
print(f"Current directory: {os.getcwd()}")

# Check if Hermes is available
try:
    result = subprocess.run(['which', 'hermes'], capture_output=True, text=True)
    if result.returncode != 0:
        print("ERROR: Hermes not found in PATH")
        sys.exit(1)
    print(f"Hermes found at: {result.stdout.strip()}")
except Exception as e:
    print(f"Error checking Hermes: {e}")
    sys.exit(1)

# Run the Price Radar Daily Research cron job
print("\nRunning Price Radar Daily Research cron job...")
job_name = "price-radar-daily-research-71882589"

cmd = ['hermes', 'cron', 'run', job_name]
print(f"Command: {' '.join(cmd)}")

# Set a timeout of 30 seconds
try:
    # Run with a timeout and capture output
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    
    print(f"\nCommand completed with return code: {result.returncode}")
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

print("\n=== Cron Job Runner Complete ===")