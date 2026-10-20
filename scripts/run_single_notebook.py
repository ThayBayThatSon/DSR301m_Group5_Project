"""
run_single_notebook.py
Chạy lẻ một Jupyter Notebook bất kỳ từ terminal và tự động lưu output.

Cách dùng:
    python scripts/run_single_notebook.py 01
    python scripts/run_single_notebook.py 02_Baselines_and_Ridge.ipynb
    python scripts/run_single_notebook.py notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb
"""

import sys
import os
import glob
import nbformat
from nbclient import NotebookClient

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

def find_notebook(query):
    all_nbs = sorted(glob.glob("notebooks/*.ipynb"))
    # Match by exact name or substring
    for nb in all_nbs:
        basename = os.path.basename(nb)
        if query in nb or query in basename:
            return nb
    return None

def run_notebook(nb_path):
    print(f"\n=======================================================")
    print(f"🚀 Bắt đầu thực thi notebook: {nb_path}")
    print(f"=======================================================")

    with open(nb_path, "r", encoding="utf-8") as f:
        nb = nbformat.read(f, as_version=4)

    client = NotebookClient(nb, timeout=600, kernel_name="python3")
    try:
        client.execute()
        with open(nb_path, "w", encoding="utf-8") as f:
            nbformat.write(nb, f)
        print(f"✅ Hoàn tất thành công và đã lưu output cho: {nb_path}")
    except Exception as e:
        print(f"❌ Lỗi khi thực thi: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Vui lòng nhập tên hoặc số thứ tự notebook cần chạy!")
        print("Ví dụ: python scripts/run_single_notebook.py 01")
        print("\nCác notebook hiện có:")
        for nb in sorted(glob.glob("notebooks/*.ipynb")):
            print(f"  - {os.path.basename(nb)}")
        sys.exit(1)

    target_query = sys.argv[1]
    nb_file = find_notebook(target_query)
    if not nb_file:
        print(f"❌ Không tìm thấy notebook khớp với từ khóa: '{target_query}'")
        sys.exit(1)

    run_notebook(nb_file)
