import os
import sys
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

def build_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]
    
    # Color tokens
    c_bg = RGBColor(248, 250, 252)        # #F8FAFC
    c_white = RGBColor(255, 255, 255)     # #FFFFFF
    c_primary = RGBColor(37, 99, 235)     # #2563EB
    c_secondary = RGBColor(124, 58, 237)  # #7C3AED
    c_dark = RGBColor(15, 23, 42)         # #0F172A
    c_muted = RGBColor(71, 85, 105)       # #475569
    c_border = RGBColor(226, 232, 240)    # #E2E8F0
    c_emerald = RGBColor(5, 150, 105)     # #059669
    c_amber = RGBColor(217, 119, 6)       # #D97706
    c_rose = RGBColor(225, 29, 72)        # #E11D48
    c_light_blue = RGBColor(239, 246, 255)# #EFF6FF
    c_light_green = RGBColor(236, 253, 245)# #ECFDF5
    c_light_amber = RGBColor(255, 251, 235)# #FFFBEB
    
    def set_slide_background(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = c_bg
        bg.line.fill.background()
        return bg

    def add_card(slide, left, top, width, height, fill_color=c_white, border_color=c_border):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = fill_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(1.5)
        else:
            card.line.fill.background()
        return card

    def add_header(slide, part_badge, title_text):
        tb = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.9))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        
        p1 = tf.paragraphs[0]
        p1.text = part_badge.upper()
        p1.font.size = Pt(10)
        p1.font.bold = True
        p1.font.color.rgb = c_primary
        p1.font.name = "Arial"
        
        p2 = tf.add_paragraph()
        p2.text = title_text
        p2.font.size = Pt(21)
        p2.font.bold = True
        p2.font.color.rgb = c_dark
        p2.font.name = "Arial"

    # ==========================================
    # SLIDE 01: PART 1 - TITLE & SCOPE
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)
    
    add_card(s1, Inches(0.8), Inches(0.7), Inches(6.8), Inches(6.1))
    tb_s1_left = s1.shapes.add_textbox(Inches(1.1), Inches(0.9), Inches(6.2), Inches(5.7))
    tf1 = tb_s1_left.text_frame
    tf1.word_wrap = True
    
    p = tf1.paragraphs[0]
    p.text = "PART 1: PROBLEM & DATA UNDERSTANDING · MILESTONE 2"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = c_primary
    
    p = tf1.add_paragraph()
    p.text = "Comparative US AQI Time Series Forecasting in California with Extreme-Event Evaluation"
    p.font.size = Pt(21)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(6)
    
    p = tf1.add_paragraph()
    p.text = "Nghiên cứu đối chuẩn thực nghiệm mô hình dự báo chuỗi thời gian AQI trong bối cảnh thiên tai cực đoan"
    p.font.size = Pt(11.5)
    p.font.color.rgb = c_muted
    p.space_after = Pt(14)
    
    p = tf1.add_paragraph()
    p.text = "📌 HORIZON 1 — NOWCASTING 1 GIỜ (t+1)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_primary
    
    p = tf1.add_paragraph()
    p.text = "• Mục tiêu: Cảnh báo tức thời cho lao động ngoài trời và điều phối giao thông đô thị.\n• Cơ chế: Khai thác quán tính tự hồi quy cảm biến mặt đất (lag 0..3) kết hợp vi phân trễ 1h."
    p.font.size = Pt(10.5)
    p.font.color.rgb = c_dark
    p.space_after = Pt(10)
    
    p = tf1.add_paragraph()
    p.text = "📌 HORIZON 2 — DAY-AHEAD 24 GIỜ (t+24)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_secondary
    
    p = tf1.add_paragraph()
    p.text = "• Mục tiêu: Điều hành hành chính, đóng cửa trường học, phương án y tế trước 1 ngày.\n• Cơ chế: Che giấu cảm biến tương lai; suy luận từ trường thời tiết số trị dự báo W_(t+24)."
    p.font.size = Pt(10.5)
    p.font.color.rgb = c_dark

    add_card(s1, Inches(7.8), Inches(0.7), Inches(4.7), Inches(6.1))
    tb_s1_right = s1.shapes.add_textbox(Inches(8.1), Inches(1.0), Inches(4.1), Inches(5.5))
    tf1_r = tb_s1_right.text_frame
    tf1_r.word_wrap = True
    
    p = tf1_r.paragraphs[0]
    p.text = "THÔNG SỐ KHOA HỌC DỰ ÁN"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(10)
    
    specs = [
        ("Quy mô Dữ liệu", "181,122 bản ghi hàng giờ (2018–2025) tại 3 lưu vực đối nghịch California."),
        ("Không gian Đối chuẩn", "8 Mô hình Nền tảng + 1 Voting Ensemble thuộc 5 họ thuật toán."),
        ("Giao thức Kiểm soát", "Zero-Leakage Temporal Split + Vùng đệm biên chống rò rỉ."),
        ("Bài kiểm tra Áp lực", "Kiểm định trên đợt cháy Park Fire 2024 và Out-of-sample Test 2025."),
        ("Khả năng Giải thích", "TreeSHAP bóc tách giá trị đóng góp Shapley theo điểm AQI thực tế.")
    ]
    for title, desc in specs:
        p = tf1_r.add_paragraph()
        p.text = f"• {title}:"
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_primary
        p = tf1_r.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = c_dark
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 02: PART 1 - WILDFIRE CRISIS & 3 GAPS
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Part 1: Problem & Data Understanding", "Bối Cảnh Khủng Hoảng Cháy Rừng & 3 Khoảng Trống Nghiên Cứu")
    
    # Left: Image Card
    add_card(s2, Inches(0.8), Inches(1.5), Inches(5.5), Inches(5.3))
    img_sf = "image/san-francisco-orange-sky.jpg"
    if os.path.exists(img_sf):
        s2.shapes.add_picture(img_sf, Inches(1.0), Inches(1.7), width=Inches(5.1))
    tb_img_cap = s2.shapes.add_textbox(Inches(1.0), Inches(5.2), Inches(5.1), Inches(1.4))
    tfic = tb_img_cap.text_frame
    tfic.word_wrap = True
    p = tfic.paragraphs[0]
    p.text = "Hình 1: Bầu trời cam San Francisco (09/09/2020) — Bão lửa August Complex"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = c_rose
    p = tfic.add_paragraph()
    p.text = "Chỉ số AQI chạm đỉnh lịch sử 496.0 tại San Jose, vượt ngưỡng nguy hại Hazardous (301+) tới 195 điểm, tiệm cận ngưỡng trần 500 của cảm biến quan trắc."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_muted

    # Right: 3 Research Gaps
    add_card(s2, Inches(6.6), Inches(1.5), Inches(5.9), Inches(5.3))
    tb_gaps = s2.shapes.add_textbox(Inches(6.8), Inches(1.7), Inches(5.5), Inches(4.9))
    tfg = tb_gaps.text_frame
    tfg.word_wrap = True
    p = tfg.paragraphs[0]
    p.text = "3 KHOẢNG TRỐNG NGHIÊN CỨU (RESEARCH GAPS)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(10)
    
    gaps = [
        ("1. CHE LẤP SAI SỐ (METRIC MASKING)", "Hơn 85% số ngày trong năm là không khí sạch (AQI <= 50). Các thang đo trung bình toàn niên (MAE, RMSE) che giấu hoàn toàn thất bại của mô hình tại các ngày thiên tai cực đoan (AQI > 150).", c_rose),
        ("2. RÒ RỈ TƯƠNG LAI (LOOKAHEAD LEAKAGE)", "Việc chia train/test ngẫu nhiên trên chuỗi thời gian làm rò rỉ tín hiệu tương lai, tạo ra điểm số ảo R² > 0.95 nhưng mất tác dụng khi triển khai vận hành thực tế.", c_amber),
        ("3. ĐIỂM MÙ KHÍ QUYỂN (ATMOSPHERIC BLINDSPOT)", "Dự báo phụ thuộc hoàn toàn vào cảm biến mặt đất sẽ mất phương hướng khi dự báo trước 24 giờ do quán tính cảm biến bị suy giảm sâu; cần tích hợp trường vi khí hậu số trị dự báo (VPD, vector gió u, v).", c_primary)
    ]
    for g_title, g_desc, g_col in gaps:
        p = tfg.add_paragraph()
        p.text = g_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = g_col
        p = tfg.add_paragraph()
        p.text = g_desc
        p.font.size = Pt(10)
        p.font.color.rgb = c_dark
        p.space_after = Pt(6)

    # ==========================================
    # SLIDE 03: PART 1 - DATA AUDIT & SKEWNESS (+4.82)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Part 1: Problem & Data Understanding", "Kiểm Toán 181k Dữ Liệu & Phân Tích Phân Phối (+4.82 Skewness)")
    
    grid_data = [
        ("1. XỬ LÝ DỮ LIỆU KHUYẾT", "Nội suy tuyến tính bảo toàn cho gián đoạn <= 6h để giữ tính liên tục vật lý khí quyển. Loại bỏ hoàn toàn khoảng trống > 6h, tuyệt đối không tạo dữ liệu giả.", Inches(0.8), Inches(1.5), c_primary),
        ("2. BẢO TỒN NGOẠI LAI CỰC ĐOAN", "Giữ nguyên 100% các đỉnh nhọn AQI cực đoan, gồm đỉnh lịch sử 496.0 AQI (August Complex 2020). Lọc bỏ ngoại lai sẽ khiến mô hình mất khả năng nhận diện bão khói.", Inches(6.8), Inches(1.5), c_rose),
        ("3. ĐỒNG BỘ MÚI GIỜ", "Chuyển toàn bộ dữ liệu từ UTC về giờ địa phương Thái Bình Dương (PST/PDT), khớp đúng chu kỳ phát thải giao thông đô thị và dao động nhiệt độ ngày đêm.", Inches(0.8), Inches(3.2), c_emerald),
        ("4. 3 LƯU VỰC ĐỊA MẠO ĐỐI NGHỊCH", "Fresno (Central Valley, 51k dòng - Lòng chảo bẫy bụi), Los Angeles (South Coast, 50k dòng - Vách núi chắn khói), San Jose (Bay Area, 26k dòng - Gió biển duyên hải).", Inches(6.8), Inches(3.2), c_secondary),
    ]
    for title, desc, l, t, col in grid_data:
        add_card(s3, l, t, Inches(5.7), Inches(1.5))
        tb = s3.shapes.add_textbox(l + Inches(0.2), t + Inches(0.15), Inches(5.3), Inches(1.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = col
        p.space_after = Pt(4)
        p = tf.add_paragraph()
        p.text = desc
        p.font.size = Pt(10)
        p.font.color.rgb = c_dark

    add_card(s3, Inches(0.8), Inches(4.9), Inches(11.7), Inches(1.9), fill_color=c_light_amber, border_color=c_amber)
    tb_callout = s3.shapes.add_textbox(Inches(1.1), Inches(5.05), Inches(11.1), Inches(1.6))
    tfc = tb_callout.text_frame
    tfc.word_wrap = True
    p = tfc.paragraphs[0]
    p.text = "💡 TẠI SAO KHÔNG LOG-TRANSFORM KHI SKEWNESS = +4.82?"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_amber
    p.space_after = Pt(4)
    
    p = tfc.add_paragraph()
    p.text = "1. Tính bất biến của thuật toán dạng Cây (Tree-based invariance): Các mô hình cây dẫn đầu (GBDT, Random Forest) phân nhánh dựa trên thứ tự xếp hạng (rank order) x_j <= theta, do đó bất kỳ phép biến đổi đơn điệu nào như log(y) cũng không làm thay đổi điểm chia nhánh tối ưu.\n2. Bất đẳng thức Jensen & Lệch kỳ vọng: Dự báo trên log rồi biến đổi ngược bằng hàm exp tạo độ chệch E[exp(y)] >= exp(E[y]). Khoảng cách log(400) - log(300) = 0.287 bị nén bằng log(13) - log(10) = 0.262, vô tình làm phẳng mức phạt sai số tại vùng đuôi nồng độ cao nguy hại (AQI > 150) — vùng tối quan trọng cần cảnh báo."
    p.font.size = Pt(10.5)
    p.font.color.rgb = c_dark

    # ==========================================
    # SLIDE 04: PART 2 - FEATURE ENGINEERING
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Part 2: Feature Engineering & Visualization", "Kỹ Nghệ Đặc Trưng Vật Lý Khí Quyển (VPD, Vector Gió u, v)")
    
    add_card(s4, Inches(0.8), Inches(1.5), Inches(5.7), Inches(5.3), border_color=c_primary)
    tb_1h = s4.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(5.1), Inches(4.9))
    tf1h = tb_1h.text_frame
    tf1h.word_wrap = True
    p = tf1h.paragraphs[0]
    p.text = "HORIZON 1: NOWCASTING 1 GIỜ (22 ĐẶC TRƯNG)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p.space_after = Pt(8)
    
    feats_1h = [
        ("Quán tính Tự hồi quy", "target_aqi_lag_0, lag_1, lag_2, lag_3 (Tín hiệu cảm biến mặt đất gần nhất)."),
        ("Tốc độ Bùng phát Khói", "diff_1h = lag_0 - lag_1 (Đạo hàm vi phân bậc 1 bắt nhịp tăng đột biến)."),
        ("Biến động Ngắn hạn", "roll_mean_3h, roll_std_3h (Độ lệch chuẩn và trung bình trượt 3 giờ)."),
        ("Vi khí hậu Khô hạn VPD", "vpd_kpa = Áp suất hơi thiếu hụt (Nhiệt độ + Độ ẩm đo độ nứt khô thảm thực vật)."),
        ("Động lực học Gió Descartes", "Phân rã vector trực giao wind_u (Tây-Đông) và wind_v (Nam-Bắc)."),
        ("Khí tượng & Chu kỳ", "temperature, relative_humidity, rain, cloud_cover, hour_sin/cos, month_sin/cos.")
    ]
    for f_title, f_desc in feats_1h:
        p = tf1h.add_paragraph()
        p.text = f"• {f_title}: "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = c_dark
        p.text += f_desc
        p.font.size = Pt(10)
        p.space_after = Pt(4)

    add_card(s4, Inches(6.8), Inches(1.5), Inches(5.7), Inches(5.3), border_color=c_secondary)
    tb_24h = s4.shapes.add_textbox(Inches(7.1), Inches(1.7), Inches(5.1), Inches(4.9))
    tf24h = tb_24h.text_frame
    tf24h.word_wrap = True
    p = tf24h.paragraphs[0]
    p.text = "HORIZON 2: DAY-AHEAD 24 GIỜ (19 ĐẶC TRƯNG)"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_secondary
    p.space_after = Pt(8)
    
    feats_24h = [
        ("Che giấu Cảm biến Tuyệt đối", "Cắt đứt 100% dữ liệu cảm biến mặt đất từ t+1 đến t+24 để chống rò rỉ."),
        ("Lags Nền Dài hạn", "lag_0, lag_24, lag_48, roll_mean_24h (Tính từ t-24 trở về trước)."),
        ("Trường Khí tượng Dự báo W_(t+24)", "future_temp_2m, future_rh_2m, future_wind_speed, future_rain, future_vpd_kpa."),
        ("Vector Gió Tương lai", "future_wind_u, future_wind_v (Định hướng luồng khói từ vùng cháy tới trạm)."),
        ("Áp suất & Độ che phủ Mây", "future_surface_pressure, future_cloud_cover (Đo mức độ nghịch nhiệt và bức xạ)."),
        ("Chu kỳ Tương lai tại t+24", "future_hour_sin/cos, future_month_sin/cos, future_is_weekend.")
    ]
    for f_title, f_desc in feats_24h:
        p = tf24h.add_paragraph()
        p.text = f"• {f_title}: "
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = c_dark
        p.text += f_desc
        p.font.size = Pt(10)
        p.space_after = Pt(4)

    # ==========================================
    # SLIDE 05: PART 2 - ZERO-LEAKAGE SPLIT & TIMESERIES (FIG 02)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Part 2: Feature Engineering & Visualization", "Giao Thức Phân Chia Tuần Tự (Zero-Leakage) & Lát Cắt Chuỗi Thời Gian")
    
    # Left: Temporal Splits
    add_card(s5, Inches(0.8), Inches(1.5), Inches(5.0), Inches(5.3))
    tb_split = s5.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(4.6), Inches(5.0))
    tfs = tb_split.text_frame
    tfs.word_wrap = True
    p = tfs.paragraphs[0]
    p.text = "PHÂN CHIA THỜI GIAN TUYỆT ĐỐI"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(8)
    
    splits = [
        ("TẬP TRAIN (2018–2023 · 61.3%)", "111,073 bản ghi (1h) / 110,733 bản ghi (24h)\nHọc quy luật khí tượng nền và các đợt cháy lịch sử (Camp Fire 2018, August Complex 2020).", c_primary),
        ("TẬP VALIDATION (2024 · 24.1%)", "43,727 bản ghi (1h) / 43,582 bản ghi (24h)\nChứa vụ cháy Park Fire (T7–T8/2024); làm bài kiểm tra áp lực thực tế để tinh chỉnh siêu tham số và Early Stopping.", c_amber),
        ("TẬP TEST ĐỘC LẬP (2025 · 14.5%)", "26,292 bản ghi (1h) / 26,207 bản ghi (24h)\nHoàn toàn độc lập, đánh giá một lần duy nhất.", c_emerald)
    ]
    for s_title, s_desc, col in splits:
        p = tfs.add_paragraph()
        p.text = s_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = col
        p = tfs.add_paragraph()
        p.text = s_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(6)
        
    p = tfs.add_paragraph()
    p.text = "✂️ VÙNG ĐỆM BIÊN (TRIM TAIL BUFFER):"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = c_rose
    p = tfs.add_paragraph()
    p.text = "Cắt bỏ đúng h dòng cuối cùng của từng trạm trên Train và Val (1h cho Nowcasting, 24h cho Day-Ahead) để triệt tiêu hoàn toàn rò rỉ ranh giới khi dịch chuyển nhãn shift(-h)."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark

    # Right: Embed Fig 02 Timeseries
    fig2_path = "artifacts/figures/02_actual_vs_predicted_1week.png"
    add_card(s5, Inches(6.0), Inches(1.5), Inches(6.5), Inches(5.3))
    if os.path.exists(fig2_path):
        s5.shapes.add_picture(fig2_path, Inches(6.1), Inches(1.6), width=Inches(6.3))
    tb_cap2 = s5.shapes.add_textbox(Inches(6.1), Inches(6.3), Inches(6.3), Inches(0.4))
    p = tb_cap2.text_frame.paragraphs[0]
    p.text = "Hình 2: Chuỗi 168h tại Fresno (09/01 - 15/01/2025) EPA thực tế vs Ensemble & Ridge. Dải sai số thặng dư < 5 AQI."
    p.font.size = Pt(9)
    p.font.color.rgb = c_muted

    # ==========================================
    # SLIDE 06: PART 3 - 5 ALGORITHM FAMILIES & CODE
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Part 3: Modeling & Evaluation", "Không Gian Đối Chuẩn: 5 Họ Thuật Toán & Kỹ Thuật Mã Nguồn")
    
    fams = [
        ("BASELINES", "Persistence (lag_0)\nClimatology (Lịch sử trạm, tháng, giờ trên Train).", c_muted),
        ("LINEAR L2", "Ridge Regression\nNghiệm ma trận giải tích đóng, thời gian fit ~0.18s.", c_primary),
        ("BAGGING", "Random Forest\n150 cây quyết định, bootstrap mẫu giảm phương sai.", c_emerald),
        ("SOTA GBDT", "LightGBM (Leaf-wise)\nXGBoost (Hessian bậc 2)\nCatBoost (Oblivious trees).", c_secondary),
        ("TABULAR NN", "MLP Regressor\n2 tầng ẩn (64, 32 units), kích hoạt ReLU, Adam.", c_amber),
    ]
    for idx, (f_name, f_desc, f_col) in enumerate(fams):
        l = Inches(0.8 + idx * 2.38)
        add_card(s6, l, Inches(1.5), Inches(2.2), Inches(2.3), border_color=f_col)
        tb = s6.shapes.add_textbox(l + Inches(0.15), Inches(1.65), Inches(1.9), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f_name
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = f_col
        p.space_after = Pt(4)
        p = tf.add_paragraph()
        p.text = f_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        
    add_card(s6, Inches(0.8), Inches(3.95), Inches(11.7), Inches(0.65), fill_color=c_light_green, border_color=c_emerald)
    tb_ens = s6.shapes.add_textbox(Inches(1.1), Inches(4.05), Inches(11.1), Inches(0.45))
    p = tb_ens.text_frame.paragraphs[0]
    p.text = "⭐ TOP META-ENSEMBLE: Voting Ensemble (Top-3 GBDT) = (y_LightGBM + y_XGBoost + y_CatBoost) / 3 triệt tiêu sai số cục bộ độc lập."
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = c_emerald

    add_card(s6, Inches(0.8), Inches(4.8), Inches(5.7), Inches(2.0))
    tb_c1 = s6.shapes.add_textbox(Inches(1.0), Inches(4.95), Inches(5.3), Inches(1.7))
    tfc1 = tb_c1.text_frame
    tfc1.word_wrap = True
    p = tfc1.paragraphs[0]
    p.text = "1. CHUẨN HÓA DỮ LIỆU DỊ BIỆT (SCALING)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p = tfc1.add_paragraph()
    p.text = "• Mô hình Cây (GBDT, RF): Dùng trực tiếp dữ liệu gốc vì điều kiện phân nhánh x_j <= theta bất biến với co giãn đơn điệu.\n• Ridge & MLP: Bắt buộc dùng StandardScaler và CHỈ GỌI fit TRÊN TẬP TRAIN, sau đó transform cho Val và Test để chống rò rỉ phân phối."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark

    add_card(s6, Inches(6.8), Inches(4.8), Inches(5.7), Inches(2.0))
    tb_c2 = s6.shapes.add_textbox(Inches(7.0), Inches(4.95), Inches(5.3), Inches(1.7))
    tfc2 = tb_c2.text_frame
    tfc2.word_wrap = True
    p = tfc2.paragraphs[0]
    p.text = "2. MÃ HÓA BIẾN TRẠM KHÔNG GIAN (station_id)"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = c_secondary
    p = tfc2.add_paragraph()
    p.text = "• Ridge & MLP: Áp dụng One-Hot Encoding (pd.get_dummies) tạo 3 cột chỉ thị nhị phân độc lập, tránh ngầm hiểu có quan hệ thứ tự khoảng cách giữa các trạm.\n• GBDT: Ép kiểu sang Integer Category (astype('category')), thuật toán histogram tự động gom cụm gradient tối ưu theo trạm mà không làm tăng số chiều ma trận."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark

    # ==========================================
    # SLIDE 07: PART 3 - LEADERBOARD (FIG 01)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Part 3: Modeling & Evaluation", "Bảng Kết Quả Leaderboard: Đối Chuẩn Đa Mô Hình Trên Test 2025")
    
    add_card(s7, Inches(0.8), Inches(1.5), Inches(5.8), Inches(5.3))
    tb_lb = s7.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.4), Inches(5.0))
    tflb = tb_lb.text_frame
    tflb.word_wrap = True
    
    p = tflb.paragraphs[0]
    p.text = "KẾT QUẢ ĐỐI CHUẨN THỰC NGHIỆM CHÍNH THỨC"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(4)
    
    p = tflb.add_paragraph()
    p.text = "🏆 HORIZON 1H — VOTING ENSEMBLE:\nMAE = 3.06 AQI · R² = 0.9555 · RMSE = 5.58\n(Giảm -82.5% sai số vs Climatology; giảm -15.1% vs Persistence)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = c_emerald
    p.space_after = Pt(4)
    
    p = tflb.add_paragraph()
    p.text = "🏆 HORIZON 24H — VOTING ENSEMBLE:\nMAE = 11.30 AQI · R² = 0.6172 · RMSE = 16.34\n(Giảm -35.2% sai số vs Climatology; giảm -13.2% vs Persistence)"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = c_secondary
    p.space_after = Pt(8)
    
    table_lines = [
        "Mô hình                | MAE 1h | R² 1h  | MAE 24h| R² 24h",
        "-----------------------+--------+--------+--------+-------",
        "Climatology (Base)     | 17.53  | 0.150  | 17.45  | 0.155",
        "Persistence (Base)     |  3.61  | 0.948  | 13.02  | 0.460",
        "Ridge Regression       |  3.72  | 0.948  | 11.86  | 0.586",
        "Random Forest          |  3.33  | 0.954  | 11.53  | 0.604",
        "LightGBM SOTA          |  3.13  | 0.954  | 11.33  | 0.617",
        "XGBoost SOTA           |  3.10  | 0.954  | 11.36  | 0.616",
        "CatBoost SOTA          |  3.13  | 0.954  | 11.40  | 0.608",
        "Tabular MLP            |  3.26  | 0.958  | 13.08  | 0.501",
        "Voting Ensemble (Top3) |  3.06  | 0.956  | 11.30  | 0.617"
    ]
    for tl in table_lines:
        p = tflb.add_paragraph()
        p.text = tl
        p.font.size = Pt(8.5)
        p.font.name = "Courier New"
        if "Voting Ensemble" in tl:
            p.font.bold = True
            p.font.color.rgb = c_emerald

    fig1_path = "artifacts/figures/01_model_comparison_mae.png"
    if os.path.exists(fig1_path):
        add_card(s7, Inches(6.9), Inches(1.5), Inches(5.6), Inches(5.3))
        s7.shapes.add_picture(fig1_path, Inches(7.0), Inches(1.6), width=Inches(5.4))
        tb_cap = s7.shapes.add_textbox(Inches(7.0), Inches(6.4), Inches(5.4), Inches(0.4))
        p = tb_cap.text_frame.paragraphs[0]
        p.text = "Hình 3: Đối chuẩn MAE và R² giữa 8 mô hình trên tập Test 2025 qua hai chân trời 1h và 24h."
        p.font.size = Pt(9)
        p.font.color.rgb = c_muted

    # ==========================================
    # SLIDE 08: PART 3 - WILDFIRE EXTREME RESILIENCE (FIG 03)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Part 3: Modeling & Evaluation", "Đánh Giá Độ Bền Bỉ Trước Cú Sốc Khói Cháy Rừng Cực Đoan")
    
    fig3_path = "artifacts/figures/03_wildfire_extreme_resilience.png"
    add_card(s8, Inches(0.8), Inches(1.5), Inches(6.0), Inches(5.3))
    if os.path.exists(fig3_path):
        s8.shapes.add_picture(fig3_path, Inches(0.9), Inches(1.6), width=Inches(5.8))
    tb_cap3 = s8.shapes.add_textbox(Inches(0.9), Inches(6.4), Inches(5.8), Inches(0.4))
    p = tb_cap3.text_frame.paragraphs[0]
    p.text = "Hình 4: Phân rã sai số MAE giữa điều kiện thường (AQI <= 100) và bão khói cực đoan (AQI > 150) ở kịch bản 24h."
    p.font.size = Pt(9)
    p.font.color.rgb = c_muted

    add_card(s8, Inches(7.0), Inches(1.5), Inches(5.5), Inches(5.3))
    tb_ext = s8.shapes.add_textbox(Inches(7.2), Inches(1.7), Inches(5.1), Inches(4.9))
    tfe = tb_ext.text_frame
    tfe.word_wrap = True
    p = tfe.paragraphs[0]
    p.text = "BẰNG CHỨNG THỰC NGHIỆM TẠI NGƯỠNG THIÊN TAI"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(8)
    
    ext_cards = [
        ("KHOẢNG CHÊNH LỆCH SAI SỐ CỰC ĐOAN", "• Sai số ở điều kiện thường (AQI <= 100): 9.9 AQI.\n• Sai số khi bão khói bùng phát (AQI > 150): 62.6 AQI.\n• Khoảng chênh lệch ghi nhận: +Δ 52.8 AQI.", c_rose),
        ("SỤP ĐỔ PHƯƠNG SAI MẪU CỦA R²", "Khi cô lập tập con AQI > 150, miền giá trị bị co hẹp làm mẫu số SS_tot giảm rất nhanh. Chỉ cần sai số dư SS_res vừa phải cũng khiến R² sụt giảm mạnh hoặc bị âm dù mô hình vẫn bám đúng hướng biến thiên.", c_amber),
        ("THƯỚC ĐO ĐỐI CHỨNG F1-SCORE (150+)", "Vì khiếm khuyết của R², nhóm bổ sung F1-Score phân loại tại ngưỡng 150+. Mô hình Top GBDT đạt F1-Score = 0.825 ở bài toán 1h, chứng minh khả năng cảnh báo sớm bão khói vẫn được bảo toàn vững chắc.", c_emerald)
    ]
    for ec_title, ec_desc, ec_col in ext_cards:
        p = tfe.add_paragraph()
        p.text = ec_title
        p.font.size = Pt(10.5)
        p.font.bold = True
        p.font.color.rgb = ec_col
        p = tfe.add_paragraph()
        p.text = ec_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark
        p.space_after = Pt(6)

    # ==========================================
    # SLIDE 09: PART 3 - TREESHAP & PHYSICAL CONSISTENCY (FIG 05)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Part 3: Modeling & Evaluation", "Luận Giải TreeSHAP: Sự Chuyển Dịch Trọng Số & Nhất Quán Vật Lý")
    
    fig5_path = "artifacts/figures/05_shap_beeswarm_summary.png"
    add_card(s9, Inches(0.8), Inches(1.5), Inches(6.5), Inches(5.3))
    if os.path.exists(fig5_path):
        s9.shapes.add_picture(fig5_path, Inches(0.9), Inches(1.6), width=Inches(6.3))
    tb_cap5 = s9.shapes.add_textbox(Inches(0.9), Inches(6.4), Inches(6.3), Inches(0.4))
    p = tb_cap5.text_frame.paragraphs[0]
    p.text = "Hình 5: SHAP Beeswarm Plot ở kịch bản 24h thể hiện chiều hướng tác động và tính nhất quán vật lý."
    p.font.size = Pt(9)
    p.font.color.rgb = c_muted

    add_card(s9, Inches(7.5), Inches(1.5), Inches(5.0), Inches(5.3))
    tb_phys = s9.shapes.add_textbox(Inches(7.7), Inches(1.7), Inches(4.6), Inches(4.9))
    tfph = tb_phys.text_frame
    tfph.word_wrap = True
    
    p = tfph.paragraphs[0]
    p.text = "CHUYỂN DỊCH CƠ CHẾ & NHẤT QUÁN VẬT LÝ"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(6)
    
    p = tfph.add_paragraph()
    p.text = "📍 CHUYỂN DỊCH CƠ CHẾ (REGIME SHIFT):"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p = tfph.add_paragraph()
    p.text = "• 1h: Quán tính cảm biến mặt đất chiếm >85% (lag_0 = 13.45 AQI, lag_1 = 2.49 AQI).\n• 24h: Vi khí hậu dự báo vươn lên dẫn đầu (future_wind_speed = 2.68 AQI, station_id = 2.35 AQI, future_temp = 1.28 AQI, wind_v = 1.24 AQI, rain = 1.10 AQI)."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark
    p.space_after = Pt(6)
    
    p = tfph.add_paragraph()
    p.text = "📍 NHẤT QUÁN VẬT LÝ KHÍ QUYỂN:"
    p.font.size = Pt(10.5)
    p.font.bold = True
    p.font.color.rgb = c_emerald
    p = tfph.add_paragraph()
    p.text = "• Gió mạnh (future_wind_speed, đỏ): Nằm ở SHAP âm -> Tăng đối lưu khuếch tán, pha loãng nồng độ ô nhiễm.\n• Nhiệt độ cao (future_temp_2m, đỏ): Nằm ở SHAP dương -> Thúc đẩy phản ứng quang hóa tạo bụi thứ cấp và làm khô thảm thực vật.\n• Vector gió (wind_u, v): Nắm bắt hướng khói từ sườn núi Sierra Nevada tràn vào lưu vực."
    p.font.size = Pt(9.5)
    p.font.color.rgb = c_dark

    # ==========================================
    # SLIDE 10: PART 3 - ERROR DIAGNOSTICS (FIG 07, 08, 09)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "Part 3: Modeling & Evaluation", "Chẩn Đoán Cơ Chế Sai Số: Parity Hexbin, Nghịch Nhiệt Đêm & Địa Mạo")
    
    figs_diag = [
        ("artifacts/figures/07_actual_vs_pred_parity_hexbin.png", "Co cụm Phương sai Đuôi (Shrinkage)", "Mật độ dày quanh đường 1:1 ở vùng sạch. Hệ số góc beta = 0.54 (< 1.0) chứng minh mô hình nén dự báo vùng đỉnh về kỳ vọng trung bình do hàm loss MAE.", Inches(0.8)),
        ("artifacts/figures/08_diurnal_hourly_error_profile.png", "Nghịch nhiệt Bức xạ Ban đêm", "Sai số thấp nhất vào trưa (11h-15h, ~8 AQI), tăng vọt vào Ban đêm (22h-4h sáng, >14 AQI) do mặt đất lạnh giữ khói bụi trong tầng biên mỏng sát đất.", Inches(4.8)),
        ("artifacts/figures/09_spatial_basin_resilience.png", "Phân rã theo 3 Lưu vực", "San Jose (Bay Area) tốt nhất MAE 9.90 (0 bão khói nhờ gió biển); Fresno MAE 10.95 (88 đợt khói bẫy bụi); LA MAE 13.06 (231 đợt bão khói do vách núi San Gabriel).", Inches(8.8)),
    ]
    for f_path, c_title, c_desc, c_left in figs_diag:
        add_card(s10, c_left, Inches(1.5), Inches(3.7), Inches(5.3))
        if os.path.exists(f_path):
            s10.shapes.add_picture(f_path, c_left + Inches(0.15), Inches(1.6), width=Inches(3.4))
        tb = s10.shapes.add_textbox(c_left + Inches(0.2), Inches(4.3), Inches(3.3), Inches(2.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = c_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = c_primary
        p.space_after = Pt(4)
        p = tf.add_paragraph()
        p.text = c_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = c_dark

    # ==========================================
    # SLIDE 11: PART 4 - CONCLUSIONS & ROADMAP
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Part 4: Conclusion & Roadmap", "Kết Luận Thực Nghiệm, Giới Hạn Kỹ Thuật & Kế Hoạch Milestone 3")
    
    cols_s11 = [
        ("4 KẾT QUẢ CỐT LÕI (MILESTONE 2)", [
            "1. Quy chuẩn hóa giao thức phân chia tuần tự chống rò rỉ trên 181k dòng 8 năm có vùng đệm biên.",
            "2. Xác lập Voting Ensemble dẫn đầu: MAE 3.06 (R² = 0.956) ở 1h và MAE 11.30 (R² = 0.617) ở 24h.",
            "3. Định lượng thành công sự chuyển dịch sang điều khiển vi khí hậu W_(t+24) qua TreeSHAP.",
            "4. Nhận diện các cơ chế gây sai số gắn liền với nghịch nhiệt đêm và co cụm phương sai đuôi (beta = 0.54)."
        ], c_light_green, c_emerald),
        ("3 GIỚI HẠN KỸ THUẬT TỒN ĐỌNG", [
            "1. Sai số ở ngưỡng cực đoan còn cao (62.6 AQI) do hàm mất mát MAE đối xứng chưa phạt nặng vùng đỉnh.",
            "2. Chưa tích hợp dữ liệu độ dày quang học AOD từ vệ tinh để đo chiều đứng cột khói trong tầng nghịch nhiệt.",
            "3. Kiến trúc Tabular MLP hiện tại chưa học được tương quan không gian liên trạm."
        ], c_light_amber, c_amber),
        ("KẾ HOẠCH BÀN GIAO MILESTONE 3", [
            "1. Tối ưu Thuật toán: Thử nghiệm hàm mất mát Asymmetric Huber Loss / Focal Loss kéo độ dốc beta tiệm cận 1.0.",
            "2. Đóng gói MLOps: Xây dựng REST API (FastAPI) đạt chuẩn độ trễ phản hồi < 50ms phục vụ tác nghiệp.",
            "3. Ứng dụng Thực tiễn: Phát triển Dashboard giám sát chất lượng không khí thời gian thực cho California."
        ], c_light_blue, c_primary),
    ]
    for idx, (col_title, items, bg_col, bdr_col) in enumerate(cols_s11):
        left_pos = Inches(0.8 + idx * 3.95)
        add_card(s11, left_pos, Inches(1.5), Inches(3.8), Inches(5.3), fill_color=bg_col, border_color=bdr_col)
        tb = s11.shapes.add_textbox(left_pos + Inches(0.2), Inches(1.7), Inches(3.4), Inches(4.9))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = col_title
        p.font.size = Pt(11.5)
        p.font.bold = True
        p.font.color.rgb = bdr_col
        p.space_after = Pt(10)
        
        for item in items:
            p = tf.add_paragraph()
            p.text = item
            p.font.size = Pt(9.5)
            p.font.color.rgb = c_dark
            p.space_after = Pt(8)

    # ==========================================
    # SLIDE 12: PART 4 - MLOPS DELIVERY & Q&A
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Part 4: Conclusion & Roadmap", "Tổng Kết Kiến Trúc Đóng Gói & Q&A Session")
    
    # Left: MLOps Delivery Pipeline
    add_card(s12, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))
    tb_m = s12.shapes.add_textbox(Inches(1.1), Inches(1.7), Inches(6.2), Inches(4.9))
    tfm = tb_m.text_frame
    tfm.word_wrap = True
    p = tfm.paragraphs[0]
    p.text = "SƠ ĐỒ CHUYỂN GIAO CÔNG NGHỆ SANG MILESTONE 3"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = c_dark
    p.space_after = Pt(12)
    
    delivery_steps = [
        ("TẦNG 1: DỮ LIỆU & TIỀN XỬ LÝ (MILESTONE 1)", "181,122 bản ghi hàng giờ · US EPA AQS & Open-Meteo · Zero-Leakage Split · Physics-Informed Feature Store Parquet.", c_primary),
        ("TẦNG 2: MÔ HÌNH HÓA ĐỐI CHUẨN (MILESTONE 2)", "5 họ thuật toán · SOTA GBDT & Top-3 Voting Ensemble (MAE 3.06 ở 1h, 11.30 ở 24h) · TreeSHAP Explainability · Error Diagnostics.", c_emerald),
        ("TẦNG 3: ĐÓNG GÓI & TRIỂN KHAI SẢN PHẨM (MILESTONE 3)", "FastAPI Microservice (Độ trễ phản hồi < 50ms) · Streamlit Real-Time Monitoring Dashboard · Asymmetric Loss cho bão khói cực đoan.", c_secondary)
    ]
    for d_title, d_desc, d_col in delivery_steps:
        p = tfm.add_paragraph()
        p.text = d_title
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = d_col
        p = tfm.add_paragraph()
        p.text = d_desc
        p.font.size = Pt(10)
        p.font.color.rgb = c_dark
        p.space_after = Pt(10)

    # Right: Thank you & Q&A Session
    add_card(s12, Inches(7.8), Inches(1.5), Inches(4.7), Inches(5.3), fill_color=c_dark, border_color=c_primary)
    tb_qa = s12.shapes.add_textbox(Inches(8.1), Inches(2.2), Inches(4.1), Inches(4.0))
    tfqa = tb_qa.text_frame
    tfqa.word_wrap = True
    
    p = tfqa.paragraphs[0]
    p.text = "THANK YOU!"
    p.font.size = Pt(28)
    p.font.bold = True
    p.font.color.rgb = c_white
    p.space_after = Pt(10)
    
    p = tfqa.add_paragraph()
    p.text = "Q&A DEFENSE SESSION"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = c_primary
    p.space_after = Pt(16)
    
    p = tfqa.add_paragraph()
    p.text = "Nhóm nghiên cứu xin chân thành cảm ơn Thầy Cô và Hội đồng đã chú ý theo dõi!\n\nNhóm rất mong nhận được những góp ý quý báu và sẵn sàng tiếp nhận các câu hỏi phản biện."
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(226, 232, 240)

    out_dir = "presentations/present2"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "present2_dsr301m.pptx")
    prs.save(out_path)
    print(f"Presentation saved successfully to: {out_path} ({len(prs.slides)} slides)")

if __name__ == "__main__":
    build_presentation()
