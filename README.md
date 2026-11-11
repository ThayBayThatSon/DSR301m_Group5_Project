# California US AQI Live Forecaster & Dual-Source Benchmark Suite (2018–2026)
### Comparative Machine Learning & Deep Learning Time Series Forecasting with Extreme Wildfire Adaptation

> **Course:** DSR301m – Data Science Research & Applied Machine Learning  
> **Topic:** California Hourly Air Quality Index (US AQI) Benchmarking Suite across 1h Nowcasting and 24h Day-Ahead Forecasting  
> **Standard:** Revised US EPA Air Quality Index Standards (February 2024 Rule)  
> **Deployment:** 24/7 Tailscale Server Edition (`starlink.tail334064.ts.net`) · CPU-Optimized Inference

---

## 1. Điểm Nhấn Công Nghệ & Tính Năng Hệ Thống

1. **Hệ thống 10 Mô hình Benchmark Toàn diện:**
   - **Deep Learning:** Spatio-Temporal LSTM (PyTorch) kết hợp kỹ thuật `Station Embedding`.
   - **Extreme Event Layer:** *Wildfire Specialist Layer* (Cơ chế Gating 2 tầng kích hoạt theo chỉ số khô hạn `VPD` & bão gió `Santa Ana Index`).
   - **GBDT SOTA & Ensemble:** LightGBM, XGBoost, CatBoost và Voting Ensemble (Top 3).
   - **Mô hình nền tảng:** Random Forest, MLP (64, 32), Ridge Regression, Persistence và Climatology.
2. **Kho Dữ liệu Kép (Dual-Source Store 2018–2026):**
   - Hợp nhất dữ liệu trạm mặt đất **US EPA AQS** (2018–2024) và dữ liệu vệ tinh phân tích khí quyển **Open-Meteo CAMS/ECMWF** (2023–2026) cho 3 lưu vực: **Fresno (San Joaquin Valley)**, **Los Angeles (South Coast)** và **San Jose (Bay Area)**.
   - Lưu trữ dạng cột siêu tốc **Parquet cache** (~204,000 dòng) và **SQLite App Store** bảo vệ hạn ngạch API.
   - **Tự động đồng bộ giờ khuyết (Active Smart Sync):** Kiểm tra và tự động kéo bù các giờ/ngày mới nhất từ Open-Meteo khi có khoảng trống.
3. **Quy chuẩn Khoa học US EPA 2024:**
   - Áp dụng ngưỡng siết chặt nồng độ bụi mịn $\text{PM}_{2.5}$ hàng năm từ $12.0$ xuống $9.0\ \mu\text{g/m}^3$ ($9.2\ \mu\text{g/m}^3 \rightarrow \text{AQI } 51$).
   - Thẻ phân rã **AQI Breakdown & Dominant Pollutant** theo $\text{PM}_{2.5}$, $\text{PM}_{10}$ và Ozone ($O_3$).
   - Phân loại màu sắc và khuyến cáo sức khỏe chuẩn hóa theo EPA (vàng `#eab308` cho mức Moderate 51–100).
4. **Trực quan hóa & Giải thích Mô hình Thời gian Thực (XAI):**
   - **Live TreeSHAP:** Bóc tách mức độ đóng góp (tăng/giảm AQI) của từng yếu tố khí tượng và nồng độ cảm biến trong 24 giờ tới.
   - **What-If Simulator & Wildfire Mode 🔥:** Giả lập độ nhạy nồng độ bụi mịn khi thay đổi nhiệt độ, độ ẩm, hướng gió hoặc kích hoạt trạng thái cháy rừng khẩn cấp.
   - **Historical Diurnal Heatmap:** Bản đồ nhiệt 7 ngày $\times$ 24 giờ phát hiện chu kỳ ô nhiễm theo giờ trong tuần.
   - **Head-to-Head Arena:** Đấu trường đối đầu trực diện giữa các kiến trúc mô hình (LSTM vs MLP/GBDT).

---

## 2. Kiến Trúc Thư Mục Dự Án (Repository Architecture)

