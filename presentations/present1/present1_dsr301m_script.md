# TÀI LIỆU KỸ THUẬT TỔNG HỢP — BÁO CÁO TIẾN ĐỘ 1 (PRESENT 1)

## ĐỀ TÀI: COMPARATIVE US AQI TIME SERIES FORECASTING IN CALIFORNIA WITH EXTREME-EVENT EVALUATION
*(Nghiên cứu đối chuẩn các mô hình dự báo chuỗi thời gian chỉ số chất lượng không khí US AQI tại California trong bối cảnh đánh giá thiên tai cực đoan)*

* **Môn học:** DSR301m – Data Science Project (Đại học FPT TP.HCM)
* **Cột mốc:** Technical Progress Report 1 (Present 1)
* **Quy mô dữ liệu:** 181,122 bản ghi hàng giờ (2018–2025) · 21 cột thuộc tính cơ sở (21 base columns)
* **Nguồn dữ liệu:** US EPA AQS (Ground Truth quan trắc mặt đất) & Open-Meteo API (Thông số khí tượng bề mặt)
* **Khu vực nghiên cứu:** 3 trạm đại diện 3 lưu vực địa mạo California: Fresno (FRES), Los Angeles (LA), San Jose (SJ)

---

## 👥 PHÂN CÔNG THUYẾT TRÌNH (GROUP 5)

| STT | Thành viên | MSSV | Phạm vi Slide |
| :---: | :--- | :---: | :--- |
| **1** | **Lê Thanh Khang** | **SE200637** | **Slide 01 – 03** (Tổng quan đề tài, Bối cảnh hỏa hoạn, 3 khoảng trống y văn, Kiến trúc 2 chân trời 1–3h vs 24h) |
| **2** | **Nguyễn Hữu Thanh Phong** | **SE191014** | **Slide 04 – 05** (Hồ sơ dữ liệu 181k dòng, 4 quyết định kiểm toán AI, Từ điển 21 cột, Dòng thời gian 8 năm EPA Category) |
| **3** | **Tạ Nguyễn Anh Minh** | **SE200416** | **Slide 06 – 09** (Phân phối lệch +4.82 & Quyết định No Log-Transform, Phân chia tuần tự chống rò rỉ, Kỹ nghệ 5 nhóm đặc trưng & GBDT SOTA, Bảng danh mục 18 đặc trưng đầu vào cuối cùng) |
| **4** | **Đồng Bảo Hân** | **SE203683** | **Slide 10 – 11** (Khung đánh giá 2 cấp độ, Khắc phục sụp đổ phương sai R², 4 đóng góp nghiên cứu, Lộ trình 3 giai đoạn & 4 sản phẩm) |

---

# PHẦN 1: NỘI DUNG KỸ THUẬT TỪNG SLIDE (01 – 11)

---

### 📍 SLIDE 01: TITLE & PRESENTATION SCOPE
* **Người phụ trách:** Lê Thanh Khang (SE200637)
* **Nội dung chính:**
  * Giới thiệu tên đề tài và cột mốc báo cáo Present 1.
  * 4 trụ cột kỹ thuật của đề tài:
    1. *Multi-Source Panel:* Tích hợp dữ liệu bảng đa nguồn EPA AQS và Open-Meteo.
    2. *181k Hourly Records:* Chuỗi thời gian 8 năm (2018–2025) trên 3 lưu vực địa mạo đặc trưng.
    3. *Zero-Leakage Protocol:* Giao thức phân chia tuần tự có vùng đệm trễ biên chống rò rỉ.
    4. *Extreme-Event Metrics:* Khung đánh giá tập trung vào các sự kiện cháy rừng cực đoan.
  * Phân công thuyết trình: Phân chia 4 thành viên theo từng mảng nội dung chuyên sâu từ dữ liệu đến mô hình và đánh giá.

---

### 📍 SLIDE 02: REAL-WORLD WILDFIRE CRISIS & THREE CRITICAL RESEARCH GAPS
* **Người phụ trách:** Lê Thanh Khang (SE200637)
* **Dữ kiện thực tế & Quy chuẩn EPA:**
  * **Hình 1a (Bầu trời cam San Francisco — 09/09/2020):** Chỉ số AQI chạm đỉnh **496.0** trong đại hỏa hoạn August Complex; khói bụi che lấp ánh sáng mặt trời.
  * **Hình 1b (Thang đo 6 cấp EPA AQI):** Mức 496.0 vượt xa ngưỡng nguy hại cao nhất **Hazardous Maroon (301+)** tới **+195 điểm**, tiệm cận mức trần 500 của cảm biến.
  * **Tác động y tế:** Nồng độ $\text{PM}_{2.5}$ vượt ngưỡng WHO hơn 10 lần, làm tăng đột biến hơn 90% số ca cấp cứu hô hấp và tim mạch (Aguilera et al., Nature Communications, 2021).
  * **Đặc tính mất cân bằng:** Hơn 85% số ngày trong năm thuộc ngưỡng an toàn ($AQI \le 50$), khiến các đợt khói độc hiếm gặp dễ bị mô hình bỏ sót.
* **3 khoảng trống nghiên cứu cốt lõi (Three Research Gaps):**
  1. *Metric Masking (Che lấp sai số bằng thước đo trung bình):* Sai số toàn niên MAE, RMSE thấp do phần lớn ngày sạch che giấu thất bại của mô hình trong các ngày thiên tai ($AQI > 300$).
  2. *Lookahead Leakage (Rò rỉ tương lai):* Chia train/test ngẫu nhiên trên chuỗi thời gian gây rò rỉ dữ liệu tương lai, tạo điểm số ảo $R^2 > 0.95$ nhưng vô dụng trong thực tế.
  3. *Atmospheric Blindspot (Điểm mù khí quyển):* Bỏ qua biến thời tiết (VPD, gió), chỉ dựa vào cảm biến mặt đất khiến mô hình mất phương hướng khi dự báo trước 24 giờ.
* **3 câu hỏi nghiên cứu (Research Questions):**
  * **[RQ1] Atmospheric Drivers:** Biến VPD và vector gió $(u, v)$ có duy trì được độ chính xác ở chân trời 24 giờ khi quán tính cảm biến suy giảm sâu?
  * **[RQ2] Metric Reform:** Khung đánh giá 2 cấp độ có giải quyết được sự sụp đổ toán học của $R^2$ trên các sự kiện cực đoan?
  * **[RQ3] Leakage Defense:** Phân chia tuần tự kết hợp vùng đệm trễ biên có đảm bảo tính độc lập tuyệt đối giữa các tập dữ liệu?

---

### 📍 SLIDE 03: TASK ARCHITECTURE & DUAL OPERATIONAL FORECAST HORIZONS (1–3H VS. 24H)
* **Người phụ trách:** Lê Thanh Khang (SE200637)
* **Pipeline dự báo nhân quả (Causal Pipeline):**
  $$\text{Lags } (t-h \text{ trở về trước}) + \text{Open-Meteo } (t) + \text{Địa mạo lưu vực} \xrightarrow{\text{Non-Lookahead GBDT Engine}} \text{Hai chân trời (1–3h \& 24h)}$$
* **Phân định 2 chân trời dự báo tác nghiệp:**
  1. **Horizon 1 — Nowcasting ngắn hạn (1–3 giờ):**
     * *Ứng dụng:* Cảnh báo lưu thông giao thông đô thị và bảo vệ lao động ngoài trời (Hình 2: Cao tốc US-101 tại Los Angeles).
     * *Tín hiệu cảm biến sẵn có:* Sử dụng các biến trễ gần `target_aqi_lag_1`, `lag_2`, `lag_3` cùng thống kê trượt `roll_mean_from_lag1_3` và `roll_std_from_lag1_3` (cửa sổ 3 giờ).
     * *Động lực chính:* Quán tính tự hồi quy cảm biến ngắn hạn.
  2. **Horizon 2 — Day-Ahead dự báo trước 1 ngày (24 giờ):**
     * *Ứng dụng:* Ra quyết định hành chính (đóng cửa trường học, y tế dự phòng, kích hoạt nơi trú ẩn không khí sạch).
     * *Khoảng trống thông tin 23 giờ (23-Hour Information Blackout Gap):* Che giấu toàn bộ thông tin cảm biến mặt đất từ $t-1$ đến $t-23$; chỉ sử dụng trễ ngày `target_aqi_lag_24, 48, 72` cùng thống kê trượt dài hạn `roll_mean/std_from_lag24_24` và `roll_mean/std_from_lag24_72`.
     * *Cơ chế & Động lực chính:* Quán tính cảm biến suy giảm sâu; các biến vi khí hậu (VPD, vector gió từ Open-Meteo) và trễ không gian liên trạm thay thế quán tính cảm biến để dự báo hướng lan truyền khói bụi.

---

### 📍 SLIDE 04: MULTI-SOURCE PANEL DATASET & CALIFORNIA GEOMORPHIC RELIEF
* **Người phụ trách:** Nguyễn Hữu Thanh Phong (SE191014)
* **Hồ sơ dữ liệu (Dataset Profile: 181,122 dòng · 21 cột cơ sở):**
  * **Nguồn 1 — US EPA AQS (Ground Truth):** Nồng độ $\text{PM}_{2.5}, \text{PM}_{10}$ và chỉ số US AQI chuẩn từ trạm quan trắc mặt đất.
  * **Nguồn 2 — Open-Meteo API (Weather Parameters):** Nhiệt độ 2m, Độ ẩm tương đối, Vector gió 10m ($u, v$), Áp suất bề mặt, Lượng mưa.
* **3 Trạm quan trắc đại diện 3 lưu vực địa mạo (Hình 3):**
  * *Fresno (FRES - 51,615 dòng):* Vùng bồn trũng Thung lũng Central Valley; bị dãy Sierra Nevada và Coast Ranges bao bọc, giữ khói bụi và sương mù mùa đông.
  * *Los Angeles (LA - 50,674 dòng):* Lưu vực ven biển phía Nam; dãy núi San Gabriel bao quanh giữ khí thải và khói cháy rừng sát mặt đất.
  * *San Jose (SJ - 26,304 dòng):* Hành lang phía Bắc; gió biển vịnh San Francisco hỗ trợ đối lưu và khuếch tán khói bụi.
