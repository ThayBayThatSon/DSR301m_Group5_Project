"""
Build Deck Script: Generates present2_dsr301m.pptx (14 Slides, 16:9 Widescreen)
Strictly adheres to:
  - presentations/present2/present2_canva_blueprint.md (Visual-First English Specs)
  - presentations/present2/present2_dsr301m_script.md (Vietnamese Speaker Notes)
"""

import os
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# ==========================================
# 1. COLOR TOKENS & DESIGN CONSTANTS
# ==========================================
BG_COLOR       = RGBColor(247, 243, 238)  # #F7F3EE Warm Cream Linen
NAVY_PRIMARY   = RGBColor(29, 38, 79)     # #1D264F Deep Navy Accent
WHITE_SURFACE  = RGBColor(255, 255, 255) # #FFFFFF Pure White
CARD_BORDER    = RGBColor(226, 232, 240)  # #E2E8F0 Subtle Border
TEXT_PRIMARY   = RGBColor(15, 23, 42)     # #0F172A Dark Slate
TEXT_MUTED     = RGBColor(71, 85, 105)    # #475569 Slate Muted

EMERALD        = RGBColor(5, 150, 105)    # #059669 SOTA / Winner
EMERALD_BG     = RGBColor(236, 253, 245)  # #ECFDF5
CRIMSON        = RGBColor(225, 29, 72)    # #E11D48 Wildfire Hazard
CRIMSON_BG     = RGBColor(255, 241, 242)  # #FFF1F2
AMBER          = RGBColor(217, 119, 6)    # #D97706 Warning / Limitation
AMBER_BG       = RGBColor(255, 251, 235)  # #FFFBEB
BLUE_ACCENT    = RGBColor(37, 99, 235)    # #2563EB Horizon 1h
BLUE_BG        = RGBColor(239, 246, 255)  # #EFF6FF
VIOLET_ACCENT  = RGBColor(124, 58, 237)   # #7C3AED Horizon 24h
VIOLET_BG      = RGBColor(245, 243, 255)  # #F5F3FF

FONT_HEADING   = "Arial"
FONT_BODY      = "Arial"
FONT_CODE      = "Consolas"

# ==========================================
# 2. HELPER FUNCTIONS
# ==========================================
def parse_speaker_notes(script_path):
    """Parse speaker notes from present2_dsr301m_script.md for each slide."""
    with open(script_path, "r", encoding="utf-8") as f:
        text = f.read()
    
    notes_dict = {}
    pattern = r"### 📍 SLIDE (\d+):[^\n]*\n(.*?)(?=\n---\n\n### 📍 SLIDE|\n# PHẦN B:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    for slide_num_str, content in matches:
        slide_num = int(slide_num_str)
        # Clean formatting for notes view
        clean_note = content.strip()
        # Remove markdown quotes '>'
        clean_note = re.sub(r"^>\s*", "", clean_note, flags=re.MULTILINE)
        notes_dict[slide_num] = clean_note
    return notes_dict

def set_slide_background_and_stripe(slide, prs):
    """Fills slide background with warm cream and adds the right navy stripe."""
    # 1. Warm Cream background shape
    bg = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), prs.slide_width, prs.slide_height
    )
    bg.fill.solid()
    bg.fill.fore_color.rgb = BG_COLOR
    bg.line.fill.background() # no line

    # 2. Right Navy Accent bar
    stripe_w = Inches(0.55)
    stripe_left = prs.slide_width - stripe_w
    stripe = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, stripe_left, Inches(0), stripe_w + Inches(0.5), prs.slide_height
    )
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = NAVY_PRIMARY
    stripe.line.fill.background()

def add_header(slide, badge_text, title_text, subtitle_text="", badge_color=BLUE_ACCENT):
    """Adds standard clean header hierarchy."""
    # Badge
    if badge_text:
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.5), Inches(0.3))
        tf = txBox.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.text = badge_text.upper()
        p.font.name = FONT_HEADING
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = badge_color

    # Title
    t_top = Inches(0.65) if badge_text else Inches(0.45)
    txBox2 = slide.shapes.add_textbox(Inches(0.8), t_top, Inches(11.5), Inches(0.55))
    tf2 = txBox2.text_frame
    tf2.word_wrap = True
    tf2.margin_left = tf2.margin_top = tf2.margin_right = tf2.margin_bottom = 0
    p2 = tf2.paragraphs[0]
    p2.text = title_text
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(23)
    p2.font.bold = True
    p2.font.color.rgb = NAVY_PRIMARY

    # Subtitle
    if subtitle_text:
        txBox3 = slide.shapes.add_textbox(Inches(0.8), t_top + Inches(0.48), Inches(11.5), Inches(0.3))
        tf3 = txBox3.text_frame
        tf3.word_wrap = True
        tf3.margin_left = tf3.margin_top = tf3.margin_right = tf3.margin_bottom = 0
        p3 = tf3.paragraphs[0]
        p3.text = subtitle_text
        p3.font.name = FONT_BODY
        p3.font.size = Pt(12)
        p3.font.color.rgb = TEXT_MUTED

