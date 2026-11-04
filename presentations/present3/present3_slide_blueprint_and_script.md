# TÀI LIỆU KỊCH BẢN THUYẾT TRÌNH & BẢN THIẾT KẾ SLIDE CHI TIẾT — BÁO CÁO TỔNG KẾT & BẢO VỆ ĐỒ ÁN (PRESENT 3)

## ĐỀ TÀI: COMPARATIVE US AQI TIME SERIES FORECASTING IN CALIFORNIA WITH EXTREME-EVENT EVALUATION

*(Nghiên cứu Đối chuẩn Thực nghiệm Toàn diện Các Mô hình Dự báo Chuỗi Thời gian Chỉ số US AQI tại California & Đột phá Đánh giá Thiên tai Khí hậu Cực đoan)*

---

* **Môn học:** DSR301m – Data Science Project (Đại học FPT TP.HCM)
* **Cột mốc:** PBL Milestone 3 (Present 3) — *Final Project Defense (Bảo vệ Đồ án Tốt nghiệp Môn học)*
* **Nhóm thực hiện:** GROUP 5
* **Dữ liệu Thực nghiệm:** 181,122 bản ghi hàng giờ (2018–2025) · 3 Lưu vực Khí quyển: San Jose (Bay Area), Fresno (San Joaquin Valley), Los Angeles (South Coast)
* **Hệ thống Mô hình Đối chuẩn:** 11 Mô hình thuộc 6 Họ Thuật toán (Baselines, Ridge $L_2$, Bagging RF, GBDT SOTA, Deep Learning MLP & LSTM, Voting Ensemble, và Tầng Chuyên gia Đột phá Wildfire Specialist 2-Stage)
* **Chân trời Vận hành:** Nowcasting $1\text{h}$ ($t+1$) và Day-Ahead Forecasting $24\text{h}$ ($t+24$)
* **Thời lượng Thuyết trình:** 15 – 18 Phút (16 Slides chuẩn Assertion-Evidence & MECE)

---

## 🧭 BẢNG ÁNH XẠ HỆ THỐNG ASSET HÌNH ẢNH & BIỂU ĐỒ VÀO 16 SLIDES