* **4 quyết định kiểm toán & tiền xử lý dữ liệu (AI Data Audit & Preprocessing Decisions):**
  1. *Missing Values:* Conservative Linear Interpolation (6h limit); `dropna` for long gaps (nội suy tuyến tính bảo toàn cho khoảng gián đoạn $\le 6\text{h}$, loại bỏ khoảng trống $> 6\text{h}$ để chống "ảo giác" dữ liệu trong các đợt biến động cháy rừng).
  2. *Outliers:* Extreme AQI spikes detected $\to$ **RETAINED** to predict wildfire events (giữ nguyên toàn bộ các đỉnh nhọn AQI cực đoan lên tới 496 vì nhận diện khủng hoảng cháy rừng là mục tiêu số 1 của đề tài).
  3. *Inconsistent:* Fixed UTC-to-Local timezone misalignment & duplicates (chuẩn hóa lệch múi giờ UTC $\to$ Pacific Time PST/PDT và loại bỏ toàn bộ mốc thời gian trùng lặp).
  4. *Skewness:* Target is highly right-skewed (+4.82) $\to$ **No log-transform (Tree models handle this natively)** (mô hình cây GBDT bất biến với phép biến đổi đơn điệu và xử lý tốt tính phi tuyến; dự báo trực tiếp thang đo AQI gốc cho các ngưỡng cảnh báo quy chuẩn EPA).

---

### 📍 SLIDE 05: 21-COLUMN BASE FEATURE SCHEMA & 8-YEAR CALIFORNIA AQI CATEGORY TIMELINE
* **Người phụ trách:** Nguyễn Hữu Thanh Phong (SE191014)
* **Từ điển dữ liệu 21 cột thuộc tính cơ sở (Harmonized 21-Column Base Schema):**
  * **Nhóm I — Geospatial & Metadata (Cột 1–6):**
    * `time` (Datetime, UTC): Mốc thời gian theo giờ chuẩn hóa đồng bộ.
    * `source` (Categorical): Nguồn gốc (`epa_aqs_station` vs. `openmeteo`).
    * `station_id` & `station_name` (Categorical/String): Mã trạm (`FRES`, `LA`, `SJ`) và tên địa danh mô tả.
    * `lat`, `lon` (Float): Tọa độ địa lý chuẩn của trạm quan trắc (°N, °W).
  * **Nhóm II — Air Quality & Target (Cột 7–10):**
    * `pm25_ug_m3` (Float): Nồng độ bụi mịn $\text{PM}_{2.5}$ ($\mu\text{g}/\text{m}^3$) — Loại bỏ cùng giờ để chống rò rỉ.
    * `pm10_ug_m3` (Float): Nồng độ bụi thô $\text{PM}_{10}$ ($\mu\text{g}/\text{m}^3$).
    * `target_aqi` (Float, $0 - 500+$): **Biến mục tiêu dự báo:** Chỉ số US AQI chuẩn EPA.
    * `target_type` (Categorical): Nhãn chuẩn hóa `pm25_proxy` (công thức từng đoạn của EPA).
  * **Nhóm III — Meteorological Variables (Cột 11–17):**
    * Nhiệt độ 2m (`temperature_2m`, $^\circ\text{C}$), Độ ẩm tương đối (`relative_humidity_2m`, $\%$), Lượng mưa (`rain`, $\text{mm}$), Độ che phủ mây (`cloud_cover`, $\%$).
    * Vector gió 10m: Tốc độ (`wind_speed_10m`, $\text{m}/\text{s}$) và Hướng gió (`wind_direction_10m`, $0^\circ - 360^\circ$).
    * Áp suất bề mặt (`surface_pressure`, $\text{hPa}$).
  * **Nhóm IV — Temporal Components (Cột 18–21):**
    * `hour` ($0 - 23$), `dayofweek` ($0 - 6$), `month` ($1 - 12$), `year` ($2018 - 2025$).
* **Phân tích chuỗi thời gian 8 năm theo thang cảnh báo EPA (Hình 4 — 2018–2026):**
  1. *Cú sốc hỏa hoạn August Complex (Cuối năm 2020):* Nồng độ AQI trung bình ngày chạm ngưỡng Tím (**Very Unhealthy • 200+**) và đỉnh giờ chạm mốc 496, tương phản hoàn toàn với ngưỡng an toàn xanh lá ($\le 50$) của phần lớn các ngày.
  2. *Tính chu kỳ mùa hỏa hoạn (Tháng 8 – Tháng 11):* Các đợt khói bùng phát tập trung vào cuối hè và mùa thu khi thảm thực vật khô kiệt (VPD đỉnh điểm) và gió khô Diablo/Santa Ana thổi mạnh.
  3. *Sự mất cân đối phân phối & Quy chuẩn cảnh báo:* Hơn 85% số ngày thuộc mức Tốt và Trung bình ($AQI \le 100$), khẳng định tính bắt buộc của việc đánh giá mô hình trên các ngưỡng cực đoan ($AQI > 150$).

---

### 📍 SLIDE 06: TARGET DISTRIBUTION (SKEWNESS +4.82) & THREE CORE STATISTICAL CHALLENGES (SKEWNESS +4.82) & THREE CORE STATISTICAL CHALLENGES
* **Người phụ trách:** Nguyễn Hữu Thanh Phong (SE191014)
* **Đặc tính phân phối thực nghiệm AQI (Hình 4):**
  * Thống kê mô tả: Mean = **42.1** | Median = **38.0** | 95th Percentile = **94.0** | Max = **496.0**.
  * Phân phối lệch phải nghiêm trọng: **Skewness = +4.82**; đuôi nặng kéo dài về phía đỉnh hỏa hoạn 496.
  * Hơn 85% số giờ quan trắc thuộc vùng an toàn ($AQI \le 50$); các giờ ô nhiễm nghiêm trọng ($AQI > 150$) chiếm dưới 0.1%.
* **3 thách thức thống kê & giải pháp:**
  1. *Bẫy hàm mất mát MSE & Quyết định No Log-Transform:*
     * Hàm MSE thông thường kéo dự báo co cụm về mức trung bình ~42 điểm.
     * **Quyết định: Không áp dụng log-transform.** Mô hình cây GBDT bất biến với phép biến đổi đơn điệu và xử lý tốt tính phi tuyến. Dự báo trực tiếp thang đo AQI gốc giúp đối chiếu thẳng với các ngưỡng cảnh báo quy chuẩn EPA mà không bị méo sai số khi đảo ngược hàm mũ ($\exp$).
  2. *Tự tương quan chuỗi cao giữa các giờ liền kề:* Vi phạm giả định i.i.d, cấm tuyệt đối việc chia tập ngẫu nhiên.
  3. *Độ trễ vận hành thực tế:* Dữ liệu cảm biến có trễ truyền nhận, đặc trưng phải tuân thủ nghiêm ngặt tính nhân quả.
* **3 bài học EDA:**
  * Đuôi hiếm chiếm < 0.1% thời gian nhưng gây ra > 90% số ca cấp cứu hô hấp.
  * Quán tính chuỗi suy giảm nhanh chóng sau 24h.
  * Địa mạo lòng chảo làm tăng rõ rệt thời gian lưu giữ khói bụi.

---

### 📍 SLIDE 07: CHRONOLOGICAL SPLIT ARCHITECTURE & ZERO-LEAKAGE PROTOCOL
* **Người phụ trách:** Tạ Nguyễn Anh Minh (SE200416)
* **Cấu trúc phân chia thời gian tuần tự (2018–2025):**
  * **Train Set (2018–2023, ~75%, ~136,000 dòng):** Học quy luật khí quyển dài hạn và các đợt cháy rừng lịch sử.
  * **Validation Set (2024, ~15%, ~26,800 dòng):** Tinh chỉnh siêu tham số, dừng sớm (early stopping), hiệu chuẩn ngưỡng.
  * **Test Set (2025, ~10%, 18,322 dòng):** Đánh giá khách quan trên dữ liệu năm mới chưa từng thấy.
  * *Chiến lược phân bổ dữ liệu học và kiểm định sự kiện cực đoan:*
    * **Giai đoạn học mẫu hình lịch sử (Train 2018–2023):** Cung cấp các chu kỳ khí quyển đa dạng cùng đợt siêu bão lửa lịch sử August Complex 2020 để thuật toán cây quyết định GBDT học được các điểm phân nhánh cực đoan ($AQI > 300$, VPD cao kỷ lục).
    * **Khung thời gian kiểm thử sự kiện cực đoan (Validation & Test):** Đánh giá Cấp độ 2 (độ nhạy bắt đỉnh khói, thời điểm bão khói ập đến, Recall/F1 tại ngưỡng 150+ và 300+) được kiểm định trực tiếp trên **đợt siêu hỏa hoạn Park Fire diễn ra từ tháng 7 đến tháng 9/2024 (Tập Validation)** và **năm 2025 (Tập Test)**. Việc kiểm tra vào đúng thời điểm thảm họa Park Fire bùng phát giúp đo lường năng lực học quy luật vật lý và khả năng dự báo thực chiến của mô hình trên một vụ cháy hoàn toàn mới ở tương lai.
  * *Bất biến nhân quả:* $\forall t \in \text{Test}, \quad \text{Train}(\mathcal{D}) \subset \{\tau \mid \tau < t - \text{buffer}\}$.
* **Giao thức kép phòng chống rò rỉ dữ liệu:**
  1. *Vùng đệm biên theo độ trễ tối đa ($\text{Buffer} \ge L_{\max}$):* Cắt bỏ vùng đệm tại ranh giới các năm:
     * Chân trời 1–3h: Độ sâu trễ 3h (`lag_1..3`) & cửa sổ trượt 3h.
     * Chân trời 24h: Che giấu $t-1..23$, độ sâu trễ `lag_24, 48, 72` và cửa sổ trượt 24h/72h.
  2. *Target Feature Blacklist:* Cấm đưa $\text{PM}_{2.5}$ tại thời điểm $t$ vào danh sách đặc trưng đầu vào.
  3. *Scaler Isolation:* Chỉ fit scaler trên tập Train (2018–2023) rồi áp dụng sang Val và Test.

---

