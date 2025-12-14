
import subprocess
import sys

with open("import_output.log", "w", encoding="utf-8") as f:
    # Use 'utf-8-sig' or just 'utf-8' depending on what the script outputs. 
    # Python scripts usually output utf-8 on Windows if configured, or cp932. 
    # We will try to decode as best as we can.
    
    # We can't force the subprocess to output utf-8 easily if it defaults to console cp932.
    # But we can set PYTHONUTF8=1 environment var.
    
    env = None # Default env
    # Or just run it.
    
    try:
        result = subprocess.run(
            [sys.executable, "backend/scripts/import_staff_csv.py", "zoff_staff_v4_tags.csv"],
            capture_output=True,
            cwd=".",
            encoding='utf-8', # Attempt to interpret output as utf-8
             errors='replace'
        )
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
    except Exception as e:
        f.write(f"Ref failed: {e}")
