import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

print('Total cells:', len(nb['cells']))
for i, c in enumerate(nb['cells']):
    src = ''.join(c.get('source', []))
    keywords = ['figure', 'beta', 'slope', 'inversion', 'shrinkage', 'shock', 'wildfire', 'extreme', '62.6', '9.9']
    if any(k in src.lower() for k in keywords):
        ct = c.get('cell_type')
        first_line = src.split('\n')[0][:80]
        print(f"Cell {i} ({ct}): {first_line}")