### 📍 SLIDE 08: ATMOSPHERIC PHYSICS DRIVERS, CYCLICAL TIME ENCODINGS & 3-TIER TABULAR GBDTS
* **Người phụ trách:** Tạ Nguyễn Anh Minh (SE200416)
* **Quy trình Xử lý Thay thế & 18 Đặc trưng Tinh gọn (18 Compact Final Features):**
  * *Bản chất phương pháp luận:* Nhóm **không làm phình to dữ liệu** bằng các biến rác hay biến tương tác tùy tiện. Thay vào đó, nhóm thực hiện **xử lý thay thế trực tiếp (In-place Transformation)** trên 21 cột gốc để tạo ra ma trận đầu vào cực kỳ tinh gọn gồm đúng **18 đặc trưng vật lý** ($X \in \mathbb{R}^{N \times 18}$) cho các mô hình GBDT:
  * **Module A — Chu kỳ thời gian lượng giác (Cyclical Encodings — 5 biến):**
    * *Công thức thay thế:*
      * Giờ trong ngày: `hour_sin = sin(2 * π * hour / 24)` & `hour_cos = cos(2 * π * hour / 24)` (thay thế cho `hour`).
      * Tháng trong năm: `month_sin = sin(2 * π * month / 12)` & `month_cos = cos(2 * π * month / 12)` (thay thế cho `month`).
      * Ngày cuối tuần: `is_weekend = (dayofweek in [5, 6])` (thay thế từ `dayofweek`).
    * *Bản chất toán học:* Chiếu các biến chu kỳ lên đường tròn đơn vị 2 chiều, khắc phục hoàn toàn hiện tượng "nhảy bậc nhân tạo" (ví dụ: $23\text{h}$ đêm và $0\text{h}$ sáng liền kề nhau nhưng chênh lệch 23 đơn vị; tháng 12 và tháng 1 liền kề nhau), giúp thuật toán cây phân nhánh mượt mà.
  * **Module B — Phân rã vector gió Descartes (Wind Vector Decomposition — 2 biến):**
    * *Công thức thay thế:*
      * Thành phần Đông – Tây: `wind_u = wind_speed_10m * cos(deg2rad(wind_direction_10m))`
      * Thành phần Bắc – Nam: `wind_v = wind_speed_10m * sin(deg2rad(wind_direction_10m))`
    * *Lợi ích:* Thay thế cặp góc cực và tốc độ gió gốc, khắc phục hiện tượng gián đoạn ở ranh giới góc gió $359^\circ \leftrightarrow 1^\circ$; phân tách hướng gió thành 2 trục độc lập mô phỏng trực tiếp hướng thổi của các luồng khói cháy rừng.
  * **Module C — Chỉ số vi khí hậu khô hạn (Microclimate VPD — 1 biến):**
    * `vpd_kpa` (Vapor Pressure Deficit — Áp suất hơi nước thiếu hụt tính từ $T$ và $\text{RH}$):
      $$\text{VPD} = e_s(T) - e_a(T, \text{RH}) = 0.6108 \times \exp\left(\frac{17.27 \times T}{T + 237.3}\right) \times \left(1 - \frac{\text{RH}}{100}\right)$$
      *Ý nghĩa vật lý:* Thước đo chuẩn mực quốc tế (Williams et al., 2019) về độ khô kiệt của thảm thực vật — động cơ chính thúc đẩy cháy rừng bùng phát tại California.
  * **Module D — Trễ tự hồi quy (Autoregressive Lags — 3 biến theo từng Horizon):**
    * *Nguyên tắc chống rò rỉ dữ liệu (Data Leakage Guard):*
      1. *Kịch bản Nowcasting ngắn hạn (Lag 1–3h):* Biến trễ `target_aqi_lag_1`, `target_aqi_lag_2`, `target_aqi_lag_3` (bắt quán tính cảm biến cực mạnh).
      2. *Kịch bản Dự báo xa (Lag 24h):* Che giấu hoàn toàn thông tin cảm biến mặt đất từ $t-1$ đến $t-23$; chỉ dùng `target_aqi_lag_24`, `target_aqi_lag_48`, `target_aqi_lag_72`.
  * **Module E — Không gian & Biến khí tượng cơ sở (7 biến còn lại):**
    * Gồm: `station_id` (hoặc `lat`, `lon`), `temperature_2m`, `relative_humidity_2m`, `surface_pressure`, `rain`, `cloud_cover`, `pm10_ug_m3`.
    * 👉 **Tổng hợp Ma trận Đầu vào ($X$):** Đúng **18 đặc trưng tinh gọn** (1 trạm + 6 khí tượng + 2 vector gió + 1 VPD + 5 chu kỳ thời gian + 3 biến trễ).
* **Bộ đối chuẩn 3 tầng (3-Tier Benchmark Suite):**
  * *Tier 1 (Naïve Baselines):* Persistence ($y_{t+h} = y_t$) và Climatology (trung bình lịch sử theo giờ và tháng).
  * *Tier 2 (Linear & Ensemble):* Ridge Regression và Random Forest.
  * *Tier 3 (Tabular SOTA GBDT):* LightGBM (phân nhánh theo lá, bắt đỉnh nhạy), XGBoost (kiểm soát độ sâu, giảm nhiễu thời tiết), CatBoost (cây đối xứng, chống quá khớp theo mùa).
  * *Lý do chọn GBDT:* Vượt trội trên dữ liệu bảng dị thể (NeurIPS 2022), chi phí thấp, không bị bất ổn trước các đợt sốc khói, giải thích được qua **TreeSHAP**.

---

### 📍 SLIDE 09: FINAL 18-FEATURE MODEL INPUT SCHEMA (X in R^{N x 18}) & ENGINEERING PRINCIPLES
* **Người phụ trách:** Tạ Nguyễn Anh Minh (SE200416)
* **Bảng danh mục 18 đặc trưng đầu vào cuối cùng ($\mathbf{X} \in \mathbb{R}^{N \times 18}$):**
  * *Bản chất phương pháp luận:* Để cung cấp cho hội đồng một cái nhìn trực quan và minh bạch nhất về ma trận đặc trưng sẽ đưa vào huấn luyện các mô hình GBDT, Slide này tổng kết toàn bộ 18 biến số được phân bổ thành 6 nhóm mạch lạc:
  1. **Nhóm I — Vị trí & Trạm (1 đặc trưng):**
     * `station_id` (Categorical): Mã định danh trạm quan trắc (`FRES`, `LA`, `SJ_OPENMETEO`). Đóng vai trò mã hóa bối cảnh địa mạo và vị trí địa lý của từng lưu vực.
  2. **Nhóm II — Khí tượng gốc & Chất ô nhiễm phụ (6 đặc trưng):**
     * `temperature_2m` ($^\circ\text{C}$): Nhiệt độ bề mặt 2m — động cơ thúc đẩy các phản ứng quang hóa và nâng cao tầng biên khí quyển.
     * `relative_humidity_2m` (%): Độ ẩm tương đối 2m — quyết định khả năng ngưng tụ và lắng đọng của sol khí.
     * `surface_pressure` ($\text{hPa}$): Áp suất khí quyển bề mặt — nhận diện các vùng nghịch nhiệt và hiện tượng nén khí giữ bụi bẩn.
     * `rain` ($\text{mm}$): Lượng mưa hàng giờ — yếu tố rửa trôi bụi mịn (wet scavenging).
     * `cloud_cover` (%): Độ che phủ mây — điều tiết bức xạ mặt trời.
     * `pm10_ug_m3` ($\mu\text{g}/\text{m}^3$): Nồng độ bụi thô $\text{PM}_{10}$ — đại diện cho tro bụi hỏa hoạn và bụi đường khu vực.
  3. **Nhóm III — Vector gió Descartes trực giao (2 đặc trưng):**
     * `wind_u` ($\text{m/s}$): Thành phần gió Đông – Tây ($s \cdot \cos(\theta)$).
     * `wind_v` ($\text{m/s}$): Thành phần gió Bắc – Nam ($s \cdot \sin(\theta)$).
     * *Bản chất:* Thay thế hoàn toàn cho cặp vận tốc và góc gió cực, loại bỏ triệt để bước nhảy gián đoạn nhân tạo $359^\circ \leftrightarrow 1^\circ$, mô phỏng chân thực hướng thổi và đối lưu khói cháy rừng.
  4. **Nhóm IV — Vi khí hậu khô hạn thảm thực vật (1 đặc trưng):**
     * `vpd` ($\text{kPa}$): Áp suất hơi nước thiếu hụt (Vapor Pressure Deficit), tính toán theo công thức Tetens từ nhiệt độ và độ ẩm. Đây là thước đo chuẩn mực quốc tế về độ khô nỏ của thảm thực vật — động cơ vật lý số 1 gây bùng phát đại hỏa hoạn tại California.
  5. **Nhóm V — Chu kỳ lượng giác thời gian (5 đặc trưng):**
     * `hour_sin`, `hour_cos` ($[-1, 1]$): Chu kỳ giờ trong ngày — bảo toàn tính liên tục vòng tròn giữa $23\text{h}$ đêm và $0\text{h}$ sáng.
     * `month_sin`, `month_cos` ($[-1, 1]$): Chu kỳ tháng trong năm — bảo toàn tính liên tục vòng tròn giữa tháng 12 và tháng 1, nắm bắt tính mùa vụ cháy rừng mùa thu.
     * `is_weekend` ($\{0, 1\}$): Biến nhị phân ngày cuối tuần — bắt sự thay đổi phát thải của các phương tiện giao thông và xe tải nặng.
  6. **Nhóm VI — Biến trễ quá khứ chuyển mạch theo chân trời (3 đặc trưng):**
     * *Mô hình Nowcasting (1–3h):* Sử dụng `target_aqi_lag_1`, `target_aqi_lag_2`, `target_aqi_lag_3` (bắt quán tính cảm biến cực mạnh).
     * *Mô hình Day-Ahead (24h):* Sử dụng `target_aqi_lag_24`, `target_aqi_lag_48`, `target_aqi_lag_72` (bắt mốc nhịp sinh học ngày hôm trước và các ngày trước đó, tuân thủ nghiêm ngặt lệnh che giấu thông tin 23 giờ).
* **3 điểm nhấn kỹ thuật quan trọng (Key Takeaways):**
  * **Tỷ lệ mẫu/biến vàng 10,000 : 1:** Với 181,122 dòng và đúng 18 biến đầu vào, tỷ lệ này giúp các thuật toán GBDT hoàn toàn miễn nhiễm với hiện tượng quá khớp (overfitting) và không bị "học vẹt" nhiễu số liệu trên các sự kiện cực đoan hiếm gặp ($< 1\%$).
  * **Xử lý thay thế trực tiếp (In-Place Physics):** Nhóm không tạo thêm các biến tương tác phức tạp gây đa cộng tuyến, mà chỉ chuyển đổi các biến gốc sang hệ tọa độ và thước đo vật lý chuẩn mực.
  * **Tính bất biến giữa 2 chân trời (Dual-Horizon Invariance):** Toàn bộ 15 biến đầu tiên ($1 \to 15$) hoàn toàn giống nhau giữa 2 mô hình; chỉ có 3 biến trễ cuối cùng ($16 \to 18$) được chuyển mạch theo đúng chân trời dự báo, đảm bảo tính nhất quán và tinh gọn trong kiến trúc tác nghiệp.

---

