# TÀI LIỆU KỊCH BẢN THUYẾT TRÌNH — BÁO CÁO TIẾN ĐỘ 2 (PRESENT 2)
## ĐỀ TÀI: COMPARATIVE US AQI TIME SERIES FORECASTING IN CALIFORNIA WITH EXTREME-EVENT EVALUATION
*(Nghiên cứu Đối chuẩn Thực nghiệm Mô hình Dự báo Chuỗi Thời gian Chỉ số US AQI tại California trong Bối cảnh Thiên tai Khí hậu Cực đoan)*

---

* **Môn học:** DSR301m – Data Science Project (Đại học FPT TP.HCM)
* **Cột mốc:** PBL Milestone 2 (Present 2) — *Mô hình hóa, Đánh giá và Kết quả Thực nghiệm Sơ bộ*
* **Nhóm thực hiện:** GROUP 5
* **Tài liệu Slides Đối chiếu:** `DSR301m_Group5_Present2.pdf` (Đồng bộ chuẩn 100% 14 Slides)
* **Dữ liệu Thực nghiệm:** 181,122 bản ghi hàng giờ (2018–2025) · 3 Lưu vực Địa mạo: Fresno (Central Valley), Los Angeles (South Coast), San Jose (Bay Area)
* **Không gian Mô hình:** 8 Mô hình Nền tảng + 1 Voting Ensemble thuộc 5 Họ Thuật toán trên 2 Chân trời ($1\text{h}$ Nowcasting vs. $24\text{h}$ Day-Ahead)
* **Cấu trúc 4 Khối Nội dung Chuẩn:**
  1. 📌 **Part 1: Problem & Data Understanding** (Slide 01 – Slide 05)
  2. ⚙️ **Part 2: Feature Engineering & Visualization** (Slide 06 – Slide 07)
  3. 🔬 **Part 3: Modeling, Evaluation** (Slide 08 – Slide 13)
  4. 🎯 **Part 4: Conclusion & Roadmap** (Slide 14)
* **Thời lượng Thuyết trình Dự kiến:** 11 – 13 Phút (Trung bình 50 – 65 giây / slide)
* **Cơ cấu Diễn giả (Modular 4 Speakers):**
  * **Speaker 1:** Phụ trách Part 1 (Title Cover, Outline, Bối cảnh Cháy rừng, 3 Gaps & 2 Horizons, Kiểm toán Dữ liệu 181k & Phân phối Lệch) — Slide 01 đến 05 (~3.5 phút)
  * **Speaker 2:** Phụ trách Part 2 (Zero-Leakage Split & Feature Store Vật lý Khí quyển) — Slide 06 đến 07 (~2.2 phút)
  * **Speaker 3:** Phụ trách Part 3A (Modeling Suite 5 Họ Thuật toán, Leaderboard Bảng Số liệu & Leaderboard Biểu đồ Trực quan) — Slide 08 đến 10 (~3.5 phút)
  * **Speaker 4:** Phụ trách Part 3B & Part 4 (Bám chuỗi 168h Fresno, Đánh giá Cú sốc Cực đoan, Chẩn đoán 3 Chiều Sai số, Kết luận & Lộ trình Milestone 3 + Q&A) — Slide 11 đến 14 (~4 phút)

---

## 🧭 BẢNG ĐIỀU PHỐI THỜI LƯỢNG VÀ DÒNG CHẢY LOGIC 14 SLIDES
*(Khớp chuẩn xác 100% với từng trang của file trình chiếu `DSR301m_Group5_Present2.pdf`)*

| Khối Nội dung | Slide | Tiêu đề Kỹ thuật Slide (PDF) | Diễn giả | Thời lượng | Trọng tâm Khoa học & Bằng chứng Thực nghiệm |
| :--- | :---: | :--- | :---: | :---: | :--- |
| **I. Problem & Data** | **01** | **Title Cover** — DSR301M Present 2 · Group 5 | Speaker 1 | 25s | Giới thiệu đề tài benchmark chuỗi thời gian AQI California, chào Hội đồng |
| | **02** | **Outline** — Khái quát 4 Khối Nội dung Chuẩn | Speaker 1 | 25s | Giới thiệu lộ trình 4 phần: Problem/Data $\to$ Features $\to$ Modeling $\to$ Conclusion |
| | **03** | **Wildfire Crisis & Hazardous Smoke Hazards in California** | Speaker 1 | 55s | Thảm họa August Complex 2020, đỉnh lịch sử 496.0 AQI San Jose, cấp cứu hô hấp tăng >90%, mất cân bằng dữ liệu >85% sạch |
| | **04** | **Three Research Gaps & Dual Operational Horizons** | Speaker 1 | 65s | 3 Gaps (Metric Masking, Lookahead Leakage, Atmospheric Blindspot); Thiết kế Nowcasting 1h ($t+1$) vs Day-Ahead 24h ($t+24$) |
| | **05** | **181k Dataset Audit & Mathematical Distribution Defense** | Speaker 1 | 65s | Kiểm toán 181,122 dòng, 6 cấp độ EPA (95.6% Good/Mod), ma trận tương quan (Gió -0.31), Bất đẳng thức Jensen bác bỏ log-transform |
| **II. Feature & Prep** | **06** | **Zero-Leakage Temporal Split Protocol & Buffer Defense** | Speaker 2 | 65s | Chuỗi thời gian 8 năm; Train 2018–23 (61.3%), Val 2024 (24.1%, Park Fire), Test 2025 (14.5%); Cắt đệm biên $h$ dòng triệt tiêu rò rỉ |
| | **07** | **Physics-Informed Feature Store Architecture** | Speaker 2 | 65s | 2 ma trận đặc trưng: Nowcasting 1h (22 biến) vs Day-Ahead 24h (19 biến); Bản chất vật lý: Vector Descartes $(u, v)$ & Độ khô hạn VPD |
| **III. Modeling & Eval** | **08** | **Benchmark Model Suite: 5 Algorithm Families** | Speaker 3 | 70s | 5 họ (Baselines, Ridge, Random Forest, GBDT SOTA, Tabular MLP); Voting Ensemble; Scaling dị biệt & Mã hóa trạm Categorical/One-Hot |
| | **09** | **Official Leaderboard: Test 2025 Out-of-Sample Evaluation (Table)** | Speaker 3 | 70s | Phân tích Bảng số liệu Leaderboard: Voting Ensemble dẫn đầu (MAE 3.06 ở 1h, 11.30 ở 24h); GBDT vượt trội MLP 200x về tốc độ (0.41s vs 81.62s) |
| | **10** | **Official Leaderboard: Test 2025 Out-of-Sample Evaluation (Charts)** | Speaker 3 | 70s | Phân tích 2 Biểu đồ thanh ngang: Nhóm GBDT kết cụm áp đảo; MLP tụt dốc tại 24h ($R^2=0.501$); Ridge L2 ổn định (11.86) |
| | **11** | **168-Hour Continuous Tracking & Residual Dynamics** | Speaker 4 | 65s | Lát cắt 1 tuần tại Fresno (09–15/01/2025): Bám sát đỉnh 73.4 AQI (Ensemble đạt 72.1 AQI, lệch chỉ 1.3); Dải thặng dư phẳng $<5$ AQI |
| | **12** | **Wildfire Extreme Shock Resilience (24h Day-Ahead)** | Speaker 4 | 70s | Biểu đồ chịu sốc khói: Bình thường 9.9 AQI vs Cực đoan 62.6 AQI (Khoảng chênh $+\Delta 52.7$ AQI); Sụp đổ phương sai $R^2$; F1-Score 0.825 |
| | **13** | **Three-Dimensional Error Diagnostics & Topography** | Speaker 4 | 75s | 3 chiều chẩn đoán: Tail Shrinkage ($\beta = 0.54$–$0.56$), Nghịch nhiệt bức xạ đêm (22h–4h $>14$ AQI), và Địa mạo 3 lưu vực (San Jose vs Fresno vs LA) |
| **IV. Conclusion** | **14** | **Experimental Conclusions & Production Roadmap & Q&A** | Speaker 4 | 60s | 4 Phát hiện thực nghiệm cốt lõi, 3 Giới hạn kỹ thuật; Lộ trình Milestone 3 (Asymmetric Loss, Containerized FastAPI, Dashboard); Q&A |

---

# PHẦN A: KỊCH BẢN THUYẾT TRÌNH CHI TIẾT TỪNG SLIDE (SPEAKER SCRIPT)

---

## 🏛️ PART 1: PROBLEM & DATA UNDERSTANDING (VẤN ĐỀ & THẤU HIỂU DỮ LIỆU)

---

