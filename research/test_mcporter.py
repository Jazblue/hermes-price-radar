import subprocess
import sys

# Try with just 'mcporter'
try:
    result = subprocess.run(['mcporter', 'call', 'exa.web_search_exa', 'query=test', 'numResults=1'], 
                          capture_output=True, text=True, timeout=10)
    print("Return code:", result.returncode)
    print("Stdout:", result.stdout[:200] if result.stdout else "None")
    print("Stderr:", result.stderr[:200] if result.stderr else "None")
except Exception as e:
    print("Error with 'mcporter':", e)

# Try with full path
full_path = r'/c/Users/Administrator/AppData/Roaming/npm/mcporter'
try:
    result = subprocess.run([full_path, 'call', 'exa.web_search_exa', 'query=test', 'numResults=1'], 
                          capture_output=True, text=True, timeout=10)
    print("\nReturn code (full path):", result.returncode)
    print("Stdout (full path):", result.stdout[:200] if result.stdout else "None")
    print("Stderr (full path):", result.stderr[:200] if result.stderr else "None")
except Exception as e:
    print("Error with full path:", e)