### 📍 SLIDE 10: EVALUATION FRAMEWORK AND RESEARCH CONTRIBUTIONS
* **Người phụ trách:** Đồng Bảo Hân (SE203683)
* **Khung đánh giá 2 cấp độ (Two-Level Evaluation Framework):**
  * **Level 1 — Hiệu năng dự báo toàn diện (Overall):**
    * *Thước đo:* $R^2, \text{MAE}, \text{RMSE}, \text{sMAPE}$ trên toàn bộ 181,122 bản ghi.
    * *Mục tiêu:* Đánh giá độ chính xác trong điều kiện vận hành thường nhật.
  * **Level 2 — Biến cố ô nhiễm cực đoan (Extremes):**
    * *Thước đo:* **Precision, Recall, F1-score** tại các ngưỡng EPA ($AQI > 150$ và $> 300$).
    * *Mục tiêu:* Đo lường năng lực phát hiện các đợt bão khói nguy hại đến sức khỏe cộng đồng.
* **Hạn chế của $R^2$ trên các sự kiện cực đoan & Cơ chế Variance Collapse:**
  * *Bẫy toán học của $R^2$:* Khi chỉ lọc riêng các ngày bão khói ($AQI > 300$), các giá trị thực tế đều cao ngang nhau $\to$ Phương sai nhãn (mẫu số $\text{SS}_{\text{tot}}$) tụt về gần bằng $0$.
  * *Nghịch lý âm sâu:* Dù mô hình dự báo rất sát thực tế (ví dụ: thực tế ~312, đoán 310–320), chỉ một sai lệch nhỏ ở tử số $\text{SS}_{\text{res}}$ cũng bị phóng đại lên gấp nhiều lần mẫu số, dẫn tới việc tỷ số $\frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} > 1$ và $R^2$ bị âm sâu vô lý (**Variance Collapse**).
  * *Nhu cầu thực tế & Giải pháp Cấp độ 2:* Ứng cứu y tế không cần biết mô hình đoán lệch 310 thành 315, mà cần biết **có bắt trúng ngày vượt ngưỡng nguy hại để sơ tán hay không**. Do đó, bắt buộc phải dùng thêm thước đo phân loại **Recall (tránh bỏ sót đợt khói độc)** và **Precision/F1 (tránh báo động giả)**.
* **4 đóng góp nghiên cứu cốt lõi:**
  1. Bộ dữ liệu chuẩn hóa 8 năm EPA–Open-Meteo 181k dòng (21 cột gốc).
  2. Thực chứng vai trò của VPD, vector gió $(u, v)$ và chu kỳ $\sin/\cos$ ở chân trời 24h.
  3. Pipeline phân chia tuần tự có vùng đệm trễ biên chống rò rỉ dữ liệu.
  4. Khung đánh giá 2 cấp độ kết hợp giữa độ chính xác thường nhật và cảnh báo y tế.

---

### 📍 SLIDE 11: THREE-PHASE IMPLEMENTATION ROADMAP & EXPECTED DELIVERABLES
* **Người phụ trách:** Đồng Bảo Hân (SE203683)
* **Lộ trình 3 giai đoạn:**
  * *Giai đoạn 1 (Tuần 1–2, Hiện tại — Present 1):* Dữ liệu sạch 181,122 dòng (21 cột gốc); quy trình chuyển đổi 18 đặc trưng tinh gọn; giao thức vùng đệm biên $\text{Buffer} \ge L_{\max}$.
  * *Giai đoạn 2 (Tuần 3–5, Sắp tới — Present 2):* Huấn luyện mô hình Tier 1–3 GBDT trên dữ liệu 2018–2023 (tiếp thu quy luật cháy 2020); tinh chỉnh ngưỡng cảnh báo và đánh giá năng lực bắt đỉnh cực đoan trên tập Validation 2024 (siêu cháy rừng Park Fire).
  * *Giai đoạn 3 (Tuần 6–8 — Final Presentation):* Đánh giá trên Test 2025; giải thích đóng góp đặc trưng bằng TreeSHAP; xây dựng ứng dụng web demo bằng Streamlit.
* **4 sản phẩm đầu ra cụ thể:**
  1. Bộ dữ liệu chuỗi thời gian sạch 181k dòng chuẩn hóa.
  2. Bộ mã nguồn Python tiền xử lý và cắt đệm chống rò rỉ tự động.
  3. Báo cáo đối chuẩn mô hình chuyên sâu kèm phân tích TreeSHAP.
  4. Ứng dụng web Streamlit demo trực quan hóa dự báo 1–3h và cảnh báo trước 24h.

---

# PHẦN 2: BỘ CẨM NANG 31 CÂU HỎI & ĐÁP ÁN BẢO VỆ PHẢN BIỆN (DEFENSE Q&A HANDBOOK)
*(Được cấu trúc theo 5 nhóm chuyên đề kỹ thuật cốt lõi — Trả lời trực diện vào luận điểm toán học, vật lý khí quyển và quy chuẩn kỹ thuật)*

---

## 📂 CHỦ ĐỀ I: DỮ LIỆU, KIỂM TOÁN & TIỀN XỬ LÝ (DATA, AUDIT & PREPROCESSING)

---

### ❓ Q01: Tại sao KHÔNG áp dụng log-transform khi Skewness của nhãn lên tới +4.82?
* **Luận điểm kỹ thuật:**
  1. **Tính bất biến đơn điệu của GBDT (Monotonic Invariance):** Các thuật toán cây (LightGBM, XGBoost, CatBoost) phân nhánh dựa trên thứ tự xếp hạng (rank order) của giá trị tại mỗi nút cắt. Phép biến đổi $\log(x)$ hay $\log(1+x)$ là hàm đơn điệu tăng nghiêm ngặt, do đó không làm thay đổi các điểm cắt phân nhánh tối ưu của cây.
  2. **Bảo toàn thang đo quy chuẩn EPA:** Mục tiêu đề tài là dự báo theo các ngưỡng cảnh báo cố định của US EPA (150 điểm — Unhealthy, 300 điểm — Hazardous). Nếu áp dụng log-transform, hàm mất mát sẽ tối ưu hóa trên sai số tương đối (relative error) trong không gian log, nén dải đỉnh 300–500 thành một khoảng rất hẹp. Khi chuyển đổi ngược bằng hàm mũ ($\exp$), sai số nhỏ ở không gian log bị khuếch đại thành sai số khổng lồ ở thang đo thực tế, làm giảm độ nhạy bắt các đỉnh thiên tai cực đoan.
* **Câu chốt trả lời Hội đồng:**
  > *"Mô hình cây GBDT bất biến với phép biến đổi đơn điệu. Giữ nguyên thang đo gốc giúp mô hình tối ưu trực tiếp trên các ngưỡng cảnh báo y tế cố định của EPA (150 và 300) mà không bị méo sai số khi đảo ngược hàm mũ."*

---

### ❓ Q02: Tại sao GIỮ NGUYÊN các giá trị ngoại lai cực đoan (Outliers Retained up to 496.0)?
* **Luận điểm kỹ thuật:**
  1. **Ngoại lai vật lý hợp lệ (Valid Physical Extremes):** Các đỉnh AQI lên tới 496.0 sinh ra bởi thảm họa cháy rừng lịch sử August Complex (tháng 9/2020), không phải do cảm biến bị lỗi hay nhiễu kỹ thuật.
  2. **Trọng tâm ứng dụng:** Giá trị cốt lõi của đề tài là xây dựng hệ thống cảnh báo sớm thiên tai bão khói ($AQI > 300$). Nếu cắt gọt (winsorize) hay loại bỏ các giá trị này, mô hình sẽ bị "mù" trước các đợt sốc ô nhiễm và mất khả năng học quy luật thiên tai.

---

### ❓ Q03: Tại sao áp dụng Linear Interpolation $\le 6\text{h}$ và `dropna` cho khoảng trống $> 6\text{h}$?
* **Luận điểm kỹ thuật:**
  1. **Khoảng ngắn $\le 6\text{h}$:** Phát sinh do mất kết nối cảm biến tạm thời hoặc truyền nhận mạng. Trong thời gian ngắn này, nồng độ sol khí mặt đất mang tính liên tục vật lý cao, nội suy tuyến tính là xấp xỉ tự nhiên và ít gây méo chuỗi nhất.
  2. **Khoảng dài $> 6\text{h}$:** Hình thế thời tiết và trường gió có thể đã thay đổi hoàn toàn. Việc dùng KNN hay MICE dựa trên dữ liệu toàn niên sẽ làm rò rỉ tương lai và sinh ra dữ liệu ảo (data hallucination) trong các đợt biến động cháy rừng. Do đó, `dropna` là giải pháp trung thực và an toàn nhất với chuỗi thời gian thực nghiệm.

---

### ❓ Q04: Việc nội suy tuyến tính 6 giờ có làm rò rỉ tương lai (Lookahead Leakage) không?
* **Luận điểm kỹ thuật:**
  1. **Cách ly tuyệt đối ranh giới phân chia (Boundary Isolation):** Nhóm cấm tuyệt đối việc nội suy xuyên qua các mốc ranh giới phân chia (ranh giới cuối năm 2023 giữa Train và Val; cuối năm 2024 giữa Val và Test).
  2. **Vùng đệm biên triệt tiêu ảnh hưởng:** Giao thức vùng đệm biên $\text{Buffer} \ge L_{\max}$ đã cắt bỏ hoàn toàn phần tiếp giáp, đảm bảo tập Test không bao giờ kế thừa bất kỳ giá trị nội suy nào từ quá khứ gần của tập Train/Val.
  3. **Trong thực tế vận hành (Production Inference):** Khi hệ thống chạy thời gian thực, nếu cảm biến bị đứt quãng ngắn chưa có tương lai, hệ thống sẽ chuyển sang dùng *Forward Fill* (giữ nguyên giá trị gần nhất) để đảm bảo tuân thủ tính nhân quả 100%.

---

### ❓ Q05: Tại sao phải loại bỏ nồng độ $\text{PM}_{2.5}$ đồng thời điểm ($t$) khỏi tập đặc trưng?
* **Luận điểm kỹ thuật:**
  1. **Phòng chống rò rỉ nhãn đại số (Label Leakage Defense):** Chỉ số US AQI trong các mùa cháy rừng được tính toán trực tiếp từ nồng độ $\text{PM}_{2.5}$ theo công thức ghép từng đoạn cố định của EPA:
     $$AQI = \frac{I_{\text{high}} - I_{\text{low}}}{C_{\text{high}} - C_{\text{low}}} (C - C_{\text{low}}) + I_{\text{low}}$$
  2. **Tránh mô hình học vẹt:** Nếu đưa $\text{PM}_{2.5}$ tại $t$ vào đầu vào, mô hình sẽ học phép xấp xỉ công thức đại số để tính ngược ra AQI ($R^2 \approx 1.0$) thay vì học quy luật lan truyền ô nhiễm và động lực học khí quyển. Do đó, chỉ cho phép dùng $\text{PM}_{2.5}$ quá khứ ($t-h$ trở về trước).

