import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('notebooks/00_EDA_California_AQI.ipynb', 'r', encoding='utf-8') as f:
    nb = json.load(f)

for i in [6, 7, 8, 9, 10, 11]:
    c = nb['cells'][i]
    print(f"\n--- CELL {i} ({c['cell_type']}) ---")
    print("SOURCE:\n", "".join(c['source']))
    for out in c.get('outputs', []):
        if 'text' in out:
            print("OUTPUT TEXT:\n", "".join(out['text']))
        elif 'data' in out:
            print("OUTPUT DATA KEYS:", list(out['data'].keys()))
            if 'text/plain' in out['data']:
                print("TEXT/PLAIN:\n", "".join(out['data']['text/plain'])[:300])
