import os
import json
import time
import sqlite3
import urllib.request
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

from app.inference_engine import STATION_META


def pm25_to_epa_aqi(pm25):
    """
    US EPA Standard (Revised 2024 Final Rule):
    Annual PM2.5 threshold tightened from 12.0 to 9.0 µg/m³.
    Therefore, 0.0 - 9.0 µg/m³ is Good (0-50), and 9.1 - 35.4 µg/m³ is Moderate (51-100).
    For example: 9.2 µg/m³ yields ((100-51)/(35.4-9.1))*(9.2-9.1)+51 = 51.18 -> AQI 51.
    """
    if pd.isna(pm25) or pm25 < 0:
        return 0.0
    breakpoints = [
        (0.0, 9.0, 0.0, 50.0),
        (9.1, 35.4, 51.0, 100.0),
        (35.5, 55.4, 101.0, 150.0),
        (55.5, 125.4, 151.0, 200.0),
        (125.5, 225.4, 201.0, 300.0),
        (225.5, 325.4, 301.0, 400.0),
        (325.5, 500.4, 401.0, 500.0),
    ]
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm25 <= c_high:
            return ((i_high - i_low) / (c_high - c_low)) * (pm25 - c_low) + i_low
    if pm25 > 500.4:
        return 500.0
    return 0.0


def pm10_to_epa_aqi(pm10):
    """US EPA Standard for 24-hr PM10 (µg/m³)."""
    if pd.isna(pm10) or pm10 < 0:
        return 0.0
    breakpoints = [
        (0.0, 54.0, 0.0, 50.0),
        (55.0, 154.0, 51.0, 100.0),
        (155.0, 254.0, 101.0, 150.0),
        (255.0, 354.0, 151.0, 200.0),
        (355.0, 424.0, 201.0, 300.0),
        (425.0, 504.0, 301.0, 400.0),
        (505.0, 604.0, 401.0, 500.0),
    ]
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= pm10 <= c_high:
            return ((i_high - i_low) / (c_high - c_low)) * (pm10 - c_low) + i_low
    if pm10 > 604.0:
        return 500.0
    return 0.0


def ozone_to_epa_aqi(o3_ug_m3):
    """
    US EPA Standard for Ozone 8-hr.
    Conversion factor: 1 ppb O3 ≈ 2.0 µg/m³.
    0-54 ppb (0-108 µg/m³) -> 0-50 (Good)
    55-70 ppb (109-140 µg/m³) -> 51-100 (Moderate)
    """
    if pd.isna(o3_ug_m3) or o3_ug_m3 < 0:
        return 0.0
    ppb = o3_ug_m3 / 1.96  # Standard temperature & pressure conversion
    breakpoints = [
        (0.0, 54.0, 0.0, 50.0),
        (55.0, 70.0, 51.0, 100.0),
        (71.0, 85.0, 101.0, 150.0),
        (86.0, 105.0, 151.0, 200.0),
        (106.0, 200.0, 201.0, 300.0),
    ]
    for c_low, c_high, i_low, i_high in breakpoints:
        if c_low <= ppb <= c_high:
            return ((i_high - i_low) / (c_high - c_low)) * (ppb - c_low) + i_low
    if ppb > 200.0:
        return 300.0
    return 0.0