```text
Project/
├── app/                                 # Ứng dụng Web FastAPI Full-Stack
│   ├── main.py                          # Khởi tạo API Server, Background Worker 24/7 & Routing
│   ├── inference_engine.py              # Động cơ nạp model, chạy dự báo 24h & TreeSHAP
│   ├── data_manager.py                  # Quản lý Parquet Cache, SQLite Quota & Active Sync
│   └── static/                          # Giao diện người dùng Single Page Application
│       ├── index.html                   # Giao diện 2 cửa sổ (Live Forecaster & Benchmark Suite)
│       ├── app.js                       # Logic tương tác, ECharts, Chart.js & Leaflet GIS
│       └── styles.css                   # Định kiểu giao diện Tailwind CSS & Dark Mode
├── artifacts/                           # Lưu trữ toàn bộ tài sản mô hình & thực nghiệm
│   ├── figures/                         # Đồ thị khoa học 300 DPI (chuẩn báo cáo Nature/IEEE)
│   ├── metrics/                         # Bảng Leaderboard, Feature Importance, TreeSHAP
│   ├── models/                          # Trọng số huấn luyện (.joblib, PyTorch .pt, scaler)
│   └── predictions/                     # File dự báo chi tiết theo giờ
├── data/                                # Kho dữ liệu ứng dụng
│   ├── app_predictions_1h.parquet       # Cache dự báo 1h (203,783 dòng, 10 mô hình)
│   ├── app_predictions_24h.parquet      # Cache dự báo 24h (203,443 dòng, 10 mô hình)
│   ├── aqi_app_store.db                 # SQLite lưu log gọi API, quota, bộ đệm
│   └── california_aqi_model_ready_extended_2026.csv # Chuỗi quan trắc mở rộng 2018–2026
├── notebooks/                           # Chuỗi 7 Jupyter Notebooks nghiên cứu (00 -> 06)
│   ├── 00_EDA_California_AQI.ipynb
│   ├── 01_Data_Prep_Feature_Store.ipynb
│   ├── 02_Baselines_and_Ridge.ipynb
│   ├── 03_Tree_Ensembles_RF.ipynb
│   ├── 04_Gradient_Boosting_SOTA.ipynb
│   ├── 05_Neural_Network_MLP.ipynb
│   └── 06_Benchmark_Leaderboard_Synthesis.ipynb
├── scripts/                             # Bộ công cụ tự động hóa & nạp dữ liệu
│   ├── build_app_parquet_cache.py       # Tái tạo toàn bộ kho dự báo 1h & 24h Parquet
│   ├── merge_backfill_csv.py            # Bù đắp giờ khuyết lịch sử và hợp nhất dữ liệu mới
│   └── execute_all_notebooks.py         # Thực thi tự động toàn bộ thí nghiệm
├── run_app.py                           # Kịch bản khởi chạy Web Server (Local, LAN, Tailscale)
├── requirements.txt                     # Danh mục thư viện phụ thuộc
└── README.md
```

---

## 3. Hai Kịch Bản Dự Báo Vận Hành (Operational Horizons)

| Tiêu chí | Kịch bản 1: Nowcasting ($t+1$) | Kịch bản 2: Day-Ahead Forecasting ($t+24$) |
| :--- | :--- | :--- |
| **Mục tiêu thực tế** | Cảnh báo nồng độ ô nhiễm tức thời giờ kế tiếp | Kế hoạch điều hành y tế & hoạt động ngoài trời 24h tới |
| **Đặc trưng chủ đạo** | Quán tính cảm biến (`lag_0..3`, `roll_mean_3h`, `diff_1h`) | Dự báo khí tượng tương lai $W_{t+24}$ (`shift(-24)`) + Lags nền |
| **Mô hình dẫn đầu** | **LSTM (PyTorch) & Voting Ensemble** ($\text{MAE} \approx 3.06\ \text{AQI}$) | **Voting Ensemble & Wildfire Layer** ($\text{MAE} \approx 11.30\ \text{AQI}$) |
| **Cơ chế vật lý chi phối**| Động học tự hồi quy nồng độ ô nhiễm cục bộ | Khuếch tán gió biển, bức xạ quang hóa, gió Santa Ana |

---

## 4. Bảng Kết Quả Thực Nghiệm Toàn Diện (Test Set)

### Kịch bản 1: 1h Nowcasting ($t+1$)
| Họ mô hình | Tên mô hình | $R^2$ Test | MAE (AQI) | RMSE (AQI) | sMAPE (%) | F1-Score (>150) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Deep Learning** | **LSTM (PyTorch)** | **0.9572** | **3.01** | **5.14** | **9.4%** | **0.564** |
| **Ensemble** | **Voting Ensemble (Top 3)** | **0.9555** | **3.06** | **5.21** | **9.6%** | **0.552** |
| Extreme Adaptation | Wildfire Specialist Layer | 0.9550 | 3.08 | 5.23 | 9.6% | 0.558 |
| GBDT | LightGBM | 0.9548 | 3.12 | 5.25 | 9.7% | 0.540 |
| GBDT | XGBoost | 0.9546 | 3.14 | 5.27 | 9.8% | 0.536 |
| GBDT | CatBoost | 0.9544 | 3.16 | 5.28 | 9.8% | 0.531 |
| Bagging | Random Forest | 0.9512 | 3.38 | 5.46 | 10.4% | 0.512 |
| Linear | Ridge Regression | 0.9405 | 3.73 | 6.03 | 11.2% | 0.449 |
| Neural Net | MLP Regressor (64, 32) | 0.9362 | 3.86 | 6.25 | 11.6% | 0.432 |
| Baseline | Naïve Persistence | 0.9482 | 3.59 | 5.62 | 10.9% | 0.505 |
| Baseline | Climatology | 0.1497 | 17.53 | 22.86 | 45.8% | 0.000 |

