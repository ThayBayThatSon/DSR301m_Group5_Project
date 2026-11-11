import os
import time
import joblib
import numpy as np
import pandas as pd
import shap
import torch
import torch.nn as nn

DEVICE = torch.device("cpu")

STATION_META = {
    "FRES": {
        "region": "Fresno",
        "basin": "San Joaquin Valley",
        "name": "Fresno - Central Valley",
        "openmeteo_id": "FRES_OPENMETEO",
        "epa_id": "FRES",
        "lat": 36.7854,
        "lon": -119.7732,
        "elevation_m": 102,
        "topography_desc": "Lòng chảo thung lũng San Joaquin bị bao bọc bởi dãy Sierra Nevada và Coast Ranges, dễ xảy ra nghịch nhiệt mùa đông và bẫy khói cháy rừng.",
    },
    "LA": {
        "region": "Los Angeles",
        "basin": "South Coast Basin",
        "name": "Los Angeles - South Coast",
        "openmeteo_id": "LA_OPENMETEO",
        "epa_id": "LA",
        "lat": 34.0664,
        "lon": -118.2268,
        "elevation_m": 87,
        "topography_desc": "Đô thị mật độ cao ven Thái Bình Dương, chịu tác động giao thoa giữa gió biển ban ngày, bức tường núi San Gabriel và gió khô nóng Santa Ana.",
    },
    "SJ": {
        "region": "San Jose",
        "basin": "San Francisco Bay Area",
        "name": "San Jose - Bay Area",
        "openmeteo_id": "SJ_OPENMETEO",
        "epa_id": "SJ_OPENMETEO",
        "lat": 37.3382,
        "lon": -121.8863,
        "elevation_m": 26,
        "topography_desc": "Cực nam vùng vịnh San Francisco, thông thoáng hơn nhờ luồng gió biển tự nhiên nhưng vẫn tích tụ khí thải đô thị vào giờ cao điểm.",
    },
}

STATION_MAP = {
    "FRES": 0,
    "FRES_OPENMETEO": 1,
    "LA": 2,
    "LA_OPENMETEO": 3,
    "SJ_OPENMETEO": 4,
}

FEATURE_LABELS_VI = {
    "target_aqi_lag_0": "AQI quan trắc hiện tại",
    "target_aqi_lag_1": "AQI 1 giờ trước",
    "target_aqi_lag_2": "AQI 2 giờ trước",
    "target_aqi_lag_3": "AQI 3 giờ trước",
    "target_aqi_lag_24": "AQI cùng giờ hôm qua",
    "target_aqi_lag_48": "AQI 2 ngày trước",
    "diff_1h": "Biến động AQI 1h gần nhất",
    "roll_mean_3h": "AQI trung bình 3 giờ qua",
    "roll_std_3h": "Độ biến động AQI 3h",
    "roll_mean_24h": "AQI trung bình 24h qua",
    "temperature_2m": "Nhiệt độ không khí (2m)",
    "relative_humidity_2m": "Độ ẩm tương đối",
    "rain": "Lượng mưa tích lũy",
    "cloud_cover": "Độ che phủ mây",
    "wind_speed_10m": "Tốc độ gió bề mặt",
    "surface_pressure": "Áp suất khí quyển",
    "wind_u": "Gió hướng Đông–Tây",
    "wind_v": "Gió hướng Bắc–Nam",
    "vpd_kpa": "Độ bốc hơi ẩm (VPD)",
    "hour_sin": "Khung giờ trong ngày",
    "hour_cos": "Chu kỳ ngày và đêm",
    "month_sin": "Mùa khí hậu trong năm",
    "month_cos": "Chu kỳ thời tiết năm",
    "is_weekend": "Tác động ngày cuối tuần",
    "station_id": "Vị trí và Lưu vực trạm",
    "future_temp_2m": "Nhiệt độ dự báo (+24h)",
    "future_rh_2m": "Độ ẩm dự báo (+24h)",
    "future_wind_speed": "Tốc độ gió dự báo (+24h)",
    "future_wind_u": "Gió Đông–Tây (+24h)",
    "future_wind_v": "Gió Bắc–Nam (+24h)",
    "future_rain": "Lượng mưa dự báo (+24h)",
    "future_cloud_cover": "Độ che phủ mây (+24h)",
    "future_surface_pressure": "Áp suất dự báo (+24h)",
    "future_vpd_kpa": "Độ bốc hơi VPD (+24h)",
}