WILDFIRE_PRESETS = [
    {
        "id": "latest_today",
        "title": "Ngày Quan Trắc Mới Nhất (24h)",
        "badge": "Default",
        "start_date": "2026-11-02",
        "end_date": "2026-11-03",
        "source_mode": "seamless",
        "description": "Hiển thị kết quả dự báo của 10 mô hình đối chiếu với thực tế trong ngày quan trắc mới nhất trên cả 3 trạm.",
    },
    {
        "id": "latest_7d",
        "title": "7 Ngày Gần Nhất (11/2026)",
        "badge": "Recent 7D",
        "start_date": "2026-10-28",
        "end_date": "2026-11-03",
        "source_mode": "seamless",
        "description": "Chuỗi 168 giờ liên tục tuần gần nhất từ Open-Meteo trên cả 3 lưu vực Fresno, Los Angeles và San Jose.",
    },
    {
        "id": "palisades_eaton_2025",
        "title": "Cháy Rừng Palisades & Eaton (01/2025)",
        "badge": "Peak 312 AQI",
        "start_date": "2025-01-07",
        "end_date": "2025-01-14",
        "source_mode": "seamless",
        "description": "Đám cháy tại Los Angeles tháng 1/2025 kết hợp gió Santa Ana đẩy AQI vọt lên 312.0 điểm.",
    },
    {
        "id": "july_smoke_2024",
        "title": "Bão Khói & Sóng Nhiệt Mùa Hè (07/2024)",
        "badge": "Peak 387 AQI",
        "start_date": "2024-07-03",
        "end_date": "2024-07-10",
        "source_mode": "seamless",
        "description": "Giai đoạn giao thoa có đủ cả 2 nguồn dữ liệu (EPA AQS & Open-Meteo), đỉnh ô nhiễm tại LA đạt 387.1 AQI.",
    },
    {
        "id": "dual_source_overlap_2023",
        "title": "Giao Thoa 2 Nguồn EPA vs Open-Meteo (07/2023)",
        "badge": "Dual-Source",
        "start_date": "2023-07-02",
        "end_date": "2023-07-09",
        "source_mode": "both_compare",
        "description": "Kiểm tra trực diện sự khác biệt giữa trạm mặt đất EPA (FRES, LA) và nguồn Open-Meteo cùng thời điểm.",
    },
    {
        "id": "knp_windy_2021",
        "title": "Cháy Rừng KNP Complex & Windy Fire (10/2021)",
        "badge": "Peak 222 AQI",
        "start_date": "2021-09-28",
        "end_date": "2021-10-05",
        "source_mode": "seamless",
        "description": "Khói cháy rừng từ rừng quốc gia Sequoia bị bẫy trong lòng chảo San Joaquin Valley (Fresno).",
    },
    {
        "id": "creek_august_2020",
        "title": "Creek Fire — Thung Lũng San Joaquin (09/2020)",
        "badge": "Peak 390 AQI",
        "start_date": "2020-09-10",
        "end_date": "2020-09-18",
        "source_mode": "seamless",
        "description": "Đợt cháy rừng quy mô lớn tại Sierra National Forest làm AQI tại Fresno vọt lên 389.8 điểm nhiều ngày liền.",
    },
    {
        "id": "camp_fire_2018",
        "title": "Camp Fire & Woolsey Fire (11/2018)",
        "badge": "Peak 189 AQI",
        "start_date": "2018-11-15",
        "end_date": "2018-11-22",
        "source_mode": "seamless",
        "description": "Đám cháy Camp Fire tháng 11/2018 gây ô nhiễm diện rộng khắp thung lũng miền Trung California.",
    },
]

MODEL_COLUMNS = [
    ("pred_wildfire_layer", "Wildfire Specialist (2-Stage)", "Extreme Adaptation", "#dc2626"),
    ("pred_voting_ensemble", "Voting Ensemble (Top 3)", "Ensemble", "#059669"),
    ("pred_lstm", "LSTM (PyTorch)", "Neural Network", "#7c3aed"),
    ("pred_lightgbm", "LightGBM", "Gradient Boosting", "#2563eb"),
    ("pred_xgboost", "XGBoost", "Gradient Boosting", "#0284c7"),
    ("pred_catboost", "CatBoost", "Gradient Boosting", "#4f46e5"),
    ("pred_random_forest", "Random Forest", "Bagging Trees", "#0d9488"),
    ("pred_mlp", "MLP (64, 32)", "Neural Network", "#db2777"),
    ("pred_ridge", "Ridge Regression", "Linear", "#d97706"),
    ("pred_persistence", "Persistence", "Baseline", "#64748b"),
    ("pred_climatology", "Climatology", "Baseline", "#94a3b8"),
]


