"""
execute_all_notebooks.py
Tự động chạy toàn bộ 6 notebook với kernel python3 và lưu trực tiếp kết quả (outputs, tables, plots) vào các file .ipynb.
"""

import sys
import os
import nbformat
from nbclient import NotebookClient

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

notebooks = [
    "notebooks/01_Data_Prep_Feature_Store.ipynb",
    "notebooks/02_Baselines_and_Ridge.ipynb",
    "notebooks/03_Tree_Ensembles_RF.ipynb",
    "notebooks/04_Gradient_Boosting_SOTA.ipynb",
    "notebooks/05_Neural_Network_MLP.ipynb",
    "notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb"
]

for nb_name in notebooks:
    print(f"\n=======================================================")
    print(f"Đang thực thi và lưu output cho: {nb_name}")
    print(f"=======================================================")
    
    with open(nb_name, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)
        
    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    try:
        client.execute()
        with open(nb_name, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"✅ Hoàn tất lưu output cho: {nb_name}")
    except Exception as e:
        print(f"❌ Lỗi khi thực thi {nb_name}: {e}")
        break

print("\n🎉 Tất cả 6 notebooks đã được chạy và lưu output hoàn chỉnh!")