class SpatioTemporalLSTM(nn.Module):
    def __init__(self, in_dim, emb_dim=8, num_stations=5, hidden_dim=64, num_layers=2, dropout=0.2):
        super().__init__()
        self.station_emb = nn.Embedding(num_stations, emb_dim)
        self.lstm = nn.LSTM(
            input_size=in_dim + emb_dim,
            hidden_size=hidden_dim,
            num_layers=num_layers,
            batch_first=True,
            dropout=dropout if num_layers > 1 else 0.0,
        )
        self.head = nn.Sequential(
            nn.LayerNorm(hidden_dim),
            nn.Dropout(dropout),
            nn.Linear(hidden_dim, 32),
            nn.SiLU(),
            nn.Linear(32, 1),
        )

    def forward(self, x_seq, x_station):
        B, T, _ = x_seq.shape
        emb = self.station_emb(x_station)
        emb_expanded = emb.unsqueeze(1).expand(-1, T, -1)
        x_in = torch.cat([x_seq, emb_expanded], dim=-1)
        lstm_out, _ = self.lstm(x_in)
        out = self.head(lstm_out[:, -1, :])
        return out.squeeze(-1)


class MultiModelInferenceEngine:
    def __init__(self, artifacts_dir="artifacts"):
        self.artifacts_dir = artifacts_dir
        self.models = {"1h": {}, "24h": {}}
        self.scalers = {"1h": {}, "24h": {}}
        self.explainers = {}
        self._load_all_models()

    def _load_all_models(self):
        for sc, in_dim in [("1h", 21), ("24h", 18)]:
            m_dir = os.path.join(self.artifacts_dir, "models")
            self.models[sc]["ridge"] = joblib.load(os.path.join(m_dir, f"model_ridge_{sc}.joblib"))
            self.scalers[sc]["ridge"] = joblib.load(os.path.join(m_dir, f"scaler_ridge_{sc}.joblib"))

            self.models[sc]["mlp"] = joblib.load(os.path.join(m_dir, f"model_mlp_{sc}.joblib"))
            self.scalers[sc]["mlp"] = joblib.load(os.path.join(m_dir, f"scaler_mlp_{sc}.joblib"))

            self.models[sc]["rf"] = joblib.load(os.path.join(m_dir, f"model_rf_{sc}.joblib"))
            self.models[sc]["lightgbm"] = joblib.load(os.path.join(m_dir, f"model_lightgbm_{sc}.joblib"))
            self.models[sc]["xgboost"] = joblib.load(os.path.join(m_dir, f"model_xgboost_{sc}.joblib"))
            self.models[sc]["catboost"] = joblib.load(os.path.join(m_dir, f"model_catboost_{sc}.joblib"))

            wf_path = os.path.join(m_dir, f"model_wildfire_specialist_{sc}.joblib")
            if os.path.exists(wf_path):
                self.models[sc]["wildfire_specialist"] = joblib.load(wf_path)
            else:
                self.models[sc]["wildfire_specialist"] = None

            self.scalers[sc]["lstm"] = joblib.load(os.path.join(m_dir, f"scaler_lstm_{sc}.joblib"))
            lstm_net = SpatioTemporalLSTM(in_dim=in_dim, emb_dim=8, num_stations=5, hidden_dim=64, num_layers=2, dropout=0.2)
            lstm_net.load_state_dict(
                torch.load(os.path.join(m_dir, f"model_lstm_{sc}.pt"), map_location=DEVICE, weights_only=True)
            )
            lstm_net.eval()
            self.models[sc]["lstm"] = lstm_net

            self.explainers[sc] = shap.TreeExplainer(self.models[sc]["lightgbm"])

    @staticmethod
    def compute_derived_physics(temp_c, rh, wind_spd, wind_dir, dt):
        e_s = 0.6108 * np.exp((17.27 * temp_c) / (temp_c + 237.3))
        vpd_kpa = float(e_s * (1.0 - rh / 100.0))
        rad = np.deg2rad(wind_dir)
        wind_u = float(wind_spd * np.cos(rad))
        wind_v = float(wind_spd * np.sin(rad))
        hour_sin = float(np.sin(2 * np.pi * dt.hour / 24.0))
        hour_cos = float(np.cos(2 * np.pi * dt.hour / 24.0))
        month_sin = float(np.sin(2 * np.pi * dt.month / 12.0))
        month_cos = float(np.cos(2 * np.pi * dt.month / 12.0))
        is_weekend = int(dt.dayofweek in [5, 6])
        return {
            "vpd_kpa": vpd_kpa,
            "wind_u": wind_u,
            "wind_v": wind_v,
            "hour_sin": hour_sin,
            "hour_cos": hour_cos,
            "month_sin": month_sin,
            "month_cos": month_cos,
            "is_weekend": is_weekend,
        }

    def predict_single_step_all_models(self, scenario, feat_dict_seq, station_str):
        """
        feat_dict_seq: list of up to 6 feature dicts (chronological, last element is current step t)
        station_str: e.g. 'FRES_OPENMETEO'
        Returns dict of predictions from all models + SHAP breakdown for the last step.
        """
        curr_feat = feat_dict_seq[-1].copy()
        num_cols = list(self.scalers[scenario]["lstm"].feature_names_in_)
        tree_cols = ["station_id"] + num_cols

        # Tree input
        st_idx = STATION_MAP.get(station_str, 1)
        row_tree = pd.DataFrame([{**curr_feat, "station_id": st_idx}])[tree_cols]

        p_lgb = float(np.clip(self.models[scenario]["lightgbm"].predict(row_tree)[0], 0, 500))
        p_xgb = float(np.clip(self.models[scenario]["xgboost"].predict(row_tree)[0], 0, 500))
        p_cat = float(np.clip(self.models[scenario]["catboost"].predict(row_tree)[0], 0, 500))
        p_rf = float(np.clip(self.models[scenario]["rf"].predict(row_tree)[0], 0, 500))
        p_ens = float((p_lgb + p_xgb + p_cat) / 3.0)

        # Dummy input for Ridge & MLP
        dummy_cols = list(self.scalers[scenario]["ridge"].feature_names_in_)
        row_dummy = {c: curr_feat.get(c, 0.0) for c in dummy_cols}
        for st_k in ["FRES_OPENMETEO", "LA", "LA_OPENMETEO", "SJ_OPENMETEO"]:
            col_k = f"station_id_{st_k}"
            if col_k in row_dummy:
                row_dummy[col_k] = 1.0 if station_str == st_k else 0.0
        df_dummy = pd.DataFrame([row_dummy])[dummy_cols]

        p_ridge = float(
            np.clip(
                self.models[scenario]["ridge"].predict(self.scalers[scenario]["ridge"].transform(df_dummy))[0],
                0,
                500,
            )
        )
        p_mlp = float(
            np.clip(
                self.models[scenario]["mlp"].predict(self.scalers[scenario]["mlp"].transform(df_dummy))[0],
                0,
                500,
            )
        )

        # LSTM sequence input (6 steps)
        seq_rows = []
        for step_d in feat_dict_seq[-6:]:
            seq_rows.append([step_d.get(c, 0.0) for c in num_cols])
        while len(seq_rows) < 6:
            seq_rows.insert(0, seq_rows[0])
        df_seq_num = pd.DataFrame(seq_rows, columns=num_cols)
        arr_seq_scaled = self.scalers[scenario]["lstm"].transform(df_seq_num)
        t_seq = torch.tensor(arr_seq_scaled, dtype=torch.float32).unsqueeze(0)
        t_st = torch.tensor([st_idx], dtype=torch.long)
        with torch.no_grad():
            p_lstm = float(np.clip(self.models[scenario]["lstm"](t_seq, t_st).item(), 0, 500))

        p_pers = float(curr_feat.get("target_aqi_lag_0", 50.0))

        # Wildfire specialist & Detector gating (v2: Physics & Santa Ana enhanced)
        p_wf_spec = p_ens
        if self.models[scenario].get("wildfire_specialist") is not None:
            row_wf = row_tree.copy()
            if scenario == "1h":
                lag0 = float(curr_feat.get("target_aqi_lag_0", 50.0))
                lag1 = float(curr_feat.get("target_aqi_lag_1", lag0))
                roll3 = float(curr_feat.get("roll_mean_3h", lag0))
                w_spd = float(curr_feat.get("wind_speed_10m", 5.0))
                vpd = float(curr_feat.get("vpd_kpa", 0.0))
                w_u = float(curr_feat.get("wind_u", 0.0))
                w_v = float(curr_feat.get("wind_v", 0.0))
                rh = float(curr_feat.get("relative_humidity_2m", 50.0))
                diff = float(curr_feat.get("diff_1h", 0.0))

                row_wf['smoke_persistence_ratio'] = (lag0 + lag1) / (roll3 + 10.0)
                row_wf['fire_dryness_flux'] = w_spd * vpd
                row_wf['mountain_wind_alignment'] = max(0.0, -w_u - w_v)
                row_wf['santa_ana_index'] = row_wf['mountain_wind_alignment'] * vpd * (100.0 / (rh + 10.0))

                dry_score = np.clip((vpd - 1.8) / 1.8, 0, 1) * 0.4 + np.clip((30.0 - rh) / 20.0, 0, 1) * 0.35 + np.clip((w_spd - 12.0) / 15.0, 0, 1) * 0.25
                smoke_score = np.clip((lag0 - 70.0) / 70.0, 0, 1) * 0.65 + np.clip(diff / 15.0, 0, 1) * 0.35
                santa_score = np.clip(float(row_wf['santa_ana_index'].iloc[0]) / 15.0, 0, 1)
                raw = dry_score * smoke_score * 1.2 + santa_score * smoke_score * 0.4 + np.clip((lag0 - 140.0) / 100.0, 0, 1) * 0.5
                prob_wf = float(np.clip(1.0 / (1.0 + np.exp(-12.0 * (raw - 0.28))), 0.0, 1.0))
            else:
                lag0 = float(curr_feat.get("target_aqi_lag_0", 50.0))
                lag24 = float(curr_feat.get("target_aqi_lag_24", lag0))
                roll24 = float(curr_feat.get("roll_mean_24h", lag0))
                w_spd = float(curr_feat.get("future_wind_speed", 5.0))
                vpd = float(curr_feat.get("future_vpd_kpa", 0.0))
                w_u = float(curr_feat.get("future_wind_u", 0.0))
                w_v = float(curr_feat.get("future_wind_v", 0.0))
                rh = float(curr_feat.get("future_rh_2m", 50.0))

                row_wf['smoke_multi_day_max'] = max(lag0, lag24)
                row_wf['smoke_persistence_ratio'] = (lag0 + lag24) / (roll24 + 10.0)
                row_wf['fire_dryness_flux'] = w_spd * vpd
                row_wf['mountain_wind_alignment'] = max(0.0, -w_u - w_v)
                row_wf['santa_ana_index'] = row_wf['mountain_wind_alignment'] * vpd * (100.0 / (rh + 10.0))

                dry_score = np.clip((vpd - 1.8) / 1.8, 0, 1) * 0.35 + np.clip((28.0 - rh) / 18.0, 0, 1) * 0.35 + np.clip((w_spd - 12.0) / 15.0, 0, 1) * 0.30
                smoke_score = np.clip((lag0 - 70.0) / 60.0, 0, 1) * 0.4 + np.clip((roll24 - 60.0) / 60.0, 0, 1) * 0.3 + np.clip((max(lag0, lag24) - 80.0) / 60.0, 0, 1) * 0.3
                santa_score = np.clip(float(row_wf['santa_ana_index'].iloc[0]) / 15.0, 0, 1)
                raw = dry_score * smoke_score * 1.1 + santa_score * smoke_score * 0.5 + np.clip((lag0 - 130.0) / 90.0, 0, 1) * 0.5
                prob_wf = float(np.clip(1.0 / (1.0 + np.exp(-12.0 * (raw - 0.28))), 0.0, 1.0))

            p_wf_spec = float(np.clip(self.models[scenario]["wildfire_specialist"].predict(row_wf)[0], 0, 500))
        else:
            prob_wf = 0.0

        p_wf_layer = float(np.clip((1.0 - prob_wf) * p_ens + prob_wf * p_wf_spec, 0, 500))

        return {
            "Wildfire Specialist (2-Stage)": round(p_wf_layer, 2),
            "Voting Ensemble": round(p_ens, 2),
            "LSTM (PyTorch)": round(p_lstm, 2),
            "LightGBM": round(p_lgb, 2),
            "XGBoost": round(p_xgb, 2),
            "CatBoost": round(p_cat, 2),
            "Random Forest": round(p_rf, 2),
            "MLP (64, 32)": round(p_mlp, 2),
            "Ridge Regression": round(p_ridge, 2),
            "Persistence": round(p_pers, 2),
        }

    def explain_live_shap(self, scenario, curr_feat, station_str, top_k=8):
        num_cols = list(self.scalers[scenario]["lstm"].feature_names_in_)
        tree_cols = ["station_id"] + num_cols
        st_idx = STATION_MAP.get(station_str, 1)
        row_tree = pd.DataFrame([{**curr_feat, "station_id": st_idx}])[tree_cols]

        explainer = self.explainers[scenario]
        shap_vals = explainer.shap_values(row_tree)[0]
        base_val = float(
            explainer.expected_value[0]
            if isinstance(explainer.expected_value, (list, np.ndarray))
            else explainer.expected_value
        )
        pred_val = float(self.models[scenario]["lightgbm"].predict(row_tree)[0])

        contributions = []
        for col, s_val in zip(tree_cols, shap_vals):
            raw_v = row_tree.iloc[0][col]
            contributions.append(
                {
                    "feature": col,
                    "label": FEATURE_LABELS_VI.get(col, col),
                    "value": round(float(raw_v), 2) if col != "station_id" else station_str,
                    "shap": round(float(s_val), 2),
                    "abs_shap": abs(float(s_val)),
                }
            )
        contributions.sort(key=lambda x: x["abs_shap"], reverse=True)
        return {
            "scenario": scenario,
            "base_value": round(base_val, 2),
            "predicted_value": round(pred_val, 2),
            "top_features": contributions[:top_k],
        }

    def forecast_next_24_hours(self, df_station_recent, station_str, weather_overrides=None, wildfire_mode=False):
        """
        df_station_recent: DataFrame sorted by time ascending, containing past 72h up to current_hour + 24h forecast weather from Open-Meteo.
        weather_overrides: optional dict for What-If simulator {'temperature_2m': ..., 'relative_humidity_2m': ..., 'wind_speed_10m': ..., 'rain': ...}
        wildfire_mode: boolean flag to simulate severe California wildfire plume conditions (Camp Fire / Palisades event).
        """
        df_w = df_station_recent.copy().sort_values("time").reset_index(drop=True)
        df_w["time"] = pd.to_datetime(df_w["time"])

        # Current time is the latest row that has actual observed AQI (or 24 hours before the end of forecast)
        now_idx = max(len(df_w) - 25, len(df_w) // 2)
        if "is_forecast" in df_w.columns:
            hist_indices = df_w.index[~df_w["is_forecast"]].tolist()
            if hist_indices:
                now_idx = hist_indices[-1]

        # Apply Wildfire smoke plume & weather overrides if active
        if wildfire_mode:
            df_w.loc[now_idx:, "temperature_2m"] = 34.0
            df_w.loc[now_idx:, "relative_humidity_2m"] = 14.0
            df_w.loc[now_idx:, "wind_speed_10m"] = 38.0
            df_w.loc[now_idx:, "rain"] = 0.0
            df_w.loc[now_idx, "target_aqi"] = 312.0
            df_w.loc[now_idx, "pm25_ug_m3"] = 262.0
            if "subindex_pm25" in df_w.columns:
                df_w.loc[now_idx, "subindex_pm25"] = 312.0
        elif weather_overrides:
            for k, v in weather_overrides.items():
                if v is not None and k in df_w.columns:
                    df_w.loc[now_idx:, k] = float(v)

        # Build sequence of feature dicts up to now_idx for 1h model
        aqi_history = df_w.loc[:now_idx, "target_aqi"].tolist()
        time_history = df_w.loc[:now_idx, "time"].tolist()

        def make_1h_feat(idx_row, aqi_hist):
            r = df_w.iloc[idx_row]
            dt = r["time"]
            phys = self.compute_derived_physics(
                r["temperature_2m"], r["relative_humidity_2m"], r["wind_speed_10m"], r["wind_direction_10m"], dt
            )
            lag0 = float(aqi_hist[-1])
            lag1 = float(aqi_hist[-2]) if len(aqi_hist) >= 2 else lag0
            lag2 = float(aqi_hist[-3]) if len(aqi_hist) >= 3 else lag1
            lag3 = float(aqi_hist[-4]) if len(aqi_hist) >= 4 else lag2
            roll3 = float(np.mean([lag1, lag2, lag3]))
            std3 = float(np.std([lag1, lag2, lag3]))
            return {
                "target_aqi_lag_0": lag0,
                "target_aqi_lag_1": lag1,
                "target_aqi_lag_2": lag2,
                "target_aqi_lag_3": lag3,
                "diff_1h": lag0 - lag1,
                "roll_mean_3h": roll3,
                "roll_std_3h": std3,
                "temperature_2m": float(r["temperature_2m"]),
                "relative_humidity_2m": float(r["relative_humidity_2m"]),
                "rain": float(r["rain"]),
                "cloud_cover": float(r["cloud_cover"]),
                "wind_speed_10m": float(r["wind_speed_10m"]),
                "surface_pressure": float(r["surface_pressure"]),
                **phys,
            }

        def make_24h_feat(idx_curr, idx_fut, aqi_hist):
            r_fut = df_w.iloc[min(idx_fut, len(df_w) - 1)]
            dt_fut = r_fut["time"]
            phys_fut = self.compute_derived_physics(
                r_fut["temperature_2m"],
                r_fut["relative_humidity_2m"],
                r_fut["wind_speed_10m"],
                r_fut["wind_direction_10m"],
                dt_fut,
            )
            lag0 = float(aqi_hist[-1])
            lag24 = float(aqi_hist[-25]) if len(aqi_hist) >= 25 else lag0
            lag48 = float(aqi_hist[-49]) if len(aqi_hist) >= 49 else lag24
            roll24 = float(np.mean(aqi_hist[-48:-24])) if len(aqi_hist) >= 48 else float(np.mean(aqi_hist[-24:]))
            return {
                "future_temp_2m": float(r_fut["temperature_2m"]),
                "future_rh_2m": float(r_fut["relative_humidity_2m"]),
                "future_wind_speed": float(r_fut["wind_speed_10m"]),
                "future_wind_u": phys_fut["wind_u"],
                "future_wind_v": phys_fut["wind_v"],
                "future_rain": float(r_fut["rain"]),
                "future_cloud_cover": float(r_fut["cloud_cover"]),
                "future_surface_pressure": float(r_fut["surface_pressure"]),
                "future_vpd_kpa": phys_fut["vpd_kpa"],
                "target_aqi_lag_0": lag0,
                "target_aqi_lag_24": lag24,
                "target_aqi_lag_48": lag48,
                "roll_mean_24h": roll24,
                "future_hour_sin": phys_fut["hour_sin"],
                "future_hour_cos": phys_fut["hour_cos"],
                "future_month_sin": phys_fut["month_sin"],
                "future_month_cos": phys_fut["month_cos"],
                "future_is_weekend": phys_fut["is_weekend"],
            }

        # Build initial 6-step window for 1h and 24h
        seq_1h = []
        seq_24h = []
        start_w = max(4, now_idx - 5)
        for idx_s in range(start_w, now_idx + 1):
            sub_hist = df_w.loc[:idx_s, "target_aqi"].tolist()
            seq_1h.append(make_1h_feat(idx_s, sub_hist))
            seq_24h.append(make_24h_feat(idx_s, min(idx_s + 24, len(df_w) - 1), sub_hist))

        # Direct 24h anchor prediction at t+24
        preds_24h_direct = self.predict_single_step_all_models("24h", seq_24h, station_str)
        shap_1h = self.explain_live_shap("1h", seq_1h[-1], station_str)
        shap_24h = self.explain_live_shap("24h", seq_24h[-1], station_str)

        # Roll forward 1..24 hours
        hourly_trajectory = []
        sim_aqi_lstm = list(aqi_history)
        sim_aqi_ens = list(aqi_history)
        sim_seq_1h = list(seq_1h)

        horizons_summary = {}

        for step_h in range(1, 25):
            fut_idx = min(now_idx + step_h, len(df_w) - 1)
            dt_target = df_w.iloc[now_idx]["time"] + pd.Timedelta(hours=step_h)

            if step_h == 1:
                step_preds = self.predict_single_step_all_models("1h", sim_seq_1h, station_str)
            else:
                step_preds = self.predict_single_step_all_models("1h", sim_seq_1h, station_str)
                # Smoothly blend with 24h direct model as horizon approaches 24h
                alpha = min(1.0, (step_h - 1) / 23.0)
                for m_k in step_preds:
                    step_preds[m_k] = round(
                        (1.0 - 0.65 * alpha) * step_preds[m_k] + (0.65 * alpha) * preds_24h_direct[m_k], 2
                    )

            if step_h == 24:
                step_preds = preds_24h_direct

            if wildfire_mode:
                for m_k in step_preds:
                    step_preds[m_k] = round(max(float(step_preds[m_k]), 285.0 + 28.0 * np.sin((step_h + 2) / 3.8)), 1)

            if step_h in [1, 2, 3, 24]:
                horizons_summary[f"+{step_h}h"] = {
                    "horizon": f"+{step_h}h",
                    "target_time": dt_target.strftime("%Y-%m-%d %H:%M"),
                    "primary_aqi": step_preds["LSTM (PyTorch)"] if step_h <= 3 else step_preds["Voting Ensemble"],
                    "primary_model": "LSTM (PyTorch)" if step_h <= 3 else "Voting Ensemble",
                    "models": step_preds,
                }

            # Compute 90% Confidence Interval (Prediction Uncertainty Band)
            m_vals = [
                step_preds["Voting Ensemble"],
                step_preds["LSTM (PyTorch)"],
                step_preds["LightGBM"],
                step_preds["MLP (64, 32)"],
                step_preds["Ridge Regression"],
            ]
            m_std = float(np.std(m_vals))
            sigma_h = max(1.8, m_std) * np.sqrt(1.0 + 0.045 * step_h)
            ci_half = 1.645 * sigma_h
            ens_center = step_preds["Voting Ensemble"]
            ci_lower = max(0.0, round(ens_center - ci_half, 1))
            ci_upper = min(500.0, round(ens_center + ci_half, 1))

            hourly_trajectory.append(
                {
                    "step": f"+{step_h}h",
                    "time": dt_target.strftime("%Y-%m-%d %H:%M"),
                    "hour_label": dt_target.strftime("%H:%M"),
                    "temp_c": round(float(df_w.iloc[fut_idx]["temperature_2m"]), 1),
                    "wind_kmh": round(float(df_w.iloc[fut_idx]["wind_speed_10m"]), 1),
                    "rh_pct": round(float(df_w.iloc[fut_idx]["relative_humidity_2m"]), 0),
                    "LSTM (PyTorch)": step_preds["LSTM (PyTorch)"],
                    "Voting Ensemble": step_preds["Voting Ensemble"],
                    "LightGBM": step_preds["LightGBM"],
                    "MLP (64, 32)": step_preds["MLP (64, 32)"],
                    "Ridge Regression": step_preds["Ridge Regression"],
                    "ci_lower": ci_lower,
                    "ci_upper": ci_upper,
                }
            )

            # Advance autoregressive state using average of LSTM and Ensemble
            next_aqi_est = 0.5 * step_preds["LSTM (PyTorch)"] + 0.5 * step_preds["Voting Ensemble"]
            sim_aqi_lstm.append(next_aqi_est)
            sim_seq_1h.append(make_1h_feat(fut_idx, sim_aqi_lstm))
            sim_seq_1h = sim_seq_1h[-6:]

        # Find best outdoor 3-hour window in the next 24h
        best_window = min(hourly_trajectory, key=lambda x: x["Voting Ensemble"])

        curr_row = df_w.iloc[now_idx]
        curr_phys = self.compute_derived_physics(
            curr_row["temperature_2m"],
            curr_row["relative_humidity_2m"],
            curr_row["wind_speed_10m"],
            curr_row["wind_direction_10m"],
            curr_row["time"],
        )

        # Determine dominant pollutant and criteria sub-indices
        sub_pm25 = round(float(curr_row.get("subindex_pm25", curr_row["target_aqi"])), 1)
        sub_pm10 = round(float(curr_row.get("subindex_pm10", 11.0)), 1)
        sub_o3 = round(float(curr_row.get("subindex_ozone", 35.0)), 1)
        o3_conc = round(float(curr_row.get("ozone_ug_m3", 40.0)), 1)

        if wildfire_mode:
            sub_pm25 = 312.0
            dom_key, dom_name, dom_sub = ("pm25", "Khói bụi cháy rừng (PM2.5)", 312.0)
        else:
            pollutant_candidates = [
                ("pm25", "Bụi mịn PM2.5", sub_pm25),
                ("pm10", "Bụi thô PM10", sub_pm10),
                ("ozone", "Khí Ozone (O₃)", sub_o3),
            ]
            dom_key, dom_name, dom_sub = max(pollutant_candidates, key=lambda x: x[2])

        return {
            "current": {
                "time": curr_row["time"].strftime("%Y-%m-%d %H:%M"),
                "aqi": round(float(curr_row["target_aqi"]), 1),
                "pm25": round(float(curr_row["pm25_ug_m3"]), 2),
                "pm10": round(float(curr_row["pm10_ug_m3"]), 2),
                "ozone": o3_conc,
                "subindex_pm25": sub_pm25,
                "subindex_pm10": sub_pm10,
                "subindex_ozone": sub_o3,
                "dominant_pollutant": dom_key,
                "dominant_pollutant_label": dom_name,
                "dominant_subindex": dom_sub,
                "epa_rule_version": "US EPA 2024 Final Rule (PM2.5 Good ≤ 9.0 µg/m³)",
                "temperature_2m": round(float(curr_row["temperature_2m"]), 1),
                "relative_humidity_2m": round(float(curr_row["relative_humidity_2m"]), 1),
                "wind_speed_10m": round(float(curr_row["wind_speed_10m"]), 1),
                "wind_direction_10m": round(float(curr_row["wind_direction_10m"]), 0),
                "surface_pressure": round(float(curr_row["surface_pressure"]), 1),
                "rain": round(float(curr_row["rain"]), 2),
                "cloud_cover": round(float(curr_row["cloud_cover"]), 0),
                "vpd_kpa": round(curr_phys["vpd_kpa"], 2),
            },
            "horizons": horizons_summary,
            "trajectory_24h": hourly_trajectory,
            "best_outdoor_window": {
                "time": best_window["time"],
                "hour_label": best_window["hour_label"],
                "expected_aqi": best_window["Voting Ensemble"],
            },
            "shap_1h": shap_1h,
            "shap_24h": shap_24h,
        }