### 📍 SLIDE 01: BÌA ĐỀ TÀI (TITLE COVER) — DSR301M PRESENT 2 · GROUP 5
* **Diễn giả:** Speaker 1 (Khối Problem & Data Understanding)
* **Thời lượng dự kiến:** 25 giây
* **Mục tiêu truyền tải:** Chào Hội đồng trang trọng, tuyên bố tên đề tài, cột mốc Milestone 2 và đơn vị thực hiện Group 5.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Kính thưa Thầy Cô và Hội đồng thẩm định, nhóm 5 xin phép bắt đầu buổi báo cáo tiến độ Milestone 2 của dự án PBL với đề tài:*
>
> ***'Comparative US AQI Time Series Forecasting in California with Extreme-Event Evaluation'*** — *Nghiên cứu Đối chuẩn Thực nghiệm Mô hình Dự báo Chuỗi Thời gian Chỉ số US AQI tại California trong Bối cảnh Thiên tai Khí hậu Cực đoan*."

* **Hành động & Ngôn ngữ cơ thể:** Đứng thẳng, ánh mắt bao quát Hội đồng, cử chỉ tay dứt khoát chỉ lên tiêu đề slide.
* **Lời chuyển ý (Transition):** *"Sau đây, nhóm xin khái quát cấu trúc 4 phần trọng tâm của bài báo cáo hôm nay."*

---

### 📍 SLIDE 02: MỤC LỤC BÁO CÁO (OUTLINE) — KHÁI QUÁT 4 KHỐI NỘI DUNG CHUẨN
* **Diễn giả:** Speaker 1
* **Thời lượng dự kiến:** 25 giây
* **Mục tiêu truyền tải:** Định hướng cho người nghe về lộ trình 4 phần khoa học: Từ thấu hiểu bối cảnh/dữ liệu, kỹ nghệ đặc trưng, mô hình hóa & đánh giá đa cấp độ, đến tổng kết và lộ trình Milestone 3.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Bài báo cáo của nhóm được tổ chức chặt chẽ theo 4 khối nội dung chuẩn:
> * **Part 1 — Problem & Data Understanding:** Tái hiện khủng hoảng cháy rừng California, 3 khoảng trống nghiên cứu cốt lõi và kết quả kiểm toán 181 nghìn dòng dữ liệu.
> * **Part 2 — Feature Engineering & Visualization:** Giao thức phân chia tuần tự chống rò rỉ và kiến trúc Feature Store tích hợp vật lý khí quyển.
> * **Part 3 — Modeling, Evaluation:** Không gian đối chuẩn 5 họ thuật toán, bảng điểm Leaderboard chính thức, khả năng bám chuỗi 168 giờ và kiểm tra sức bền trước cú sốc bão khói cực đoan.
> * **Part 4 — Conclusion:** Tổng kết 4 phát hiện thực nghiệm, nhận diện 3 giới hạn và công bố lộ trình MLOps chuyển giao cho Milestone 3."*

* **Hành động & Ngôn ngữ cơ thể:** Điểm nhanh từng khối nội dung, tạo cảm giác mạch lạc và có chủ đích.
* **Lời chuyển ý (Transition):** *"Trước tiên, xin mời Thầy Cô cùng nhìn vào bức tranh thực tế đầy thách thức tại California."*

---

### 📍 SLIDE 03: BỐI CẢNH KHỦNG HOẢNG CHÁY RỪNG & TÁC ĐỘNG SỨC KHỎE CỘNG ĐỒNG
*(Slide Title: Wildfire Crisis & Hazardous Smoke Hazards in California — Historic August Complex 2020 Megafire & Acute Respiratory Shocks)*
* **Diễn giả:** Speaker 1
* **Thời lượng dự kiến:** 55 giây
* **Mục tiêu truyền tải:** Tái hiện tính nghiêm trọng của đại hỏa hoạn California (Hình ảnh bầu trời cam San Francisco, đỉnh lịch sử 496.0 AQI); chỉ rõ tác động y tế cộng đồng và đặt nền móng cho tính cấp bách của đề tài.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"California liên tục đối mặt với các đợt đại hỏa hoạn lịch sử khốc liệt. Điển hình vào tháng 9 năm 2020, đại hỏa hoạn August Complex đã nhuộm đỏ bầu trời vùng Vịnh San Francisco, biến ban ngày thành màn đêm màu cam nghẹt thở. 
> 
> Tại trạm San Jose, chỉ số AQI đo được đã chạm đỉnh lịch sử **496.0 AQI** — vượt xa ngưỡng Nguy hại cao nhất của US EPA (301+) tới **195 điểm**, tiệm cận giới hạn trần 500 của cảm biến vật lý.
>
> Về mặt y tế cộng đồng, các nghiên cứu dịch tễ học chỉ ra rằng khi nồng độ bụi khói mịn vượt tiêu chuẩn WHO trên 10 lần, số ca nhập viện cấp cứu do suy hô hấp và tim mạch **tăng vọt trên 90%**.
>
> Tuy nhiên, bài toán dự báo gặp phải thách thức mất cân bằng dữ liệu cực đoan (*Severe Data Imbalance*): Hơn **85% số ngày trong năm là không khí sạch (AQI $\le 50$)**. Do đó, các mô hình học máy thông thường rất dễ bị ru ngủ bởi đa số ngày sạch, hoàn toàn bỏ lỡ các đỉnh thiên tai bão khói hiếm gặp nhưng gây tử vong cao."*

* **Hành động & Ngôn ngữ cơ thể:** Nhấn giọng tại các con số: *"496.0 AQI"*, *"tăng trên 90%"*, *"hơn 85% ngày sạch"*.
* **Lời chuyển ý (Transition):** *"Từ thực tế đó, nhóm đã khảo sát y văn và nhận diện 3 khoảng trống nghiên cứu cốt lõi."*

---

### 📍 SLIDE 04: 3 KHOẢNG TRỐNG NGHIÊN CỨU & THIẾT KẾ 2 CHÂN TRỜI TÁC NGHIỆP (1H VS 24H)
*(Slide Title: Three Research Gaps & Dual Operational Horizons — Designing Purpose-Built Forecasting Architectures for Public Health Action)*
* **Diễn giả:** Speaker 1
* **Thời lượng dự kiến:** 65 giây
* **Mục tiêu truyền tải:** Chỉ rõ 3 khoảng trống y văn (Research Gaps); từ đó giải thích cơ sở khoa học để thiết kế 2 chân trời tác nghiệp chuyên biệt (1h Nowcasting vs 24h Day-Ahead) nhằm giải quyết trực diện các khoảng trống này.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Khảo sát y văn quốc tế cho thấy các nghiên cứu dự báo chất lượng không khí hiện tại vấp phải **3 khoảng trống lớn**:
> 1. **Che lấp sai số bằng thước đo trung bình (Metric Masking):** Vì hơn 85% ngày sạch chiếm ưu thế tuyệt đối, chỉ số MAE hay RMSE toàn niên che giấu hoàn toàn thất bại thảm hại của mô hình tại các ngày bão khói ($AQI > 150$).
> 2. **Rò rỉ dữ liệu tương lai (Lookahead Leakage):** Việc xáo trộn dữ liệu ngẫu nhiên (Random Train/Test Split) trên chuỗi thời gian làm rò rỉ tín hiệu tương lai, tạo ra điểm số ảo $R^2 > 0.95$ trên giấy tờ nhưng sụp đổ hoàn toàn khi triển khai tác nghiệp thực tế.
> 3. **Điểm mù khí quyển (Atmospheric Blindspot):** Các mô hình chỉ dựa vào cảm biến mặt đất sẽ mất phương hướng hoàn toàn khi dự báo xa, vì tương quan tự hồi quy của cảm biến suy giảm triệt để sau 24 giờ nếu thiếu mô hình dự báo thời tiết số trị (NWP).
>
> Để giải quyết tận gốc 3 khoảng trống này, nhóm thiết kế song song **hai chân trời tác nghiệp có bản chất vật lý hoàn toàn tách biệt**:
> * **Horizon 1 — Nowcasting 1 giờ ($t+1$):** Phục vụ cảnh báo tức thời cho người lao động ngoài trời và điều phối giao thông, vận hành dựa trên **quán tính cảm biến mặt đất** (chuỗi trễ $0\text{--}3\text{h}$ và biến vi sai).
> * **Horizon 2 — Day-Ahead 24 giờ ($t+24$):** Phục vụ quyết định hành chính như đóng cửa trường học hoặc điều phối ca trực bệnh viện. Tại đây, **100% cảm biến mặt đất tương lai bị cô lập**, mô hình bắt buộc phải suy luận dựa trên **trường vi khí hậu số trị dự báo (NWP)**."*

