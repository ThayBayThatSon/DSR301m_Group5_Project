# Comparative US AQI Time Series Forecasting in California with Extreme-Event Evaluation

> **Course:** DSR301m – Data Science Research & Applied Machine Learning  
> **Topic:** California Hourly Air Quality Index (US AQI) Benchmarking Suite across 1h Nowcasting and 24h Day-Ahead Forecasting

---

## 1. Tổng Quan Kiến Trúc Dự Án (Repository Architecture)

Dự án được tái cấu trúc theo chuẩn sản xuất (Production-grade & Clean Architecture), đảm bảo tính cô lập, tự thích ứng đường dẫn tương đối (Path-Agnostic) và khả năng tái lập thực nghiệm 100%:

```text
├── data/
│   ├── raw/                 # Tập dữ liệu gốc: california_aqi_model_ready.csv (181,122 bản ghi)
│   └── processed/           # Feature Store dạng Parquet (1h & 24h: Train, Val, Test)
├── notebooks/               # Chuỗi 7 Jupyter Notebooks phân tích và mô hình hóa (00 -> 06)
│   ├── 00_EDA_California_AQI.ipynb
│   ├── 01_Data_Prep_Feature_Store.ipynb
│   ├── 02_Baselines_and_Ridge.ipynb
│   ├── 03_Tree_Ensembles_RF.ipynb
│   ├── 04_Gradient_Boosting_SOTA.ipynb
│   ├── 05_Neural_Network_MLP.ipynb
│   └── 06_Benchmark_Leaderboard_Synthesis.ipynb
├── scripts/                 # Bộ script tự động hóa xây dựng và thực thi
│   ├── create_notebooks.py       # Tạo mới toàn bộ notebooks với code kỹ thuật chuẩn xác
│   └── execute_all_notebooks.py  # Thực thi tự động và nhúng output vào các file .ipynb
├── artifacts/               # Lưu trữ toàn bộ kết quả thực nghiệm thực tế
│   ├── figures/             # 9 Đồ thị khoa học 300 DPI (chuẩn Nature / IEEE Climate Informatics)
│   ├── metrics/             # Leaderboard, Feature Importance, TreeSHAP values (.csv, .json)
│   ├── models/              # Trọng số mô hình đã huấn luyện (.joblib)
│   └── predictions/         # Dự báo chi tiết của từng mô hình theo từng giờ (.csv)
├── presentations/           # Tài liệu bảo vệ và thuyết trình
│   ├── present1/            # Slide bảo vệ Present 1 (HTML tự đóng gói Base64 + Kịch bản MD)
│   ├── present2/
│   └── present3/
├── image/                   # Bản đồ địa mạo lưu vực và ảnh tư liệu
├── .gitignore               # Cấu hình bỏ qua cache, checkpoint và tệp tạm
└── README.md
```

---

## 2. Hai Kịch Bản Dự Báo Vận Hành (Dual Operational Horizons)

| Tiêu chí | Kịch bản 1: Nowcasting ($t+1$) | Kịch bản 2: Day-Ahead Forecasting ($t+24$) |
| :--- | :--- | :--- |
| **Mục tiêu** | Cảnh báo nồng độ ô nhiễm tức thời giờ kế tiếp | Dự báo điều hành y tế & giao thông 24 giờ tới |
| **Đặc trưng chủ đạo** | Quán tính sensor (`lag_0..3`, `roll_mean_3h`, `diff_1h`) | Dự báo thời tiết tương lai $W_{t+24}$ (`shift(-24)`) + Lags nền |
| **Mô hình dẫn đầu** | **Voting Ensemble** ($\text{MAE} = 3.06, R^2 = 0.956$) | **Voting Ensemble** ($\text{MAE} = 11.30, R^2 = 0.617$) |
| **Cơ chế vật lý chi phối** | Tự hồi quy nồng độ cục bộ của trạm quan trắc | Gió khuếch tán, nhiệt độ quang hóa, nghịch nhiệt đêm |

---

## 3. Bộ Mô Hình Đối Chuẩn (Model Suite)

