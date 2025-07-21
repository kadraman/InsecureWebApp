# etc/print_makefile_help.py
import re
import sys
import os

makefile_path = os.path.join(os.path.dirname(__file__), '..', 'Makefile')
makefile_path = os.path.abspath(makefile_path)

try:
    with open(makefile_path, encoding="utf-8") as f:
        lines = f.readlines()
except FileNotFoundError:
    print(f"Makefile not found at {makefile_path}", file=sys.stderr)
    sys.exit(1)

help_entries = []
for line in lines:
    m = re.match(r"^([a-zA-Z0-9_-]+):.*?## (.*)$", line)
    if m:
        help_entries.append((m.group(1), m.group(2)))

for name, desc in sorted(help_entries):
    print(f"\033[36m{name:<30}\033[0m {desc}")