class AQIDataManager:
    CACHE_TTL_SEC = 3600  # 60 minutes cache
    COOLDOWN_SEC = 300    # 5 minutes manual refresh cooldown
    DAILY_QUOTA_LIMIT = 10000

    def __init__(self, data_dir="data"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "aqi_app_store.db")
        self._init_db()
        self.df_1h = None
        self.df_24h = None
        self.df_raw_ext = None
        self.load_precomputed_stores()

    def _get_conn(self):
        return sqlite3.connect(self.db_path, check_same_thread=False)

    def _init_db(self):
        os.makedirs(self.data_dir, exist_ok=True)
        with self._get_conn() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS api_fetch_logs (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fetched_at TEXT NOT NULL,
                    fetched_ts REAL NOT NULL,
                    region_key TEXT NOT NULL,
                    station_id TEXT NOT NULL,
                    trigger_type TEXT NOT NULL,
                    api_called INTEGER NOT NULL,
                    current_aqi REAL,
                    pm25 REAL,
                    pm10 REAL,
                    temp_c REAL,
                    rh_pct REAL,
                    wind_kmh REAL,
                    wind_dir REAL,
                    pressure_hpa REAL,
                    pred_1h_aqi REAL,
                    pred_24h_aqi REAL,
                    payload_json TEXT
                )
                """
            )
            conn.commit()

    def load_precomputed_stores(self):
        p1 = os.path.join(self.data_dir, "app_predictions_1h.parquet")
        p24 = os.path.join(self.data_dir, "app_predictions_24h.parquet")
        if os.path.exists(p1) and os.path.exists(p24):
            self.df_1h = pd.read_parquet(p1)
            self.df_24h = pd.read_parquet(p24)
        else:
            # Fallback to 2025 predictions if parquet cache is still building
            f1 = os.path.join("artifacts", "predictions", "all_predictions_1h.csv")
            f24 = os.path.join("artifacts", "predictions", "all_predictions_24h.csv")
            self.df_1h = pd.read_csv(f1)
            self.df_24h = pd.read_csv(f24)
            self.df_1h["source"] = "openmeteo"
            self.df_24h["source"] = "openmeteo"

        # Map each station_id to region_key ('FRES', 'LA', 'SJ')
        for df_p in [self.df_1h, self.df_24h]:
            df_p["region_key"] = df_p["station_id"].apply(
                lambda s: "FRES" if "FRES" in str(s) else ("LA" if "LA" in str(s) else "SJ")
            )
            df_p["date"] = df_p["time"].str.slice(0, 10)

        ext_csv = os.path.join(self.data_dir, "california_aqi_model_ready_extended_2026.csv")
        if os.path.exists(ext_csv):
            self.df_raw_ext = pd.read_csv(ext_csv)
        else:
            self.df_raw_ext = pd.read_csv(os.path.join(self.data_dir, "california_aqi_model_ready.csv"))

        self.diurnal_heatmaps = {}
        self._precompute_diurnal_heatmaps()

    def _precompute_diurnal_heatmaps(self):
        try:
            df = self.df_raw_ext.copy()
            df["time_dt"] = pd.to_datetime(df["time"], errors="coerce")
            df = df.dropna(subset=["time_dt", "target_aqi"])
            df["day_idx"] = df["time_dt"].dt.dayofweek  # 0=Monday, 6=Sunday
            df["hour"] = df["time_dt"].dt.hour
            day_names = ["Thứ 2", "Thứ 3", "Thứ 4", "Thứ 5", "Thứ 6", "Thứ 7", "Chủ Nhật"]
            hour_labels = [f"{h:02d}:00" for h in range(24)]

            mapping = {
                "FRES": "FRES_OPENMETEO",
                "LA": "LA_OPENMETEO",
                "SJ": "SJ_OPENMETEO",
                "ALL": "ALL",
            }
            for rk, st_id in mapping.items():
                sub = df if st_id == "ALL" else df[df["station_id"] == st_id]
                if sub.empty and st_id != "ALL":
                    sub = df[df["station_id"].str.contains(rk, na=False)]
                if sub.empty:
                    sub = df

                grp = sub.groupby(["day_idx", "hour"])["target_aqi"].mean().round(1)
                matrix = []
                for d in range(7):
                    for h in range(24):
                        val = float(grp.get((d, h), 45.0))
                        matrix.append([h, d, val])

                vals = [m[2] for m in matrix]
                min_v = min(vals) if vals else 20.0
                max_v = max(vals) if vals else 120.0
                max_cell = max(matrix, key=lambda m: m[2])
                min_cell = min(matrix, key=lambda m: m[2])

                self.diurnal_heatmaps[rk] = {
                    "region_key": rk,
                    "days": day_names,
                    "hours": hour_labels,
                    "data": matrix,
                    "min_aqi": min_v,
                    "max_aqi": max_v,
                    "peak": {
                        "day": day_names[max_cell[1]],
                        "hour": f"{max_cell[0]:02d}:00",
                        "aqi": max_cell[2],
                    },
                    "cleanest": {
                        "day": day_names[min_cell[1]],
                        "hour": f"{min_cell[0]:02d}:00",
                        "aqi": min_cell[2],
                    },
                }
        except Exception as e:
            print(f"[DiurnalHeatmap] Warning precomputing heatmaps: {e}")
            self.diurnal_heatmaps = {}

    def get_historical_diurnal_heatmap(self, region_key="FRES"):
        rk = region_key.upper() if region_key.upper() in ["FRES", "LA", "SJ", "ALL"] else "FRES"
        if not hasattr(self, "diurnal_heatmaps") or not self.diurnal_heatmaps:
            self._precompute_diurnal_heatmaps()
        return self.diurnal_heatmaps.get(rk, self.diurnal_heatmaps.get("FRES", {}))

    def get_api_quota_stats(self):
        today_str = datetime.now().strftime("%Y-%m-%d")
        with self._get_conn() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT COUNT(*) FROM api_fetch_logs WHERE fetched_at LIKE ? AND api_called = 1",
                (f"{today_str}%",),
            )
            calls_today = cur.fetchone()[0]

            cur.execute(
                "SELECT COUNT(*) FROM api_fetch_logs WHERE fetched_at LIKE ? AND api_called = 0",
                (f"{today_str}%",),
            )
            cache_hits_today = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM api_fetch_logs")
            total_logs = cur.fetchone()[0]

        total_reqs = calls_today + cache_hits_today
        saved_pct = round((cache_hits_today / total_reqs * 100), 1) if total_reqs > 0 else 100.0
        return {
            "calls_today": calls_today,
            "cache_hits_today": cache_hits_today,
            "daily_limit": self.DAILY_QUOTA_LIMIT,
            "saved_percent": saved_pct,
            "total_history_records": total_logs,
            "cache_ttl_minutes": self.CACHE_TTL_SEC // 60,
            "cooldown_minutes": self.COOLDOWN_SEC // 60,
        }

    def get_fetch_history(self, limit=30):
        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                """
                SELECT id, fetched_at, region_key, station_id, trigger_type, api_called,
                       current_aqi, pm25, pm10, temp_c, rh_pct, wind_kmh, wind_dir,
                       pred_1h_aqi, pred_24h_aqi
                FROM api_fetch_logs
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(r) for r in cur.fetchall()]

    def fetch_live_or_cached_station_data(self, region_key="FRES", force_refresh=False, trigger_type="user_view"):
        meta = STATION_META.get(region_key, STATION_META["FRES"])
        station_id = meta["openmeteo_id"]
        now_ts = time.time()
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with self._get_conn() as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()
            cur.execute(
                """
                SELECT * FROM api_fetch_logs
                WHERE region_key = ? AND api_called = 1 AND payload_json IS NOT NULL
                ORDER BY fetched_ts DESC LIMIT 1
                """,
                (region_key,),
            )
            last_real = cur.fetchone()

        if last_real is not None:
            age_sec = now_ts - float(last_real["fetched_ts"])
            # Check Cooldown on manual force refresh
            if force_refresh and age_sec < self.COOLDOWN_SEC:
                cooldown_left = int(self.COOLDOWN_SEC - age_sec)
                df_cached = pd.DataFrame(json.loads(last_real["payload_json"]))
                return {
                    "df": df_cached,
                    "cache_status": "cooldown_blocked",
                    "api_called": False,
                    "age_seconds": int(age_sec),
                    "ttl_remaining_seconds": max(0, int(self.CACHE_TTL_SEC - age_sec)),
                    "cooldown_remaining_seconds": cooldown_left,
                    "last_fetched_at": last_real["fetched_at"],
                    "message": f"Dữ liệu vừa được cập nhật gần đây. Bạn có thể làm mới tiếp sau {cooldown_left} giây.",
                }

            # Standard Cache Hit within 60-minute TTL
            if not force_refresh and age_sec < self.CACHE_TTL_SEC:
                df_cached = pd.DataFrame(json.loads(last_real["payload_json"]))
                # Record cache hit log
                with self._get_conn() as conn:
                    conn.execute(
                        """
                        INSERT INTO api_fetch_logs (
                            fetched_at, fetched_ts, region_key, station_id, trigger_type, api_called,
                            current_aqi, pm25, pm10, temp_c, rh_pct, wind_kmh, wind_dir, pressure_hpa,
                            pred_1h_aqi, pred_24h_aqi, payload_json
                        ) VALUES (?, ?, ?, ?, ?, 0, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL)
                        """,
                        (
                            now_iso,
                            now_ts,
                            region_key,
                            station_id,
                            "cache_hit",
                            last_real["current_aqi"],
                            last_real["pm25"],
                            last_real["pm10"],
                            last_real["temp_c"],
                            last_real["rh_pct"],
                            last_real["wind_kmh"],
                            last_real["wind_dir"],
                            last_real["pressure_hpa"],
                            last_real["pred_1h_aqi"],
                            last_real["pred_24h_aqi"],
                        ),
                    )
                    conn.commit()

                return {
                    "df": df_cached,
                    "cache_status": "cache_hit",
                    "api_called": False,
                    "age_seconds": int(age_sec),
                    "ttl_remaining_seconds": max(0, int(self.CACHE_TTL_SEC - age_sec)),
                    "cooldown_remaining_seconds": max(0, int(self.COOLDOWN_SEC - age_sec)),
                    "last_fetched_at": last_real["fetched_at"],
                    "message": f"Dữ liệu quan trắc trạm sẵn sàng (cập nhật cách đây {int(age_sec // 60)} phút).",
                }

        # Otherwise call Open-Meteo Live API (past 3 days + forecast 2 days)
        lat, lon = meta["lat"], meta["lon"]
        try:
            url_w = (
                f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
                f"&hourly=temperature_2m,relative_humidity_2m,rain,cloud_cover,wind_speed_10m,wind_direction_10m,surface_pressure"
                f"&past_days=3&forecast_days=2&timezone=America%2FLos_Angeles"
            )
            url_aq = (
                f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
                f"&hourly=pm2_5,pm10,ozone,us_aqi,us_aqi_pm2_5,us_aqi_pm10,us_aqi_ozone&past_days=3&forecast_days=2&timezone=America%2FLos_Angeles"
            )
            req_w = urllib.request.Request(url_w, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req_w, timeout=12) as resp_w:
                data_w = json.loads(resp_w.read().decode("utf-8"))

            req_aq = urllib.request.Request(url_aq, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req_aq, timeout=12) as resp_aq:
                data_aq = json.loads(resp_aq.read().decode("utf-8"))

            df_w = pd.DataFrame(data_w["hourly"])
            df_aq = pd.DataFrame(data_aq["hourly"]).rename(
                columns={"pm2_5": "pm25_ug_m3", "pm10": "pm10_ug_m3", "ozone": "ozone_ug_m3"}
            )
            merged = pd.merge(df_aq, df_w, on="time", how="inner")
            merged["pm25_ug_m3"] = merged["pm25_ug_m3"].ffill().bfill().fillna(5.0)
            merged["pm10_ug_m3"] = merged["pm10_ug_m3"].ffill().bfill().fillna(10.0)
            if "ozone_ug_m3" in merged:
                merged["ozone_ug_m3"] = merged["ozone_ug_m3"].ffill().bfill().fillna(40.0)
            else:
                merged["ozone_ug_m3"] = 40.0

            # Compute individual criteria sub-indices according to EPA standards
            merged["subindex_pm25"] = merged["pm25_ug_m3"].apply(pm25_to_epa_aqi).round(1)
            if "us_aqi_pm10" in merged and not merged["us_aqi_pm10"].isna().all():
                merged["subindex_pm10"] = (
                    merged["us_aqi_pm10"].fillna(merged["pm10_ug_m3"].apply(pm10_to_epa_aqi)).round(1)
                )
            else:
                merged["subindex_pm10"] = merged["pm10_ug_m3"].apply(pm10_to_epa_aqi).round(1)

            if "us_aqi_ozone" in merged and not merged["us_aqi_ozone"].isna().all():
                merged["subindex_ozone"] = (
                    merged["us_aqi_ozone"].fillna(merged["ozone_ug_m3"].apply(ozone_to_epa_aqi)).round(1)
                )
            else:
                merged["subindex_ozone"] = merged["ozone_ug_m3"].apply(ozone_to_epa_aqi).round(1)

            for col_w in [
                "temperature_2m",
                "relative_humidity_2m",
                "rain",
                "cloud_cover",
                "wind_speed_10m",
                "wind_direction_10m",
                "surface_pressure",
            ]:
                merged[col_w] = merged[col_w].ffill().bfill().fillna(0.0)

            # US EPA Composite AQI: maximum of all criteria sub-indices
            merged["target_aqi"] = merged[["subindex_pm25", "subindex_pm10", "subindex_ozone"]].max(axis=1)
            # Mark last 24 rows as future forecast horizon
            merged["is_forecast"] = False
            if len(merged) > 24:
                merged.loc[len(merged) - 24 :, "is_forecast"] = True

            actual_trigger = "manual_force" if force_refresh else trigger_type
            return {
                "df": merged,
                "cache_status": "fresh_api_call",
                "api_called": True,
                "age_seconds": 0,
                "ttl_remaining_seconds": self.CACHE_TTL_SEC,
                "cooldown_remaining_seconds": self.COOLDOWN_SEC,
                "last_fetched_at": now_iso,
                "trigger_type": actual_trigger,
                "message": "Đã cập nhật dữ liệu quan trắc bề mặt và khí tượng thời gian thực mới nhất thành công.",
            }
        except Exception as e:
            # Fallback to local extended CSV dataset if offline
            sub_local = (
                self.df_raw_ext[self.df_raw_ext["station_id"] == station_id]
                .tail(96)
                .copy()
                .reset_index(drop=True)
            )
            if "ozone_ug_m3" not in sub_local.columns:
                sub_local["ozone_ug_m3"] = 40.0
            sub_local["subindex_pm25"] = sub_local["pm25_ug_m3"].apply(pm25_to_epa_aqi).round(1)
            sub_local["subindex_pm10"] = sub_local["pm10_ug_m3"].apply(pm10_to_epa_aqi).round(1)
            sub_local["subindex_ozone"] = sub_local["ozone_ug_m3"].apply(ozone_to_epa_aqi).round(1)
            sub_local["target_aqi"] = sub_local[["subindex_pm25", "subindex_pm10", "subindex_ozone"]].max(axis=1)
            sub_local["is_forecast"] = False
            if len(sub_local) > 24:
                sub_local.loc[len(sub_local) - 24 :, "is_forecast"] = True
                sub_local.loc[len(sub_local) - 24 :, "is_forecast"] = True
            return {
                "df": sub_local,
                "cache_status": "offline_fallback",
                "api_called": False,
                "age_seconds": 0,
                "ttl_remaining_seconds": 1800,
                "cooldown_remaining_seconds": 60,
                "last_fetched_at": now_iso,
                "trigger_type": "offline_fallback",
                "message": "Đang sử dụng dữ liệu quan trắc lưu trữ của trạm (chế độ dự phòng ngoại tuyến).",
            }

    def save_live_fetch_log(self, region_key, station_id, trigger_type, df_merged, forecast_res):
        now_ts = time.time()
        now_iso = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        curr = forecast_res["current"]
        p1h = forecast_res["horizons"]["+1h"]["primary_aqi"]
        p24h = forecast_res["horizons"]["+24h"]["primary_aqi"]
        payload_str = df_merged.to_json(orient="records")

        with self._get_conn() as conn:
            conn.execute(
                """
                INSERT INTO api_fetch_logs (
                    fetched_at, fetched_ts, region_key, station_id, trigger_type, api_called,
                    current_aqi, pm25, pm10, temp_c, rh_pct, wind_kmh, wind_dir, pressure_hpa,
                    pred_1h_aqi, pred_24h_aqi, payload_json
                ) VALUES (?, ?, ?, ?, ?, 1, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    now_iso,
                    now_ts,
                    region_key,
                    station_id,
                    trigger_type,
                    curr["aqi"],
                    curr["pm25"],
                    curr["pm10"],
                    curr["temperature_2m"],
                    curr["relative_humidity_2m"],
                    curr["wind_speed_10m"],
                    curr["wind_direction_10m"],
                    curr["surface_pressure"],
                    p1h,
                    p24h,
                    payload_str,
                ),
            )
            conn.commit()

    def query_time_window_dashboard(
        self,
        scenario="1h",
        start_date=None,
        end_date=None,
        source_mode="seamless",
        leaderboard_region="ALL",
    ):
        df_base = self.df_1h if scenario == "1h" else self.df_24h
        min_avail = str(df_base["date"].min())
        max_avail = str(df_base["date"].max())

        if not start_date or not end_date:
            # Default: Latest day in the dataset ("Ngày hôm đó")
            end_date = max_avail
            dt_end = pd.to_datetime(max_avail)
            start_date = (dt_end - pd.Timedelta(days=1)).strftime("%Y-%m-%d")

        sub = df_base[(df_base["date"] >= start_date) & (df_base["date"] <= end_date)].copy()
        if sub.empty:
            sub = df_base.tail(72).copy()

        # Check if dual-source overlap exists in this window
        sources_in_window = sub["source"].unique().tolist()
        stations_in_window = sub["station_id"].unique().tolist()
        has_dual_overlap = (
            ("FRES" in stations_in_window and "FRES_OPENMETEO" in stations_in_window)
            or ("LA" in stations_in_window and "LA_OPENMETEO" in stations_in_window)
        )

        # Apply Dual-Source Resolution
        if source_mode == "epa_only":
            sub_resolved = sub[sub["source"] == "epa_aqs_station"].copy()
        elif source_mode == "openmeteo_only":
            sub_resolved = sub[sub["source"] == "openmeteo"].copy()
        elif source_mode == "seamless":
            # Priority: EPA Ground Truth (0) over Open-Meteo (1) when same region_key + timestamp
            sub["src_prio"] = sub["source"].apply(lambda x: 0 if x == "epa_aqs_station" else 1)
            sub_resolved = (
                sub.sort_values(["region_key", "time", "src_prio"])
                .drop_duplicates(subset=["region_key", "time"], keep="first")
                .sort_values(["region_key", "time"])
                .reset_index(drop=True)
            )
        else:
            # 'both_compare': keep all records separated by station_id
            sub_resolved = sub.sort_values(["station_id", "time"]).reset_index(drop=True)

        # Downsample gracefully if window > 600 points per station so browser renders at 60fps
        stations_series = {}
        for rk, r_title in [("FRES", "Fresno (San Joaquin Valley)"), ("LA", "Los Angeles (South Coast)"), ("SJ", "San Jose (Bay Area)")]:
            r_df = sub_resolved[sub_resolved["region_key"] == rk].sort_values("time")
            if r_df.empty:
                stations_series[rk] = {
                    "region_key": rk,
                    "title": r_title,
                    "empty": True,
                    "active_sources": [],
                    "timestamps": [],
                    "actual": [],
                    "models": {},
                }
                continue

            active_srcs = r_df["station_id"].unique().tolist()
            # If 'both_compare' and 2 station_ids exist in this region, prefer plotting the primary series + secondary actual
            plot_df = r_df.drop_duplicates(subset=["time"], keep="first").copy()
            if len(plot_df) > 500:
                step = max(1, len(plot_df) // 400)
                plot_df = plot_df.iloc[::step].copy()

            models_dict = {}
            for col_k, m_label, _, _ in MODEL_COLUMNS:
                if col_k in plot_df.columns:
                    models_dict[m_label] = np.round(plot_df[col_k].values.astype(float), 2).tolist()

            dual_actual = None
            if source_mode == "both_compare" and len(active_srcs) > 1:
                epa_sub = r_df[r_df["source"] == "epa_aqs_station"].set_index("time")["actual"]
                om_sub = r_df[r_df["source"] == "openmeteo"].set_index("time")["actual"]
                aligned_om = om_sub.reindex(plot_df["time"]).values
                dual_actual = [round(float(x), 2) if not pd.isna(x) else None for x in aligned_om]

            stations_series[rk] = {
                "region_key": rk,
                "title": r_title,
                "empty": False,
                "active_sources": active_srcs,
                "record_count": len(r_df),
                "max_aqi": round(float(r_df["actual"].max()), 1),
                "mean_aqi": round(float(r_df["actual"].mean()), 1),
                "timestamps": plot_df["time"].tolist(),
                "actual": np.round(plot_df["actual"].values.astype(float), 2).tolist(),
                "dual_openmeteo_actual": dual_actual,
                "models": models_dict,
            }

        # Dynamic Leaderboard calculation on the selected window
        lb_df = (
            sub_resolved
            if leaderboard_region == "ALL"
            else sub_resolved[sub_resolved["region_key"] == leaderboard_region]
        )
        if lb_df.empty:
            lb_df = sub_resolved

        y_true = lb_df["actual"].values.astype(float)
        leaderboard_rows = []

        # Calculate hourly winner across models
        err_matrix = {}
        for col_k, m_label, m_fam, m_color in MODEL_COLUMNS:
            if col_k in lb_df.columns:
                y_p = lb_df[col_k].values.astype(float)
                err_matrix[m_label] = np.abs(y_true - y_p)

        for col_k, m_label, m_fam, m_color in MODEL_COLUMNS:
            if col_k not in lb_df.columns or len(y_true) == 0:
                continue
            y_p = lb_df[col_k].values.astype(float)
            mae = float(mean_absolute_error(y_true, y_p))
            rmse = float(np.sqrt(mean_squared_error(y_true, y_p)))
            r2 = float(r2_score(y_true, y_p)) if len(y_true) > 2 and np.std(y_true) > 1e-5 else 0.0
            smape = float(np.mean(2 * np.abs(y_p - y_true) / (np.abs(y_true) + np.abs(y_p) + 1e-8)) * 100)

            act_150 = y_true > 150
            pred_150 = y_p > 150
            tp_150 = np.sum(act_150 & pred_150)
            f1_150 = (
                float(2 * tp_150 / (np.sum(act_150) + np.sum(pred_150) + 1e-8))
                if np.sum(act_150) > 0
                else None
            )

            leaderboard_rows.append(
                {
                    "model": m_label,
                    "family": m_fam,
                    "color": m_color,
                    "MAE": round(mae, 2),
                    "RMSE": round(rmse, 2),
                    "R2": round(r2, 4),
                    "sMAPE": round(smape, 2),
                    "F1_150": round(f1_150, 4) if f1_150 is not None else None,
                    "max_error": round(float(np.max(np.abs(y_true - y_p))), 1),
                }
            )

        leaderboard_rows.sort(key=lambda x: x["MAE"])
        for rank_idx, r_item in enumerate(leaderboard_rows, start=1):
            r_item["rank"] = rank_idx

        # Head-to-Head Battle: LSTM (PyTorch) vs MLP (64, 32)
        battle_stats = {}
        if "LSTM (PyTorch)" in err_matrix and "MLP (64, 32)" in err_matrix and len(y_true) > 0:
            err_lstm = err_matrix["LSTM (PyTorch)"]
            err_mlp = err_matrix["MLP (64, 32)"]
            lstm_wins = int(np.sum(err_lstm < err_mlp))
            total_pts = len(y_true)
            win_rate = round(lstm_wins / total_pts * 100, 1)
            mae_lstm = float(np.mean(err_lstm))
            mae_mlp = float(np.mean(err_mlp))
            battle_stats = {
                "model_a": "LSTM (PyTorch)",
                "model_b": "MLP (64, 32)",
                "lstm_win_rate_pct": win_rate,
                "lstm_wins_count": lstm_wins,
                "total_hours": total_pts,
                "lstm_mae": round(mae_lstm, 2),
                "mlp_mae": round(mae_mlp, 2),
                "mae_saved": round(mae_mlp - mae_lstm, 2),
                "improvement_pct": round((mae_mlp - mae_lstm) / (mae_mlp + 1e-8) * 100, 1),
            }

        return {
            "scenario": scenario,
            "start_date": start_date,
            "end_date": end_date,
            "min_available_date": min_avail,
            "max_available_date": max_avail,
            "source_mode": source_mode,
            "has_dual_source_overlap": has_dual_overlap,
            "sources_in_window": sources_in_window,
            "total_window_records": len(lb_df),
            "extreme_hours_150": int(np.sum(y_true > 150)),
            "stations": stations_series,
            "leaderboard": leaderboard_rows,
            "head_to_head": battle_stats,
        }