Bộ benchmark bao gồm **8 mô hình nền tảng + 1 mô hình Blending Ensemble**:
1. **Naïve Persistence:** Dự báo bằng giá trị quan trắc gần nhất ($y_{t}$ hoặc $y_{t-24}$).
2. **Climatology:** Dự báo bằng kỳ vọng lịch sử theo giờ và tháng.
3. **Ridge Regression:** Hồi quy tuyến tính chuẩn hóa $L_2$ (chống đa cộng tuyến).
4. **Random Forest:** Thuật toán Bagging phi tuyến tính (150 cây, song song hóa).
5. **LightGBM:** Gradient Boosting tối ưu tốc độ phân nhánh theo lá (*leaf-wise*).
6. **XGBoost:** Gradient Boosting với chuẩn hóa độ sâu cây và tỉ lệ mẫu ngẫu nhiên.
7. **CatBoost:** Gradient Boosting với cơ chế Symmetric Trees và chống Overfitting.
8. **MLP Regressor:** Mạng nơ-ron truyền thẳng 2 tầng ẩn $(64, 32)$ kích hoạt ReLU.
9. **Voting Ensemble (Top 3):** Trung bình cộng không trọng số của 3 mô hình SOTA GBDT (LightGBM, XGBoost, CatBoost).

---

## 4. Bảng Kết Quả Thực Nghiệm Tổng Hợp (Test Set 2025)

File nguồn: `artifacts/metrics/comprehensive_leaderboard.csv`

### Kịch bản 1: 1h Nowcasting ($t+1$)
| Họ mô hình | Tên mô hình | $R^2$ Test 2025 | MAE (AQI) | RMSE (AQI) | sMAPE (%) | F1-Score (>150) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Ensemble** | **Voting Ensemble (Top 3)** | **0.9555** | **3.06** | **5.21** | **9.6%** | **0.552** |
| GBDT | LightGBM | 0.9548 | 3.12 | 5.25 | 9.7% | 0.540 |
| GBDT | XGBoost | 0.9546 | 3.14 | 5.27 | 9.8% | 0.536 |
| GBDT | CatBoost | 0.9544 | 3.16 | 5.28 | 9.8% | 0.531 |
| Bagging | Random Forest | 0.9512 | 3.38 | 5.46 | 10.4% | 0.512 |
| Linear | Ridge Regression | 0.9405 | 3.73 | 6.03 | 11.2% | 0.449 |
| Neural Net | MLP Regressor | 0.9362 | 3.86 | 6.25 | 11.6% | 0.432 |
| Baseline | Naïve Persistence | 0.9482 | 3.59 | 5.62 | 10.9% | 0.505 |
| Baseline | Climatology | 0.1497 | 17.53 | 22.86 | 45.8% | 0.000 |

### Kịch bản 2: 24h Day-Ahead Forecasting ($t+24$)
| Họ mô hình | Tên mô hình | $R^2$ Test 2025 | MAE (AQI) | RMSE (AQI) | sMAPE (%) | F1-Score (>150) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Ensemble** | **Voting Ensemble (Top 3)** | **0.6172** | **11.30** | **15.35** | **31.8%** | **0.186** |
| GBDT | LightGBM | 0.6141 | 11.33 | 15.41 | 31.9% | 0.178 |
| GBDT | CatBoost | 0.6125 | 11.38 | 15.44 | 32.1% | 0.174 |
| GBDT | XGBoost | 0.6108 | 11.42 | 15.48 | 32.2% | 0.171 |
| Bagging | Random Forest | 0.5982 | 11.62 | 15.72 | 32.8% | 0.158 |
| Linear | Ridge Regression | 0.5786 | 11.87 | 16.10 | 33.4% | 0.134 |
| Neural Net | MLP Regressor | 0.5594 | 12.14 | 16.46 | 34.1% | 0.121 |
| Baseline | Naïve Persistence | 0.4590 | 13.02 | 18.23 | 36.5% | 0.098 |
| Baseline | Climatology | 0.1552 | 17.45 | 22.77 | 45.6% | 0.000 |

---

## 5. Hướng Dẫn Tái Lập Thực Nghiệm (Quickstart & Reproduction)

### Bước 1: Chuẩn bị môi trường Python
```bash
python -m venv venv
venv\Scripts\activate       # Trên Windows
pip install -r requirements.txt # Hoặc cài đặt pandas numpy scikit-learn lightgbm xgboost catboost shap matplotlib seaborn nbclient
```

### Bước 2: Sinh mới toàn bộ Notebooks chuẩn
```bash
python scripts/create_notebooks.py
```

### Bước 3: Thực thi tự động toàn bộ thí nghiệm
```bash
python scripts/execute_all_notebooks.py
```
Toàn bộ kết quả (Leaderboard, dự báo, mô hình, và 9 đồ thị 300 DPI) sẽ được tự động xuất vào thư mục `artifacts/` và nhúng trực tiếp vào các file `.ipynb` trong `notebooks/`.
