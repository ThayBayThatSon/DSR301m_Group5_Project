import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb', encoding='utf-8') as f:
    nb = json.load(f)

for i in [22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]:
    c = nb['cells'][i]
    src = ''.join(c.get('source', []))
    print(f"\n================ CELL {i} ({c.get('cell_type')}) ================")
    print(src[:1000])
