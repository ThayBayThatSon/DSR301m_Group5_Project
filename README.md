# Dự Báo Chuỗi Thời Gian Chỉ Số Chất Lượng Không Khí (US AQI) Tại California

> **Học phần:** DSR301m – Data Science Research & Applied Machine Learning  
> **Đề tài:** Hệ thống đối chuẩn và dự báo chỉ số chất lượng không khí theo giờ tại California (Nowcasting 1h và Day-Ahead 24h)  
> **Tiêu chuẩn tính toán:** US EPA Air Quality Index (Cập nhật tháng 02/2024)  
> **Môi trường triển khai:** Web service FastAPI, hỗ trợ mạng nội bộ và mạng riêng ảo Tailscale (`starlink.tail334064.ts.net`)

---

## 1. Tổng Quan Hệ Thống

Dự án nghiên cứu và triển khai mô hình học máy, học sâu nhằm dự báo chỉ số US AQI theo thời gian thực tại 3 khu vực thuộc California: Fresno (San Joaquin Valley), Los Angeles (South Coast) và San Jose (Bay Area).

### 1.1. Danh mục mô hình
- **Học sâu (Deep Learning):** Spatio-Temporal LSTM triển khai trên PyTorch, sử dụng Station Embedding để biểu diễn thông tin trạm quan trắc.
- **Mô hình chuyên biệt cực đoan (Wildfire Specialist Layer):** Sử dụng cơ chế Gating hai tầng dựa trên chỉ số gió Santa Ana và áp suất hơi thiếu hụt (VPD) để xử lý các đợt phát thải khói cháy rừng.
- **Gradient Boosting Decision Trees (GBDT):** LightGBM, XGBoost, CatBoost.
- **Mô hình kết hợp (Ensemble):** Voting Ensemble trung bình cộng không trọng số từ 3 mô hình GBDT.
- **Mô hình đối chuẩn cơ sở (Baselines):** Random Forest, Multi-Layer Perceptron (MLP 64-32), Ridge Regression, Persistence (quán tính nồng độ) và Climatology (trung bình lịch sử theo giờ và tháng).

### 1.2. Nguồn dữ liệu (2018–2026)
- **US EPA AQS (2018–2024):** Số liệu đo đạc thực tế từ trạm quan trắc mặt đất tại Fresno và Los Angeles.
- **Open-Meteo Air Quality & Weather API (2023–2026):** Số liệu phân tích khí quyển vệ tinh (CAMS/ECMWF) và khí tượng bề mặt (nhiệt độ, độ ẩm, áp suất, mây, mưa, thành phần gió $u, v$).
- **Lưu trữ:** Dữ liệu dự báo của 10 mô hình được lưu dưới định dạng Parquet (`data/app_predictions_*.parquet`, ~204.000 dòng). Trạng thái gọi API và bộ đệm (TTL 60 phút, cooldown 5 phút) được quản lý qua SQLite (`data/aqi_app_store.db`).
- **Cơ chế đồng bộ:** Hệ thống tự động kiểm tra mốc thời gian và tải bổ sung dữ liệu khi phát hiện khoảng trống chuỗi thời gian.

### 1.3. Tiêu chuẩn US EPA 2024
- Áp dụng ngưỡng nồng độ bụi $\text{PM}_{2.5}$ trung bình năm theo quy chuẩn ban hành ngày 07/02/2024 (ngưỡng chuyển mức Tốt sang Trung bình giảm từ $12.0$ xuống $9.0\ \mu\text{g/m}^3$).
- Hiển thị thành phần quyết định AQI (Dominant Pollutant) dựa trên giá trị cực đại giữa các chỉ số thành phần $\text{PM}_{2.5}$, $\text{PM}_{10}$ và Ozone ($O_3$).
- Phân loại màu sắc và khuyến cáo sức khỏe đồng bộ theo bảng phân cấp của EPA (mức Trung bình 51–100 sử dụng mã màu `#eab308`).