---

### ❓ Q06: Tại sao trong bảng dữ liệu cơ sở có cả $\text{PM}_{10}$, biến này có nguy cơ gây rò rỉ (Leakage) như $\text{PM}_{2.5}$ không?
* **Luận điểm kỹ thuật:**
  1. **Không gây rò rỉ công thức:** Chỉ số US AQI trong đề tài được tính từ $\text{PM}_{2.5}$ proxy. $\text{PM}_{10}$ là hạt bụi thô (bụi đất cát, tro than lớn), không có công thức đại số trực tiếp nào suy ngược ra nhãn mục tiêu.
  2. **Tín hiệu vật lý phân biệt nguồn gốc:** Tỷ lệ $\frac{\text{PM}_{2.5}}{\text{PM}_{10}}$ là một chỉ số kinh điển trong khí tượng học: tỷ lệ này rất cao ($> 0.7 - 0.8$) trong các đợt cháy rừng (toàn sol khí khói mịn), nhưng lại thấp ($< 0.4$) trong các đợt bão cát hoặc bụi giao thông đô thị. Do đó, $\text{PM}_{10}$ là đặc trưng vật lý quan trọng giúp cây phân loại chính xác bản chất ô nhiễm.

---

### ❓ Q07: Sự kiện cực đoan ($AQI > 150$) chỉ chiếm < 0.1% dữ liệu. Tại sao KHÔNG dùng SMOTE, ADASYN hay Random Undersampling để cân bằng dữ liệu?
* **Luận điểm kỹ thuật:**
  1. **Phá vỡ cấu trúc chuỗi thời gian (Temporal Autocorrelation Destruction):** Kỹ thuật SMOTE tạo mẫu nhân tạo dựa trên phép nội suy k-láng giềng trong không gian đặc trưng thuần túy, hoàn toàn không có trục thời gian. Việc chèn các điểm dữ liệu nhân tạo vào giữa chuỗi làm hỏng trật tự nhân quả, phá vỡ tính liên tục của các biến trễ (`lag_1..3`, `lag_24`) và làm méo các cửa sổ trượt thống kê (rolling mean/std).
  2. **Đứt gãy chuỗi khi Undersampling:** Lọc bỏ các ngày bình thường ($AQI \le 50$) sẽ biến chuỗi thời gian 8 năm liên tục thành một chuỗi rời rạc chắp vá, khiến mô hình không thể học được quá trình chuyển pha từ trạng thái bình thường sang bùng phát cháy rừng.
  3. **Giải pháp chuẩn công nghiệp:** Giữ nguyên chuỗi thời gian gốc và giải quyết mất cân bằng bằng phương pháp cấp độ thuật toán: gán trọng số mẫu theo hàm chi phí (Sample Weighting / Cost-Sensitive Loss cho các điểm cực đoan) và hiệu chuẩn ngưỡng phân loại (Threshold Tuning) ở Cấp độ 2.

---

## 📂 CHỦ ĐỀ II: KỸ NGHỆ ĐẶC TRƯNG & VẬT LÝ KHÍ QUYỂN (FEATURE ENGINEERING & ATMOSPHERIC PHYSICS)

---

### ❓ Q08: Mã hóa chu kỳ ngày và tháng $(\sin, \cos)$ mang lại lợi ích toán học gì cho GBDT?
* **Luận điểm kỹ thuật:**
  1. **Bản chất vòng tròn khép kín (Circular Continuity):** Giờ trong ngày ($0 \to 23$) và tháng trong năm ($1 \to 12$) là đại lượng tuần hoàn khép kín.
  2. **Xóa bỏ bước nhảy nhân tạo (Artificial Step-Jump):** Nếu để số nguyên đơn thuần, cây quyết định coi khoảng cách giữa $23\text{h}$ và $0\text{h}$ là $23$ đơn vị (bước nhảy phi vật lý). Khi chiếu lên đường tròn đơn vị $(\sin, \cos)$:
     $$\text{hour\_sin} = \sin\left(\frac{2\pi \times \text{hour}}{24}\right), \quad \text{hour\_cos} = \cos\left(\frac{2\pi \times \text{hour}}{24}\right)$$
     Mốc $23\text{h}$ và $0\text{h}$ nằm liền kề nhau trong không gian 2D, giúp cây phân nhánh liên tục và học chính xác quy luật ngày/đêm và mùa cháy rừng.

---