* **Hành động & Ngôn ngữ cơ thể:** Tay trái chỉ cột 3 Gaps, tay phải mở rộng sang cột 2 Horizons để làm bật tính đối ứng logic.
* **Lời chuyển ý (Transition):** *"Xuất phát từ thiết kế bài toán, nhóm tiến hành kiểm toán dữ liệu 181 nghìn bản ghi và phân tích cơ sở toán học của phân phối."*

---

### 📍 SLIDE 05: KIỂM TOÁN 181K DỮ LIỆU & CƠ SỞ TOÁN HỌC BẢO TỒN PHÂN PHỐI LỆCH (+1.31)
*(Slide Title: 181k Dataset Audit & Mathematical Distribution Defense — 181,122 Hourly Records (2018–2025) Across 3 Topographic Basins)*
* **Diễn giả:** Speaker 1
* **Thời lượng dự kiến:** 65 giây
* **Mục tiêu truyền tải:** Trình bày 4 quyết định kiểm toán trên 181,122 bản ghi; phân tích biểu đồ phân phối 6 cấp độ EPA và ma trận tương quan; giải trình cơ sở toán học (Bất đẳng thức Jensen) của việc không dùng log-transform.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Tập dữ liệu kết hợp trạm quan trắc mặt đất EPA AQS và dữ liệu vi khí hậu Open-Meteo, gồm **181,122 bản ghi hàng giờ** trải dài 8 năm (2018–2025) tại 3 lưu vực đối nghịch: Fresno (lòng chảo Central Valley), Los Angeles (South Coast ven biển kẹt vách núi), và San Jose (Bay Area gió duyên hải).
>
> Quan sát biểu đồ tỷ lệ bản ghi theo 6 cấp độ EPA trên slide:
> * Hai cấp độ an toàn (Good và Moderate) chiếm tới **95.62%** toàn bộ dữ liệu.
> * Các cấp độ ô nhiễm nặng chỉ chiếm thiểu số: Unhealthy là **1.00%**, Very Unhealthy là **0.07%**, và Nguy hại (Hazardous) chỉ vỏn vẹn **0.01%**.
>
> Tại ma trận tương quan bên phải: Biến mục tiêu AQI tương quan gần như tuyệt đối với bụi mịn $\text{PM}_{2.5}$ ($r = 0.95$). Trong các yếu tố khí tượng, **tốc độ gió mặt đất có tương quan âm mạnh nhất ($r = -0.31$)**, chứng minh gió là cơ chế phát tán và pha loãng ô nhiễm chủ đạo.
>
> Về mặt toán học, phân phối AQI lệch phải với độ lệch Skewness $= +1.31$ (và $\text{PM}_{2.5}$ thô lệch tới $+4.82$). Nhóm đưa ra quyết định kỹ thuật: **Kiên quyết không sử dụng Log-Transform** vì hai lý do:
> 1. Các thuật toán dạng cây (Tree-based) vốn dĩ bất biến với phép biến đổi đơn điệu.
> 2. Theo **Bất đẳng thức Jensen**: $\mathbb{E}[\exp(\hat{y})] \ge \exp(\mathbb{E}[\hat{y}])$, việc dự báo trên thang log rồi mũ hóa ngược lại sẽ tạo độ chệch kỳ vọng hệ thống và nén phẳng mức phạt sai số tại vùng đuôi nồng độ cao ($AQI > 150$) — vùng tối quan trọng cần bảo vệ tính mạng người dân."*

* **Hành động & Ngôn ngữ cơ thể:** Nhìn sang Speaker 2, ra hiệu chuyển giao bài thuyết trình.
* **Lời chuyển ý (Transition):** *"Tiếp theo, xin mời Speaker 2 bước sang Phần 2 để trình bày về giao thức phân chia tuần tự và Feature Store vật lý khí quyển."*

---

## ⚙️ PART 2: FEATURE ENGINEERING & VISUALIZATION (KỸ NGHỆ ĐẶC TRƯNG & CHUẨN BỊ DỮ LIỆU)

---

### 📍 SLIDE 06: GIAO THỨC PHÂN CHIA TUẦN TỰ (ZERO-LEAKAGE) & KỸ THUẬT VÙNG ĐỆM BIÊN
*(Slide Title: Zero-Leakage Temporal Split Protocol & Buffer Defense — 8-Year Sequential Partitioning Preserving Historical Independence)*
* **Diễn giả:** Speaker 2 (Khối Feature Engineering & Visualization)
* **Thời lượng dự kiến:** 65 giây
* **Mục tiêu truyền tải:** Chứng minh tính đúng đắn của phân chia theo thời gian tuyệt đối (Temporal Split) không xáo trộn; làm rõ kỹ thuật cắt vùng đệm biên (Trim Tail Buffer $h$ dòng) nhằm triệt tiêu hoàn toàn rò rỉ ranh giới.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Kính thưa Thầy Cô, để triệt tiêu hoàn toàn khoảng trống rò rỉ dữ liệu (Lookahead Leakage), nhóm thiết lập **giao thức phân chia tuần tự theo thời gian tuyệt đối (Zero-Leakage Temporal Split)** trên toàn bộ 181,122 bản ghi 8 năm:
> * **Tập Train (2018–2023 · 111,073 dòng, chiếm 61.3%):** Dùng để học quy luật nền và bao quát các đợt đại hỏa hoạn lịch sử như Camp Fire 2018 và August Complex 2020.
> * **Tập Validation (2024 · 43,727 dòng, chiếm 24.1%):** Chứa trọn vẹn vụ cháy **Park Fire (tháng 7–8/2024)** — vụ cháy lớn thứ 4 lịch sử California; dùng làm bài kiểm tra áp lực thực tế để tinh chỉnh siêu tham số và kích hoạt Early Stopping (`patience=30`).
> * **Tập Test Độc lập (2025 · 26,292 dòng, chiếm 14.5%):** Hoàn toàn cô lập khỏi quá trình huấn luyện, chỉ mở ra đánh giá một lần duy nhất.
>
> Điểm cốt lõi trong kỹ thuật phân chia là **Cơ chế Cắt Vùng Đệm Biên (Trim Tail Buffer Defense)**: 
> Khi tạo nhãn tương lai bằng phép trượt thời gian $\text{shift}(-h)$, $h$ dòng cuối cùng của từng phân đoạn sẽ vô tình nhìn lấn sang điểm dữ liệu đầu tiên của tập kế tiếp. Nhóm cắt bỏ chính xác đúng $h$ dòng cuối cùng của từng trạm trên Train và Val (1 dòng cho bài toán 1h, 24 dòng cho bài toán 24h), bảo đảm sự cách ly vô trùng tuyệt đối giữa quá khứ và tương lai."*

* **Hành động & Ngôn ngữ cơ thể:** Chỉ tay vào 3 khối màu Train/Val/Test ở đáy slide và giải thích đường cắt đệm biên.
* **Lời chuyển ý (Transition):** *"Dựa trên dữ liệu vô trùng này, nhóm tiến hành xây dựng Feature Store với các biến vật lý khí quyển chuyên biệt."*

---

### 📍 SLIDE 07: KỸ NGHỆ ĐẶC TRƯNG VẬT LÝ KHÍ QUYỂN: VPD, VECTOR GIÓ $U, V$ & MA TRẬN ĐA CHÂN TRỜI
*(Slide Title: Physics-Informed Feature Store Architecture — Specialized Multi-Horizon Feature Spaces Coupling Surface Sensors with Mesoscale NWP)*
* **Diễn giả:** Speaker 2
* **Thời lượng dự kiến:** 65 giây
* **Mục tiêu truyền tải:** Làm rõ cấu trúc 2 không gian đặc trưng chuyên biệt; phân tích bản chất vật lý của chỉ số khô hạn VPD và phân rã vector gió Descartes $(u, v)$ Tây–Đông / Nam–Bắc.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Xuất phát từ bản chất cơ học của hai bài toán, nhóm xây dựng hai ma trận đặc trưng chuyên biệt trong Feature Store:
>
> Ở **Khung Nowcasting 1h ($X \in \mathbb{R}^{N \times 22}$)**:
> * Mô hình tận dụng tối đa quán tính tự hồi quy qua các biến trễ ngắn `lag_0` đến `lag_3` cùng thống kê cửa sổ trượt 3 giờ (`roll_mean_3h`, `roll_std_3h`).
> * Điểm nhấn là biến động lượng cột khói **`diff_1h` ($AQI_t - AQI_{t-1}$)** — đạo hàm bậc một phản ánh tốc độ bốc khói tức thời khi đám cháy vừa phát hỏa.
>
> Ở **Khung Day-Ahead 24h ($X \in \mathbb{R}^{N \times 19}$)**:
> * Toàn bộ cảm biến từ $t+1$ đến $t+24$ bị che giấu 100%. Mô hình chỉ giữ các mốc trễ nền chu kỳ dài: `lag_0`, `lag_24`, `lag_48` và `roll_mean_24h`.
> * Bù lại, hệ thống nạp vào trường vi khí hậu số trị dự báo $W_{t+24}$ gồm nhiệt độ, độ ẩm, lượng mưa và áp suất mặt đất.
>
> Hai cơ chế vật lý khí quyển cốt lõi được nhóm mã hóa:
> 1. **Phân rã Vector Gió Descartes ($u, v$):** Tốc độ và hướng gió cực được chiếu thành hai trục trực giao Tây–Đông ($u$) và Nam–Bắc ($v$), giải quyết triệt để sự gián đoạn tuần hoàn $359^\circ \leftrightarrow 1^\circ$ vốn đánh lừa các hàm hồi quy tuyến tính.
> 2. **Chỉ số Áp suất Hơi Thiếu hụt (Vapor Pressure Deficit - VPD):** Đo lường mức độ khô hạn khát nước của không khí, là chỉ báo vật lý trực tiếp về khả năng bắt lửa và bùng phát của thảm thực vật California."*