### 1.4. Công cụ phân tích và giải thích mô hình
- **TreeSHAP:** Tính toán giá trị đóng góp của các đặc trưng đầu vào đối với kết quả dự báo trong 24 giờ kế tiếp.
- **Mô phỏng kịch bản (What-If):** Kiểm tra phản ứng đầu ra của mô hình khi điều chỉnh các biến khí tượng hoặc giả lập điều kiện cháy rừng.
- **Bản đồ nhiệt chu kỳ ô nhiễm (Diurnal Heatmap):** Ma trận 7 ngày $\times$ 24 giờ thể hiện phân bố AQI trung bình lịch sử.
- **So sánh mô hình (Head-to-Head):** Đối chiếu tỷ lệ dự báo chính xác và sai số giữa hai mô hình bất kỳ trong tập dữ liệu.

---

## 2. Cấu Trúc Thư Mục

```text
Project/
├── app/                                 # Ứng dụng Web FastAPI
│   ├── main.py                          # Định tuyến API và tiến trình nền
│   ├── inference_engine.py              # Xử lý suy luận mô hình và SHAP
│   ├── data_manager.py                  # Quản lý dữ liệu, bộ đệm và đồng bộ
│   └── static/                          # Giao diện người dùng
│       ├── index.html                   # Cấu trúc giao diện
│       ├── app.js                       # Logic xử lý và biểu đồ (Chart.js, ECharts, Leaflet)
│       └── styles.css                   # Định kiểu giao diện
├── artifacts/                           # Trọng số mô hình và kết quả thực nghiệm
│   ├── figures/                         # Biểu đồ khoa học xuất từ notebook
│   ├── metrics/                         # Bảng số liệu đánh giá mô hình (.csv, .json)
│   ├── models/                          # File mô hình (.joblib, .pt, scaler)
│   └── predictions/                     # Kết quả dự báo chi tiết
├── data/                                # Tệp dữ liệu vận hành
│   ├── app_predictions_1h.parquet       # Bảng dự báo 1h (203.783 dòng)
│   ├── app_predictions_24h.parquet      # Bảng dự báo 24h (203.443 dòng)
│   ├── aqi_app_store.db                 # Cơ sở dữ liệu SQLite
│   └── california_aqi_model_ready_extended_2026.csv # Chuỗi thời gian mở rộng
├── notebooks/                           # Chuỗi Jupyter Notebook phân tích và huấn luyện
│   ├── 00_EDA_California_AQI.ipynb
│   ├── 01_Data_Prep_Feature_Store.ipynb
│   ├── 02_Baselines_and_Ridge.ipynb
│   ├── 03_Tree_Ensembles_RF.ipynb
│   ├── 04_Gradient_Boosting_SOTA.ipynb
│   ├── 05_Neural_Network_MLP.ipynb
│   └── 06_Benchmark_Leaderboard_Synthesis.ipynb
├── scripts/                             # Script phụ trợ
│   ├── build_app_parquet_cache.py       # Tái tạo cache Parquet
│   ├── merge_backfill_csv.py            # Bù đắp dữ liệu khuyết
│   └── execute_all_notebooks.py         # Thực thi toàn bộ notebook
├── run_app.py                           # File khởi chạy máy chủ
├── requirements.txt                     # Danh mục thư viện Python
└── README.md
```

---

## 3. Kịch Bản Dự Báo

| Tiêu chí | Kịch bản 1: Nowcasting ($t+1$) | Kịch bản 2: Day-Ahead ($t+24$) |
| :--- | :--- | :--- |
| **Mục tiêu** | Dự báo nồng độ ô nhiễm cho giờ tiếp theo | Dự báo xu hướng ô nhiễm cho 24 giờ tới |
| **Đặc trưng chính** | Độ trễ cảm biến (`lag_0..3`, `roll_mean_3h`, `diff_1h`) | Dự báo thời tiết tương lai $W_{t+24}$ và độ trễ chu kỳ |
| **Mô hình tối ưu** | LSTM (PyTorch) & Voting Ensemble ($\text{MAE} \approx 3,0\ \text{AQI}$) | Voting Ensemble & Wildfire Layer ($\text{MAE} \approx 11,2\ \text{AQI}$) |
| **Yếu tố chi phối** | Quán tính phát thải và lưu chuyển nồng độ cục bộ | Điều kiện khí quyển, bức xạ mặt trời, gió bình lưu |