### ❓ Q09: Biến VPD (Vapor Pressure Deficit) từ bài báo khoa học nào và công thức vật lý là gì?
* **Luận điểm kỹ thuật & Trích dẫn y văn:**
  1. **Williams et al. (2019, Earth's Future - AGU) & Abatzoglou & Williams (2016, PNAS):** Công trình kinh điển chứng minh **VPD là yếu tố khí quyển chi phối số 1 (primary atmospheric driver)** quyết định diện tích và mức độ cháy rừng tại California ($r = 0.72 - 0.79$). VPD là thước đo chuẩn vàng về độ khô hạn nhiên liệu thực vật (fuel aridity).
  2. **Tetens (1930) / Chuẩn FAO-56:** Công thức tính áp suất hơi bão hòa $e_s(T)$ và chênh lệch bốc thoát hơi nước từ Nhiệt độ 2m và Độ ẩm tương đối:
     $$\text{VPD} = e_s(T) - e_a(T, \text{RH}) = 0.6108 \times \exp\left(\frac{17.27 \times T}{T + 237.3}\right) \times \left(1 - \frac{\text{RH}}{100}\right)$$
  3. **Aguilera et al. (2021, Nature Communications):** Chứng minh các đợt tăng vọt VPD gây cháy rừng lớn, đẩy nồng độ $\text{PM}_{2.5}$ vượt ngưỡng nguy hại EPA gấp hàng chục lần.

---

### ❓ Q10: Tại sao phải phân rã vector gió Descartes $(u, v)$ thay vì để góc độ và tốc độ gió thô?
* **Luận điểm kỹ thuật:**
  1. **Khắc phục gián đoạn góc $359^\circ \leftrightarrow 1^\circ$:** Nếu dùng góc gió trực tiếp từ $0^\circ$ đến $360^\circ$, hai luồng gió Bắc hướng $359^\circ$ và $1^\circ$ hoàn toàn giống nhau về mặt vật lý nhưng lại chênh lệch $358^\circ$ trong dữ liệu số, khiến cây phân nhánh sai lệch.
  2. **Tách biệt thành phần động lực học:** Công thức chiếu Descartes:
     $$u = \text{wind\_speed} \times \cos(\text{rad}), \quad v = \text{wind\_speed} \times \sin(\text{rad})$$
     Tách gió thành 2 trục độc lập: trục Đông – Tây ($u$) và trục Bắc – Nam ($v$), mô tả trực tiếp vận tốc và hướng dịch chuyển của các luồng khói cháy rừng theo địa mạo thung lũng.

---

### ❓ Q11: Các biến vi khí hậu ($T$, RH, VPD, Dry Heat) có tương quan rất cao ($r > 0.8$). Có gây hiện tượng Đa cộng tuyến (Multicollinearity) làm hỏng GBDT không?
* **Luận điểm kỹ thuật:**
  1. **Khác biệt cốt lõi giữa Hồi quy OLS và Cây GBDT:** Trong hồi quy tuyến tính, đa cộng tuyến làm ma trận $(X^T X)^{-1}$ gần suy biến, làm hệ số $\beta$ bị thổi phồng phương sai. Nhưng với GBDT, thuật toán phân nhánh dựa trên độ giảm tạp chất (variance reduction / split gain) của từng biến độc lập tại mỗi nút một cách tham lam (greedy).
  2. **Lợi ích phi tuyến:** Dù nhiệt độ ($T$) và độ ẩm ($\text{RH}$) tương quan với VPD, hàm biến đổi của VPD là một phương trình hàm mũ phi tuyến phức tạp (công thức Tetens). Một cây quyết định phải thực hiện hàng chục nhát cắt liên tiếp mới xấp xỉ được đường cong hàm mũ này. Khi kỹ nghệ trực tiếp biến `vpd_kpa`, mô hình chỉ cần một vài nhát cắt đơn giản là nắm bắt được quy luật khô kiệt khí quyển, giảm độ sâu của cây và chống quá khớp (overfitting).
  3. **Kiểm soát bằng Colsample:** Cài đặt `colsample_bytree = 0.7 - 0.8` (XGBoost) hoặc `feature_fraction = 0.8` (LightGBM) ép các cây học trên các tập con thuộc tính khác nhau, ngăn chặn hiện tượng một nhóm biến tương quan chi phối toàn bộ mô hình.

---

### ❓ Q12: Căn cứ khoa học nào để nhóm chọn độ dài cửa sổ trượt là 3 giờ, 24 giờ và 72 giờ?
* **Luận điểm kỹ thuật & Ý nghĩa chu kỳ khí quyển:**
  1. **Cửa sổ 3 giờ (3h Rolling Window):** Phù hợp với chu kỳ hoạt động giao thông đô thị (rush hour: 6h–9h sáng và 16h–19h chiều) và khoảng thời gian bán rã xáo trộn tầng biên khí quyển (atmospheric boundary layer mixing). Đây là khoảng thời gian tối ưu để đo lường quán tính động học tức thời của sol khí mặt đất.
  2. **Cửa sổ 24 giờ (Diurnal Cycle):** Đúng bằng chu kỳ nhật triều của Trái Đất (chu kỳ ngày/đêm 24 giờ). Việc tính toán trung bình và độ lệch chuẩn trượt 24h giúp triệt tiêu nhiễu dao động chu kỳ ngày, trích xuất được mức ô nhiễm nền thực sự (baseline air pollution level) của ngày hôm đó.
  3. **Cửa sổ 72 giờ (Synoptic Weather Scale):** Trong khí tượng học vùng California, các hình thế thời tiết quy mô synop gây cháy rừng khốc liệt (như áp cao Great Basin tạo ra các đợt gió khô nóng cực mạnh Diablo và Santa Ana) thường kéo dài từ 2 đến 3 ngày (48h–72h). Cửa sổ 72h đo lường mức độ tích lũy khô hạn và xu hướng tích tụ năng lượng khí quyển trước khi đợt bão khói bùng nổ.

---

### ❓ Q13: Tại sao thiết kế tập biến trễ (Lags & Rolling Windows) tách biệt nghiêm ngặt theo từng chân trời (1–3h vs. 24h)?
* **Luận điểm kỹ thuật:**
  1. **Triệt tiêu nguy cơ rò rỉ thông tin tương lai (Anti-Leakage Guard):** Ở chân trời dự báo xa 24 giờ (Day-Ahead), trong thực tế vận hành tại mốc $t$, ta không thể có số đo cảm biến của $t-1 \dots t-23$. Do đó, phải che giấu hoàn toàn các mốc này và chỉ dùng trễ từ $t-24, t-48, t-72$ cùng cửa sổ trượt dài hạn (24h, 72h).
  2. **Thích ứng với sự suy giảm quán tính chuỗi:** Ở chân trời ngắn 1–3h, quán tính cảm biến cực mạnh, các biến trễ gần `target_aqi_lag_1..3` và `roll_mean/std_3h` đóng vai trò chủ đạo. Ngược lại ở chân trời 24h, mô hình buộc phải chuyển dịch trọng số sang các chỉ số vi khí hậu vật lý (VPD, vector gió $u, v$, chỉ số nhiệt khô, gió khô) và trễ không gian liên trạm `spatial_target_aqi_{station}_lag_{k}` để bắt luồng khói di chuyển giữa các bồn trũng Fresno, LA và San Jose.

---

### ❓ Q14: Biến trễ không gian liên trạm (Spatial Cross-Station Lags) hoạt động như thế nào và cơ chế Fallback khi trạm lân cận bị mất dữ liệu là gì?
* **Luận điểm kỹ thuật:**
  1. **Bản chất vật lý:** Các đợt khói cháy rừng ở California thường di chuyển từ các đám cháy rừng phía Bắc hoặc dãy Sierra Nevada tràn qua Thung lũng Trung tâm rồi tản sang các vùng lân cận. Khói di chuyển qua lại giữa các trạm mất từ vài giờ đến 1 ngày. Biến trễ không gian $t-k$ giúp mô hình bắt trước được hướng lan truyền của luồng khói từ trạm đón gió sang trạm khuất gió.
  2. **Cơ chế Fallback không gian (Spatial Mean Fallback):** Khi một trạm lân cận gặp sự cố mất tín hiệu cảm biến ở mốc $t-k$, hệ thống tự động thay thế bằng **giá trị trung bình không gian** của tất cả các trạm còn lại có dữ liệu tại cùng mốc giờ đó. Cơ chế này đảm bảo đường ống đặc trưng luôn đầy đủ mà không bị lỗi hay làm mất bản ghi.

---

## 📂 CHỦ ĐỀ III: MÔ HÌNH HÓA, ĐỐI CHUẨN & TINH CHỈNH (MODELING, BENCHMARK & TUNING)

---

### ❓ Q15: Tại sao chọn Tabular GBDT thay vì Deep Learning (LSTM, PINNs) hay Foundation Models (Chronos, TimesFM)?
* **Luận điểm kỹ thuật:**
  1. **Hiệu năng trên dữ liệu bảng dị thể:** Nghiên cứu thực nghiệm quy mô lớn (Grinsztajn et al., NeurIPS 2022; McElfresh et al., NeurIPS 2023) chứng minh mô hình cây GBDT vượt trội hơn Deep Learning trên dữ liệu bảng dị thể (kết hợp biến số thực, biến phân loại và chuỗi thời gian).
  2. **Độ ổn định trước cú sốc dữ liệu:** Deep Learning và Foundation Models dễ bị overfit trên phân phối lệch nặng và kém ổn định trước các bước nhảy gián đoạn của cháy rừng.
  3. **Tính khả giải thích (Explainability):** GBDT hỗ trợ tính toán giá trị đóng góp đặc trưng chính xác và nhanh chóng thông qua thuật toán **TreeSHAP**, đáp ứng yêu cầu minh bạch của cơ quan quản lý môi trường.

---

### ❓ Q16: So với các kiến trúc Deep Learning chuỗi thời gian gần đây (DLinear, PatchTST, iTransformer), GBDT có những ưu điểm cốt lõi gì trong bài toán này?
* **Luận điểm kỹ thuật:**
  1. **Mô hình hóa hàm từng đoạn (Step-function Modeling):** Công thức US AQI chuẩn EPA là một hàm ghép từng đoạn (Piecewise Linear Function) với các ngưỡng gãy đột ngột tại 50, 100, 150, 200, 300. Cây quyết định phân nhánh trực giao cực kỳ thích hợp để mô hình hóa chính xác các hàm này, trong khi các mạng nơ-ron sâu với hàm kích hoạt trơn (GELU, SiLU) thường gặp hiện tượng dao động Runge hoặc xấp xỉ kém tại các điểm gãy.
  2. **Tài nguyên và độ trễ tính toán:** GBDT huấn luyện trong vài phút trên CPU thông thường, thời gian suy luận dưới 5 mili-giây, không đòi hỏi cụm máy chủ GPU đắt đỏ và hoàn toàn miễn nhiễm với hiện tượng vanishing/exploding gradient khi gặp giá trị ngoại lai 496.

---

### ❓ Q17: Tại sao Tier 1 & Tier 2 trong Bộ đối chuẩn KHÔNG đưa ARIMA / SARIMAX hay Facebook Prophet vào so sánh?
* **Luận điểm kỹ thuật:**
  1. **Vấn đề kích thước và biến ngoại sinh (Scalability):** Dữ liệu nghiên cứu gồm 181,122 dòng với chuỗi 18 biến ngoại sinh tinh gọn có tính phi tuyến và tương quan chéo cao. Mô hình SARIMAX đòi hỏi đảo ma trận kích thước lớn trong phép tối ưu hóa Maximum Likelihood, thường xuyên gặp hiện tượng tràn bộ nhớ, mất hội tụ hoặc ma trận suy biến (Singular Matrix).
  2. **Hạn chế cố hữu của Facebook Prophet:** Prophet được tối ưu cho chuỗi dữ liệu kinh doanh/thương mại điện tử có xu hướng tuyến tính/logistic và tính mùa vụ tuần hoàn êm dịu. Prophet hoàn toàn bất lực trước các cú sốc gián đoạn tức thời của thiên tai cháy rừng (bước nhảy từ 30 lên 496 trong vài giờ) vì không có cơ chế học các mối quan hệ tương tác phi tuyến vật lý cấp tốc từ gió và VPD.
  3. **Bộ đối chuẩn được chọn lọc khoa học:** Tier 1 chọn Persistence & Climatology (chuẩn vàng WMO trong khí tượng học); Tier 2 chọn Ridge Regression & Random Forest; Tier 3 chọn bộ ba GBDT SOTA (LightGBM, XGBoost, CatBoost).

---

### ❓ Q18: Dự báo ở chân trời xa 24 giờ được triển khai theo chiến lược nào: Direct (Trực tiếp) hay Recursive (Đệ quy)?
* **Luận điểm kỹ thuật:**
  1. **Chiến lược Direct Forecasting (Dự báo trực tiếp):** Nhóm chọn chiến lược **Direct Multi-step Forecasting**, nghĩa là huấn luyện một mô hình chuyên biệt học ánh xạ trực tiếp từ các đặc trưng có sẵn ở mốc $t$ sang nhãn mục tiêu tại $t+24$:
     $$\hat{y}_{t+24} = f_{24h}(\mathbf{X}_t)$$
  2. **Ưu điểm so với Recursive:** Chiến lược đệ quy (dự báo $t+1 \to$ lấy kết quả làm đầu vào đoán $t+2 \to \dots \to t+24$) bị hiện tượng **tích lũy sai số (error accumulation)** rất nặng, đồng thời vi phạm giả định tác nghiệp che giấu thông tin 23 giờ. Chiến lược Direct hoàn toàn miễn nhiễm với tích lũy sai số và khai thác tối đa sức mạnh của các biến vi khí hậu dự báo thời tiết Open-Meteo.

---

### ❓ Q19: Làm sao để tinh chỉnh siêu tham số (Hyperparameter Tuning) cho GBDT mà không bị Overfitting trên chuỗi thời gian?
* **Luận điểm kỹ thuật:**
  1. **Cấm K-Fold Shuffle:** Tuyệt đối không dùng K-Fold ngẫu nhiên vì làm đảo lộn thứ tự thời gian và rò rỉ tương lai.
  2. **Tập Validation độc lập (Năm 2024):** Tinh chỉnh siêu tham số và chọn mô hình tốt nhất trên tập Validation cố định theo thời gian.
  3. **Early Stopping:** Cài đặt dừng sớm sau 50–100 vòng lặp không cải thiện hàm mất mát trên tập Validation để chống học vẹt (overfitting).
  4. **Các tham số kiểm soát độ phức tạp của cây:**
     * `learning_rate` nhỏ ($0.03 - 0.05$) kết hợp số lượng cây lớn.
     * `max_depth` (XGBoost: 6–8), `num_leaves` (LightGBM: 31–63).
     * `colsample_bytree` / `feature_fraction` ($0.7 - 0.8$) lấy mẫu ngẫu nhiên cột đặc trưng để giảm tương quan giữa các cây.
     * Hệ số điều chuẩn L1/L2 (`reg_alpha`, `reg_lambda`) để triệt tiêu các đặc trưng nhiễu.

---

### ❓ Q20: Làm sao chứng minh việc bổ sung các biến vi khí hậu thực sự có đóng góp chứ không phải thêm biến rác (Ablation Study)?
* **Luận điểm kỹ thuật & Phương pháp Ablation Study:**
  1. **Nghiên cứu cắt bỏ đặc trưng đa tầng (Ablation Study) ở Present 2:**
     * *Experiment 1 (Autoregressive Baseline):* Chỉ dùng các biến trễ AQI lịch sử $\to$ Đo lường độ chính xác chuẩn.
     * *Experiment 2 (+ Raw Weather):* Thêm $T$, RH, Tốc độ gió, Áp suất $\to$ Đánh giá mức cải thiện cơ bản.
     * *Experiment 3 (+ Physical Interactions):* Thêm VPD, Vector gió $(u, v)$, Dry Heat, Wind Pressure $\to$ Kiểm chứng giả thuyết vật lý.
     * *Experiment 4 (+ Spatial Lags):* Thêm trễ không gian 3 trạm $\to$ Đánh giá năng lực lan truyền xuyên lưu vực.
  2. **Tiêu chuẩn kiểm chứng khách quan:**
     * Mức cải thiện phải được đo trên **Tập Validation 2024 độc lập**, không được đo trên tập Train.
     * Kiểm chứng ý nghĩa thống kê bằng kiểm định giả thuyết (Wilcoxon Signed-Rank Test) với mức ý nghĩa $p < 0.01$.
     * Phân tích đóng góp qua **TreeSHAP Global Summary Plot**: Chỉ giữ lại các biến có giá trị trung bình $|SHAP|$ vượt trội và loại bỏ những biến có độ đóng góp tiệm cận 0.

---

## 📂 CHỦ ĐỀ IV: KHUNG ĐÁNH GIÁ, THƯỚC ĐO & VẤN ĐỀ TOÁN HỌC (EVALUATION & MATHEMATICAL RIGOR)

---

### ❓ Q21: Nhóm đánh giá các mô hình vào thời điểm sự kiện cực đoan diễn ra trên khoảng thời gian nào và tại sao lại thiết kế như vậy?
* **Luận điểm kỹ thuật & Phương pháp luận chuẩn mực:**
  1. **Xác định chính xác khung thời gian kiểm thử sự kiện cực đoan:**
     * Đánh giá hiệu năng Cấp độ 2 trên sự kiện cực đoan ($AQI > 150$ và $> 300$) được tiến hành trên **giai đoạn tháng 7 đến tháng 9 năm 2024 (Tập Validation)** và **năm 2025 (Tập Test)**.
     * Cụ thể, tâm điểm kiểm định là **đợt siêu hỏa hoạn Park Fire (bùng phát từ cuối tháng 7 đến tháng 9/2024)** — vụ cháy rừng lớn thứ 4 trong lịch sử bang California với diện tích thiêu rụi hơn 429,000 mẫu Anh, đẩy chỉ số AQI tại nhiều trạm lên mức Nguy hại ($> 150 - 250+$).
  2. **Tại sao lại chọn khoảng thời gian này và phân bổ như vậy?**
     * **Tuân thủ đúng trục thời gian tự nhiên (Forward Out-of-Sample Testing):** Tập Train gồm 6 năm lịch sử (2018–2023) với 138,582 bản ghi, bao gồm cả đợt cháy lịch sử August Complex 2020. Giai đoạn này cung cấp đầy đủ các mẫu hình vật lý cực đoan ($VPD > 3.0\,	ext{kPa}$, gió đối lưu mạnh) để thuật toán cây quyết định GBDT học cách phân nhánh và không bị "mù thiên tai".
     * **Đo lường năng lực học quy luật vật lý thay vì học vẹt:** Vụ cháy Park Fire 2024 có tọa độ, thảm thực vật và hướng gió hoàn toàn khác biệt so với các vụ cháy cũ. Việc mô hình đứng ở quá khứ (cuối 2023) và dự báo chính xác đỉnh ô nhiễm của Park Fire (tháng 7–9/2024) chứng minh mô hình thực sự hiểu mối tương quan nhân quả từ các biến khí tượng và vi khí hậu VPD, chứ không hề ghi nhớ máy móc mốc thời gian.
     * **Mô phỏng chân thực điều kiện tác nghiệp thực tế:** Trong đời thực, hệ thống cảnh báo sớm phải vận hành trên các năm tương lai mà dữ liệu chưa từng được ghi nhận. Thiết kế này chứng minh năng lực tổng quát hóa thực chiến (Generalization) của hệ thống.
* **Câu chốt trả lời Hội đồng:**
  > *"Nhóm huấn luyện mô hình trên giai đoạn 2018–2023 để tiếp thu đầy đủ các quy luật khí quyển khắc nghiệt. Toàn bộ quá trình kiểm thử sự kiện cực đoan được thực hiện vào đúng thời điểm thảm họa siêu cháy rừng Park Fire diễn ra (tháng 7–9/2024) và năm 2025. Thiết kế này giúp chứng minh khách quan rằng mô hình thực sự học được bản chất vật lý của bão khói để dự báo cho các thiên tai chưa từng thấy trong tương lai."*

---

### ❓ Q22: Tại sao chỉ số $R^2$ bị âm sâu / sụp đổ khi đánh giá riêng trên các sự kiện cực đoan ($AQI > 150$ hoặc $> 300$)?
* **Luận điểm kỹ thuật & Ví dụ trực quan:**
  1. **Hiện tượng sụp đổ phương sai (Variance Collapse):**
     * Công thức toán học:
       $$R^2 = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = 1 - \frac{\sum (y_i - \hat{y}_i)^2}{\sum (y_i - \bar{y})^2}$$
     * Trên toàn năm, AQI dao động từ $10$ đến $496$, phương sai mẫu số $\text{SS}_{\text{tot}}$ cực lớn nên $R^2$ đạt điểm cao ($0.8 - 0.9$).
     * Khi lọc riêng các giờ cực đoan ($AQI > 300$), các giá trị thực tế đều cao ngang nhau và co cụm quanh đỉnh $\to$ Mẫu số $\text{SS}_{\text{tot}}$ sụp đổ về gần $0$.
  2. **Ví dụ bằng số thực tế:**
     * Thực tế: $y = [310, 312, 315, 308, 315]$ (trung bình $\bar{y} = 312$) $\to$ Mẫu số $\text{SS}_{\text{tot}} = 38$.
     * Mô hình đoán cực sát: $\hat{y} = [300, 320, 310, 318, 305]$ (sai số chỉ $\sim 2-3\%$) $\to$ Tử số $\text{SS}_{\text{res}} = 389$.
     * Tỷ số: $\frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}} = \frac{389}{38} \approx 10.2 \implies R^2 = 1 - 10.2 = \mathbf{-9.2}$.
     * Dù mô hình báo đúng 100% các đợt khói độc, $R^2$ vẫn bị âm sâu do mẫu số quá bé, gây hiểu lầm tai hại nếu chỉ nhìn vào một thước đo này.
  3. **Giải pháp thực tế (Cấp độ 2):**
     * Y tế công cộng không cần biết đoán lệch 310 thành 315, mà cần biết **có cảnh báo vượt ngưỡng nguy hại để sơ tán hay không**.
     * Bắt buộc kết hợp với các thước đo phân loại Cấp độ 2: **Recall (đo năng lực bắt trúng các đợt cháy, tránh bỏ sót)** và **Precision/F1 (tránh báo động giả gây hoang mang)**.