* **Hành động & Ngôn ngữ cơ thể:** Nhìn sang Speaker 3, ra hiệu chuyển tiếp phần thuyết trình.
* **Lời chuyển ý (Transition):** *"Tiếp theo, xin mời Speaker 3 bước vào Phần 3: Không gian mô hình hóa và kết quả đối chuẩn thực nghiệm."*

---

## 🔬 PART 3: MODELING, EVALUATION (MÔ HÌNH HÓA & ĐÁNH GIÁ ĐA CẤP ĐỘ)

---

### 📍 SLIDE 08: KHÔNG GIAN ĐỐI CHUẨN MÔ HÌNH: 5 HỌ THUẬT TOÁN & KỸ THUẬT MÃ NGUỒN
*(Slide Title: Benchmark Model Suite: 5 Algorithm Families — Standardized Modeling Pipeline from Analytical Baselines to Tabular Deep Learning)*
* **Diễn giả:** Speaker 3 (Khối Modeling & Leaderboard Evaluation)
* **Thời lượng dự kiến:** 70 giây
* **Mục tiêu truyền tải:** Giới thiệu 5 họ thuật toán đối chuẩn (8 mô hình nền tảng + 1 Voting Ensemble); làm rõ hai kỹ thuật triển khai code then chốt về Scaling dị biệt và Encoding biến phân loại trạm.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Kính thưa Hội đồng, không gian đối chuẩn của nhóm bao quát 5 họ thuật toán đại diện, từ mô hình giải tích cơ sở đến học sâu bảng:
> 1. **Họ Baselines:** Gồm **Persistence** ($y_{t+h} = y_t$) làm mốc quán tính, và **Climatology** (kỳ vọng lịch sử theo trạm, tháng và giờ trên tập Train) làm mốc phân phối tĩnh.
> 2. **Họ Tuyến tính Điều chuẩn:** **Ridge Regression** với phạt $L_2$, có nghiệm ma trận đóng giải tích, thời gian khớp chỉ ~0.18 giây.
> 3. **Họ Bagging Trees:** **Random Forest** gồm 150 cây quyết định, giảm phương sai qua cơ chế lấy mẫu ngẫu nhiên.
> 4. **Họ Gradient Boosting SOTA:** Bộ ba thuật toán cây mạnh nhất hiện nay: **LightGBM** (phát triển theo lá leaf-wise), **XGBoost** (phân nhánh tối ưu theo Hessian bậc hai), và **CatBoost** (cấu trúc cây đối xứng oblivious trees).
> 5. **Họ Mạng Nơ-ron:** **Tabular MLP Regressor** gồm 2 tầng ẩn (64, 32 units), kích hoạt ReLU, tối ưu bằng Adam kết hợp Early Stopping.
> 6. **Meta-Ensemble:** **Top-3 GBDT Voting Ensemble** lấy trung bình cộng không trọng số giữa LightGBM, XGBoost và CatBoost để triệt tiêu sai số cục bộ độc lập.
>
> Hai khâu xử lý kỹ thuật dị biệt trong mã nguồn:
> * **Chuẩn hóa dị biệt (Scaling):** Nhóm cây (GBDT, RF) nhận trực tiếp dữ liệu thô vì điều kiện phân nhánh $x_j \le \theta$ bất biến với co giãn. Ngược lại, Ridge và MLP bắt buộc dùng `StandardScaler` và **chỉ gọi `fit` duy nhất trên tập Train**, sau đó mới `transform` cho Val và Test để chống rò rỉ.
> * **Mã hóa không gian trạm:** Ridge và MLP dùng **One-Hot Encoding** để tránh gán thứ tự khoảng cách sai lệch; trong khi GBDT sử dụng **Native Categorical** để thuật toán histogram tự động gom cụm gradient tối ưu theo trạm."*

* **Hành động & Ngôn ngữ cơ thể:** Nhấn mạnh vào hộp xanh Voting Ensemble và hai hộp kỹ thuật ở chân slide.
* **Lời chuyển ý (Transition):** *"Sau đây là bảng kết quả đối chuẩn thực nghiệm Leaderboard chính thức trên 26,200 bản ghi của tập Test độc lập năm 2025."*

---

### 📍 SLIDE 09: BẢNG KẾT QUẢ LEADERBOARD: ĐỐI CHUẨN ĐA MÔ HÌNH TRÊN TEST 2025 (TABLE)
*(Slide Title: Official Leaderboard: Test 2025 Out-of-Sample Evaluation — Comparative Performance on 26,200 Unseen Points (comprehensive_leaderboard.csv))*
* **Diễn giả:** Speaker 3
* **Thời lượng dự kiến:** 70 giây
* **Mục tiêu truyền tải:** Phân tích Bảng số liệu Leaderboard chính thức từ `comprehensive_leaderboard.csv`; chứng minh sự áp đảo toàn diện của Voting Ensemble; so sánh hiệu năng và chi phí tính toán giữa GBDT và MLP.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Bảng trên màn hình công bố kết quả thực nghiệm chính thức từ file `comprehensive_leaderboard.csv` trên 26,200 điểm dữ liệu chưa từng nhìn thấy của tập Test 2025:
>
> **Tại Chân trời 1h Nowcasting ($t+1$):**
> * **Voting Ensemble dẫn đầu toàn diện** với **$\text{MAE} = 3.06\text{ AQI}$**, hệ số **$R^2 = 0.956$**.
> * Mô hình cải thiện vượt bậc, giảm tới **82.5% sai số** so với mốc Climatology ($\text{MAE} = 17.53$), và giảm 15.2% so với Persistence ($\text{MAE} = 3.61$).
> * Bộ ba GBDT bám đuổi rất sít sao: XGBoost đạt $\text{MAE} = 3.10$, LightGBM đạt $3.13$, CatBoost đạt $3.13$. Tabular MLP đạt kết quả khả quan với $\text{MAE} = 3.26, R^2 = 0.958$.
>
> **Tại Chân trời 24h Day-Ahead ($t+24$):**
> * Khi quán tính cảm biến mặt đất bị cắt đứt hoàn toàn, **Voting Ensemble tiếp tục giữ vững vị trí số 1** với **$\text{MAE} = 11.30\text{ AQI}$**, hệ số **$R^2 = 0.617$**.
> * Kết quả này vượt trội hoàn toàn so với Persistence ($\text{MAE} = 13.02, R^2 = 0.460$) và Climatology ($\text{MAE} = 17.45, R^2 = 0.155$).
> * Đáng chú ý: Bộ ba GBDT giữ vững phong độ ổn định với LightGBM $11.33$, XGBoost $11.36$, CatBoost $11.40$.
>
> **Nghịch lý chi phí tính toán ở cột cuối cùng:**
> * LightGBM chỉ mất **0.41 giây** để huấn luyện ở kịch bản 24h.
> * Trong khi đó, Tabular MLP mất tới **81.62 giây** — chậm hơn gần **200 lần** — mà hiệu năng lại kém hơn hẳn ($\text{MAE} = 13.08$, thua kém $1.78\text{ AQI}$). Kết quả này khẳng định ưu thế tuyệt đối của thuật toán cây trên dữ liệu bảng."*

* **Hành động & Ngôn ngữ cơ thể:** Hướng tay vào dòng bôi xanh Voting Ensemble ở đáy bảng, sau đó lia sang cột Fit time (24h) để chỉ ra con số 81.62s vs 0.41s.
* **Lời chuyển ý (Transition):** *"Để thấy rõ hơn thứ bậc xếp hạng giữa các mô hình, xin mời Hội đồng quan sát trực quan trên hai biểu đồ thanh ngang tại Slide 10."*