---

## 4. Kết Quả Thực Nghiệm Trên Tập Kiểm Tra (Test Set)

### Kịch bản 1: Nowcasting 1 giờ ($t+1$)
| Họ mô hình | Tên mô hình | $R^2$ | MAE (AQI) | RMSE (AQI) | sMAPE (%) | F1-Score (>150) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Deep Learning | LSTM (PyTorch) | 0.9572 | 3.01 | 5.14 | 9.4% | 0.564 |
| Ensemble | Voting Ensemble (Top 3) | 0.9555 | 3.06 | 5.21 | 9.6% | 0.552 |
| Gating Layer | Wildfire Specialist Layer | 0.9550 | 3.08 | 5.23 | 9.6% | 0.558 |
| GBDT | LightGBM | 0.9548 | 3.12 | 5.25 | 9.7% | 0.540 |
| GBDT | XGBoost | 0.9546 | 3.14 | 5.27 | 9.8% | 0.536 |
| GBDT | CatBoost | 0.9544 | 3.16 | 5.28 | 9.8% | 0.531 |
| Bagging | Random Forest | 0.9512 | 3.38 | 5.46 | 10.4% | 0.512 |
| Linear | Ridge Regression | 0.9405 | 3.73 | 6.03 | 11.2% | 0.449 |
| Neural Net | MLP Regressor (64, 32) | 0.9362 | 3.86 | 6.25 | 11.6% | 0.432 |
| Baseline | Naïve Persistence | 0.9482 | 3.59 | 5.62 | 10.9% | 0.505 |
| Baseline | Climatology | 0.1497 | 17.53 | 22.86 | 45.8% | 0.000 |

### Kịch bản 2: Day-Ahead 24 giờ ($t+24$)
| Họ mô hình | Tên mô hình | $R^2$ | MAE (AQI) | RMSE (AQI) | sMAPE (%) | F1-Score (>150) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| Gating Layer | Wildfire Specialist Layer | 0.6214 | 11.22 | 15.28 | 31.5% | 0.208 |
| Ensemble | Voting Ensemble (Top 3) | 0.6172 | 11.30 | 15.35 | 31.8% | 0.186 |
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

## 5. Hướng Dẫn Cài Đặt Và Vận Hành

### 5.1. Chạy trên môi trường cục bộ

1. Tạo và kích hoạt môi trường ảo Python:
   ```bash
   python -m venv venv
   # Trên Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Trên Linux hoặc macOS:
   source venv/bin/activate
   ```
2. Cài đặt các gói phụ thuộc:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. Khởi chạy ứng dụng:
   ```bash
   python run_app.py
   ```
4. Truy cập giao diện: `http://localhost:8000`

---

### 5.2. Cấu hình dịch vụ hệ thống trên máy chủ Linux (systemd)

Tạo tệp cấu hình dịch vụ `/etc/systemd/system/aqi-app.service`:

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

Nạp cấu hình và kích hoạt tiến trình:
```bash
sudo systemctl daemon-reload
sudo systemctl enable aqi-app
sudo systemctl start aqi-app
```

---

### 5.3. Cấu hình truy cập từ xa qua Tailscale

Để chuyển tiếp cổng dịch vụ và thiết lập chứng chỉ SSL tự động:
1. Đặt tên định danh thiết bị trên mạng Tailnet:
   ```bash
   sudo tailscale up --hostname=starlink
   ```
2. Kích hoạt tính năng HTTPS trong mục cấu hình DNS tại Tailscale Admin Console.
3. Chuyển tiếp cổng 8000:
   ```bash
   tailscale serve --bg 8000
   ```
4. Địa chỉ truy cập bảo mật: `https://starlink.tail334064.ts.net`

---

## 6. Thực Thi Lại Nghiên Cứu (Notebooks)

Để thực thi tuần tự 7 tệp Jupyter Notebook và xuất các biểu đồ khoa học:
```bash
python scripts/execute_all_notebooks.py
```
Biểu đồ đầu ra định dạng PNG 300 DPI được lưu tại thư mục `artifacts/figures/`.
