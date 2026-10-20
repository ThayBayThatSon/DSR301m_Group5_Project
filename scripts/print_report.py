import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for c in nb['cells']:
    for out in c.get('outputs', []):
        if 'text' in out:
            t = ''.join(out['text'])
            if 'BÁO CÁO ĐỊNH LƯỢNG' in t:
                print(t)