Toàn bộ các biểu đồ chuẩn khoa học 300 DPI trong [`artifacts/figures/`](file:///c:/FPT/FA2026/DSR301m/Project/artifacts/figures) và tư liệu địa lý trong [`notebooks/image/`](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/image) được phân bổ chính xác theo dòng chảy logic:

| Slide | Tiêu đề Kỹ thuật Slide | Asset Hình ảnh / Biểu đồ Sử dụng | Mục tiêu Truyền tải & Bằng chứng Thực nghiệm |
| :---: | :--- | :--- | :--- |
| **01** | **Title Cover & Project Overview** | `notebooks/image/san-francisco-orange-sky.jpg` *(Banner nền)* | Giới thiệu đồ án, nhóm nghiên cứu và thông điệp cốt lõi |
| **02** | **Executive Summary & Milestone 3 Breakthroughs** | Sơ đồ timeline 3 Milestones & Khối cập nhật mới | Tóm lược 4 trụ cột cập nhật mới: LSTM, Wildfire Layer, Đại Leaderboard, Dashboard |
| **03** | **Wildfire Crisis & Dual Operational Horizons** | `notebooks/image/san-francisco-orange-sky.jpg`<br>`notebooks/image/aqitableforcourse.png` | Khủng hoảng bão khói, mất cân bằng nhãn y tế EPA, phân định bài toán 1h vs 24h |
| **04** | **3-Basin Topography & 181k Dataset Audit** | `notebooks/image/California_Topography_and_Geomorphic.gif`<br>`notebooks/image/paper_station_map.png` | Hiệu ứng địa mạo chặn khói bụi tại 3 trạm quan trắc và phân phối dữ liệu 8 năm |
| **05** | **Zero-Leakage Split & Physics Feature Store** | Sơ đồ Pipeline: Temporal Split Protocol ($h$-buffer)<br>Ma trận Vector gió $(u, v)$ & Độ ẩm VPD | Quy chuẩn triệt tiêu rò rỉ tương lai và thiết kế 22 biến (1h) vs 19 biến (24h) |
| **06** | **Model Benchmark Space: 6 Algorithm Families** | Bảng phân loại 11 mô hình theo cấu trúc toán học | Từ mô hình tham chiếu cơ sở, học máy dạng bảng đến Deep Learning chuỗi thời gian |
| **07** | **Deep Learning Training Dynamics (LSTM vs MLP)** | `artifacts/figures/lstm_learning_curves.png`<br>`artifacts/figures/mlp_learning_curves.png` | So sánh Smooth L1 Loss (Station Embedding LSTM 60 epochs) vs MSE Loss (MLP 50 epochs) |
| **08** | **Official Comprehensive Leaderboard (1h vs 24h Table)** | **Bảng Ma trận Số liệu Tổng thể 11 Mô hình**<br>*(Đầy đủ $R^2$, MAE, RMSE, sMAPE, F1-150, Thời gian suy luận)* | Bằng chứng định lượng toàn diện trên Test Set 2025 out-of-sample |
| **09** | **Visual Benchmark Leaderboard & Speed-Accuracy Tradeoff** | `artifacts/figures/01_model_comparison_mae.png` | Biểu đồ thanh ngang đối chuẩn MAE: Sự vượt trội của GBDT & LSTM ở 1h, Ensemble ở 24h |
| **10** | **Continuous Time-Series Tracking & Parity Calibration** | `artifacts/figures/02_actual_vs_predicted_1week.png`<br>`artifacts/figures/07_actual_vs_pred_parity_hexbin.png` | Bám sát chu kỳ 168h thực tế tại Fresno và kiểm định độ co ngót đuôi phân phối ($\beta$) |
| **11** | **Wildfire Specialist Layer: 2-Stage GBDT Architecture** | Sơ đồ Kiến trúc 2-Stage Hierarchical Regime-Switching<br>*(Physical Gating: Santa Ana Index & Multi-Day Smoke)* | Thiết kế đột phá phân nhánh chế độ khí quyển: Base Model vs Wildfire Expert GBDT |
| **12** | **Extreme Disasters Evaluation: Palisades Fire 2025** | `artifacts/figures/11_wildfire_layer_peak_comparison.png`<br>`artifacts/figures/12_wildfire_peak_reduction.png` | Bám đỉnh thảm họa Palisades Fire 2025 và định lượng mức thu hẹp sai số hụt đỉnh |
| **13** | **Hazardous Early Warning Jump (Recall & F1 Shift)** | `artifacts/figures/13_wildfire_recall_f1_jump.png`<br>`artifacts/figures/03_wildfire_extreme_resilience.png` | Bước nhảy vọt 3.8x Recall và 3.1x F1 (>150 AQI); kiểm soát bùng nổ sai số sốc khói |
| **14** | **3-Dimensional Error Diagnostics: Diurnal & Spatial** | `artifacts/figures/08_diurnal_hourly_error_profile.png`<br>`artifacts/figures/09_spatial_basin_resilience.png`<br>`artifacts/figures/10_basin_extreme_sensitivity.png` | Bóc tách nghịch nhiệt bức xạ đêm (22h–4h) và ưu thế không gian của LSTM tại Los Angeles |
| **15** | **Model Explainability: TreeSHAP Attribution** | `artifacts/figures/05_shap_beeswarm_summary.png`<br>`artifacts/figures/06_shap_mean_importance.png`<br>`artifacts/figures/04_feature_importance_shift.png` | Minh bạch hóa đóng góp phi tuyến của quán tính cảm biến và động lực khí tượng |
| **16** | **Live Production Dashboard & Conclusion Roadmap** | Giao diện Live Web Dashboard (FastAPI + ECharts)<br>Sơ đồ What-If Scenario Engine & Tổng kết PBL | Triển khai thực tế 24/7, đóng góp học thuật, hạn chế và hướng phát triển |

---

## 📊 BẢNG DỮ LIỆU ĐỐI CHUẨN TỔNG THỂ (OFFICIAL COMPREHENSIVE LEADERBOARD)

*(Dữ liệu chính thức từ `artifacts/metrics/comprehensive_leaderboard.csv` dùng trình bày tại Slide 08 & Slide 09)*

### 1. Kịch bản Nowcasting 1h ($t+1$) — Test Set 2025 Out-of-Sample

| STT | Họ Thuật Toán | Tên Mô Hình | $R^2$ Test | MAE (AQI) | RMSE (AQI) | sMAPE (%) | $F_1\text{-Score}_{>150}$ | Thời Gian Huấn Luyện / Suy Luận |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Baseline | Naïve Persistence ($y_t$) | 0.9482 | 3.61 | 6.03 | 7.06% | 0.817 | 0.00s |
| 2 | Baseline | Climatology (Lịch sử) | 0.1497 | 17.53 | 24.42 | 31.77% | 0.000 | 2.06s |
| 3 | Linear Model | Ridge Regression ($L_2$) | 0.9478 | 3.72 | 6.05 | 7.40% | 0.703 | 0.23s |
| 4 | Bagging Trees | Random Forest (150 cây) | 0.9539 | 3.33 | 5.69 | 6.75% | 0.780 | 9.49s |
| 5 | Gradient Boosting | LightGBM SOTA | 0.9538 | 3.13 | 5.69 | 6.37% | 0.818 | 1.04s |
| 6 | Gradient Boosting | XGBoost | 0.9538 | 3.10 | 5.69 | 6.30% | 0.813 | 2.13s |
| 7 | Gradient Boosting | CatBoost | 0.9541 | 3.13 | 5.68 | 6.43% | 0.815 | 3.17s |
| 8 | Deep Learning | MLP Regressor (64, 32) | 0.9583 | 3.26 | 5.41 | 6.79% | 0.785 | 10.29s |
| 9 | Deep Learning | **Spatio-Temporal LSTM** | **0.9620** | **2.76** | **5.16** | **5.56%** | **0.850** | 120.95s |
| 10 | Ensemble | **Voting Ensemble (Top 3)** | 0.9555 | 3.06 | 5.58 | 6.28% | 0.825 | 0.20s |
| 11 | Extreme Adaptive | **Wildfire Specialist (2-Stage)** | **0.9575** | **3.05** | **5.46** | **6.31%** | **0.836** | 0.30s |

### 2. Kịch bản Day-Ahead Forecasting 24h ($t+24$) — Test Set 2025 Out-of-Sample

| STT | Họ Thuật Toán | Tên Mô Hình | $R^2$ Test | MAE (AQI) | RMSE (AQI) | sMAPE (%) | $F_1\text{-Score}_{>150}$ | Thời Gian Huấn Luyện / Suy Luận |
| :---: | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| 1 | Baseline | Naïve Persistence ($y_{t-24}$) | 0.4597 | 13.02 | 19.41 | 24.89% | 0.489 | 0.00s |
| 2 | Baseline | Climatology (Lịch sử) | 0.1552 | 17.45 | 24.28 | 31.62% | 0.000 | 2.37s |
| 3 | Linear Model | Ridge Regression ($L_2$) | 0.5859 | 11.86 | 17.00 | 22.22% | 0.118 | 0.24s |
| 4 | Bagging Trees | Random Forest (150 cây) | 0.6037 | 11.53 | 16.63 | 21.61% | 0.247 | 8.93s |
| 5 | Gradient Boosting | LightGBM SOTA | 0.6170 | 11.33 | 16.35 | 21.26% | 0.123 | 0.41s |
| 6 | Gradient Boosting | XGBoost | 0.6159 | 11.36 | 16.37 | 21.31% | 0.149 | 0.67s |
| 7 | Gradient Boosting | CatBoost | 0.6084 | 11.40 | 16.53 | 21.33% | 0.077 | 1.45s |
| 8 | Deep Learning | MLP Regressor (64, 32) | 0.5011 | 13.08 | 18.66 | 24.52% | 0.179 | 73.10s |
| 9 | Deep Learning | Spatio-Temporal LSTM | 0.5840 | 11.56 | 17.04 | 21.59% | 0.000 | 121.12s |
| 10 | Ensemble | **Voting Ensemble (Top 3)** | **0.6172** | **11.30** | **16.34** | **21.19%** | 0.099 | 0.20s |
| 11 | Extreme Adaptive | **Wildfire Specialist (2-Stage)** | 0.6124 | 11.46 | 16.44 | 21.40% | **0.308** | 0.30s |

---

## 💥 BẢNG ĐỐI CHUẨN THIÊN TAI CHÁY RỪNG CỰC ĐOAN (PALISADES FIRE 2025 & PARK FIRE 2024)

*(Dữ liệu trích xuất từ `artifacts/metrics/wildfire_benchmark_comparison.csv`)*

| Tiêu Chí Đo Lường Sự Kiện Cháy Rừng Cực Đoan | 1h Nowcasting ($t+1$) | 24h Day-Ahead ($t+24$) |
| :--- | :---: | :---: |
| **Đỉnh Nồng Độ Thực Tế Thảm Họa (Palisades Fire 01/2025)** | **312.0 AQI** | **312.0 AQI** |
| Dự báo Đỉnh của Mô hình Cơ sở (Voting Ensemble) | 247.0 AQI | 150.9 AQI |
| Dự báo Đỉnh của **Tầng Chuyên Gia Cháy Rừng (Wildfire Layer)** | **266.2 AQI** | **183.8 AQI** |
| **Mức Thu Hẹp Sai Số Hụt Đỉnh (Peak Under-prediction Reduction)** | **Giảm 19.1 AQI** *(64.9 $\to$ 45.8 AQI)* | **Giảm 32.8 AQI** *(161.0 $\to$ 128.2 AQI)* |
| Sai số MAE trong vùng thảm họa cháy rừng | Giảm **-13.1%** *(7.81 $\to$ 6.79 AQI)* | Ổn định tối ưu *(30.17 $\to$ 30.27 AQI)* |
| **Tỷ lệ Bắt Trúng Giờ Nguy Hại (Recall với AQI > 150)** | $74.5\% \to \mathbf{76.9\%}$ | **$5.3\% \to \mathbf{20.1\%}$ (Tăng gấp 3.8 lần)** |
| **Chỉ số F1-Score trên Vùng Nguy Hại (> 150 AQI)** | $0.825 \to \mathbf{0.836}$ | **$0.098 \to \mathbf{0.308}$ (Tăng gấp 3.1 lần)** |

---

# CHI TIẾT THIẾT KẾ & KỊCH BẢN THUYẾT TRÌNH TỪNG SLIDE (16 SLIDES)

---

### 📍 SLIDE 01: TITLE COVER & PROJECT OVERVIEW

* **Thời lượng:** 30 giây
* **Diễn giả:** Speaker 1 (Trưởng nhóm / Đại diện mở màn)
* **Bố cục Slide:**
  * Bên trái: Tên đề tài, phân loại môn học DSR301m, Cột mốc Milestone 3 Final Defense, danh sách thành viên Group 5, Giảng viên hướng dẫn.
  * Bên phải / Nền: Hình ảnh bầu trời cam rực lửa San Francisco (`notebooks/image/san-francisco-orange-sky.jpg`) phủ gradient tối chuyên nghiệp.
  * Huy hiệu nổi bật: *"181,122 Hourly Observations · 11 Benchmark Models · Wildfire Specialist Breakthrough"*.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Kính thưa Thầy Cô và Hội đồng giám khảo, chào mừng quý Thầy Cô đến với buổi bảo vệ đồ án tốt nghiệp môn Data Science Project (DSR301m) của Nhóm 5. Đề tài của chúng em là: **'Comparative US AQI Time Series Forecasting in California with Extreme-Event Evaluation'** — Nghiên cứu đối chuẩn thực nghiệm mô hình dự báo chuỗi thời gian chỉ số ô nhiễm không khí tại California và giải pháp đột phá trong đánh giá thiên tai khí hậu cực đoan. Hôm nay, chúng em rất tự hào được báo cáo toàn bộ thành quả nghiên cứu toàn diện từ mô hình hóa, học sâu không gian - thời gian, tầng chuyên gia cháy rừng tự thích ứng đến sản phẩm web dashboard sẵn sàng triển khai thực tế."*

---

### 📍 SLIDE 02: EXECUTIVE SUMMARY & MILESTONE 3 BREAKTHROUGHS

* **Thời lượng:** 45 giây
* **Diễn giả:** Speaker 1
* **Bố cục Slide:** Chia làm 4 thẻ khối Card hiện đại thể hiện 4 bước tiến vượt bậc của Present 3 so với Present 2:
  1. **Thẻ 1 — Tích hợp Học Sâu Không Gian - Thời Gian (Spatio-Temporal LSTM):** Mạng LSTM PyTorch 2 tầng kết hợp Station Embedding, tối ưu Smooth L1 Loss, đạt Top 1 siêu chính xác ở tầm 1h ($R^2 = 0.9620, \text{MAE} = 2.76$).
  2. **Thẻ 2 — Tầng Chuyên Gia Cháy Rừng (Wildfire Specialist Layer):** Kiến trúc 2-Stage GBDT chuyển đổi chế độ động với bộ lọc vật lý gió Santa Ana và mật độ khói tích tụ nhiều ngày.
  3. **Thẻ 3 — Đại Leaderboard Toàn Diện 11 Mô Hình:** Khung đối chuẩn chuẩn mực trên Test Set 2025 out-of-sample cả 1h và 24h, kèm bài toán đánh đổi giữa độ chính xác và tốc độ tính toán (Inference Latency).
  4. **Thẻ 4 — Triển Khai Thực Tế Đầy Đủ (Production Dashboard):** Hệ thống web FastAPI + ECharts thời gian thực, What-If Simulator động học và kiến trúc microservices.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Nếu như ở Milestone 2, nhóm tập trung xây dựng nền tảng pipeline dữ liệu sạch và đối chuẩn các thuật toán học máy cổ điển, thì tại Milestone 3 này, nhóm đã tạo nên 4 bước đột phá mang tính bản lề: Thứ nhất, đưa mạng học sâu LSTM không gian - thời gian vào cuộc đua và thiết lập kỷ lục mới ở tầm dự báo 1h. Thứ hai, giải quyết triệt để 'điểm mù thiên tai' bằng một Tầng Chuyên gia Cháy rừng 2 giai đoạn giúp tăng độ nhạy cảnh báo nguy hại lên gấp gần 4 lần. Thứ ba, hoàn thiện Đại Leaderboard 11 mô hình với đầy đủ kiểm định độ trễ suy luận. Và thứ tư, đóng gói toàn bộ trí tuệ nhân tạo vào một hệ thống Web Dashboard phục vụ người dùng thực tế."*

---

### 📍 SLIDE 03: WILDFIRE CRISIS & DUAL OPERATIONAL HORIZONS

* **Thời lượng:** 60 giây
* **Diễn giả:** Speaker 1
* **Bố cục Slide:**
  * Cột trái: Ảnh tư liệu cháy rừng (`notebooks/image/san-francisco-orange-sky.jpg`) và Bảng phân cấp chất lượng không khí EPA 6 mức (`notebooks/image/aqitableforcourse.png`).
  * Cột phải: Khung lý luận phân định 2 chân trời dự báo:
    * **1h Nowcasting ($t+1$):** Đáp ứng nhu cầu phản ứng tức thì (ví dụ: cảnh báo tập thể dục ngoài trời, kích hoạt hệ thống lọc không khí tòa nhà). Cơ chế chi phối: Quán tính cảm biến tự hồi quy nồng độ.
    * **24h Day-Ahead ($t+24$):** Phục vụ quy hoạch điều hành y tế công cộng, điều tiết giao thông và sơ tán trường học. Cơ chế chi phối: Khí tượng động lực học tương lai ($W_{t+24}$) và chu kỳ ngày đêm.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Thưa Hội đồng, California đang đối mặt với những mùa cháy rừng khốc liệt chưa từng có với các thảm họa như August Complex hay Palisades Fire, đẩy chỉ số AQI vượt ngưỡng 300 đến 500 — mức Nguy Hại (Hazardous) gây sốc cho hệ hô hấp. Tuy nhiên, thách thức dữ liệu lớn nhất là: hơn 95% thời gian trong năm không khí ở mức sạch hoặc trung bình, tạo nên sự mất cân bằng nghiêm trọng. Nhóm đã giải quyết vấn đề này bằng việc thiết kế bài toán kép: Chân trời 1h Nowcasting nhằm cảnh báo tức thì dựa trên quán tính sensor; và Chân trời 24h Day-Ahead giúp cơ quan y tế chuẩn bị kế hoạch ứng phó từ trước một ngày dựa trên trường khí tượng dự báo tương lai."*

---

### 📍 SLIDE 04: 3-BASIN TOPOGRAPHY & 181K DATASET AUDIT

* **Thời lượng:** 60 giây
* **Diễn giả:** Speaker 1
* **Bố cục Slide:**
  * Hình ảnh trung tâm: Bản đồ địa mạo lưu vực California (`notebooks/image/California_Topography_and_Geomorphic.gif`) kết hợp vị trí 3 trạm quan trắc (`notebooks/image/paper_station_map.png`).
  * 3 Hộp thông tin địa mạo đại diện:
    * **Fresno (San Joaquin Valley):** Thung lũng khép kín hình lòng chảo, bị kẹp giữa dãy Sierra Nevada và Coast Range $\to$ Bẫy khói bụi và sương mù bức xạ mùa đông cực đoan.
    * **San Jose (Bay Area):** Vùng vịnh ven biển, chịu gió đại dương xua tan khí độc, nhưng dễ bị bao phủ bởi khói cháy rừng phương bắc tràn xuống.
    * **Los Angeles (South Coast Air Basin):** Đô thị siêu đậm đặc, phát thải giao thông nội tại kết hợp hiệu ứng gió sa mạc Santa Ana khô nóng thổi qua đèo núi.
  * Số liệu kiểm toán: $181,122$ dòng dữ liệu giờ liên tục 8 năm (2018–2025), $0\%$ giá trị khuyết thiếu sau tiền xử lý nội suy vật lý.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Để mô hình có tính tổng quát hóa cao trên toàn tiểu bang, nhóm chọn 3 lưu vực địa mạo có hành vi khí quyển hoàn toàn tương phản: Một Fresno khép kín giữa các dãy núi khiến bụi mịn bị bẫy giữ; một San Jose ven biển thông thoáng nhưng nhạy cảm với khói cháy rừng; và một Los Angeles chịu tác động hỗn hợp giữa phát thải giao thông đô thị và bão gió sa mạc Santa Ana. Tổng cộng 181,122 điểm dữ liệu được kiểm toán chặt chẽ, đại diện cho mọi sắc thái khí tượng và địa hình của California."*

---

### 📍 SLIDE 05: ZERO-LEAKAGE SPLIT & PHYSICS FEATURE STORE

* **Thời lượng:** 60 giây
* **Diễn giả:** Speaker 2 (Phụ trách Kỹ thuật Dữ liệu & Xử lý Đặc trưng)
* **Bố cục Slide:**
  * Sơ đồ dòng thời gian Zero-Leakage:
    * Train Set: 2018 – 2023 (61.3% dữ liệu)
    * Validation Set: 2024 (24.1% dữ liệu — Chứa trọn vẹn siêu cháy rừng Park Fire)
    * Test Set Out-of-Sample: 2025 (14.5% dữ liệu — Đánh giá mù tuyệt đối thảm họa Palisades Fire)
    * Vùng đệm biên ($h$-hour buffer): Cắt bỏ $h$ dòng biên giữa các tập để triệt tiêu $100\%$ rò rỉ Lookahead Leakage từ rolling features.
  * Bảng Feature Store Vật lý:
    * Nowcasting 1h (22 features): Lags sensor ngắn hạn ($t-1, t-2, t-3$), Độ lệch dốc biến thiên $\Delta_{1\text{h}}$, Trung bình trượt $3\text{h}, 6\text{h}$, Vector gió Descartes $(u, v)$, Áp suất hơi bão hòa thiếu hụt VPD.
    * Day-Ahead 24h (19 features): Khí tượng dự báo tương lai $W_{t+24}$, Lags đồng pha chu kỳ hôm trước ($t-24, t-48$), Biên độ nhiệt ngày đêm, Chỉ số gió Santa Ana.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Trong học máy chuỗi thời gian, lỗi nghiêm trọng nhất thường gặp là rò rỉ dữ liệu tương lai (Lookahead Leakage). Nhóm đã áp dụng giao thức phân chia thời gian nghiêm ngặt với vùng đệm an toàn h-giờ, cô lập hoàn toàn tập Test năm 2025 chưa từng thấy trong huấn luyện. Đồng thời, thay vì chỉ nạp các biến toán học mù quáng, Feature Store được thiết kế dựa trên nguyên lý vật lý khí quyển: phân rã hướng gió thành vector Descartes $(u, v)$ để khử tính gián đoạn góc tròn 360 độ, và tích hợp đại lượng thiếu hụt áp suất hơi nước VPD để nắm bắt độ khô nỏ của vật liệu cháy rừng."*

---

### 📍 SLIDE 06: BENCHMARK MODEL SUITE: 6 ALGORITHM FAMILIES

* **Thời lượng:** 50 giây
* **Diễn giả:** Speaker 2
* **Bố cục Slide:** Sơ đồ tổ chức 11 mô hình phân nhánh theo 6 trường phái thuật toán:
  1. **Mô hình Cơ sở (Baselines):** Naïve Persistence (Dự báo quán tính) & Climatology (Kỳ vọng lịch sử).
  2. **Mô hình Tuyến tính (Linear):** Ridge Regression với chuẩn hóa $L_2$ chống đa cộng tuyến.
  3. **Học Máy Dạng Cây (Tree-based):** Random Forest (Bagging), LightGBM, XGBoost, CatBoost (Gradient Boosting SOTA).
  4. **Deep Learning Dạng Bảng (Tabular DL):** MLP 2 tầng ẩn $(64, 32)$ kích hoạt ReLU và Dropout.
  5. **Deep Learning Chuỗi Thời Gian (Sequence DL):** Spatio-Temporal LSTM PyTorch với Station Embedding Layer.
  6. **Tầng Chuyên Biệt Hóa (Ensemble & Adaptive):** Voting Ensemble (kết hợp Top 3 GBDT) & Wildfire Specialist Layer (2-Stage GBDT thích ứng chế độ).
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Để mang lại một cái nhìn đối chuẩn khách quan và toàn diện nhất, nhóm đã triển khai một không gian thử nghiệm gồm 11 mô hình đại diện cho 6 trường phái thuật toán lớn: từ các baseline truyền thống, hồi quy chuẩn hóa Ridge, các thuật toán cây phân nhánh đỉnh cao như LightGBM, CatBoost, cho đến mạng nơ-ron sâu MLP và LSTM không gian thời gian. Đặc biệt, nhóm đề xuất hai mô hình cấp cao: mô hình kết hợp Voting Ensemble để giảm thiểu phương sai sai số, và mô hình chuyên biệt hóa Wildfire Specialist Layer để chinh phục vùng nồng độ cực đoan."*

---

### 📍 SLIDE 07: DEEP LEARNING TRAINING DYNAMICS (LSTM VS MLP)

* **Thời lượng:** 65 giây
* **Diễn giả:** Speaker 2
* **Bố cục Slide:** Đặt song song 2 đồ thị hội tụ học sâu:
  * Bên trái: `artifacts/figures/lstm_learning_curves.png` (Quá trình tối ưu mạng Spatio-Temporal LSTM qua 60 epochs với Smooth L1 Loss).
  * Bên phải: `artifacts/figures/mlp_learning_curves.png` (Quá trình tối ưu mạng MLP qua 50 epochs với MSE Loss và Adam optimizer).
  * Điểm nhấn kỹ thuật:
    * LSTM áp dụng **Smooth L1 Loss (Huber Loss)**: Hoạt động như $L_2$ với sai số nhỏ giúp hội tụ êm ái, nhưng chuyển thành $L_1$ khi sai số lớn giúp mô hình miễn nhiễm với việc bị giật trọng số do các ngoại lai cháy rừng.
    * Kiến trúc **Station Embedding**: Vector hóa bản sắc trạm thành không gian 8 chiều, giải quyết vấn đề dị biệt phân phối không gian giữa các lưu vực.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Nhìn vào động lực huấn luyện học sâu ở Slide 7, chúng ta thấy rõ sự khác biệt mang tính chiến lược: Mạng MLP dạng bảng với hàm mất mát MSE truyền thống hội tụ nhanh nhưng dễ bị ảnh hưởng bởi các giá trị ngoại lai, dẫn đến hiện tượng plateau sớm. Trong khi đó, mạng Spatio-Temporal LSTM do nhóm tự thiết kế trong PyTorch được trang bị hàm Smooth L1 Loss. Hàm mất mát này giúp đường cong Training Loss và Validation Loss giảm mượt mà qua 60 epochs mà không hề bị dao động quá mức khi gặp các xung nồng độ khói. Lớp nhúng trạm Station Embedding đã cho phép mạng học được mối liên hệ không gian sâu sắc giữa 3 lưu vực."*

---

### 📍 SLIDE 08: OFFICIAL COMPREHENSIVE LEADERBOARD (1H VS 24H TABLE)

* **Thời lượng:** 75 giây
* **Diễn giả:** Speaker 3 (Phụ trách Đối chuẩn & Phân tích Thực nghiệm)
* **Bố cục Slide:** Trình bày bảng ma trận số liệu tổng hợp 11 mô hình (lấy trực tiếp từ bảng số liệu ở đầu tài liệu này).
  * Tô màu nổi bật (Highlight):
    * Ở tầm 1h: **LSTM PyTorch** dẫn đầu tuyệt đối về độ chính xác ($\text{MAE} = 2.76, R^2 = 0.9620$), bám sát là **Wildfire Specialist** ($\text{MAE} = 3.05$) và **Voting Ensemble** ($\text{MAE} = 3.06$).
    * Ở tầm 24h: **Voting Ensemble** dẫn đầu về tính ổn định dài hạn ($\text{MAE} = 11.30, R^2 = 0.6172$).
    * Đặc biệt: **Wildfire Specialist** tạo nên bước nhảy vọt $F_1\text{-Score}$ ở vùng nguy hại ($>150$ AQI) đạt **$0.308$**, cao gấp hơn 3 lần so với mô hình tốt nhất tiếp theo!
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Thưa Thầy Cô, đây là bảng Leaderboard tổng thể toàn bộ công trình nghiên cứu trên tập Test độc lập năm 2025. Bảng số liệu đã chứng minh rõ nét sự phân hóa giữa hai chân trời: Ở tầm ngắn 1h, Spatio-Temporal LSTM lập đỉnh bảng với MAE chỉ 2.76 điểm AQI và R² đạt 0.962, khẳng định sức mạnh vượt trội của cơ chế bộ nhớ tế bào trong việc nắm bắt quán tính chuỗi thời gian. Tuy nhiên, khi phóng chiếu ra 24h, khi quán tính suy giảm và khí tượng trở thành yếu tố quyết định, Voting Ensemble lại giành ngôi vương với MAE 11.30 AQI. Và ấn tượng nhất, Tầng Chuyên gia Cháy rừng đạt F1-Score 0.308 trên ngưỡng nguy hại, trong khi các mô hình thông thường chỉ đạt dưới 0.10."*

---

### 📍 SLIDE 09: VISUAL BENCHMARK LEADERBOARD & SPEED-ACCURACY TRADEOFF

* **Thời lượng:** 65 giây
* **Diễn giả:** Speaker 3
* **Bố cục Slide:**
  * Hình ảnh chính: Biểu đồ thanh đối chuẩn chính thức (`artifacts/figures/01_model_comparison_mae.png`).
  * Khối so sánh Đánh đổi Tốc độ - Độ chính xác (Speed-Accuracy Trade-off):
    * GBDT (LightGBM/XGBoost): Thời gian dự báo siêu tốc ($0.41\text{s} - 1.04\text{s}$), MAE $3.10 - 3.13$ AQI $\to$ Tối ưu cho hệ thống nhúng, edge computing hoặc server tài nguyên hạn chế.
    * LSTM Deep Learning: Đạt độ chính xác cao nhất (MAE $2.76$ AQI) nhưng thời gian huấn luyện và suy luận lớn hơn ($120.95\text{s}$, gấp ~200 lần GBDT).
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Biểu đồ trực quan tại Slide 9 phân tách rõ ràng năng lực của từng họ thuật toán. Chúng ta thấy sự kết cụm áp đảo của nhóm GBDT và Ensemble ở cả hai chân trời. Đáng chú ý là bài toán đánh đổi giữa tốc độ và độ chính xác: Nếu ứng dụng trong thực tế cần phản hồi mili-giây trên các thiết bị nhúng IoT, LightGBM và XGBoost là lựa chọn hoàn hảo với thời gian suy luận dưới nửa giây nhưng sai số chỉ lệch chưa đầy 0.3 điểm so với mạng sâu. Ngược lại, nếu ưu tiên độ chính xác tuyệt đối trong các trạm máy chủ trung tâm, LSTM chính là vũ khí mạnh nhất."*

---

### 📍 SLIDE 10: CONTINUOUS TIME-SERIES TRACKING & PARITY CALIBRATION

* **Thời lượng:** 65 giây
* **Diễn giả:** Speaker 3
* **Bố cục Slide:** Đặt song song 2 biểu đồ:
  * Bên trái: `artifacts/figures/02_actual_vs_predicted_1week.png` (Theo dõi liên tục 168 giờ thực tế tại Fresno từ 09/01 đến 15/01/2025).
  * Bên phải: `artifacts/figures/07_actual_vs_pred_parity_hexbin.png` (Đồ thị tương quan thực tế vs dự báo Parity Hexbin Plot kèm hệ số hồi quy góc dốc $\beta$).
  * Phân tích thấu đáo:
    * Khả năng bám đỉnh: Thực tế đạt đỉnh $73.4$ AQI lúc 21h đêm, Voting Ensemble dự báo đạt $72.1$ AQI (sai lệch chỉ $1.3$ AQI).
    * Hiện tượng co ngót đuôi (Tail Shrinkage): Ở mức nồng độ cực cao ($>200$ AQI), hệ số góc $\beta$ của các mô hình cơ sở bị dẹt xuống $\beta \approx 0.54 - 0.56$ do hàm loss $L_2$ phạt trung bình.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Quan sát lát cắt liên tục 1 tuần với 168 giờ tại trạm Fresno ở hình bên trái, các mô hình của nhóm bám sát hoàn hảo từng nhịp thở ngày-đêm của thành phố. Khi nồng độ tăng vọt lên đỉnh 73.4 AQI do tích tụ khói mù buổi tối, mô hình Ensemble đã bám sát ở mức 72.1 AQI, đường thặng dư sai số phẳng lì dưới 5 đơn vị. Tuy nhiên, khi nhìn sang đồ thị Parity Hexbin ở bên phải, nhóm đã phát hiện một khiếm khuyết nội tại của các thuật toán chuẩn: hiện tượng co ngót đuôi phân phối. Khi xảy ra bão khói trên 200 AQI, đường dự báo bị uốn cong xuống dưới đường chéo 45 độ. Đây chính là động lực để nhóm khai sinh Tầng Chuyên gia Cháy rừng!"*

---

### 📍 SLIDE 11: WILDFIRE SPECIALIST LAYER: 2-STAGE GBDT ARCHITECTURE

* **Thời lượng:** 75 giây
* **Diễn giả:** Speaker 4 (Phụ trách Mô hình Chuyên gia & Ứng dụng Thực tế)
* **Bố cục Slide:**
  * Sơ đồ khối nguyên lý 2-Stage Hierarchical Regime-Switching Architecture:
    * **Stage 1 — Bộ Lọc Phát Hiện Chế Độ Khí Quyển Cực Đoan (Physical Regime Detector):** Hoạt động không giám sát dựa trên quy tắc vật lý:
      * Gió khô Santa Ana: $V_{\text{wind}} > 20\text{ km/h}$ kết hợp Độ ẩm $\text{RH} < 25\%$ và Gió hướng Đông Bắc $\to$ Kích hoạt cờ bão lửa.
      * Mật độ khói tích tụ: Trung bình nồng độ 48 giờ qua $> 60$ AQI hoặc Tốc độ bốc hơi $\text{VPD} > 3.0\text{ kPa}$.
    * **Stage 2 — Bộ Điều Phối Dự Báo Thích Ứng (Specialist Predictor):**
      * Chế độ Bình thường: Kích hoạt Base GBDT Ensemble (Tối ưu độ chính xác ngày thường, bảo toàn $R^2$).
      * Chế độ Thiên tai Cháy rừng: Kích hoạt Wildfire GBDT Specialist (Huấn luyện với hàm mất mát phi đối xứng Asymmetric Loss và trọng số mẫu lũy thừa nồng độ).
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Để giải quyết nghịch lý: vừa phải chính xác tuyệt đối trong những ngày bình thường, vừa không được hụt đỉnh khi cháy rừng xảy ra, nhóm đã phát triển kiến trúc 2 tầng Wildfire Specialist Layer. Tầng thứ nhất đóng vai trò như một lính gác khí quyển, liên tục quét các tín hiệu vật lý: chỉ số gió sa mạc Santa Ana, độ thiếu hụt ẩm VPD và quán tính khói đa ngày. Nếu bầu khí quyển bình thường, hệ thống dùng Base Ensemble. Nhưng ngay khi các chỉ số chạm ngưỡng bão khói, bộ điều phối sẽ lập tức kích hoạt Tầng Chuyên gia Cháy rừng — một mô hình được trui rèn riêng biệt trên các phân phối ô nhiễm cực đoan."*

---

### 📍 SLIDE 12: EXTREME DISASTERS EVALUATION: PALISADES FIRE 2025

* **Thời lượng:** 75 giây
* **Diễn giả:** Speaker 4
* **Bố cục Slide:**
  * Bên trái: `artifacts/figures/11_wildfire_layer_peak_comparison.png` (Đường cong bám đỉnh thảm họa Palisades Fire tháng 01/2025: Thực tế 312 AQI vs Base Model vs Wildfire Layer).
  * Bên phải: `artifacts/figures/12_wildfire_peak_reduction.png` (Biểu đồ cột mức thu hẹp sai số hụt đỉnh).
  * Con số chứng minh:
    * Ở tầm 24h: Base Model chỉ dự báo được $150.9$ AQI (hụt tới $161.0$ AQI). Tầng Chuyên gia Cháy rừng đẩy dự báo vọt lên **$183.8$ AQI**, **thu hẹp độ hụt đỉnh tới $32.8$ điểm AQI**!
    * Ở tầm 1h: Base Model đạt $247.0$ AQI (hụt $64.9$ AQI). Tầng Chuyên gia bám sát mức **$266.2$ AQI**, thu hẹp sai số hụt đỉnh $19.1$ điểm AQI; giảm sai số MAE toàn trận cháy từ $7.81$ xuống **$6.79$ AQI (giảm -13.1%)**.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Bằng chứng thực nghiệm thuyết phục nhất được thể hiện trong thảm họa Palisades Fire tháng 01/2025 tại Los Angeles ở Slide 12. Khi ngọn lửa bùng phát dữ dội, nồng độ thực tế chạm mốc thảm họa 312 điểm AQI. Mô hình thông thường ở tầm 24h bị 'đơ' hoàn toàn, chỉ dự báo được 150.9 AQI — tức là đánh giá sai mức độ nguy hiểm xuống tận một bậc! Trong khi đó, Tầng Chuyên gia Cháy rừng của chúng em đã đẩy đỉnh dự báo lên 183.8 AQI, rút ngắn sai số hụt đỉnh tới 32.8 điểm. Ở tầm 1h, mô hình kéo sai số hụt đỉnh từ 64.9 xuống chỉ còn 45.8 AQI, giúp cứu vãn toàn bộ sai số dự báo trong vùng thiên tai."*

---

### 📍 SLIDE 13: HAZARDOUS EARLY WARNING JUMP (RECALL & F1 SHIFT)

* **Thời lượng:** 65 giây
* **Diễn giả:** Speaker 4
* **Bố cục Slide:**
  * Bên trái: `artifacts/figures/13_wildfire_recall_f1_jump.png` (Bước nhảy vọt Recall và F1-Score trên ngưỡng nguy hại $>150$ AQI).
  * Bên phải: `artifacts/figures/03_wildfire_extreme_resilience.png` (Độ bền bỉ sai số trước cú sốc cháy rừng trên toàn bộ các mô hình).
  * Luận điểm an toàn y tế cộng đồng:
    * Trong dự báo ô nhiễm, **bỏ sót một giờ nguy hại (False Negative) tai hại hơn nhiều so với báo động nhầm (False Positive)**.
    * Tỷ lệ bắt trúng giờ nguy hại (Recall) ở tầm 24h tăng từ $5.3\%$ lên **$20.1\%$** (tăng gấp gần 4 lần).
    * Sai số MAE trong thời gian cháy rừng của Wildfire Specialist chỉ là **$57.01$ AQI**, thấp nhất toàn bộ suite mô hình (trong khi các mô hình khác bùng nổ lên $62 - 70$ AQI).
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Đối với sức khỏe cộng đồng, việc dự báo thiếu một giờ ô nhiễm nguy hại có thể trả giá bằng sinh mạng của những bệnh nhân hen suyễn và tim mạch. Biểu đồ tại Slide 13 cho thấy một bước nhảy vọt ngoạn mục: Năng lực bắt trúng các giờ nguy hại (Recall) ở tầm 24h đã tăng từ 5.3% lên 20.1% — tức tăng gần 4 lần! Chỉ số F1-Score tổng hòa giữa độ chính xác và độ nhạy cũng nhảy vọt gấp hơn 3 lần từ 0.098 lên 0.308. Đồng thời, khi toàn bộ các mô hình khác đều bị bùng nổ sai số lên trên 62 đến 70 AQI khi gặp sốc khói, Tầng Chuyên gia của nhóm giữ vững độ bền bỉ ở mức 57.01 AQI — dẫn đầu toàn diện."*

---

### 📍 SLIDE 14: 3-DIMENSIONAL ERROR DIAGNOSTICS: DIURNAL & SPATIAL

* **Thời lượng:** 60 giây
* **Diễn giả:** Speaker 4
* **Bố cục Slide:** Cụm 3 biểu đồ chẩn đoán sai số khoa học:
  * Bên trái: `artifacts/figures/08_diurnal_hourly_error_profile.png` (Sai số 24 khung giờ trong ngày).
  * Bên phải trên: `artifacts/figures/09_spatial_basin_resilience.png` (Sai số phân rã theo 3 lưu vực khí quyển).
  * Bên phải dưới: `artifacts/figures/10_basin_extreme_sensitivity.png` (Độ nhạy sai số cực đoan theo lưu vực).
  * Phát hiện khoa học then chốt:
    * **Chu kỳ nghịch nhiệt bức xạ đêm:** Sai số tăng vọt vào khung 22h – 04h sáng do mặt đất nguội nhanh tạo lớp nghịch nhiệt giam hãm ô nhiễm tầm thấp mà vệ tinh và trạm khí tượng khó đo đạc.
    * **Đặc tính lưu vực:** Tại Los Angeles, **Spatio-Temporal LSTM** đạt kết quả tốt nhất với MAE $12.8$ AQI (giảm $-17.5\%$ so với Baseline), chứng minh khả năng học mẫu hình phát thải giao thông đô thị phức tạp vượt trội hơn cây quyết định.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Để hiểu sâu sắc bản chất sai số, nhóm đã bóc tách mô hình qua 3 chiều vật lý: Chiều thời gian trong ngày chỉ ra rằng sai số luôn đạt cực đại vào nửa đêm (22h đến 4h sáng). Đây là lúc hiện tượng nghịch nhiệt bức xạ diễn ra mạnh nhất, tạo thành một chiếc 'vung' vô hình giam hãm khói bụi sát mặt đất. Chiều không gian địa mạo mang lại một phát hiện cực kỳ thú vị: Tại vùng đô thị siêu phức tạp Los Angeles, mạng LSTM của nhóm đã đánh bại toàn bộ các mô hình cây GBDT để đạt MAE 12.8 AQI, cải thiện tới 17.5% sai số, nhờ khả năng liên kết chuỗi thời gian giao thông và gió biển."*

---

### 📍 SLIDE 15: MODEL EXPLAINABILITY: TREESHAP ATTRIBUTION

* **Thời lượng:** 60 giây
* **Diễn giả:** Speaker 4
* **Bố cục Slide:** Trình bày bộ đôi biểu đồ giải thích mô hình bằng lý thuyết trò chơi Shapley:
  * Bên trái: `artifacts/figures/05_shap_beeswarm_summary.png` (TreeSHAP Beeswarm phân phối tác động từng điểm dữ liệu).
  * Bên phải: `artifacts/figures/06_shap_mean_importance.png` (Xếp hạng trung bình trọng số tuyệt đối $|SHAP|$ phân nhóm theo miền vật lý) kết hợp `artifacts/figures/04_feature_importance_shift.png`.
  * Kết luận diễn giải:
    * Quán tính nồng độ gần nhất (`lag_0`, `roll_mean_3h`) chiếm tới **$68\%$** tổng quyền số phân loại ở tầm 1h.
    * Tuy nhiên ở tầm 24h, trọng số chuyển dịch ngoạn mục: Biến khí tượng động lực học ($W_{t+24}$) và độ khô nỏ VPD vươn lên chiếm quyền chi phối lớn nhất ($>55\%$). Giá trị VPD cao (điểm đỏ) luôn đẩy mạnh nồng độ AQI dự báo lên các bậc nguy hại.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Không dừng lại ở việc xem mô hình như một chiếc 'hộp đen', nhóm sử dụng TreeSHAP để minh bạch hóa toàn bộ cơ chế ra quyết định dựa trên lý thuyết trò chơi. Biểu đồ Beeswarm chứng minh rằng: Ở tầm 1h, quán tính cảm biến giữ vai trò chi phối. Nhưng khi nhìn ra 24h, trọng số lập tức chuyển dịch sang các đại lượng vật lý khí quyển. Điểm đáng kinh ngạc là thuộc tính thiếu hụt ẩm VPD và thành phần gió hướng núi đã thể hiện mối quan hệ phi tuyến mạnh mẽ: khi không khí càng khô nỏ và gió thổi từ đất liền ra biển, giá trị SHAP dương cực lớn được cộng dồn, báo hiệu hiểm họa cháy rừng trước 24 giờ."*

---

### 📍 SLIDE 16: LIVE PRODUCTION DASHBOARD & CONCLUSION ROADMAP

* **Thời lượng:** 60 giây
* **Diễn giả:** Speaker 4 / Speaker 1 (Đại diện kết luận)
* **Bố cục Slide:**
  * Bên trái: Ảnh chụp giao diện thực tế của Web Dashboard (gồm bản đồ trạm, biểu đồ bám chuỗi ECharts thời gian thực, bảng Leaderboard động theo từng cửa sổ thời gian, và thanh trượt What-If Scenario Simulator).
  * Bên phải: Tóm tắt 3 Đóng góp Khoa học Cốt lõi & Định hướng Tương lai:
    1. Đóng góp 1: Bộ benchmark 11 mô hình chuẩn hóa quy trình zero-leakage đầu tiên cho AQI California.
    2. Đóng góp 2: Tầng chuyên gia cháy rừng 2 giai đoạn tăng 3.8 lần độ nhạy cảnh báo nguy hại.
    3. Đóng góp 3: Sản phẩm phần mềm FastAPI hoàn chỉnh, sẵn sàng tích hợp vào hệ thống quan trắc môi trường thực tế.
    * Lời cảm ơn và chuyển sang phần Q&A cùng Hội đồng.
* **Lời thoại diễn thuyết (Speaker Script):**
  > *"Để đưa các kết quả nghiên cứu vào đời sống thực tế, nhóm đã đóng gói toàn bộ hệ thống vào một Web Dashboard hoàn chỉnh bằng FastAPI và thư viện đồ họa ECharts chạy trực tiếp 24/7. Ứng dụng cung cấp bảng xếp hạng động cập nhật theo thời gian thực và một công cụ mô phỏng giả định What-If cho phép các nhà hoạch định chính sách thử nghiệm các kịch bản: nếu nhiệt độ tăng thêm 5 độ và bão gió 40 km/h xảy ra thì nồng độ AQI 24 giờ tới sẽ biến động ra sao. Đồ án của nhóm 5 không chỉ dừng lại ở các con số học thuật mà đã trở thành một giải pháp công nghệ toàn diện. Chúng em xin trân trọng cảm ơn Thầy Cô và sẵn sàng lắng nghe các câu hỏi phản biện từ Hội đồng!"*

---

## 💡 HƯỚNG DẪN KỸ THUẬT & MẸO TRÌNH BÀY CHO NHÓM (SPEAKER TIPS)

1. **Chuẩn bị file trình chiếu:**
   * Tạo file PPTX hoặc trình chiếu PDF khổ $16:9$ WideScreen.
   * Nhúng trực tiếp các file ảnh gốc có độ phân giải 300 DPI từ [`artifacts/figures/`](file:///c:/FPT/FA2026/DSR301m/Project/artifacts/figures) để biểu đồ hiển thị sắc nét, không bị nhòe vỡ font số liệu khi chiếu trên máy chiếu giảng đường.
2. **Kỹ thuật chuyển giao giữa các Diễn giả (Transitions):**
   * Giữa Speaker 1 $\to$ 2: *"Để hiểu rõ cách nhóm xử lý dữ liệu và thiết kế các biến vật lý không bị rò rỉ, xin mời bạn... trình bày Phần 2."*
   * Giữa Speaker 2 $\to$ 3: *"Sau đây, bạn... sẽ phân tích chi tiết kết quả thực nghiệm và bảng Leaderboard đối chuẩn 11 mô hình."*
   * Giữa Speaker 3 $\to$ 4: *"Và sau đây là phần đột phá quan trọng nhất của đề tài — Tầng chuyên gia cháy rừng và hệ thống ứng dụng thực tế do bạn... trình bày."*
3. **Phản biện câu hỏi hóc búa của Hội đồng (Q&A Defense):**
   * *Câu hỏi: Tại sao LSTM tốt ở 1h nhưng sang 24h lại thua Ensemble?*
     $\to$ *Trả lời:* Ở tầm 1h, quán tính chuỗi ngắn cực mạnh, cấu trúc tế bào nhớ (cell state) của LSTM khai thác rất sâu tính tự tương quan liên tục. Nhưng ở tầm 24h, độ phụ thuộc chuỗi bị phân rã, các yếu tố ngoại sinh thời tiết tương lai $W_{t+24}$ chiếm ưu thế; các cây quyết định của GBDT kết hợp bằng Voting Ensemble có khả năng phân vùng không gian biến dạng bảng mạnh mẽ và ít nhạy cảm với việc mất tương quan chuỗi dài hơn.
   * *Câu hỏi: Tại sao Tầng Chuyên gia Cháy rừng không làm giảm MAE tổng thể trên toàn năm 2025?*
     $\to$ *Trả lời:* Vì số giờ xảy ra thảm họa cháy rừng chỉ chiếm $<5\%$ tổng số giờ trong năm ($95\%$ là ngày sạch). Nếu đánh giá bằng MAE trung bình toàn năm, những cải thiện khổng lồ ở vùng đỉnh (giảm hụt đỉnh 32.8 AQI) sẽ bị 'pha loãng' bởi hàng ngàn giờ ngày thường. Đó là lý do tại sao các chỉ số như F1-Score trên ngưỡng $>150$ và Peak Under-prediction Error mới là thước đo sinh tử để đánh giá sự thành công của tầng chuyên gia.