* **Câu chốt trả lời Hội đồng:**
  > *"Chỉ số $R^2$ bị âm trên tập cực đoan không phải vì mô hình dự đoán tệ, mà do hiện tượng toán học Variance Collapse khi mẫu số bị co cụm về 0. Vì mục tiêu số 1 là cảnh báo sức khỏe, nhóm em bắt buộc đánh giá bằng Recall và F1-score tại các ngưỡng EPA 150 và 300 để đo lường chính xác năng lực bảo vệ cộng đồng."*

---

### ❓ Q23: Tại sao lại bổ sung chỉ số sMAPE (Symmetric MAPE) bên cạnh MAE và RMSE?
* **Luận điểm kỹ thuật:**
  1. **Hạn chế của MAPE truyền thống:**
     $$\text{MAPE} = \frac{1}{n} \sum \frac{|y_i - \hat{y}_i|}{|y_i|}$$
     Trong những ngày không khí trong lành tại San Jose mùa xuân, giá trị thực tế rất nhỏ ($y_i \approx 5 - 10$ AQI). Nếu mô hình dự đoán lệch chỉ 5 điểm ($\hat{y} = 15$), sai số tuyệt đối rất nhỏ ($\text{MAE} = 5$), nhưng MAPE lại tính ra là $\frac{5}{10} = 50\%$, thổi phồng sai số vô lý.
  2. **Ưu thế của sMAPE:**
     $$\text{sMAPE} = \frac{100\%}{n} \sum \frac{2 |y_i - \hat{y}_i|}{|y_i| + |\hat{y}_i|}$$
     sMAPE đưa cả thực tế và dự báo vào mẫu số, tự động giới hạn sai số trong khoảng $[0\%, 200\%]$, loại bỏ hoàn toàn hiện tượng chia cho 0 và giúp so sánh công bằng hiệu năng giữa các trạm có mức ô nhiễm nền khác nhau (Fresno ô nhiễm nặng quanh năm vs San Jose ven biển sạch hơn).

---

### ❓ Q24: Khi tính toán thống kê trượt (Rolling Mean, Rolling Std), làm sao lập trình để đảm bảo KHÔNG bị Lookahead Leakage từ nhãn hiện tại?
* **Luận điểm kỹ thuật & Mã nguồn chuẩn hóa:**
  1. **Nguyên tắc lệch pha (Strict Shift & Closed='left'):** Khi tính toán bất kỳ thống kê trượt nào tại thời điểm $t$, giá trị của $t$ tuyệt đối không được nằm trong cửa sổ tính toán.
  2. **Cụ thể trong triển khai:**
     * Với chân trời 1–3h: Cửa sổ trượt 3h được tính xuất phát từ `lag_1`:
       ```python
       df['roll_mean_from_lag1_3'] = df['target_aqi'].shift(1).rolling(window=3).mean()
       ```
       Khoảng dữ liệu tính toán là $[t-3, t-2, t-1]$, hoàn toàn loại trừ mốc $t$.
     * Với chân trời 24h: Cửa sổ trượt 24h và 72h được tính xuất phát từ `lag_24`:
       ```python
       df['roll_mean_from_lag24_24'] = df['target_aqi'].shift(24).rolling(window=24).mean()
       ```
       Khoảng dữ liệu tính toán kết thúc ở $t-24$, tôn trọng 100% khoảng trống che giấu thông tin 23 giờ.

---

### ❓ Q25: Khí hậu California đang biến đổi (nóng hơn, khô hơn, cháy nhiều hơn). Mô hình đối phó thế nào với hiện tượng Concept Drift / Climate Shift khi sang năm 2025?
* **Luận điểm kỹ thuật:**
  1. **Phòng ngừa ngay từ Kỹ nghệ đặc trưng (Physics-Informed Invariance):**
     * Thay vì để mô hình học vẹt trên giá trị tuyệt đối của nhiệt độ ($T$) và độ ẩm ($\text{RH}$) (vốn là những biến bị trôi dạt mạnh theo xu hướng nóng lên toàn cầu), nhóm đã chuyển hóa chúng thành **VPD (Vapor Pressure Deficit)**.
     * VPD là một quy luật nhiệt động lực học bất biến: khi nhiệt độ tăng nhưng độ ẩm không đổi, áp suất hơi nước bão hòa tăng theo hàm mũ, phản ánh trực tiếp trạng thái khô hạn của thực vật mà không phụ thuộc vào mốc năm cụ thể.
     * Tương tự, việc phân rã vector gió $(u, v)$ và chu kỳ $\sin/\cos$ giúp mô hình nắm bắt hướng gió và nhịp điệu mùa vụ mang tính bất biến thiên văn.
  2. **Chiến lược vận hành Tái huấn luyện trượt (Rolling Retraining Strategy):**
     * Khi đưa vào môi trường sản xuất thực tế, hệ thống không đóng băng trọng số mô hình vĩnh viễn mà áp dụng cơ chế tái huấn luyện định kỳ (ví dụ: huấn luyện lại hàng quý hoặc trước mỗi mùa cháy rừng tháng 8) với cửa sổ trượt 3–5 năm gần nhất để liên tục cập nhật xu thế khí hậu mới.