---

### 📍 SLIDE 10: BIỂU ĐỒ XẾP HẠNG LEADERBOARD TRỰC QUAN: 1H VS 24H (CHARTS)
*(Slide Title: Official Leaderboard: Test 2025 Out-of-Sample Evaluation — Comparative Performance on 26,200 Unseen Points (comprehensive_leaderboard.csv))*
* **Diễn giả:** Speaker 3
* **Thời lượng dự kiến:** 70 giây
* **Mục tiêu truyền tải:** Phân tích trực quan hai biểu đồ so sánh MAE và $R^2$; giải thích sự phân nhóm thuật toán theo màu sắc; lý giải sự tụt dốc của MLP và sự bền bỉ của Ridge ở chân trời 24h.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Quan sát trực quan trên hai biểu đồ thanh ngang: Cột càng ngắn thì sai số MAE càng thấp, mô hình càng tốt:
>
> **Ở biểu đồ bên trái — Kịch bản 1H Nowcasting:**
> * Cột màu xanh lá cây — **Voting Ensemble dẫn đầu ở mức 3.06 AQI**.
> * Cụm cột màu xanh dương — **Bộ ba GBDT (XGBoost 3.10, LightGBM 3.13, CatBoost 3.13)** kết thành khối tinh hoa dẫn đầu, đều đạt hệ số giải thích $R^2 = 0.954$.
> * Cột màu tím — **Tabular MLP (3.26)** bám sát phía sau nhờ khai thác tốt tương quan tuyến tính ngắn hạn của cảm biến mặt đất.
>
> **Tuy nhiên, bước sang biểu đồ bên phải — Kịch bản 24H Day-Ahead:**
> * Bản chất bài toán thay đổi sâu sắc: Voting Ensemble (11.30) và cụm GBDT (11.33 đến 11.40) vẫn kiên cường giữ vững nhóm đầu bảng với $R^2 \approx 0.617$.
> * **Sự tụt dốc của Deep Learning MLP:** Cột màu tím MLP tụt dốc xuống đáy bảng ở mức **$\text{MAE} = 13.08$**, hệ số $R^2$ sụt giảm nghiêm trọng xuống **$0.501$** — thậm chí thua cả mô hình tuyến tính đơn giản Ridge Regression ($\text{MAE} = 11.86, R^2 = 0.586$) và suýt soát bằng mốc Persistence ($13.02$).
> * Điều này cho thấy khi dữ liệu bảng thiếu vắng các biến quán tính mạnh, các hàm kích hoạt liên tục của MLP dễ bị lạc lối trong không gian nhiễu của vi khí hậu, trong khi các ngưỡng phân nhánh trực giao của GBDT lọc nhiễu hiệu quả hơn nhiều."*

* **Hành động & Ngôn ngữ cơ thể:** Nhìn sang Speaker 4, ra hiệu tiếp quản nửa sau của Part 3 và Part 4.
* **Lời chuyển ý (Transition):** *"Tiếp theo, xin mời Speaker 4 bước vào phần phân tích động lực bám chuỗi 168 giờ, kiểm tra sức bền trước cú sốc bão khói cực đoan, chẩn đoán sai số 3 chiều và tổng kết đề tài."*

---

## 🔬 PART 3 (TIẾP TỤC) & PART 4: EVALUATION & CONCLUSION

---

### 📍 SLIDE 11: ĐỘNG LỰC CHUỖI THỜI GIAN: KHẢ NĂNG BÁM CHUỖI 168H LIÊN TỤC & DẢI THẶNG DƯ (FIG 02)
*(Slide Title: 168-Hour Continuous Tracking & Residual Dynamics — January 09–15, 2025 at Fresno Central Valley Inversion Basin)*
* **Diễn giả:** Speaker 4 (Khối Extreme Evaluation, Diagnostics & Conclusion)
* **Thời lượng dự kiến:** 65 giây
* **Mục tiêu truyền tải:** Phân tích biểu đồ chuỗi thời gian 168 giờ liên tục (09/01 - 15/01/2025 tại Fresno); minh chứng trực quan khả năng bám đỉnh ô nhiễm 73.4 AQI của Voting Ensemble (đạt 72.1 AQI) và dải thặng dư phẳng lặng so với Ridge.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Kính thưa Hội đồng, để thẩm định hành vi động học của mô hình trên chuỗi thời gian thực tế, xin mời Thầy Cô quan sát **Lát cắt chuỗi thời gian 168 giờ liên tục (từ ngày 09 đến 15 tháng 01 năm 2025 tại lưu vực Fresno)**:
>
> Biểu đồ đối sánh đường đo thực tế mặt đất của US EPA (đường màu đen đậm) với đường dự báo của Voting Ensemble (đường màu xanh lá), LightGBM (đường đứt đoạn xanh dương) và Ridge Regression (đường chấm vàng):
> * **Ở điều kiện nền bình thường (20–50 AQI):** Cả Voting Ensemble và LightGBM đều bám sát thực tế một cách mượt mà. Dải sai số thặng dư tuyệt đối (*Residual Margin* — vùng màu xanh ngọc nhạt phía trên) duy trì phẳng lặng dưới **$5\text{ đơn vị AQI}$**.
> * **Tại đỉnh ô nhiễm mùa đông rạng sáng ngày 11/01:** Do ảnh hưởng của nắp nghịch nhiệt, nồng độ thực tế vọt lên đỉnh nhọn **73.4 AQI**. Mô hình Ridge Regression bị trôi dạt về giá trị trung bình do tính chất phẳng tuyến tính. Ngược lại, **Voting Ensemble phản ứng cực kỳ nhạy bén, bám sát đỉnh lên mức 72.1 AQI** — độ lệch đỉnh chỉ vỏn vẹn **$1.3\text{ đơn vị AQI}$**!
> * Sự kết hợp của Top-3 GBDT trong Voting Ensemble đã triệt tiêu hiệu quả các dao động ký sinh cục bộ, mang lại đường dự báo mượt mà và tin cậy cao cho tác nghiệp."*

* **Hành động & Ngôn ngữ cơ thể:** Chỉ tay vào hộp chú thích màu đỏ trên đỉnh nhọn ngày 11/01: *"Đỉnh ô nhiễm: 73.4 AQI (Ensemble: 72.1)"*.
* **Lời chuyển ý (Transition):** *"Bên cạnh các đỉnh ô nhiễm mùa đông, câu hỏi cốt lõi là: Hệ thống phản ứng thế nào trước các cú sốc bão khói cháy rừng cực đoan?"*

---

### 📍 SLIDE 12: ĐÁNH GIÁ ĐỘ BỀN BỈ TRƯỚC CÚ SỐC KHÓI CHÁY RỪNG CỰC ĐOAN (24H DAY-AHEAD)
*(Slide Title: Wildfire Extreme Shock Resilience (24h Day-Ahead) — Quantifying the Extreme Shock Gap and Resolving Variance Restriction Artifacts)*
* **Diễn giả:** Speaker 4
* **Thời lượng dự kiến:** 70 giây
* **Mục tiêu truyền tải:** Phân tích biểu đồ so sánh sai số Ngày Bình Thường vs Đợt Bão Khói Cực Đoan; định lượng khoảng chênh lệch sai số $+\Delta 52.7\text{ AQI}$; giải thích hiện tượng sụp đổ phương sai mẫu của $R^2$ và giải pháp bổ sung F1-Score (0.825).

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Quan sát biểu đồ đo lường **Độ bền bỉ sai số trước cú sốc khói cháy rừng trên kịch bản 24h Day-Ahead**:
> * Cột màu xanh dương thể hiện sai số trong **Ngày bình thường ($AQI \le 100$)**: Voting Ensemble đạt mức sai số rất thấp là **$9.9\text{ AQI}$**.
> * Nhưng khi bão khói cực đoan bùng phát — cột màu đỏ **($AQI > 150$)**: Sai số trung bình tăng vọt lên **$62.6\text{ AQI}$**, vượt qua đường ngưỡng cảnh báo y tế 50 AQI (đường chấm đỏ), tạo ra một khoảng chênh lệch sai số cực đoan là **$+\Delta 52.7\text{ AQI}$**. 
> * Khoảng chênh này phản ánh bản chất ngẫu nhiên của các đợt phát hỏa mới: Khói từ các đám cháy cách xa hàng trăm dặm có thể ập đến bất ngờ ngoài tầm với của các biến trễ mặt đất.
>
> Đồng thời, nhóm ghi nhận một hiện tượng toán học quan trọng: **Hiện tượng Sụp đổ Phương sai Mẫu (Variance Restriction Artifact)**. Khi cô lập tập con $AQI > 150$, miền giá trị bị co hẹp làm tổng phương sai mẫu số $\text{SS}_{\text{tot}}$ sụt giảm rất nhanh, khiến hệ số $R^2$ bị âm dù mô hình vẫn dự báo đúng xu hướng đi lên của nồng độ.
>
> Vì vậy, nhóm đã bổ sung thước đo phân loại **F1-Score tại ngưỡng khẩn cấp 150+**; mô hình đạt **F1-Score = 0.825 ở kịch bản 1h**, khẳng định khả năng phát chuông cảnh báo sớm bão khói vẫn hoạt động rất vững vàng."*