### Kịch bản 2: 24h Day-Ahead Forecasting ($t+24$)
| Họ mô hình | Tên mô hình | $R^2$ Test | MAE (AQI) | RMSE (AQI) | sMAPE (%) | F1-Score (>150) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Extreme Adaptation** | **Wildfire Specialist Layer** | **0.6214** | **11.22** | **15.28** | **31.5%** | **0.208** |
| **Ensemble** | **Voting Ensemble (Top 3)** | **0.6172** | **11.30** | **15.35** | **31.8%** | **0.186** |
| GBDT | LightGBM | 0.6141 | 11.33 | 15.41 | 31.9% | 0.178 |
| GBDT | CatBoost | 0.6125 | 11.38 | 15.44 | 32.1% | 0.174 |
| GBDT | XGBoost | 0.6108 | 11.42 | 15.48 | 32.2% | 0.171 |
| Deep Learning | LSTM (PyTorch) | 0.6085 | 11.49 | 15.56 | 32.4% | 0.182 |
| Bagging | Random Forest | 0.5982 | 11.62 | 15.72 | 32.8% | 0.158 |
| Linear | Ridge Regression | 0.5786 | 11.87 | 16.10 | 33.4% | 0.134 |
| Neural Net | MLP Regressor (64, 32) | 0.5594 | 12.14 | 16.46 | 34.1% | 0.121 |
| Baseline | Naïve Persistence | 0.4590 | 13.02 | 18.23 | 36.5% | 0.098 |
| Baseline | Climatology | 0.1552 | 17.45 | 22.77 | 45.6% | 0.000 |

---

## 5. Hướng Dẫn Khởi Chạy Ứng Dụng (Quickstart & Deployment)

### 5.1. Khởi chạy trên máy cục bộ (Local Development)

```bash
# 1. Tạo môi trường ảo (venv)
python -m venv venv

# 2. Kích hoạt môi trường ảo
.\venv\Scripts\Activate.ps1    # Trên Windows PowerShell
source venv/bin/activate       # Trên Linux / macOS

# 3. Cài đặt các thư viện cần thiết
pip install --upgrade pip
pip install -r requirements.txt

# 4. Khởi động Web Server
python run_app.py
```

Truy cập ngay tại: **`http://localhost:8000`**

---

### 5.2. Chạy ứng dụng trên Máy Server từ xa (Linux VPS / Ubuntu 24/7)

```bash
# Cài đặt dịch vụ hệ thống chạy ngầm tự khởi động khi reboot
sudo nano /etc/systemd/system/aqi-app.service
```

Dán cấu hình sau:
```ini
[Unit]
Description=California AQI Forecaster & Model Benchmark Suite
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/Project
ExecStart=/home/ubuntu/Project/venv/bin/python run_app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Kích hoạt và khởi động:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aqi-app
sudo systemctl start aqi-app
```

---

### 5.3. Cấu hình Tên miền Bảo mật qua Tailscale MagicDNS

Hệ thống hỗ trợ ánh xạ tên miền cá nhân bảo mật HTTPS qua **Tailscale Serve**:

1. **Đặt tên máy chủ:** `sudo tailscale up --hostname=starlink`
2. **Kích hoạt HTTPS:** Trên [Tailscale DNS Console](https://login.tailscale.com/admin/dns), bấm **Enable HTTPS Certificates**.
3. **Chuyển hướng cổng 8000:**
   ```bash
   tailscale serve --bg 8000
   ```
Truy cập qua HTTPS mã hóa không cần gõ cổng:  
👉 **`https://starlink.tail334064.ts.net`**

---

## 6. Tái Lập Thí Nghiệm Nghiên Cứu (Jupyter Notebooks)

Nếu muốn tái tạo lại kết quả nghiên cứu và xuất 9 biểu đồ 300 DPI:
```bash
# Thực thi tự động chuỗi 7 Notebooks
python scripts/execute_all_notebooks.py
```
Toàn bộ biểu đồ sẽ được lưu tự động tại `artifacts/figures/` và nhúng trực tiếp vào các tệp `.ipynb`.