---

## 📂 CHỦ ĐỀ V: KHẢ GIẢI THÍCH, TRIỂN KHAI & TÁC ĐỘNG XÃ HỘI (EXPLAINABILITY, PRODUCTION & IMPACT)

---

### ❓ Q26: Tại sao lại chọn TreeSHAP để giải thích mô hình mà không dùng LIME hay Permutation Importance?
* **Luận điểm kỹ thuật:**
  1. **Tối ưu riêng cho kiến trúc cây (Tree-Specific Efficiency):** Thuật toán **TreeSHAP** (Lundberg et al., Nature Machine Intelligence, 2020) tính toán giá trị đóng góp Shapley chính xác trong thời gian đa thức $\mathcal{O}(T L D^2)$, nhanh hơn hàng nghìn lần so với KernelSHAP hay LIME (vốn dựa trên xấp xỉ lấy mẫu ngẫu nhiên tốn kém).
  2. **Tính nhất quán toán học (Mathematical Consistency):** Permutation Feature Importance bị méo khi dữ liệu có các đặc trưng tương quan cao (ví dụ: nhiệt độ, độ ẩm và VPD). TreeSHAP bảo toàn định lý Shapley (Efficiency, Symmetry, Additivity).
  3. **Giải thích cả 2 cấp độ:** Cung cấp cả bức tranh toàn cục (Global feature importance cho toàn bang) và bức tranh cục bộ (Local force plot giải thích chính xác tại sao vào đúng 15h ngày 09/09/2020 mô hình lại kích hoạt báo động đỉnh khói 496).

---

### ❓ Q27: Tại sao nghiên cứu chọn 3 trạm Fresno, Los Angeles và San Jose? Tính đại diện địa mạo là gì?
* **Luận điểm kỹ thuật:**
  1. **Fresno (Thung lũng Central Valley):** Lưu vực nông nghiệp lòng chảo nội địa, bị bao bọc bởi hai dãy núi Sierra Nevada và Coast Ranges. Không khí trì trệ và hiện tượng nghịch nhiệt mùa đông khiến khói bụi và bụi mịn bị giam cầm nhiều ngày sát mặt đất.
  2. **Los Angeles (Lưu vực ven biển Nam California):** Đô thị siêu dày đặc, mật độ giao thông khổng lồ; gió biển ép khói thải vào sườn núi San Gabriel.
  3. **San Jose (Hành lang Vịnh San Francisco - Bay Area):** Địa hình duyên hải phía Bắc có gió biển vịnh San Francisco đối lưu mạnh, phân tán khói nhanh hơn.
  4. **Tính khái quát hóa:** 3 trạm đại diện cho 3 cơ chế địa mạo - khí tượng hoàn toàn đối nghịch của California (Lòng chảo nội địa - Đô thị ven biển - Vịnh duyên hải gió mạnh).

---

### ❓ Q28: Dữ liệu thời tiết Open-Meteo là Reanalysis hay Forecast? Làm sao đảm bảo chân trời 24h khả thi trong môi trường vận hành thực tế?
* **Luận điểm kỹ thuật:**
  1. **Bản chất trong tập dữ liệu nghiên cứu (2018–2025):** Là dữ liệu tái phân tích độ phân giải cao (Reanalysis ERA5 / HRRR của ECMWF và NOAA) kết hợp đo đạc thực tế, đóng vai trò là "mô phỏng trạng thái khí quyển chuẩn xác nhất" cho quá trình huấn luyện và kiểm định mô hình.
  2. **Khả thi 100% trong môi trường vận hành thực tế:**
     * Open-Meteo cung cấp API dự báo thời tiết số trị (Numerical Weather Prediction - NWP: ECMWF IFS, GFS, HRRR) hoàn toàn miễn phí với độ phân giải hàng giờ cho 1–7 ngày tới.
     * Khi chạy tác nghiệp ở thời điểm $t$ để dự báo $t+24$, hệ thống gửi request lấy dự báo thời tiết của $t+24$ từ Open-Meteo Forecast API (nhiệt độ, độ ẩm, vector gió dự báo) làm biến ngoại sinh đầu vào.
     * Sai số dự báo thời tiết trong vòng 24 giờ của các mô hình NWP hiện đại rất nhỏ ($< 1.0^\circ\text{C}$ đối với nhiệt độ, $< 5\%$ đối với độ ẩm), hoàn toàn nằm trong ngưỡng chịu đựng của mô hình GBDT có điều chuẩn.

---

### ❓ Q29: Nếu trong thực tế vận hành, cảm biến EPA hoặc API Open-Meteo bị sập vài giờ hoặc vài ngày thì hệ thống xử lý thế nào (Graceful Degradation)?
* **Luận điểm kỹ thuật & Cơ chế dự phòng:**
  1. **Sự cố mất kết nối cảm biến EPA (Ground Sensor Outage):**
     * Mất kết nối ngắn ($\le 3\text{h}$): Sử dụng kỹ thuật *Forward Fill* (giữ nguyên giá trị gần nhất) hoặc ước lượng từ mô hình suy luận khí tượng thuần túy.
     * Mất kết nối dài ($> 3\text{h}$): Chuyển sang chế độ dự phòng bằng **Trung bình không gian từ các trạm lân cận** kết hợp nội suy nghịch đảo khoảng cách (Inverse Distance Weighting - IDW).
  2. **Sự cố mất kết nối API thời tiết Open-Meteo:** Hệ thống tự động chuyển sang nguồn khí tượng dự phòng thứ hai (như NOAA GFS API hoặc dữ liệu khí tượng cục bộ của trạm EPA).
  3. **Khả năng chịu đựng của mô hình cây:** Các mô hình GBDT như LightGBM và XGBoost hỗ trợ cơ chế bản địa xử lý giá trị khuyết (native missing value handling): cây tự động gán dữ liệu khuyết vào nhánh con (default split direction) tối ưu dựa trên hàm mất mát trong quá trình huấn luyện mà không làm sập pipeline.

---

### ❓ Q30: Ứng dụng thực tiễn của đề tài sau khi hoàn thành là gì và mô hình có khả năng mở rộng sang các trạm quan trắc khác tại California không?
* **Luận điểm kỹ thuật & Tác động xã hội:**
  1. **Chân trời 1–3h (Nowcasting):** Tích hợp vào hệ thống điều phối giao thông thông minh (như bảng điện tử cao tốc US-101 LA), ứng dụng di động cảnh báo công nhân xây dựng, người giao hàng và người chạy bộ tránh giờ đỉnh điểm ô nhiễm.
  2. **Chân trời 24h (Day-Ahead):** Cung cấp công cụ hỗ trợ ra quyết định hành chính trước 1 ngày cho:
     * **Học khu (School Districts):** Quyết định chuyển sang học trực tuyến hoặc hủy các hoạt động thể thao ngoài trời.
     * **Bệnh viện & Sở Y tế:** Chuẩn bị ca trực cấp cứu hô hấp, tăng cường máy lọc không khí và dự trữ bình oxy.
     * **Chính quyền địa phương:** Kích hoạt trước các Trạm trú ẩn không khí sạch (Clean Air Shelters) cho người vô gia cư và người cao tuổi.
  3. **Khả năng tổng quát hóa không gian (Spatial Transferability):**
     * Toàn bộ các đặc trưng khí tượng, vi khí hậu (`vpd_kpa`, `dry_heat_index`), vector gió $(u, v)$, thời gian $(\sin, \cos)$ và tọa độ địa lý (`lat`, `lon`) đều có thể thu thập tự động từ Open-Meteo API cho bất kỳ tọa độ địa lý nào tại California mà không cần cảm biến mặt đất.
     * Với trạm mới, hệ thống áp dụng thuật toán nội suy nghịch đảo khoảng cách (IDW) từ 3 trạm hạt nhân để tạo ra trường đặc trưng không gian đại diện, mở ra tiềm năng mở rộng ra toàn bộ 58 quận hạt của bang California.

---

### ❓ Q31: Tại sao nhóm chỉ sử dụng 18 đặc trưng tinh gọn thay vì tạo ra hàng chục hay hàng trăm biến kỹ nghệ tương tác?
* **Luận điểm kỹ thuật & Phương pháp luận:**
  1. **Tránh Lời nguyền Chiều dữ liệu (Curse of Dimensionality) & Hiện tượng Quá khớp (Overfitting):**
     * Trong chuỗi thời gian ô nhiễm không khí với các hiện tượng cực đoan hiếm gặp ($< 1\%$), việc nhồi nhét quá nhiều biến tương tác tùy tiện ($A \times B, A / B, \dots$) làm tăng bậc tự do của mô hình, khiến cây quyết định học các phân nhánh rác vô nghĩa (noise memorization) thay vì quy luật vật lý.
     * Tỷ lệ quan sát trên số chiều đặc trưng của nhóm là $\approx 181,122 / 18 \approx 10,000 : 1$ — đây là tỷ lệ vàng trong học máy bảng giúp mô hình tổng quát hóa cực kỳ vững chắc trên các năm kiểm thử chưa từng thấy (2024, 2025).
  2. **Bản chất "Xử lý thay thế" (In-place Transformation) chứ không làm phình to dữ liệu:**
     * Nhóm không tạo thêm biến rác mà **chuyển hóa trực tiếp** các biến gốc sang dạng toán học và vật lý chuẩn mực:
       * Cặp góc gió cực và vận tốc $\to$ Vector Descartes trực giao $(u, v)$ (bắt luồng khói không bị gián đoạn $359^\circ \leftrightarrow 1^\circ$).
       * Biến thời gian dạng bậc thang $\to$ Tọa độ vòng tròn đơn vị $(\sin, \cos)$ (bắt tính tuần hoàn 24h và 12 tháng).
       * Cặp nhiệt độ $T$ và độ ẩm $\text{RH}$ $\to$ Áp suất hơi nước thiếu hụt $\text{VPD}$ (chỉ số khô hạn tiêu chuẩn quốc tế).
  3. **Tối ưu hóa Chi phí Huấn luyện & Khả năng Giải thích (Interpretability):**
     * Ma trận 18 cột giúp thời gian huấn luyện các mô hình GBDT (LightGBM, XGBoost, CatBoost) trên 181k dòng chỉ mất vài giây đến nửa phút, tạo điều kiện thuận lợi cho việc chạy Cross-Validation tuần tự và dò siêu tham số diện rộng.
     * Khi giải thích mô hình bằng **TreeSHAP**, ma trận 18 đặc trưng hiển thị trực quan, mạch lạc, không bị pha loãng giá trị SHAP do hiện tượng đa cộng tuyến giữa hàng chục biến phụ thuộc sinh ra.