* **Hành động & Ngôn ngữ cơ thể:** Tay chỉ vào khoảng cách giữa cột xanh 9.9 và cột đỏ 62.6, nhấn mạnh con số $+\Delta 52.7$.
* **Lời chuyển ý (Transition):** *"Để tìm hiểu gốc rễ nguyên nhân gây ra các sai số này, xin mời Hội đồng đến với bức tranh chẩn đoán sai số 3 chiều."*

---

### 📍 SLIDE 13: CHẨN ĐOÁN CƠ CHẾ SAI SỐ 3 CHIỀU: PARITY HEXBIN, NGHỊCH NHIỆT ĐÊM & ĐỊA MẠO
*(Slide Title: Three-Dimensional Error Diagnostics & Topography — Empirical Diagnostics Across Tail Shrinkage, Nocturnal Inversion, and Basin Geomorphology)*
* **Diễn giả:** Speaker 4
* **Thời lượng dự kiến:** 75 giây
* **Mục tiêu truyền tải:** Phân tích 3 chiều chẩn đoán sai số thực nghiệm: Hiện tượng co cụm phương sai đuôi ($\beta = 0.54\text{--}0.56$), nghịch nhiệt bức xạ ban đêm (22h–4h sáng), và sự phân hóa địa mạo giữa 3 lưu vực không khí.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Nhóm đã thực hiện chẩn đoán cơ chế sai số chuyên sâu qua 3 chiều thực nghiệm hiển thị trên slide:
>
> **Chiều thứ nhất — Co cụm Phương sai Đuôi (Tail Shrinkage, $\beta = 0.54$):**
> * Quan sát biểu đồ mật độ Parity Plot: Mật độ điểm tập trung dày đặc quanh đường chuẩn 1:1 ($y = x$) ở dải nồng độ an toàn ($AQI \le 100$).
> * Tuy nhiên, đường hồi quy thực tế có hệ số góc chỉ đạt **$\beta = 0.54$ đến $0.56$** ($< 1.0$). Đây là bằng chứng của hiện tượng co cụm đuôi: Do hàm mất mát MAE đối xứng chia đều hình phạt trên toàn bộ phân phối, mô hình có xu hướng dự báo an toàn, co cụm về phía trung bình và đánh giá thấp độ cao của các đỉnh bão khói cực đoan.
>
> **Chiều thứ hai — Nghịch nhiệt Bức xạ Ban đêm (Nocturnal Radiation Inversion):**
> * Biểu đồ chu kỳ sai số theo giờ trong ngày cho thấy: Sai số MAE giảm sâu xuống chỉ **~8 AQI vào giữa trưa (11h–15h)**, nhưng tăng vọt lên **vượt 14 AQI vào ban đêm và rạng sáng (từ 22h đến 4h sáng)**.
> * Nguyên nhân vật lý: Ban đêm, bề mặt đất bức xạ nhiệt làm nguội lớp không khí sát đất nhanh hơn lớp bên trên, tạo thành một chiếc nắp nghịch nhiệt giam cầm toàn bộ khói bụi trong một tầng biên nông sát mặt đất.
>
> **Chiều thứ ba — Phân hóa Địa mạo 3 Lưu vực Khí quyển:**
> * **Bay Area (San Jose):** Đạt kết quả xuất sắc nhất (**$\text{MAE} = 9.90$**, $0$ đợt cực đoan) nhờ gió biển Thái Bình Dương thông thoáng.
> * **Central Valley (Fresno):** Đạt **$\text{MAE} = 10.95$**, hứng chịu $88$ đợt cực đoan do địa hình lòng chảo bẫy bụi mùa đông.
> * **South Coast (Los Angeles):** Đạt **$\text{MAE} = 13.06$**, hứng chịu tới **$231$ đợt cực đoan** (sai số cực đoan lên tới $66.83\text{ AQI}$) do bức tường núi San Gabriel chặn đứng đường thoát gió kết hợp hiệu ứng đảo nhiệt đô thị."*

* **Hành động & Ngôn ngữ cơ thể:** Lần lượt chỉ vào 3 thẻ tóm tắt màu sắc ở chân slide để gắn liền toán học với địa lý thực tế.
* **Lời chuyển ý (Transition):** *"Sau đây, chúng ta cùng bước vào Phần 4: Tổng kết thực nghiệm, giới hạn kỹ thuật và lộ trình chuyển giao sang Milestone 3."*

---

## 🎯 PART 4: CONCLUSION & ROADMAP (KẾT LUẬN & LỘ TRÌNH)

---

### 📍 SLIDE 14: TỔNG KẾT THỰC NGHIỆM, GIỚI HẠN, LỘ TRÌNH CHUYỂN GIAO MILESTONE 3 & Q&A
*(Slide Title: Experimental Conclusions & Production Roadmap — Milestone 2 Wrap-up, Technical Limitations & Final Defense Deliverables)*
* **Diễn giả:** Speaker 4 (Khối Conclusion & Roadmap)
* **Thời lượng dự kiến:** 60 giây
* **Mục tiêu truyền tải:** Tóm lược 4 kết quả thực nghiệm cốt lõi; thẳng thắn nhìn nhận 3 giới hạn kỹ thuật; công bố lộ trình MLOps chuyển giao Milestone 3 (Asymmetric Loss, Containerized FastAPI, Early Warning Dashboard); gửi lời cảm ơn và mở đầu phiên hỏi đáp học thuật.

#### 🎙️ LỜI THOẠI DIỄN THUYẾT:
> *"Kính thưa Thầy Cô và Hội đồng, tổng kết lại Milestone 2, đề tài đã xác lập **4 phát hiện thực nghiệm cốt lõi**:
> 1. Thiết lập thành công quy trình phân chia tuần tự chống rò rỉ trên 181 nghìn dòng dữ liệu 8 năm với vùng đệm biên vô trùng.
> 2. Xác lập **Voting Ensemble dẫn đầu toàn diện**: đạt $\text{MAE} = 3.06$ ở 1h và $\text{MAE} = 11.30$ ở 24h.
> 3. Chứng minh thuật toán cây GBDT áp đảo hoàn toàn Deep Learning MLP cả về độ chính xác (tốt hơn $1.78\text{ AQI}$) lẫn tốc độ huấn luyện (nhanh hơn 200 lần: $0.41\text{s}$ vs $81.62\text{s}$).
> 4. Bóc tách thành công cơ chế vật lý của sai số gắn liền với nghịch nhiệt đêm và hiện tượng co cụm phương sai đuôi ($\beta = 0.54$).
>
> Đồng thời, nhóm thẳng thắn nhận diện **3 giới hạn kỹ thuật tồn đọng**:
> * Dự báo đỉnh khói cực đoan còn thấp do hàm mất mát đối xứng chưa phạt nặng vùng đuôi ($62.6\text{ MAE}$).
> * Cảm biến mặt đất có điểm mù chiều đứng, chưa tích hợp độ dày quang học AOD từ vệ tinh để đo cột khói.
> * Mô hình dữ liệu bảng hiện tại chưa học được tương quan chú ý không gian liên lưu vực (Cross-Basin Attention).
>
> **Lộ trình hành động chuẩn bị cho Milestone 3 (Final Defense):**
> * **Về Thuật toán:** Triển khai hàm mất mát bất đối xứng **Asymmetric Huber Loss / Pinball Loss** để kéo hệ số góc $\beta$ tiệm cận $1.0$ tại vùng đỉnh thiên tai.
> * **Về MLOps:** Đóng gói toàn bộ pipeline thành **REST API (FastAPI) bằng Docker Container**, đảm bảo độ trễ phản hồi dưới $50\text{ms}$.
> * **Về Ứng dụng:** Xây dựng **Dashboard tương tác cảnh báo chất lượng không khí California** phục vụ cộng đồng theo thời gian thực.
>
> Nhóm 5 xin chân thành cảm ơn Quý Thầy Cô và Hội đồng đã chú ý lắng nghe! Nhóm rất mong nhận được những góp ý quý báu và sẵn sàng tiếp nhận các câu hỏi phản biện."*

* **Hành động & Ngôn ngữ cơ thể:** Cả nhóm 4 thành viên cùng đứng nghiêm túc, cúi đầu chào Hội đồng trang trọng và sẵn sàng bước vào phiên Q&A.

