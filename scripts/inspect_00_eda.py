import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/00_EDA_California_AQI.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

print(f"Total cells in 00_EDA: {len(nb['cells'])}")
for i, c in enumerate(nb['cells']):
    if c['cell_type'] == 'markdown':
        print(f"Cell {i} [MD]: {''.join(c['source'])[:100]}...")
    elif c['cell_type'] == 'code':
        src = "".join(c['source'])
        first_line = src.strip().split('\n')[0] if src.strip() else ""
        print(f"Cell {i} [Code]: {first_line[:80]}")
        for out in c.get('outputs', []):
            if 'text' in out:
                lines = "".join(out['text']).strip().split('\n')
                print(f"   out: {lines[0][:100]} ({len(lines)} lines)")
