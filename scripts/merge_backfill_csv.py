import os
import sys
import time
import pandas as pd
import numpy as np

sys.stdout.reconfigure(encoding="utf-8")

print("=== BẮT ĐẦU QUY TRÌNH NẠP BỔ SUNG CÁC NGÀY KHUYẾT ===")

# 1. Đọc dữ liệu hiện tại
csv_path = "data/california_aqi_model_ready_extended_2026.csv"
print(f"1. Đang nạp {csv_path}...")
df_orig = pd.read_csv(csv_path)
print(f"   Dữ liệu gốc: {len(df_orig):,} dòng. Max date: {df_orig['time'].max()}")

# 2. Xử lý 1 giờ khuyết ở LA_OPENMETEO: 2025-01-10 00:00:00
print("2. Kiểm tra và bù đắp 1 giờ khuyết tại LA_OPENMETEO (2025-01-10 00:00:00)...")
la_om = df_orig[df_orig["station_id"] == "LA_OPENMETEO"].copy()
if "2025-01-10 00:00:00" not in set(la_om["time"]):
    # Lấy bản ghi lúc 2025-01-09 23:00 và 2025-01-10 01:00 để nội suy
    prev_row = la_om[la_om["time"] == "2025-01-09 23:00:00"].iloc[0]
    next_row = la_om[la_om["time"] == "2025-01-10 01:00:00"].iloc[0]
    
    interp_row = prev_row.copy()
    interp_row["time"] = "2025-01-10 00:00:00"
    num_cols = ["pm25_ug_m3", "pm10_ug_m3", "target_aqi", "temperature_2m", "relative_humidity_2m", 
                "rain", "cloud_cover", "wind_speed_10m", "wind_direction_10m", "surface_pressure"]
    for c in num_cols:
        interp_row[c] = (float(prev_row[c]) + float(next_row[c])) / 2.0
    interp_row["hour"] = 0
    interp_row["dayofweek"] = 4
    interp_row["month"] = 1
    interp_row["year"] = 2025
    
    df_orig = pd.concat([df_orig, pd.DataFrame([interp_row])], ignore_index=True)
    print("   -> Đã bù đắp thành công 2025-01-10 00:00:00 cho LA_OPENMETEO.")
else:
    print("   -> 2025-01-10 00:00:00 đã tồn tại.")

# 3. Nạp dữ liệu các ngày khuyết 2026-11-04 đến 2026-11-11
print("3. Nạp 576 dòng mới từ 2026-11-04 đến 2026-11-11...")
df_new = pd.read_csv("scratch/backfilled_missing_dates.csv")
df_new["time"] = pd.to_datetime(df_new["time"]).dt.strftime("%Y-%m-%d %H:%M:%S")

# Loại bỏ các dòng đã có nếu có
existing_keys = set(df_orig["station_id"] + "_" + df_orig["time"])
df_to_add = df_new[~(df_new["station_id"] + "_" + df_new["time"]).isin(existing_keys)].copy()
print(f"   Số dòng mới cần bổ sung vào dataset chính: {len(df_to_add):,} dòng.")

if len(df_to_add) > 0:
    df_combined = pd.concat([df_orig, df_to_add], ignore_index=True)
    df_combined = df_combined.sort_values(["station_id", "time"]).reset_index(drop=True)
    df_combined.to_csv(csv_path, index=False)
    print(f"   -> Đã cập nhật {csv_path}: {len(df_combined):,} dòng.")
    print(f"   -> Khoảng thời gian mới: từ {df_combined['time'].min()} đến {df_combined['time'].max()}")
    
    # Cập nhật openmeteo_latest_2026.csv
    om_path = "data/openmeteo_latest_2026.csv"
    if os.path.exists(om_path):
        df_om = pd.read_csv(om_path)
        df_om_new = pd.concat([df_om, df_to_add], ignore_index=True).drop_duplicates(subset=["station_id", "time"]).sort_values(["station_id", "time"]).reset_index(drop=True)
        df_om_new.to_csv(om_path, index=False)
        print(f"   -> Đã cập nhật {om_path}: {len(df_om_new):,} dòng.")

print("\nHoàn tất nạp bổ sung CSV. Sẵn sàng cho việc tạo lại Parquet cache!")