def add_card(slide, left, top, width, height, bg_color=WHITE_SURFACE, border_color=CARD_BORDER, border_width=1.0):
    """Draws a card rectangle shape."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    card.fill.solid()
    card.fill.fore_color.rgb = bg_color
    if border_color:
        card.line.color.rgb = border_color
        card.line.width = Pt(border_width)
    else:
        card.line.fill.background()
    return card

def add_image_card(slide, img_path, left, top, width, height, border_color=CARD_BORDER):
    """Adds a framed image card."""
    card = add_card(slide, left, top, width, height, bg_color=WHITE_SURFACE, border_color=border_color)
    if os.path.exists(img_path):
        pad = Inches(0.06)
        slide.shapes.add_picture(img_path, left + pad, top + pad, width - (pad * 2), height - (pad * 2))
    return card

# ==========================================
# 3. BUILD SLIDES
# ==========================================
def build_all_slides(prs, notes):
    blank_layout = prs.slide_layouts[6] # completely blank slide

    # ----------------------------------------------------
    # SLIDE 01: TITLE COVER
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    
    # Subtitle Badge
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(10.5), Inches(0.4))
    p = tb.text_frame.paragraphs[0]
    p.text = "DSR301M · PRESENT 2"
    p.font.name = FONT_HEADING
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY

    # Main Title
    tb_title = slide.shapes.add_textbox(Inches(1.0), Inches(2.6), Inches(11.0), Inches(2.6))
    tf = tb_title.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.text = "PBL: COMPARATIVE US AQI\nTIME SERIES FORECASTING IN CALIFORNIA"
    p1.font.name = FONT_HEADING
    p1.font.size = Pt(36)
    p1.font.bold = True
    p1.font.color.rgb = NAVY_PRIMARY

    p2 = tf.add_paragraph()
    p2.text = "WITH EXTREME-EVENT EVALUATION"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(24)
    p2.font.color.rgb = NAVY_PRIMARY
    p2.space_before = Pt(14)

    p3 = tf.add_paragraph()
    p3.text = "Empirical Benchmark of 8 Baseline/SOTA Machine Learning Models Across 1h Nowcasting & 24h Day-Ahead"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(14)
    p3.font.italic = True
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(12)

    # Footer
    tb_foot = slide.shapes.add_textbox(Inches(1.0), Inches(6.1), Inches(10.5), Inches(0.5))
    p_foot = tb_foot.text_frame.paragraphs[0]
    p_foot.text = "GROUP 5  ·  FPT UNIVERSITY HCMC  ·  DATA SCIENCE PROJECT (FA2026)"
    p_foot.font.name = FONT_HEADING
    p_foot.font.size = Pt(14)
    p_foot.font.bold = True
    p_foot.font.color.rgb = NAVY_PRIMARY

    if 1 in notes:
        slide.notes_slide.notes_text_frame.text = notes[1]

    # ----------------------------------------------------
    # SLIDE 02: OUTLINE
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "AGENDA & ROADMAP", "OUTLINE", "Four-Phase Systematic Research & Benchmark Execution")

    pills_data = [
        ("Part 1", "Problem & Data Understanding",
         ["• Wildfire crisis & historic 496.0 AQI shock",
          "• 3 Critical research gaps (Metric, Leakage, Weather)",
          "• 181k Data audit & Jensen's inequality proof"]),
        ("Part 2", "Feature Engineering & Visualization",
         ["• Zero-leakage temporal split (Train/Val/Test)",
          "• Trim tail buffer defense against label shift",
          "• Physics-informed feature store (VPD, wind u, v)"]),
        ("Part 3", "Modeling, Evaluation",
         ["• 5 Algorithm families & 8 baseline/SOTA models",
          "• Official Test 2025 leaderboard & 168h tracking",
          "• Wildfire shock resilience, TreeSHAP & 3D diagnostics"]),
        ("Part 4", "Conclusion",
         ["• 4 Empirical breakthroughs & 3 technical limits",
          "• Milestone 3 MLOps: Asymmetric loss & FastAPI",
          "• Real-time California air quality dashboard & Q&A"])
    ]

    col_coords = [(Inches(0.8), Inches(1.55)), (Inches(6.6), Inches(1.55)),
                  (Inches(0.8), Inches(4.3)),  (Inches(6.6), Inches(4.3))]
    card_w, card_h = Inches(5.5), Inches(2.5)

    for i, (p_num, p_title, bullets) in enumerate(pills_data):
        c_left, c_top = col_coords[i]
        add_card(slide, c_left, c_top, card_w, card_h, bg_color=WHITE_SURFACE, border_color=NAVY_PRIMARY, border_width=1.8)
        
        tb = slide.shapes.add_textbox(c_left + Inches(0.3), c_top + Inches(0.2), card_w - Inches(0.6), card_h - Inches(0.4))
        tf = tb.text_frame
        tf.word_wrap = True
        
        p = tf.paragraphs[0]
        p.text = p_num
        p.font.name = FONT_HEADING
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = NAVY_PRIMARY

        p_t = tf.add_paragraph()
        p_t.text = p_title
        p_t.font.name = FONT_HEADING
        p_t.font.size = Pt(14)
        p_t.font.bold = True
        p_t.font.color.rgb = BLUE_ACCENT
        p_t.space_after = Pt(8)

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.text = b
            p_b.font.name = FONT_BODY
            p_b.font.size = Pt(11.5)
            p_b.font.color.rgb = TEXT_MUTED

    if 2 in notes:
        slide.notes_slide.notes_text_frame.text = notes[2]

    # ----------------------------------------------------
    # SLIDE 03: WILDFIRE CRISIS & PUBLIC HEALTH BURDEN
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "REAL-WORLD CRISIS & PUBLIC HEALTH BURDEN", "Wildfire Crisis & Hazardous Smoke Hazards in California", "Historic August Complex 2020 Megafire & Acute Respiratory Shocks", CRIMSON)

    # Left: Dual Images
    img1 = "artifacts/image/san-francisco-orange-sky.jpg"
    img2 = "artifacts/image/aqitableforcourse.png"
    add_image_card(slide, img1, Inches(0.8), Inches(1.5), Inches(5.3), Inches(3.1))
    add_image_card(slide, img2, Inches(0.8), Inches(4.75), Inches(5.3), Inches(2.2))

    # Right: 3 Fact Cards
    right_x = Inches(6.3)
    right_w = Inches(5.9)
    
    # Card 1: 496.0 AQI
    add_card(slide, right_x, Inches(1.5), right_w, Inches(1.65), bg_color=CRIMSON_BG, border_color=CRIMSON, border_width=1.5)
    tb = slide.shapes.add_textbox(right_x + Inches(0.25), Inches(1.62), right_w - Inches(0.5), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HISTORIC WILDFIRE PEAK: 496.0 AQI"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CRIMSON
    
    p2 = tf.add_paragraph()
    p2.text = "• Surpasses Hazardous threshold (301+) by +195 pts"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_PRIMARY
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = "• San Jose (Sept 2020) · Daylight blotted out across Bay Area"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = TEXT_MUTED

    # Card 2: Public Health Impact
    add_card(slide, right_x, Inches(3.3), right_w, Inches(1.7), bg_color=AMBER_BG, border_color=AMBER, border_width=1.5)
    tb = slide.shapes.add_textbox(right_x + Inches(0.25), Inches(3.42), right_w - Inches(0.5), Inches(1.45))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "ACUTE PUBLIC HEALTH BURDEN"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AMBER
    
    p2 = tf.add_paragraph()
    p2.text = "• >90% surge in emergency cardiopulmonary hospitalizations"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_PRIMARY
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = "• Wildfire PM2.5 exceeded WHO guidelines by >10x (Aguilera, 2021)"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = TEXT_MUTED

    # Card 3: Imbalance
    add_card(slide, right_x, Inches(5.15), right_w, Inches(1.8), bg_color=WHITE_SURFACE, border_color=NAVY_PRIMARY, border_width=1.5)
    tb = slide.shapes.add_textbox(right_x + Inches(0.25), Inches(5.27), right_w - Inches(0.5), Inches(1.55))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SEVERE DATA IMBALANCE (>85% CLEAN)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    
    p2 = tf.add_paragraph()
    p2.text = "• >85% of days are clean air baseline (AQI <= 50)"
    p2.font.name = FONT_BODY
    p2.font.size = Pt(11)
    p2.font.color.rgb = TEXT_PRIMARY
    p2.space_before = Pt(4)
    
    p3 = tf.add_paragraph()
    p3.text = "• Standard models optimize for normal air, failing rare toxic peaks"
    p3.font.name = FONT_BODY
    p3.font.size = Pt(10.5)
    p3.font.color.rgb = TEXT_MUTED

    if 3 in notes:
        slide.notes_slide.notes_text_frame.text = notes[3]

    # ----------------------------------------------------
    # SLIDE 04: 3 RESEARCH GAPS & DUAL FORECAST HORIZONS
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "PROBLEM STATEMENT & FORMULATION", "Three Research Gaps & Dual Operational Horizons", "Designing Purpose-Built Forecasting Architectures for Public Health Action")

    # Left: 3 Gaps Cards (Width 5.3 in)
    gap_x = Inches(0.8)
    gap_w = Inches(5.3)
    gaps_data = [
        ("GAP 1: METRIC MASKING", CRIMSON,
         "• Clean days (>85%) heavily dominate average MAE\n• Masks catastrophic failure during wildfire shocks (AQI > 150)"),
        ("GAP 2: LOOKAHEAD DATA LEAKAGE", AMBER,
         "• Random train/test split leaks future samples into training\n• Illusory R² > 0.95 collapses to negative in real deployment"),
        ("GAP 3: ATMOSPHERIC BLINDSPOT", BLUE_ACCENT,
         "• Surface sensor autocorrelation vanishes by 24h\n• Blind to weather shifts without Numerical Weather Prediction")
    ]
    for i, (g_title, g_color, g_text) in enumerate(gaps_data):
        g_top = Inches(1.5 + (i * 1.8))
        add_card(slide, gap_x, g_top, gap_w, Inches(1.65), bg_color=WHITE_SURFACE, border_color=g_color, border_width=1.5)
        tb = slide.shapes.add_textbox(gap_x + Inches(0.2), g_top + Inches(0.12), gap_w - Inches(0.4), Inches(1.4))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = g_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12.5)
        p.font.bold = True
        p.font.color.rgb = g_color
        p2 = tf.add_paragraph()
        p2.text = g_text
        p2.font.name = FONT_BODY
        p2.font.size = Pt(10.5)
        p2.font.color.rgb = TEXT_PRIMARY

    # Right: Dual Horizons (Width 5.9 in)
    hz_x = Inches(6.3)
    hz_w = Inches(5.9)

    # Horizon 1
    add_card(slide, hz_x, Inches(1.5), hz_w, Inches(2.65), bg_color=BLUE_BG, border_color=BLUE_ACCENT, border_width=2.0)
    tb = slide.shapes.add_textbox(hz_x + Inches(0.25), Inches(1.6), hz_w - Inches(0.5), Inches(2.45))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HORIZON 1 · NOWCASTING 1h (t+1)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    bullets_h1 = [
        "Tactical Action: Rapid outdoor worker alerts & traffic rerouting.",
        "Physical Driver: Autoregressive inertia (lag_0..3, roll_mean_3h, diff_1h).",
        "Top Result: Voting Ensemble achieves MAE 3.06 AQI, R² = 0.956."
    ]
    for b in bullets_h1:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(4)

    # Horizon 2
    add_card(slide, hz_x, Inches(4.3), hz_w, Inches(2.65), bg_color=VIOLET_BG, border_color=VIOLET_ACCENT, border_width=2.0)
    tb = slide.shapes.add_textbox(hz_x + Inches(0.25), Inches(4.4), hz_w - Inches(0.5), Inches(2.45))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "HORIZON 2 · DAY-AHEAD 24h (t+24)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = VIOLET_ACCENT
    bullets_h2 = [
        "Strategic Action: School closures & emergency ICU hospital staging 1 day prior.",
        "Physical Driver: Zero future sensors; powered by 24h NWP weather forecasts.",
        "Top Result: Voting Ensemble achieves MAE 11.30 AQI, R² = 0.617."
    ]
    for b in bullets_h2:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(4)

    if 4 in notes:
        slide.notes_slide.notes_text_frame.text = notes[4]

    # ----------------------------------------------------
    # SLIDE 05: DATA AUDIT & JENSEN'S INEQUALITY (+1.31)
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "DATA AUDIT & DISTRIBUTION PRESERVATION", "181k Dataset Audit & Mathematical Distribution Defense", "181,102 Hourly Records (2018–2025) Across 3 Topographic Basins")

    # Left: Distribution Image
    dist_img = "artifacts/image/paper_aqi_distribution.png"
    add_image_card(slide, dist_img, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.4))

    # Right: 4 Audit Rules + Jensen Proof Card
    r_x = Inches(6.4)
    r_w = Inches(5.8)

    # 4 Rules Card
    add_card(slide, r_x, Inches(1.5), r_w, Inches(2.55), bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(r_x + Inches(0.25), Inches(1.6), r_w - Inches(0.5), Inches(2.35))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "4 RIGOROUS DATA AUDIT PROTOCOLS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    audit_bullets = [
        "Missing Data: Linear interpolation strictly for gaps <= 6h (no synthetic noise).",
        "Spike Retention: 100% preservation of extreme events (up to 459.4 AQI).",
        "Timezone Alignment: UTC converted to Pacific Local Time (PDT/PST diurnal cycle).",
        "Topography: 3 contrasting air basins (San Jose, Fresno, Los Angeles)."
    ]
    for b in audit_bullets:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(3)

    # Jensen's Inequality Callout
    add_card(slide, r_x, Inches(4.2), r_w, Inches(2.7), bg_color=AMBER_BG, border_color=AMBER, border_width=1.5)
    tb = slide.shapes.add_textbox(r_x + Inches(0.25), Inches(4.3), r_w - Inches(0.5), Inches(2.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "WHY REJECT LOG-TRANSFORM (SKEWNESS = +1.31)?"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = AMBER
    jensen_bullets = [
        "Tree Monotonic Invariance: GBDT and RF partition on feature ranks; log transforms yield identical split trees.",
        "Jensen's Inequality Bias: E[exp(ŷ)] ≥ exp(E[ŷ]) systematically under-predicts life-threatening peak toxicity.",
        "Loss Penalty Compression: ln(400) - ln(300) = 0.287 ≈ ln(13) - ln(10), severely diluting penalties for disaster errors."
    ]
    for b in jensen_bullets:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(4)

    if 5 in notes:
        slide.notes_slide.notes_text_frame.text = notes[5]

    # ----------------------------------------------------
    # SLIDE 06: ZERO-LEAKAGE TEMPORAL SPLIT PROTOCOL
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "DATA PREPARATION & HYGIENE", "Zero-Leakage Temporal Split Protocol & Buffer Defense", "8-Year Sequential Partitioning Preserving Historical Independence")

    # Left: Timeline Graphic
    tl_img = "artifacts/image/aqi_categoty_timeline.png"
    add_image_card(slide, tl_img, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.4))

    # Right: 3 Dataset Cards + Buffer Explanation
    rx = Inches(6.4)
    rw = Inches(5.8)

    # Train
    add_card(slide, rx, Inches(1.5), rw, Inches(1.35), bg_color=WHITE_SURFACE, border_color=BLUE_ACCENT, border_width=1.2)
    tb = slide.shapes.add_textbox(rx + Inches(0.2), Inches(1.55), rw - Inches(0.4), Inches(1.2))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TRAIN SET · 2018–2023 (61.3% | 111,073 rows)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    p2 = tf.add_paragraph()
    p2.text = "Establishes baseline ambient distributions and trains on major historical megafires (Camp Fire 2018, August Complex 2020)."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    # Validation
    add_card(slide, rx, Inches(3.0), rw, Inches(1.45), bg_color=WHITE_SURFACE, border_color=AMBER, border_width=1.2)
    tb = slide.shapes.add_textbox(rx + Inches(0.2), Inches(3.05), rw - Inches(0.4), Inches(1.3))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "VALIDATION SET · 2024 (24.1% | 43,727 rows)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p2 = tf.add_paragraph()
    p2.text = "Encompasses Park Fire (July–Aug 2024, 4th largest in CA history); acts as real-world stress test for hyperparameter tuning and Early Stopping (patience=30)."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    # Test
    add_card(slide, rx, Inches(4.6), rw, Inches(1.2), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.5)
    tb = slide.shapes.add_textbox(rx + Inches(0.2), Inches(4.65), rw - Inches(0.4), Inches(1.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TEST SET · 2025 (14.5% | 26,292 rows)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p2 = tf.add_paragraph()
    p2.text = "Completely untouched out-of-sample partition; evaluated strictly once for final leaderboard."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    # Trim Tail Buffer
    add_card(slide, rx, Inches(5.95), rw, Inches(0.95), bg_color=BLUE_BG, border_color=NAVY_PRIMARY, border_width=1.2)
    tb = slide.shapes.add_textbox(rx + Inches(0.2), Inches(6.0), rw - Inches(0.4), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TRIM TAIL BUFFER PROTOCOL:"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "The last h rows of each station are trimmed on Train & Val (1h/24h) to eliminate label leakage from shift(-h)."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_PRIMARY

    if 6 in notes:
        slide.notes_slide.notes_text_frame.text = notes[6]

    # ----------------------------------------------------
    # SLIDE 07: PHYSICS-INFORMED FEATURE STORE
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "FEATURE ENGINEERING", "Physics-Informed Feature Store Architecture", "Specialized Multi-Horizon Feature Spaces Coupling Surface Sensors with Mesoscale NWP")

    # Left: 1h Space (X in R^{N x 22})
    add_card(slide, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.4), bg_color=BLUE_BG, border_color=BLUE_ACCENT, border_width=1.8)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(1.65), Inches(5.0), Inches(5.1))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NOWCASTING 1h MATRIX (X in R^{N x 22})"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    bullets_h1_feat = [
        "Sensor Autoregression: target_aqi_lag_0, lag_1, lag_2, lag_3",
        "Plume Acceleration: diff_1h = AQI_t - AQI_{t-1} (First-difference)",
        "Short-term Dynamics: roll_mean_3h, roll_std_3h",
        "Surface Meteorology: temp_2m, rh_2m, surface_pressure, rain, cloud_cover, wind_speed",
        "Orthogonal Wind: wind_u (West-East), wind_v (South-North)",
        "Cyclic Calendar: hour_sin, hour_cos, month_sin, month_cos, is_weekend"
    ]
    for b in bullets_h1_feat:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(6)

    # Right: 24h Space + Physical Drivers
    add_card(slide, Inches(6.4), Inches(1.5), Inches(5.8), Inches(3.2), bg_color=VIOLET_BG, border_color=VIOLET_ACCENT, border_width=1.8)
    tb = slide.shapes.add_textbox(Inches(6.6), Inches(1.65), Inches(5.4), Inches(2.9))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DAY-AHEAD 24h MATRIX (X in R^{N x 19})"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = VIOLET_ACCENT
    bullets_h2_feat = [
        "Sensor Isolation: ZERO ground-truth sensor features from t+1 to t+24.",
        "Macro Base Lags: lag_0, lag_24, lag_48, roll_mean_24h (prior to t-24).",
        "Future NWP Meteorology (W_{t+24}): future_temp_2m, future_rh_2m, future_wind_speed, future_wind_u, future_wind_v, future_rain, future_cloud_cover, future_surface_pressure, future_vpd_kpa.",
        "Future Calendar: future_hour_sin/cos, future_month_sin/cos, is_weekend."
    ]
    for b in bullets_h2_feat:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(4)

    # Physics Callout Box
    add_card(slide, Inches(6.4), Inches(4.85), Inches(5.8), Inches(2.05), bg_color=WHITE_SURFACE, border_color=NAVY_PRIMARY, border_width=1.2)
    tb = slide.shapes.add_textbox(Inches(6.6), Inches(4.95), Inches(5.4), Inches(1.85))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TWO CORE ATMOSPHERIC PHYSICAL DRIVERS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p_u = tf.add_paragraph()
    p_u.text = "1. Wind Vector Cartesian Decomposition (u, v): Decomposes polar wind into orthogonal components, resolving 359 deg <-> 1 deg discontinuity."
    p_u.font.name = FONT_BODY
    p_u.font.size = Pt(10)
    p_u.font.color.rgb = TEXT_PRIMARY
    p_v = tf.add_paragraph()
    p_v.text = "2. Vapor Pressure Deficit (VPD): Calculated from saturated vapor pressure and relative humidity; quantifies wildland fuel aridity and fire spread velocity."
    p_v.font.name = FONT_BODY
    p_v.font.size = Pt(10)
    p_v.font.color.rgb = TEXT_PRIMARY

    if 7 in notes:
        slide.notes_slide.notes_text_frame.text = notes[7]

    # ----------------------------------------------------
    # SLIDE 08: BENCHMARK MODEL SUITE & PIPELINE ENGINEERING
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "MODELING SPACE & PIPELINE ENGINEERING", "Benchmark Model Suite: 5 Algorithm Families", "Standardized Modeling Pipeline from Analytical Baselines to Tabular Deep Learning")

    # 5 Families Grid (Width ~2.2 in each)
    fams = [
        ("BASELINES", ["Persistence (y_t)", "Climatology (Hist. mean)", "Zero-training benchmark"], "#64748B"),
        ("LINEAR L2", ["Ridge Regression", "Analytical closed-form", "Fit time: ~0.18s"], "#2563EB"),
        ("BAGGING", ["Random Forest", "150 Decision Trees", "Subsampling variance cut"], "#0D9488"),
        ("GBDT SOTA", ["LightGBM (leaf-wise)", "XGBoost (exact Hessian)", "CatBoost (oblivious)"], "#7C3AED"),
        ("DEEP LEARNING", ["Tabular MLP Regressor", "2 Layers (64, 32 units)", "ReLU, Adam, Early stop"], "#EA580C")
    ]
    card_w = Inches(2.2)
    card_h = Inches(2.6)
    start_x = Inches(0.8)

    for i, (f_title, f_items, f_color_hex) in enumerate(fams):
        x = start_x + (i * Inches(2.32))
        add_card(slide, x, Inches(1.5), card_w, card_h, bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
        tb = slide.shapes.add_textbox(x + Inches(0.12), Inches(1.6), card_w - Inches(0.24), card_h - Inches(0.2))
        tf = tb.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = f_title
        p.font.name = FONT_HEADING
        p.font.size = Pt(12)
        p.font.bold = True
        p.font.color.rgb = RGBColor.from_string(f_color_hex[1:])
        for item in f_items:
            pi = tf.add_paragraph()
            pi.text = "• " + item
            pi.font.name = FONT_BODY
            pi.font.size = Pt(10)
            pi.font.color.rgb = TEXT_PRIMARY
            pi.space_before = Pt(4)

    # Meta-Ensemble Banner
    add_card(slide, Inches(0.8), Inches(4.25), Inches(11.4), Inches(0.65), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.5)
    tb_ens = slide.shapes.add_textbox(Inches(1.0), Inches(4.35), Inches(11.0), Inches(0.5))
    p = tb_ens.text_frame.paragraphs[0]
    p.text = "TOP-3 GBDT VOTING ENSEMBLE: Unweighted blending of LightGBM + XGBoost + CatBoost to eliminate idiosyncratic error."
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    # Bottom 2 Pipeline Rules (Split 50/50)
    add_card(slide, Inches(0.8), Inches(5.05), Inches(5.6), Inches(1.85), bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(Inches(1.0), Inches(5.15), Inches(5.2), Inches(1.65))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "DIFFERENTIAL FEATURE SCALING"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    bullets_pipe1 = [
        "Tree Models (GBDT, RF): Fed raw unscaled data (scale-invariant).",
        "Ridge & MLP: Require StandardScaler; scaler fit strictly on Train only, transform applied to Val and Test to eliminate leakage."
    ]
    for b in bullets_pipe1:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_PRIMARY

    add_card(slide, Inches(6.6), Inches(5.05), Inches(5.6), Inches(1.85), bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(Inches(6.8), Inches(5.15), Inches(5.2), Inches(1.65))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "SPATIAL CATEGORICAL ENCODING"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    bullets_pipe2 = [
        "Ridge & MLP: One-Hot Encoding (pd.get_dummies) avoids assigning misleading numeric distance between geographic basins.",
        "GBDT Suite: Native Integer Category allows histogram-based algorithms to automatically group gradient statistics by station."
    ]
    for b in bullets_pipe2:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_PRIMARY

    if 8 in notes:
        slide.notes_slide.notes_text_frame.text = notes[8]

    # ----------------------------------------------------
    # SLIDE 09: BENCHMARK LEADERBOARD (TEST 2025 OUT-OF-SAMPLE)
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "EMPIRICAL BENCHMARK RESULTS", "Official Leaderboard: Test 2025 Out-of-Sample Evaluation", "Comparative Performance on 26,200 Unseen Points (comprehensive_leaderboard.csv)")

    # Left: 2 Badges + Native PPTX Table
    lx = Inches(0.8)
    lw = Inches(5.4)

    # 2 KPI Winner Badges
    add_card(slide, lx, Inches(1.5), lw, Inches(0.65), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.5)
    tb = slide.shapes.add_textbox(lx + Inches(0.15), Inches(1.55), lw - Inches(0.3), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "1h WINNER: Voting Ensemble · MAE 3.06 AQI | R2 = 0.956 (-82.5% vs Clim.)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    add_card(slide, lx, Inches(2.25), lw, Inches(0.65), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.5)
    tb = slide.shapes.add_textbox(lx + Inches(0.15), Inches(2.3), lw - Inches(0.3), Inches(0.5))
    p = tb.text_frame.paragraphs[0]
    p.text = "24h WINNER: Voting Ensemble · MAE 11.30 AQI | R2 = 0.617 (-35.2% vs Clim.)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = EMERALD

    # Native PPTX Table
    rows = 9
    cols = 6
    tbl_shape = slide.shapes.add_table(rows, cols, lx, Inches(3.05), lw, Inches(3.7))
    tbl = tbl_shape.table
    tbl.columns[0].width = Inches(1.5) # Model
    tbl.columns[1].width = Inches(0.75) # MAE 1h
    tbl.columns[2].width = Inches(0.7)  # R2 1h
    tbl.columns[3].width = Inches(0.8)  # MAE 24h
    tbl.columns[4].width = Inches(0.75) # R2 24h
    tbl.columns[5].width = Inches(0.9)  # Time 24h

    table_data = [
        ["Model", "MAE 1h", "R² 1h", "MAE 24h", "R² 24h", "Fit (24h)"],
        ["Climatology", "17.53", "0.150", "17.45", "0.155", "1.44s"],
        ["Persistence", "3.61", "0.948", "13.02", "0.460", "0.00s"],
        ["Ridge Reg.", "3.72", "0.948", "11.86", "0.586", "0.18s"],
        ["LightGBM", "3.13", "0.954", "11.33", "0.617", "0.41s"],
        ["XGBoost", "3.10", "0.954", "11.36", "0.616", "0.67s"],
        ["CatBoost", "3.13", "0.954", "11.40", "0.608", "1.45s"],
        ["Tabular MLP", "3.26", "0.958", "13.08", "0.501", "81.62s"],
        ["Voting Ensem.", "3.06", "0.956", "11.30", "0.617", "0.20s"]
    ]

    for r_idx, row_vals in enumerate(table_data):
        for c_idx, val in enumerate(row_vals):
            cell = tbl.cell(r_idx, c_idx)
            cell.text = val
            p = cell.text_frame.paragraphs[0]
            p.font.name = FONT_CODE if c_idx > 0 else FONT_HEADING
            p.font.size = Pt(9.5) if r_idx > 0 else Pt(10)
            if r_idx == 0:
                p.font.bold = True
                p.font.color.rgb = WHITE_SURFACE
                cell.fill.solid()
                cell.fill.fore_color.rgb = NAVY_PRIMARY
            elif r_idx == 8: # Voting Ensemble
                p.font.bold = True
                p.font.color.rgb = EMERALD
                cell.fill.solid()
                cell.fill.fore_color.rgb = EMERALD_BG
            else:
                p.font.color.rgb = TEXT_PRIMARY
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE_SURFACE if r_idx % 2 == 1 else RGBColor(248, 250, 252)

    # Right: High-Res Leaderboard Bar Chart
    fig1 = "artifacts/figures/01_model_comparison_mae.png"
    add_image_card(slide, fig1, Inches(6.4), Inches(1.5), Inches(5.8), Inches(5.3))

    if 9 in notes:
        slide.notes_slide.notes_text_frame.text = notes[9]

    # ----------------------------------------------------
    # SLIDE 10: 168-HOUR CONTINUOUS FORECAST TRACKING
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "CONTINUOUS DYNAMIC EVALUATION", "168-Hour Continuous Tracking & Residual Dynamics", "January 09–15, 2025 at Fresno Central Valley Inversion Basin")

    # Left: Large Time-Series Graph
    fig2 = "artifacts/figures/02_actual_vs_predicted_1week.png"
    add_image_card(slide, fig2, Inches(0.8), Inches(1.5), Inches(6.8), Inches(5.3))

    # Right: 3 Residual Dynamics Badges
    rx = Inches(7.8)
    rw = Inches(4.5)

    add_card(slide, rx, Inches(1.5), rw, Inches(1.65), bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(rx + Inches(0.2), Inches(1.6), rw - Inches(0.4), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "FLAT BASELINE RESIDUALS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "Under ambient conditions (20–40 AQI), residual margins remain strictly within <5 AQI with zero systemic drift."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    add_card(slide, rx, Inches(3.3), rw, Inches(1.75), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.5)
    tb = slide.shapes.add_textbox(rx + Inches(0.2), Inches(3.4), rw - Inches(0.4), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "WINTER INVERSION PEAK TRACKING"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p2 = tf.add_paragraph()
    p2.text = "During Jan 11 pollution surge (EPA actual peaked at 73.4 AQI), Ridge collapsed to the mean, while Voting Ensemble surged directly to 68.2 AQI."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    add_card(slide, rx, Inches(5.2), rw, Inches(1.6), bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(rx + Inches(0.2), Inches(5.3), rw - Inches(0.4), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "PARASITIC NOISE CANCELLATION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "Blending Top-3 GBDT cancels individual tree variance spikes, producing smooth, reliable continuous operational forecasts."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    if 10 in notes:
        slide.notes_slide.notes_text_frame.text = notes[10]

    # ----------------------------------------------------
    # SLIDE 11: WILDFIRE EXTREME SHOCK RESILIENCE
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "EXTREME EVENT EVALUATION", "Wildfire Extreme Shock Resilience (24h Day-Ahead)", "Quantifying the Extreme Shock Gap and Resolving Variance Restriction Artifacts", CRIMSON)

    # Left: Resilience Plot
    fig3 = "artifacts/figures/03_wildfire_extreme_resilience.png"
    add_image_card(slide, fig3, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.3))

    # Right: 3 Shock Analysis Badges
    rx = Inches(6.4)
    rw = Inches(5.8)

    add_card(slide, rx, Inches(1.5), rw, Inches(1.65), bg_color=CRIMSON_BG, border_color=CRIMSON, border_width=1.5)
    tb = slide.shapes.add_textbox(rx + Inches(0.25), Inches(1.6), rw - Inches(0.5), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "EXTREME ERROR SHOCK GAP: +Δ 52.8 AQI"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = CRIMSON
    p2 = tf.add_paragraph()
    p2.text = "Normal Air (AQI <= 100): MAE = 9.9 AQI\nWildfire Smoke (AQI > 150): MAE = 62.6 AQI\nProves that whole-year metrics mask severe performance degradation during smoke crises."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    add_card(slide, rx, Inches(3.3), rw, Inches(1.75), bg_color=AMBER_BG, border_color=AMBER, border_width=1.5)
    tb = slide.shapes.add_textbox(rx + Inches(0.25), Inches(3.4), rw - Inches(0.5), Inches(1.5))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MATHEMATICAL ARTIFACT OF R² COLLAPSE"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p2 = tf.add_paragraph()
    p2.text = "Subsetting AQI > 150 shrinks sample variance (SS_tot), driving R² < 0 mathematically despite correct directional tracking. Evaluating extreme events requires dedicated classification metrics."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    add_card(slide, rx, Inches(5.2), rw, Inches(1.6), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.5)
    tb = slide.shapes.add_textbox(rx + Inches(0.25), Inches(5.3), rw - Inches(0.5), Inches(1.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "CLASSIFICATION SAFEGUARD: F1-SCORE = 0.825"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    p2 = tf.add_paragraph()
    p2.text = "At the critical 150+ AQI emergency threshold, GBDT maintains F1-Score = 0.825 (1h), confirming dependable early warning capability for public health protection."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(10.5)
    p2.font.color.rgb = TEXT_PRIMARY

    if 11 in notes:
        slide.notes_slide.notes_text_frame.text = notes[11]

    # ----------------------------------------------------
    # SLIDE 12: TREESHAP EXPLAINABILITY & PHYSICAL LAWS
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "EXPLAINABLE AI (XAI)", "TreeSHAP Interpretability: Regime Shift & Physical Laws", "Decomposing 24h Predictions into Physics-Aligned Shapley Attributions")

    # Left: SHAP Beeswarm Summary Plot
    fig5 = "artifacts/figures/05_shap_beeswarm_summary.png"
    add_image_card(slide, fig5, Inches(0.8), Inches(1.5), Inches(5.4), Inches(5.3))

    # Right: Regime Shift & Physics
    rx = Inches(6.4)
    rw = Inches(5.8)

    add_card(slide, rx, Inches(1.5), rw, Inches(2.6), bg_color=WHITE_SURFACE, border_color=NAVY_PRIMARY, border_width=1.5)
    tb = slide.shapes.add_textbox(rx + Inches(0.25), Inches(1.6), rw - Inches(0.5), Inches(2.4))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "QUANTITATIVE REGIME SHIFT (1h -> 24h)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    bullets_shap = [
        "1h Nowcasting: Sensor inertia accounts for >85% of SHAP attribution (target_aqi_lag_0 = 13.45 AQI, lag_1 = 2.49 AQI, diff_1h = 1.29 AQI).",
        "24h Day-Ahead: Future meteorology (W_{t+24}) takes command: future_wind_speed (2.68 AQI) > station_id (2.35 AQI) > future_temp_2m (1.28 AQI) > future_wind_v (1.24 AQI) > future_rain (1.10 AQI)."
    ]
    for b in bullets_shap:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10.5)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(4)

    add_card(slide, rx, Inches(4.25), rw, Inches(2.55), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.5)
    tb = slide.shapes.add_textbox(rx + Inches(0.25), Inches(4.35), rw - Inches(0.5), Inches(2.35))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "STRICT PHYSICAL LAW CONSISTENCY"
    p.font.name = FONT_HEADING
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    bullets_phys = [
        "High Wind Speed (Red dots) -> Negative SHAP: Strong winds trigger advective dispersion, diluting surface particulate concentrations.",
        "High Temperature (Red dots) -> Positive SHAP: Elevated heat drives photochemical secondary aerosol formation and desiccates wildland fuels.",
        "Wind Vectors (u, v): Directional vectors accurately capture smoke transport from Sierra Nevada slopes downward into the Central Valley."
    ]
    for b in bullets_phys:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(10)
        pb.font.color.rgb = TEXT_PRIMARY
        pb.space_before = Pt(3)

    if 12 in notes:
        slide.notes_slide.notes_text_frame.text = notes[12]

    # ----------------------------------------------------
    # SLIDE 13: THREE-DIMENSIONAL ERROR DIAGNOSTICS
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "ERROR MECHANISMS & FORENSICS", "Three-Dimensional Error Diagnostics & Topography", "Empirical Diagnostics Across Tail Shrinkage, Nocturnal Inversion, and Basin Geomorphology")

    col_w = Inches(3.6)
    c1_x = Inches(0.8)
    c2_x = Inches(4.7)
    c3_x = Inches(8.6)

    # Col 1: Parity Hexbin
    fig7 = "artifacts/figures/07_actual_vs_pred_parity_hexbin.png"
    add_image_card(slide, fig7, c1_x, Inches(1.5), col_w, Inches(3.4))
    add_card(slide, c1_x, Inches(5.05), col_w, Inches(1.8), bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(c1_x + Inches(0.15), Inches(5.15), col_w - Inches(0.3), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "TAIL SHRINKAGE (β = 0.54)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "Dense alignment on 1:1 line for safe levels (AQI <= 100). Regression slope β = 0.54 reveals symmetric MAE under-penalizes rare peaks, causing conservative tail shrinkage."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_PRIMARY

    # Col 2: Diurnal Hourly Curve
    fig8 = "artifacts/figures/08_diurnal_hourly_error_profile.png"
    add_image_card(slide, fig8, c2_x, Inches(1.5), col_w, Inches(3.4))
    add_card(slide, c2_x, Inches(5.05), col_w, Inches(1.8), bg_color=AMBER_BG, border_color=AMBER)
    tb = slide.shapes.add_textbox(c2_x + Inches(0.15), Inches(5.15), col_w - Inches(0.3), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "NOCTURNAL RADIATION INVERSION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = AMBER
    p2 = tf.add_paragraph()
    p2.text = "MAE plunges at midday (~8 AQI), but surges at night & dawn (22h–4h >14 AQI) as radiative surface cooling creates a thermal lid, trapping particulate matter in a shallow boundary layer."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_PRIMARY

    # Col 3: Spatial Basin
    fig9 = "artifacts/figures/09_spatial_basin_resilience.png"
    add_image_card(slide, fig9, c3_x, Inches(1.5), col_w, Inches(3.4))
    add_card(slide, c3_x, Inches(5.05), col_w, Inches(1.8), bg_color=WHITE_SURFACE, border_color=CARD_BORDER)
    tb = slide.shapes.add_textbox(c3_x + Inches(0.15), Inches(5.15), col_w - Inches(0.3), Inches(1.6))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "BASIN GEOMORPHOLOGY"
    p.font.name = FONT_HEADING
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = NAVY_PRIMARY
    p2 = tf.add_paragraph()
    p2.text = "San Jose MAE 9.90 (0 extremes, marine breeze) vs. Fresno MAE 10.95 (88 extremes, Central Valley bowl trap) vs. Los Angeles MAE 13.06 (231 extremes, San Gabriel barrier)."
    p2.font.name = FONT_BODY
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_PRIMARY

    if 13 in notes:
        slide.notes_slide.notes_text_frame.text = notes[13]

    # ----------------------------------------------------
    # SLIDE 14: CONCLUSIONS & ROADMAP
    # ----------------------------------------------------
    slide = prs.slides.add_slide(blank_layout)
    set_slide_background_and_stripe(slide, prs)
    add_header(slide, "SYNTHESIS & MILESTONE 3 ROADMAP", "Experimental Conclusions & Production Roadmap", "Milestone 2 Wrap-up, Technical Limitations & Final Defense Deliverables")

    lx = Inches(0.8)
    lw = Inches(6.8)

    # 4 Findings Card
    add_card(slide, lx, Inches(1.5), lw, Inches(1.7), bg_color=EMERALD_BG, border_color=EMERALD, border_width=1.2)
    tb = slide.shapes.add_textbox(lx + Inches(0.2), Inches(1.55), lw - Inches(0.4), Inches(1.55))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "4 CORE EMPIRICAL FINDINGS (MILESTONE 2)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = EMERALD
    findings = [
        "1. Standardized zero-leakage temporal split across 181k records with boundary trim buffer.",
        "2. Voting Ensemble leads overall: MAE 3.06 (R2 0.956) at 1h; MAE 11.30 (R2 0.617) at 24h.",
        "3. GBDT vastly outperforms Deep MLP (+1.78 MAE) and trains 200x faster (0.41s vs 81.62s).",
        "4. Uncovered physical mechanisms: Nocturnal inversion error spike & slope shrinkage (β = 0.54)."
    ]
    for b in findings:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = TEXT_PRIMARY

    # 3 Limitations Card
    add_card(slide, lx, Inches(3.3), lw, Inches(1.6), bg_color=AMBER_BG, border_color=AMBER, border_width=1.2)
    tb = slide.shapes.add_textbox(lx + Inches(0.2), Inches(3.35), lw - Inches(0.4), Inches(1.45))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "3 KNOWN TECHNICAL LIMITATIONS"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = AMBER
    limits = [
        "• Wildfire peak error gap remains elevated (62.6 AQI) due to symmetric MAE loss penalty.",
        "• Absence of satellite Aerosol Optical Depth (AOD) column data to resolve vertical smoke plume height.",
        "• Tabular MLP architecture lacks cross-station spatial attention mechanisms."
    ]
    for b in limits:
        pb = tf.add_paragraph()
        pb.text = b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = TEXT_PRIMARY

    # Roadmap Card
    add_card(slide, lx, Inches(5.0), lw, Inches(1.85), bg_color=BLUE_BG, border_color=BLUE_ACCENT, border_width=1.5)
    tb = slide.shapes.add_textbox(lx + Inches(0.2), Inches(5.05), lw - Inches(0.4), Inches(1.7))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "MILESTONE 3 PRODUCTION DELIVERABLES (FINAL DEFENSE)"
    p.font.name = FONT_HEADING
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = BLUE_ACCENT
    roadmap = [
        "1. Algorithm Optimization: Implement Asymmetric Huber Loss / Focal Loss to pull slope β -> 1.0.",
        "2. Production Packaging: Containerized FastAPI REST API delivering <50ms real-time inference.",
        "3. Web Dashboard: Interactive Streamlit/React dashboard for live California AQI early warning."
    ]
    for b in roadmap:
        pb = tf.add_paragraph()
        pb.text = "• " + b
        pb.font.name = FONT_BODY
        pb.font.size = Pt(9.5)
        pb.font.color.rgb = TEXT_PRIMARY

    # Right: Q&A Box
    rx = Inches(7.8)
    rw = Inches(4.5)
    add_card(slide, rx, Inches(1.5), rw, Inches(5.35), bg_color=NAVY_PRIMARY, border_color=BLUE_ACCENT, border_width=2.0)
    tb = slide.shapes.add_textbox(rx + Inches(0.3), Inches(2.2), rw - Inches(0.6), Inches(4.0))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = "Q&A DEFENSE SESSION"
    p.font.name = FONT_HEADING
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = WHITE_SURFACE
    p.alignment = PP_ALIGN.CENTER

    p2 = tf.add_paragraph()
    p2.text = "THANK YOU!"
    p2.font.name = FONT_HEADING
    p2.font.size = Pt(28)
    p2.font.bold = True
    p2.font.color.rgb = EMERALD
    p2.alignment = PP_ALIGN.CENTER
    p2.space_before = Pt(24)

    p3 = tf.add_paragraph()
    p3.text = "Group 5 sincerely thanks the Examination Board and Faculty for your guidance and attention.\n\nWe welcome all questions and feedback."
    p3.font.name = FONT_BODY
    p3.font.size = Pt(13)
    p3.font.color.rgb = RGBColor(226, 232, 240)
    p3.alignment = PP_ALIGN.CENTER
    p3.space_before = Pt(24)

    if 14 in notes:
        slide.notes_slide.notes_text_frame.text = notes[14]

def main():
    script_path = "presentations/present2/present2_dsr301m_script.md"
    out_path = "presentations/present2/present2_dsr301m.pptx"
    
    print(f"Reading speaker script from: {script_path}")
    notes = parse_speaker_notes(script_path)
    print(f"Loaded notes for {len(notes)} slides.")

    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    print("Building 14 slides...")
    build_all_slides(prs, notes)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    prs.save(out_path)
    print(f"Successfully generated: {out_path} ({os.path.getsize(out_path)} bytes)")

if __name__ == "__main__":
    main()
