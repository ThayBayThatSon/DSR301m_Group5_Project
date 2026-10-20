import json
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

notebooks = [
    '00_EDA_California_AQI.ipynb',
    '01_Data_Prep_Feature_Store.ipynb',
    '02_Baselines_and_Ridge.ipynb',
    '03_Tree_Ensembles_RF.ipynb',
    '04_Gradient_Boosting_SOTA.ipynb',
    '05_Neural_Network_MLP.ipynb',
    '06_Benchmark_Leaderboard_Synthesis.ipynb'
]

print("=== INSPECTING ALL NOTEBOOKS ===")

for nb_name in notebooks:
    path = os.path.join('notebooks', nb_name)
    with open(path, 'r', encoding='utf-8') as f:
        nb = json.load(f)
    print(f"\n{'='*30}\nFILE: {nb_name} (Total cells: {len(nb['cells'])})\n{'='*30}")
    
    for idx, c in enumerate(nb['cells']):
        if c['cell_type'] == 'markdown':
            text = "".join(c['source']).strip()
            # print headings
            headings = [line for line in text.split('\n') if line.strip().startswith('#')]
            if headings:
                print(f"Cell {idx} [MD]: {headings}")
        elif c['cell_type'] == 'code':
            src = "".join(c['source'])
            # Check cell outputs for text/plain
            out_texts = []
            for out in c.get('outputs', []):
                if 'text' in out:
                    out_texts.append("".join(out['text']))
                elif 'data' in out and 'text/plain' in out['data']:
                    out_texts.append("".join(out['data']['text/plain']))
            
            combined_out = "\n".join(out_texts).strip()
            
            # Look for key indicators
            keywords = ['shape', 'MAE', 'R2', 'RMSE', 'Split', 'train', 'test', 'val', 'feature', 'columns', 'target', 'leaderboard', 'metrics']
            has_kw = any(k.lower() in src.lower() for k in ['train', 'test', 'split', 'mae', 'leaderboard', 'r2', 'columns'])
            
            if combined_out and (len(combined_out) < 500 or 'MAE' in combined_out or 'leaderboard' in combined_out.lower() or 'shape' in combined_out.lower()):
                # print snippet of code and output
                first_code_line = src.strip().split('\n')[0] if src.strip() else ""
                print(f"  [Code Cell {idx}] First line: {first_code_line[:60]}")
                print(f"    --> Output snippet: {combined_out[:300]}...")