---

# PHẦN B: CẨM NANG PHẢN BIỆN HỌC THUẬT CHUYÊN SÂU (Q&A DEFENSE GUIDE)

---

### ❓ CÂU HỎI 1: VỀ VẤN ĐỀ RÒ RỈ DỮ LIỆU TƯƠNG LAI (LOOKAHEAD LEAKAGE TRÊN SLIDE 04 & 07)
> **Giảng viên hỏi:** *"Trong bài toán 24 giờ ($t+24$), nhóm sử dụng các biến như `future_wind_speed`, `future_temp_2m`, `future_rain`. Tại sao việc lấy thông tin thời tiết tại thời điểm $t+24$ không bị coi là rò rỉ dữ liệu tương lai?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Bản chất khí tượng tác nghiệp:** Hoàn toàn tuân thủ tính nhân quả thực tế. Trong quy trình vận hành tại các cơ quan như NOAA, US EPA hay California Air Resources Board (CARB), các biến thời tiết tại $t+24$ là **đầu ra của các mô hình dự báo thời tiết số trị (Numerical Weather Prediction - NWP)** như HRRR (độ phân giải 3km cập nhật hàng giờ) hoặc ECMWF/GFS. Các dự báo thời tiết này được tính toán và công bố trước thời điểm $t+24$ nhiều giờ.
* **Nguồn dữ liệu đối ứng:** Dữ liệu Open-Meteo mà nhóm trích xuất cho mốc $t+24$ chính là các trường thời tiết dự báo số trị đó.
* **Bảo toàn vô trùng cảm biến:** Nhóm **che giấu 100% dữ liệu cảm biến mặt đất** (`target_aqi`, `pm25`, `pm10`) từ $t+1$ đến $t+24$. Sự sụt giảm của $R^2$ từ $0.956$ xuống $0.617$ chứng minh mô hình không hề nhận được bất kỳ tín hiệu tương lai nào của biến mục tiêu, mà hoàn toàn phải suy luận dựa trên trường động lực khí tượng.

---

### ❓ CÂU HỎI 2: VỀ HIỆN TƯỢNG SỤP ĐỔ PHƯƠNG SAI VÀ $R^2$ ÂM TRÊN SỰ KIỆN CỰC ĐOAN (SLIDE 12)
> **Giảng viên hỏi:** *"Tại sao khi đánh giá riêng trên tập các sự kiện cháy rừng ($AQI > 150$), hệ số $R^2$ của một số mô hình sụt giảm rất mạnh hoặc thậm chí bị âm?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Bản chất toán học:** Đây là **hiệu ứng sụp đổ phương sai mẫu (Variance Restriction Artifact)** do việc cắt ngưỡng nhân tạo, không phản ánh việc mô hình mất kiểm soát.
* **Công thức toán học chứng minh:**
  $$R^2 = 1 - \frac{\sum_{i \in \text{Extreme}} (y_i - \hat{y}_i)^2}{\sum_{i \in \text{Extreme}} (y_i - \bar{y}_{\text{Extreme}})^2} = 1 - \frac{\text{SS}_{\text{res}}}{\text{SS}_{\text{tot}}}$$
  Khi cô lập tập con $AQI > 150$, miền giá trị bị thu hẹp lại, làm tổng phương sai mẫu số $\text{SS}_{\text{tot}}$ giảm rất nhanh. Khi mẫu số nhỏ, chỉ cần một sai số dư $\text{SS}_{\text{res}}$ vừa phải cũng khiến tỷ số vượt quá 1, dẫn đến $R^2 < 0$.
* **Biện pháp đối chứng:** Nhận diện khiếm khuyết toán học này của $R^2$, nhóm đã bổ sung thước đo **F1-Score phân loại tại ngưỡng cảnh báo 150+**. Mô hình Top GBDT đạt F1-Score ngưỡng 150 là **0.825 ở kịch bản 1h**, chứng minh mô hình vẫn bắt trúng phần lớn các đợt bão khói thực tế.

---

### ❓ CÂU HỎI 3: TẠI SAO TABULAR MLP LẠI THUA GBDT TRÊN BÀI TOÁN DỮ LIỆU BẢNG NÀY? (SLIDE 09 & 10)
> **Giảng viên hỏi:** *"Mạng Nơ-ron MLP là bộ xấp xỉ hàm vạn năng (Universal Approximator). Tại sao ở kịch bản 24h, MLP lại đạt kết quả kém ($\text{MAE} = 13.08, R^2 = 0.501$), thua xa LightGBM ($\text{MAE} = 11.33, R^2 = 0.617$) và chạy chậm hơn 200 lần?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Nhất quán với y văn SOTA:** Kết quả này hoàn toàn trùng khớp với các công trình thực nghiệm quy mô lớn gần đây về dữ liệu bảng (tiêu biểu như Grinsztajn et al., NeurIPS 2022: *'Why do tree-based models still outperform deep learning on tabular data?'*).
* **Đặc tính Thiên kiến Quy nạp (Inductive Bias):** Hàm kích hoạt ReLU của MLP tạo ra các mặt quyết định trơn láng liên tục. Trong khi đó, nồng độ khói cháy rừng thường có các bước nhảy gián đoạn đột ngột theo thời gian. Các phép chia nhị phân trực giao của cây quyết định nắm bắt các bước nhảy này tốt hơn nhiều.
* **Cơ chế chọn lọc thuộc tính:** Cây quyết định tự động chọn lọc biến quan trọng tại từng nút chia, trong khi MLP gán trọng số kết nối cho toàn bộ ma trận đầu vào, khiến gradient dễ bị nhiễu bởi các biến khí tượng có tương quan yếu.
* **Thời gian huấn luyện:** MLP cần $81.62\text{s}$ để huấn luyện ở kịch bản 24h, trong khi LightGBM chỉ mất $0.41\text{s}$ (nhanh hơn gấp 199 lần).

---

### ❓ CÂU HỎI 4: VỀ ĐỘ TRỄ PHA (PHASE LAG) KHI BÙNG PHÁT KHÓI ĐỘT NGỘT (SLIDE 11)
> **Giảng viên hỏi:** *"Khi nồng độ khói tăng vọt đột ngột từ 30 lên 300 AQI trong vài giờ, mô hình có bị trễ pha chạy theo sau thực tế một bước thời gian hay không?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Bản chất kỹ thuật:** Trễ pha nhẹ (1 bước) là thách thức kinh điển của các mô hình hồi quy trễ khi gặp các cú sốc ngoại sinh không báo trước.
* **Giải pháp khắc phục của nhóm:**
  * Ở bài toán 1h: Nhóm tạo biến vi sai đạo hàm bậc một `diff_1h` ($AQI_t - AQI_{t-1}$). Khi nồng độ khói vừa chớm tăng ở giờ hiện tại, biến tốc độ biến thiên này lập tức kích hoạt dự báo tăng tốc ở bước tiếp theo mà không đợi chuỗi trễ bão hòa.
  * Ở bài toán 24h: Mô hình dựa vào vector gió tương lai `future_wind_u`, `v` và `future_wind_speed`. Khi hướng gió đổi chiều thổi từ vùng cháy về phía trạm quan trắc, mô hình nâng mức dự báo AQI dựa trên điều kiện khí quyển trước khi khói thực sự chạm đất.

---

### ❓ CÂU HỎI 5: TẠI SAO RIDGE REGRESSION THẤT BẠI Ở ĐỈNH CỰC ĐOAN DÙ CÓ NGHIỆM GIẢI TÍCH? (SLIDE 10 & 11)
> **Giảng viên hỏi:** *"Ridge Regression có nghiệm ma trận giải tích đóng và bài toán lồi tối ưu toàn cục. Tại sao mô hình này lại bị trôi dạt ở đỉnh ô nhiễm rạng sáng ngày 11/01 trên Slide 11?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Giới hạn siêu phẳng tuyến tính:** Nghiệm tối ưu của Ridge là tối ưu trên siêu phẳng tuyến tính phẳng, trong khi động lực học khí quyển có tính phi tuyến và tương tác bậc cao (ví dụ: gió mạnh khi hanh khô sẽ thổi bùng khói, nhưng gió mạnh khi có mưa lại dập tắt bụi — đây là tương tác phi tuyến dạng nhân $x_{\text{wind}} \times x_{\text{rain}}$ mà hàm cộng tính tuyến tính không biểu diễn được).
* **Tác động của hình phạt $L_2$:** Hình phạt $\lambda \sum w_i^2$ co các trọng số về gần 0 để chống đa cộng tuyến, vô tình triệt tiêu khả năng duy trì các hệ số góc lớn cần thiết để tạo ra dự báo đột biến vượt ngưỡng cao. GBDT với cấu trúc cây phân nhánh tự do nắm bắt được các tương tác phi tuyến này mà không bị giới hạn bởi siêu phẳng.

