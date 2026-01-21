import sys
import os

# Open a file to write output
log_file = open(os.path.expanduser("~/anki_print.log"), "w", encoding="utf-8")

# Save the original stdout
original_stdout = sys.stdout
original_stderr = sys.stderr

# Redirecting output
sys.stdout = log_file
sys.stderr = log_file

print("=== ANKI DEBUG START ===")

# Restore after use
def restore_output():
    sys.stdout = original_stdout
    sys.stderr = original_stderr
    log_file.close()