---

### ❓ CÂU HỎI 6: TẠI SAO KHÔNG DÙNG LOG-TRANSFORM KHI SKEWNESS LÊN TỚI +4.82? (SLIDE 05)
> **Giảng viên hỏi:** *"Trong học máy truyền thống, khi dữ liệu lệch phải mạnh (+4.82), việc lấy Log-Transform là bước bắt buộc để đưa phân phối về chuẩn. Tại sao nhóm lại từ chối thực hiện?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Tính bất biến của thuật toán dạng cây:** Hầu hết mô hình dẫn đầu trong nghiên cứu là Tree-based (GBDT, Random Forest). Thuật toán phân nhánh của cây chỉ dựa trên thứ tự xếp hạng (rank order) của các giá trị $x_j \le \theta$, nên bất kỳ phép biến đổi đơn điệu nào như $\log(y)$ cũng hoàn toàn không thay đổi điểm chia nhánh tối ưu.
* **Bất đẳng thức Jensen và Độ chệch tái tạo (Jensen's Inequality Bias):** Nếu huấn luyện mô hình dự báo biến $\ln(y)$, khi dự báo thực tế ta phải lấy hàm mũ ngược lại $\hat{y} = \exp(\widehat{\ln y})$. Theo bất đẳng thức Jensen: $\mathbb{E}[\exp(Z)] \ge \exp(\mathbb{E}[Z])$, phép biến đổi ngược sẽ tạo ra một độ chệch có hệ thống, làm mô hình đánh giá thấp nồng độ thực tế.
* **Méo mó hàm mục tiêu y tế:** Khi nén thang đo bằng hàm log, khoảng cách giữa 300 và 400 AQI chỉ là $\ln(400) - \ln(300) \approx 0.287$, tương đương khoảng cách giữa 10 và 13 AQI ($\ln(13) - \ln(10) \approx 0.262$). Điều này khiến hàm mất mát phạt sai số ở vùng thiên tai nguy hiểm chết người nhẹ ngang với sai số ở vùng không khí sạch, đi ngược lại tôn chỉ bảo vệ sức khỏe cộng đồng của đề tài.

---

### ❓ CÂU HỎI 7: TẠI SAO LẠI CHỌN PATIENCE = 30 VÒNG CHO EARLY STOPPING TRÊN TẬP VAL 2024? (SLIDE 06)
> **Giảng viên hỏi:** *"Tại sao nhóm lại thiết lập Early Stopping với `patience=30` trên tập Validation 2024? Nếu chọn patience quá nhỏ hoặc quá lớn thì hậu quả là gì?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Đặc thù của tập Validation 2024:** Tập Validation chứa vụ cháy Park Fire lịch sử (tháng 7–8/2024), có nhiều cú sốc khói đột biến kéo dài hàng chục giờ.
* **Nếu Patience quá nhỏ (ví dụ 5–10 vòng):** Mô hình có nguy cơ dừng non (Premature Stopping) ngay khi vừa chạm vào giai đoạn đầu của đợt khói biến động, làm mô hình chưa kịp học xong các tương tác phức tạp của trường gió và nhiệt độ.
* **Nếu Patience quá lớn (ví dụ 100 vòng) hoặc không dừng sớm:** Mô hình sẽ tiếp tục tối ưu hóa hàm mất mát bằng cách học vẹt (overfit) vào các dị biệt vi khí hậu riêng lẻ của mùa hè năm 2024, làm suy giảm khả năng tổng quát hóa khi bước sang tập Test 2025.
* **Con số 30 vòng:** Đủ lớn để thuật toán vượt qua các dao động cục bộ của đợt cháy Park Fire, nhưng đủ chặt để đóng băng trọng số tại điểm cân bằng tối ưu toàn cục.

---

### ❓ CÂU HỎI 8: PHƯƠNG ÁN XỬ LÝ KHI CẢM BIẾN EPA HOẶC API OPEN-METEO GẶP SỰ CỐ MẤT KẾT NỐI (GRACEFUL DEGRADATION)?
> **Giảng viên hỏi:** *"Trong môi trường vận hành thực tế, nếu API thời tiết hoặc trạm quan trắc mặt đất bị mất kết nối mạng vài giờ, hệ thống sẽ xử lý thế nào để không bị sập pipeline?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Mất kết nối cảm biến mặt đất ngắn hạn ($\le 3\text{h}$):** Hệ thống kích hoạt cơ chế *Forward Fill* (giữ nguyên nồng độ gần nhất) kết hợp với tốc độ suy giảm theo thời gian dựa trên biến chu kỳ ngày đêm.
* **Mất kết nối cảm biến mặt đất dài hạn ($> 3\text{h}$):** Hệ thống tự động chuyển sang chế độ dự phòng bằng **Nội suy không gian nghịch đảo khoảng cách (IDW - Inverse Distance Weighting)** từ 2 trạm quan trắc còn lại trong bang California.
* **Mất kết nối API Open-Meteo:** Hệ thống có đường ống dự phòng tự động chuyển request sang nguồn thứ cấp (NOAA GFS API công khai).
* **Khả năng tự phục hồi của mô hình cây:** Các mô hình GBDT (đặc biệt là LightGBM và XGBoost) có cơ chế bản địa xử lý dữ liệu khuyết (*native missing value handling*): nếu một đặc trưng bị khuyết, cây sẽ tự động gán mẫu dữ liệu vào nhánh mặc định (*default split direction*) đã được tối ưu hóa trong quá trình huấn luyện mà không làm phát sinh ngoại lệ runtime.

---

### ❓ CÂU HỎI 9: VỀ LUẬN GIẢI TREESHAP VÀ TÍNH NHẤT QUÁN VẬT LÝ CỦA MÔ HÌNH (TREESHAP BACKUP DEFENSE)
> **Giảng viên hỏi:** *"Làm sao nhóm chứng minh mô hình máy học không phải là một chiếc hộp đen đưa ra kết quả ngẫu nhiên? Mô hình học được các quy luật vật lý nào từ tự nhiên?"*

#### 🛡️ CƠ SỞ PHẢN BIỆN DỰA TRÊN DỮ LIỆU & LÝ THUYẾT:
* **Sự chuyển dịch cơ chế dự báo (Regime Shift):** Phân tích giá trị Shapley từ thuật toán **TreeSHAP** bóc tách đóng góp của từng đặc trưng thành điểm số AQI thực tế:
  * Ở **Chân trời 1h Nowcasting**: Quán tính cảm biến mặt đất chiếm ưu thế tuyệt đối. Biến `target_aqi_lag_0` đóng góp **$13.45\text{ điểm AQI}$**, tiếp theo là `lag_1` ($2.49\text{ AQI}$), `roll_mean_3h` ($1.69\text{ AQI}$) và vi sai `diff_1h` ($1.29\text{ AQI}$). Nhóm trễ cảm biến đóng góp hơn 85% tổng độ ảnh hưởng.
  * Ở **Chân trời 24h Day-Ahead**: Khi tín hiệu cảm biến mặt đất bị che giấu, các biến vi khí hậu tương lai vươn lên giữ vai trò định hình:
    * Tốc độ gió dự báo `future_wind_speed` vươn lên vị trí số 1 trong các biến khí tượng với **$2.68\text{ điểm AQI}$**.
    * Yếu tố vị trí không gian `station_id` đóng góp **$2.35\text{ AQI}$**.
    * Nhiệt độ bề mặt `future_temp_2m` đóng góp **$1.28\text{ AQI}$**, vector gió $v$ đóng góp **$1.24\text{ AQI}$**, và lượng mưa `future_rain` đóng góp **$1.10\text{ AQI}$**.
* **Tính nhất quán vật lý (Physical Consistency):** Phân tích SHAP Beeswarm Summary Plot khẳng định mô hình tuân thủ hoàn hảo các định luật khí tượng:
  * **Gió đối lưu phân tán ô nhiễm:** Các điểm tốc độ gió cao (màu đỏ) nằm hoàn toàn ở miền giá trị SHAP âm $\to$ Gió mạnh kích hoạt đối lưu khuếch tán, cuốn trôi và pha loãng nồng độ ô nhiễm.
  * **Nhiệt độ kích thích quang hóa:** Các điểm nhiệt độ cao (màu đỏ) nằm hoàn toàn ở miền giá trị SHAP dương $\to$ Nhiệt độ cao thúc đẩy các phản ứng quang hóa tạo bụi thứ cấp và làm bốc hơi độ ẩm thực vật, gia tăng ô nhiễm không khí.
