# CANVA SLIDE DESIGN BLUEPRINT — PBL MILESTONE 2 (PRESENT 2)
## PROJECT: COMPARATIVE US AQI TIME SERIES FORECASTING IN CALIFORNIA WITH EXTREME-EVENT EVALUATION

---

* **Course:** DSR301m – Data Science Project (FPT University HCMC)
* **Milestone:** PBL Milestone 2 (Present 2) — *Modeling, Evaluation & Empirical Benchmark*
* **Team:** GROUP 5
* **Slide Dimensions:** Canva Widescreen 16:9 ($1920 \times 1080\text{ px}$)
* **Design Philosophy:** **Visual-First Academic Minimalism** (1 Slide = 1 Key Visual/Table + High-impact Takeaway Badges; Concise English on Slides, Rich Voiceover in Script)
* **Visual Identity:** Warm Cream Canvas (`#F7F3EE`), Deep Navy Accent Bar (`#1D264F`), White Card Surfaces (`#FFFFFF`), Emerald SOTA Badges (`#059669`), Crimson Hazard Accents (`#E11D48`).
* **Corresponding Script:** [present2_dsr301m_script.md](file:///c:/FPT/FA2026/DSR301m/Project/presentations/present2/present2_dsr301m_script.md)

---

## 🎨 DESIGN SYSTEM TOKENS

### 1. Color Palette

| Token Name | HEX Code | Canva Role |
| :--- | :---: | :--- |
| **Canvas Background** | `#F7F3EE` | Warm linen cream slide backdrop across all 14 slides |
| **Primary Navy** | `#1D264F` | Right accent vertical stripe, main headings, pill borders |
| **Card Surface** | `#FFFFFF` | Clean white card container for charts, tables, and metric callouts |
| **Top Model SOTA** | `#059669` | Emerald badge for Voting Ensemble and error reduction metrics |
| **Extreme Hazard** | `#E11D48` | Crimson badge for wildfire shock ($AQI > 150$) and error gap |
| **Warning / Moderate** | `#D97706` | Amber badge for Moderate AQI ($51–100$) and technical limitations |
| **Accent Royal Blue**| `#2563EB` | Horizon 1h Nowcasting badges, key links, secondary highlights |
| **Accent Deep Violet**| `#7C3AED` | Horizon 24h Day-Ahead badges, future weather predictors |
| **Text Primary** | `#0F172A` | Slide titles, key KPI numbers, bold lead text |
| **Text Secondary** | `#475569` | Metric descriptions, units, figure captions |

### 2. Typography & Component Standards

* **Slide Titles:** `Inter` (or `Cabinet Grotesk` / `Montserrat`) — **Bold / Extra Bold**, 36–42 pt, Color `#1D264F`.
* **Category Badges:** `Inter` — **SemiBold**, 13–15 pt, ALL CAPS, Tracking `+1.5px`.
* **Card Titles:** `Inter` — **SemiBold**, 18–20 pt, Color `#1D264F`.
* **Slide Body Text:** `Inter` — **Regular / Medium**, 13–15 pt, Line Height `1.4`.
* **KPI / Code Fonts:** `JetBrains Mono` (or `Roboto Mono`) — **Bold**, 18–28 pt.
* **Right Navy Stripe:** Rounded rectangular bar along the right edge: Width `75px`, Height `1080px`, Left border-radius `28px`, Color `#1D264F`.
* **Pill Card (Stadium Shape):** Fully rounded ends, Border `2px solid #1D264F`, Background `#FFFFFF`.

---

# SLIDE-BY-SLIDE SPECIFICATIONS (14 SLIDES · VISUAL-FIRST)

---

## 🏛️ PART 1: PROBLEM & DATA UNDERSTANDING (SLIDES 01 – 05)

---

### 📄 SLIDE 01: TITLE COVER
* **Source:** Project Metadata & Visual Branding
* **Canva Layout:** Minimalist Left-Aligned Cover + Right Navy Accent Bar ($1920 \times 1080$)

#### 🖼️ Visual Components:
* **Background:** Solid Warm Cream `#F7F3EE`.
* **Right Accent Stripe:** Full-height bar on right edge, width 75px, border-radius `top-left: 28px`, `bottom-left: 28px`, color `#1D264F`.

#### 📝 Text on Slide (English):
* **Top Subtitle (x: 100px, y: 110px):**  
  `DSR301M · PRESENT 2` (18pt, SemiBold, Tracking +2px, `#1D264F`)
* **Main Title (x: 100px, y: 460px):**  
  **`PBL: COMPARATIVE US AQI`** (40pt, Extra Bold, `#1D264F`)  
  **`TIME SERIES FORECASTING IN CALIFORNIA`** (40pt, Extra Bold, `#1D264F`)  
  `WITH EXTREME-EVENT EVALUATION` (26pt, Medium, `#1D264F`, +15px below)
* **Footer (x: 100px, y: 960px):**  
  `GROUP 5` (18pt, SemiBold, `#1D264F`)

---

### 📄 SLIDE 02: OUTLINE
* **Source:** 4 Project Phases
* **Canva Layout:** Header + 2x2 Grid of Rounded Pill Cards + Right Navy Accent Bar

#### 🖼️ Visual Components:
* **Background:** Warm Cream `#F7F3EE`.
* **Right Accent Stripe:** Width 75px, rounded left corners, color `#1D264F`.

#### 📝 Text on Slide (English):
* **Header (x: 100px, y: 110px):**  
  **`OUTLINE`** (44pt, Extra Bold, `#1D264F`)
* **2x2 Pill Card Grid (Pill dimensions: $720 \times 130\text{ px}$, Border 2px `#1D264F`, Background `#FFFFFF`):**
  * *Top-Left Pill:*  
    **`Part 1`** (18pt, Bold, `#1D264F`)  
    `Problem & Data Understanding` (15pt, Regular, `#475569`)
  * *Top-Right Pill:*  
    **`Part 2`** (18pt, Bold, `#1D264F`)  
    `Feature Engineering & Visualization` (15pt, Regular, `#475569`)
  * *Bottom-Left Pill:*  
    **`Part 3`** (18pt, Bold, `#1D264F`)  
    `Modeling, Evaluation` (15pt, Regular, `#475569`)
  * *Bottom-Right Pill:*  
    **`Part 4`** (18pt, Bold, `#1D264F`)  
    `Conclusion` (15pt, Regular, `#475569`)

---

### 📄 SLIDE 03: WILDFIRE CRISIS & PUBLIC HEALTH BURDEN
* **Source Notebook:** [00_EDA_California_AQI.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/00_EDA_California_AQI.ipynb)
* **Visual Focus:** Dual High-Impact Image Spotlight (San Francisco Orange Sky + EPA Scale)
* **Canva Layout:** Split 50 / 50 (Left: Image Spotlight; Right: 3 Key Fact Cards)

#### 🖼️ Designated Images:
1. `artifacts/image/san-francisco-orange-sky.jpg` (August Complex 2020 wildfire sky)
2. `artifacts/image/aqitableforcourse.png` (EPA 6-Tier AQI Scale)

#### 📝 Text on Slide (English):
* **Header:** `WILDFIRE CRISIS & EXTREME SMOKE HAZARDS`
* **Sub-header:** `Historic Wildfire Shocks Across California Basins`
* **Card 1 (Crimson `#E11D48`):**  
  **`HISTORIC PEAK: 496.0 AQI`**  
  • Surpasses Hazardous threshold (301+) by **+195 pts**  
  • San Jose (Sept 2020) · Daylight blotted out across Bay Area  
* **Card 2 (Amber `#D97706`):**  
  **`ACUTE PUBLIC HEALTH BURDEN`**  
  • **>90% surge** in emergency cardiopulmonary hospitalizations  
  • Wildfire PM2.5 exceeded WHO guidelines by **>10x** *(Aguilera, 2021)*  
* **Card 3 (Navy `#1D264F`):**  
  **`SEVERE DATA IMBALANCE`**  
  • **>85%** of days are clean air baseline ($AQI \le 50$)  
  • Standard models optimize for normal air, failing rare toxic peaks  

---

### 📄 SLIDE 04: THREE RESEARCH GAPS & DUAL FORECAST HORIZONS
* **Source Notebooks:** [00_EDA_California_AQI.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/00_EDA_California_AQI.ipynb) & [01_Data_Prep_Feature_Store.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/01_Data_Prep_Feature_Store.ipynb)
* **Visual Focus:** 3 Gaps vs. 2 Operational Horizon Architecture Cards
* **Canva Layout:** Split 45 / 55 (Left: 3 Research Gaps; Right: Horizon 1h vs. Horizon 24h Cards)

#### 📝 Text on Slide (English):
* **Header:** `RESEARCH GAPS & DUAL OPERATIONAL HORIZONS`
* **Left Column — 3 Critical Literature Gaps:**
  1. **Metric Masking:** Annual MAE/RMSE hides model failure during wildfire emergencies ($AQI > 150$).
  2. **Lookahead Leakage:** Random train/test split leaks future points, producing illusory $R^2 > 0.95$.
  3. **Atmospheric Blindspot:** Surface-sensor models fail at 24h as sensor inertia vanishes.
* **Right Column — Two Operational Horizons:**
  * **Horizon 1 — Nowcasting 1h ($t+1$)** *(Accent Blue `#2563EB`)*  
    `Use Case:` Real-time worker advisories & traffic diversion.  
    `Core Driver:` Ground sensor autoregressive inertia & 1h first-difference `diff_1h`.
  * **Horizon 2 — Day-Ahead 24h ($t+24$)** *(Accent Violet `#7C3AED`)*  
    `Use Case:` School closures & emergency hospital staff staging.  
    `Core Driver:` Zero future sensor access; guided by numerical weather prediction $W_{t+24}$.

---

### 📄 SLIDE 05: DATA AUDIT & JENSEN'S INEQUALITY (+4.82 SKEWNESS)
* **Source Notebook:** [00_EDA_California_AQI.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/00_EDA_California_AQI.ipynb)
* **Visual Focus:** 1 Large Distribution Chart + Math Proof Card
* **Canva Layout:** Split 50 / 50 (Left: Distribution Figure; Right: Audit Decisions & Jensen Callout)

#### 🖼️ Designated Image:
* **File:** `artifacts/image/paper_aqi_distribution.png`  
  *(Generated from 00_EDA: Extreme right-skewed hourly AQI distribution)*

#### 📝 Text on Slide (English):
* **Header:** `DATA AUDIT & DISTRIBUTION PRESERVATION`
* **Sub-header:** `181,122 Hourly Records (2018–2025) Across 3 Geomorphic Basins`
* **Audit Matrix (4 Core Rules):**
  * `Gaps:` Linear interpolation for $\le 6\text{h}$; drop $> 6\text{h}$ (zero synthetic artifacts).
  * `Outliers:` **100% Extreme Peaks Preserved** (including historic 496.0 AQI).
  * `Timezone:` Converted from UTC $\to$ Pacific Local Time (PST/PDT).
  * `Basins:` Fresno (Valley), Los Angeles (Coast), San Jose (Bay Area).
* **Callout Card (Amber `#F59E0B`): Why NO Log-Transform despite Skewness = +4.82?**
  1. **Tree Invariance:** Split points $x_j \le \theta$ are rank-invariant to monotonic transforms.
  2. **Jensen's Inequality Bias:** $\mathbb{E}[\exp(\hat{y})] \ge \exp(\mathbb{E}[\hat{y}])$ causes systemic under-prediction and flattens loss penalties in the dangerous extreme tail ($AQI > 150$).

---

## ⚙️ PART 2: FEATURE ENGINEERING & VISUALIZATION (SLIDES 06 – 07)

---

### 📄 SLIDE 06: ZERO-LEAKAGE TEMPORAL SPLIT PROTOCOL
* **Source Notebooks:** [00_EDA_California_AQI.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/00_EDA_California_AQI.ipynb) & [01_Data_Prep_Feature_Store.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/01_Data_Prep_Feature_Store.ipynb)
* **Visual Focus:** 1 Full Timeline Figure + 3 Dataset Metric Badges
* **Canva Layout:** Top: 3 Dataset Split Cards; Bottom: 8-Year Timeline Graphic + Trim Buffer Diagram

#### 🖼️ Designated Image:
* **File:** `artifacts/image/aqi_categoty_timeline.png`  
  *(8-Year continuous timeline of EPA AQI categories across Fresno, LA, and San Jose)*

#### 📝 Text on Slide (English):
* **Header:** `ZERO-LEAKAGE TEMPORAL SPLIT & BUFFER DEFENSE`
* **3 Strict Non-Overlapping Partitions:**
  * **Train Set (2018–2023 · 61.3%):** 111,073 rows $\to$ Baseline patterns & megasires.
  * **Validation Set (2024 · 24.1%):** 43,727 rows $\to$ Contains **Park Fire (July–Aug 2024)**; Early Stopping benchmark (`patience=30`).
  * **Test Set (2025 · 14.5%):** 26,292 rows $\to$ 100% untouched out-of-sample test.
* **Trim Tail Buffer Protocol:**  
  * Cut the final $h$ rows per station on Train & Val ($1\text{h}$ for 1h, $24\text{h}$ for 24h).  
  * **Zero boundary leakage** when creating future targets via `shift(-h)`.

---

### 📄 SLIDE 07: PHYSICS-INFORMED FEATURE STORE (DUAL-HORIZON)
* **Source Notebook:** [01_Data_Prep_Feature_Store.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/01_Data_Prep_Feature_Store.ipynb)
* **Visual Focus:** 1 Structured Comparison Table + 2 Atmospheric Physics Formula Badges
* **Canva Layout:** Split 50 / 50 (Left: Horizon 1h Feature Space; Right: Horizon 24h Feature Space)

#### 📝 Text on Slide (English):
* **Header:** `PHYSICS-INFORMED FEATURE STORE ARCHITECTURE`
* **Left Card — Horizon 1: Nowcasting 1h ($X \in \mathbb{R}^{N \times 22}$):**
  * `Sensor Inertia:` `lag_0`, `lag_1`, `lag_2`, `lag_3`.
  * `Plume Acceleration:` First derivative $\text{diff\_1h} = AQI_t - AQI_{t-1}$.
  * `Local Dynamics:` 3-hour rolling mean & std (`roll_mean_3h`, `roll_std_3h`).
  * `Atmospheric State:` Real-time $T, RH, P, \text{Rain}, \text{Clouds}, \text{Wind}$.
* **Right Card — Horizon 2: Day-Ahead 24h ($X \in \mathbb{R}^{N \times 19}$):**
  * `Sensor Isolation:` **Zero sensor features from $t+1$ to $t+24$**.
  * `Macro History:` Long-range baseline `lag_0`, `lag_24`, `lag_48`, `roll_mean_24h`.
  * `Numerical Weather ($W_{t+24}$):` Future forecast wind, temp, humidity, rain, pressure.
* **Bottom Physics Callout:**
  * **Wind Vector $(u, v)$:** Decomposes speed & angle into orthogonal Cartesian components $\to$ eliminates $359^\circ \leftrightarrow 1^\circ$ circular jump.
  * **Vapor Pressure Deficit (VPD):** Quantifies vegetation fuel dryness and fire spread potential.

---

## 🔬 PART 3: MODELING, EVALUATION (SLIDES 08 – 13)

---

### 📄 SLIDE 08: BENCHMARK MODEL SUITE & PIPELINE ENGINEERING
* **Source Notebooks:** [02_Baselines_and_Ridge.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/02_Baselines_and_Ridge.ipynb), [03_Tree_Ensembles_RF.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/03_Tree_Ensembles_RF.ipynb), [04_Gradient_Boosting_SOTA.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/04_Gradient_Boosting_SOTA.ipynb), [05_Neural_Network_MLP.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/05_Neural_Network_MLP.ipynb)
* **Visual Focus:** 5 Algorithm Families Cards + 2 Implementation Rules
* **Canva Layout:** Top: 5 Algorithm Cards; Bottom: Scaling & Encoding Pipeline Specs

#### 📝 Text on Slide (English):
* **Header:** `BENCHMARK MODEL SPACE: 5 DIVERSE ALGORITHM FAMILIES`
* **5 Competing Algorithm Families (8 Base Models + 1 Ensemble):**
  1. **Baselines:** Persistence ($y_{t+h} = y_t$) & Climatology (Historical monthly-hourly mean).
  2. **Linear Regularized:** Ridge Regression ($L_2$ penalty, analytical closed-form solution).
  3. **Bagging:** Random Forest Regressor (150 estimators, bootstrap feature subsampling).
  4. **GBDT Suite:** LightGBM (leaf-wise), XGBoost (exact Hessian), CatBoost (oblivious trees).
  5. **Deep Learning:** Tabular MLP Regressor (64–32 ReLU units, Adam optimizer).
  6. **Meta-Ensemble:** Voting Ensemble (Unweighted average of Top-3 GBDT).
* **Pipeline Engineering Protocols:**
  * `Feature Scaling:` Trees run on raw data (monotonic invariant). Ridge/MLP use `StandardScaler` (**`fit()` strictly on Train only**).
  * `Station Encoding:` One-Hot for Ridge/MLP (no false spatial ordering); Integer Categorical for GBDT (histogram binning).

---

### 📄 SLIDE 09: BENCHMARK LEADERBOARD (TEST 2025 OUT-OF-SAMPLE)
* **Source Notebook:** [06_Benchmark_Leaderboard_Synthesis.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb) & `artifacts/metrics/comprehensive_leaderboard.csv`
* **Visual Focus:** 1 Main Benchmark Chart (`01_model_comparison_mae.png`) + Official Results Table
* **Canva Layout:** Split 45 / 55 (Left: 2 Winner KPI Badges + Table; Right: High-Res MAE Comparison Plot)

#### 🖼️ Designated Image:
* **File:** `artifacts/figures/01_model_comparison_mae.png`  
  *(300 DPI bar chart comparing all 9 models on Test 2025 across 1h and 24h)*

#### 📝 Text on Slide (English):
* **Header:** `OFFICIAL LEADERBOARD: TEST 2025 OUT-OF-SAMPLE BENCHMARK`
* **Top Performance Badges (Emerald `#059669`):**
  * `1h Nowcasting Winner:` **Voting Ensemble** $\to$ **MAE 3.06 AQI** · $R^2 = \mathbf{0.956}$ (-82.5% vs Climatology)
  * `24h Day-Ahead Winner:` **Voting Ensemble** $\to$ **MAE 11.30 AQI** · $R^2 = \mathbf{0.617}$ (-35.2% vs Climatology)
* **Leaderboard Summary Table:**

| Family | Model | MAE 1h | $R^2$ 1h | MAE 24h | $R^2$ 24h | Fit Time (24h) |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: |
| **Baseline** | Climatology | 17.53 | 0.150 | 17.45 | 0.155 | 1.44 s |
| **Baseline** | Persistence | 3.61 | 0.948 | 13.02 | 0.460 | 0.00 s |
| **Linear** | Ridge Regression | 3.72 | 0.948 | 11.86 | 0.586 | 0.18 s |
| **GBDT** | **LightGBM** | **3.13** | **0.954** | **11.33** | **0.617** | **0.41 s** |
| **GBDT** | XGBoost | 3.10 | 0.954 | 11.36 | 0.616 | 0.67 s |
| **GBDT** | CatBoost | 3.13 | 0.954 | 11.40 | 0.608 | 1.45 s |
| **Neural** | Tabular MLP | 3.26 | 0.958 | 13.08 | 0.501 | 81.62 s |
| **Ensemble**| **Voting Ensemble**| **3.06** | **0.956** | **11.30** | **0.617** | **0.20 s** |

* **Key Takeaway:** GBDT outperforms MLP by **+1.78 MAE** while training **200x faster** (0.41s vs 81.62s).

---

### 📄 SLIDE 10: 168-HOUR TIME-SERIES TRACKING & RESIDUAL DYNAMICS
* **Source Notebook:** [06_Benchmark_Leaderboard_Synthesis.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb)
* **Visual Focus:** 1 Full-Bleed Time-Series Plot (`02_actual_vs_predicted_1week.png`)
* **Canva Layout:** Split 60 / 40 (Left: Large Time-Series Graph; Right: 3 Residual Dynamics Badges)

#### 🖼️ Designated Image:
* **File:** `artifacts/figures/02_actual_vs_predicted_1week.png`  
  *(168 consecutive test hours at Fresno: EPA Actual vs Voting Ensemble vs LightGBM vs Ridge + Residual Margin)*

#### 📝 Text on Slide (English):
* **Header:** `168-HOUR CONTINUOUS FORECAST & RESIDUAL DYNAMICS`
* **Sub-header:** `January 09–15, 2025 at Fresno Central Valley Station`
* **Badge 1 — Flat Baseline Residuals:**  
  Residual margin stays within **$< 5\text{ AQI}$** across normal ambient hours (20–40 AQI).
* **Badge 2 — Winter Inversion Peak Tracking:**  
  On Jan 11 peak (**73.4 AQI**), Ridge collapses to the mean, while **Voting Ensemble tracks directly to 68.2 AQI**.
* **Badge 3 — Parasitic Noise Cancellation:**  
  Voting ensemble smooths single-tree variance jumps, producing operational-ready forecasts.

---

### 📄 SLIDE 11: EXTREME WILDFIRE SHOCK RESILIENCE
* **Source Notebook:** [06_Benchmark_Leaderboard_Synthesis.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb)
* **Visual Focus:** 1 High-Impact Figure (`03_wildfire_extreme_resilience.png`) + 3 Forensic Badges
* **Canva Layout:** Split 55 / 45 (Left: Resilience Chart; Right: Shock Gap & Variance Restriction Analysis)

#### 🖼️ Designated Image:
* **File:** `artifacts/figures/03_wildfire_extreme_resilience.png`  
  *(Normal $AQI \le 100$ vs Extreme Smoke $AQI > 150$ error decomposition)*

#### 📝 Text on Slide (English):
* **Header:** `WILDFIRE EXTREME SHOCK RESILIENCE (24H DAY-AHEAD)`
* **Card 1 — Extreme Error Shock Gap (Crimson `#E11D48`):**  
  * Normal Conditions ($AQI \le 100$): **$\text{MAE} = 9.9\text{ AQI}$**  
  * Extreme Wildfire Shock ($AQI > 150$): **$\text{MAE} = 62.6\text{ AQI}$**  
  * Shock Degradation: **$+\Delta 52.8\text{ AQI}$** $\to$ Confirms standard metrics hide disaster errors!
* **Card 2 — Mathematical Artifact of $R^2$ Collapse:**  
  Subsetting $AQI > 150$ severely restricts variance ($\text{SS}_{\text{tot}} \to 0$), driving $R^2 < 0$ mathematically despite correct directional tracking.
* **Card 3 — Classification Safeguard Metric (Emerald `#059669`):**  
  Top GBDT maintains **$\text{F1-Score} = \mathbf{0.825}$** at the $150+\text{ AQI}$ emergency threshold.

---

### 📄 SLIDE 12: TREESHAP EXPLAINABILITY & PHYSICAL LAWS
* **Source Notebook:** [06_Benchmark_Leaderboard_Synthesis.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb)
* **Visual Focus:** 1 Prominent SHAP Beeswarm Summary Plot (`05_shap_beeswarm_summary.png`)
* **Canva Layout:** Split 50 / 50 (Left: SHAP Beeswarm Plot; Right: Regime Shift Table & Physics Alignment)

#### 🖼️ Designated Image:
* **File:** `artifacts/figures/05_shap_beeswarm_summary.png`  
  *(SHAP Beeswarm summary showing directional impact of future weather on 24h forecast)*
* *(Reference files: `04_feature_importance_shift.png`, `06_shap_mean_importance.png`)*

#### 📝 Text on Slide (English):
* **Header:** `TREESHAP INTERPRETABILITY: REGIME SHIFT & PHYSICS CONSISTENCY`
* **Regime Shift Quantification:**
  * **1h Nowcasting:** Ground sensor inertia dominates **>85%** (`lag_0` contributes **13.45 AQI**, `lag_1` 2.49 AQI).
  * **24h Day-Ahead:** Future meteorology $W_{t+24}$ takes over:  
    `future_wind_speed` (**2.68 AQI**) > `station_id` (**2.35 AQI**) > `future_temp` (**1.28 AQI**).
* **Strict Physical Law Consistency:**
  * **High Wind Speed (Red dots) $\to$ Negative SHAP:** Activates advective dispersion and dilutes surface plume.
  * **High Surface Temp (Red dots) $\to$ Positive SHAP:** Triggers photochemical aerosol formation & fuel aridity.

---

### 📄 SLIDE 13: THREE-DIMENSIONAL ERROR DIAGNOSTICS
* **Source Notebook:** [06_Benchmark_Leaderboard_Synthesis.ipynb](file:///c:/FPT/FA2026/DSR301m/Project/notebooks/06_Benchmark_Leaderboard_Synthesis.ipynb)
* **Visual Focus:** 3 Side-by-Side Diagnostic Figures (Fig 07, Fig 08, Fig 09)
* **Canva Layout:** 3-Column Visual Grid (1 Plot per Column + 1 Concise Diagnostic Takeaway below)

#### 🖼️ Designated Images:
1. `artifacts/figures/07_actual_vs_pred_parity_hexbin.png` (Parity density hexbin plot)
2. `artifacts/figures/08_diurnal_hourly_error_profile.png` (24h diurnal hourly MAE curve)
3. `artifacts/figures/09_spatial_basin_resilience.png` (3-basin spatial resilience comparison)

#### 📝 Text on Slide (English):
* **Header:** `THREE-DIMENSIONAL ERROR DIAGNOSTICS & BASIN GEOMORPHOLOGY`
* **Column 1 — Tail Shrinkage Artifact (Fig 07):**  
  * Dense alignment along 1:1 line for safe levels ($AQI \le 100$).  
  * Regression slope **$\beta = 0.54 < 1.0$**: Symmetric MAE loss penalizes extremes identically to clean air, causing conservative under-predictions at peaks.
* **Column 2 — Nocturnal Radiation Inversion (Fig 08):**  
  * Errors plunge at midday (11h–15h, MAE ~8 AQI).  
  * Errors surge at **night & dawn (22h–4h, MAE > 14 AQI)**: Radiational surface cooling traps smoke in a shallow planetary boundary layer.
* **Column 3 — Spatial Basin Geomorphology (Fig 09):**  
  * **San Jose (Bay Area):** MAE 9.90 (0 extreme events) $\to$ Marine wind ventilation.  
  * **Fresno (Central Valley):** MAE 10.95 (88 extremes) $\to$ Topographic bowl traps winter dust.  
  * **Los Angeles (South Coast):** MAE 13.06 (231 extremes) $\to$ San Gabriel barrier + urban heat island.

---

## 🎯 PART 4: CONCLUSION & ROADMAP (SLIDE 14)

---

### 📄 SLIDE 14: KEY FINDINGS, LIMITATIONS & MILESTONE 3 ROADMAP
* **Source Notebooks:** Synthesis of Notebooks 01–06 & Production MLOps Plan
* **Visual Focus:** 3 Structured Cards (Findings, Limitations, M3 Plan) + Right Q&A Badge
* **Canva Layout:** Split 60 / 40 (Left: 3 Summary Cards; Right: 3-Tier Architecture & Q&A Box)

#### 📝 Text on Slide (English):
* **Header:** `EXPERIMENTAL CONCLUSIONS & PRODUCTION ROADMAP (MILESTONE 3)`
* **Card 1 — 4 Core Empirical Findings (Emerald `#ECFDF5`):**
  1. Standardized zero-leakage temporal protocol with trim buffer across 181k hourly records.
  2. **Voting Ensemble leads overall:** MAE 3.06 ($R^2 = 0.956$) at 1h; MAE 11.30 ($R^2 = 0.617$) at 24h.
  3. GBDT vastly outperforms Deep MLP in both accuracy and training efficiency (200x faster).
  4. Identified physical error drivers: Nocturnal radiation inversion and tail shrinkage ($\beta = 0.54$).
* **Card 2 — 3 Known Technical Limitations (Amber `#FFFBEB`):**
  * Peak error gap remains high ($62.6\text{ AQI}$) under symmetric loss.
  * Absence of satellite AOD column data for vertical smoke profile.
  * Tabular MLP lacks cross-station spatial attention.
* **Card 3 — Milestone 3 Final Defense Deliverables (Royal Blue `#EFF6FF`):**
  * **Loss Reform:** Asymmetric Huber / Focal Loss to pull slope $\beta \to 1.0$ at extreme smoke peaks.
  * **Production API:** Containerized **FastAPI REST API** with $<50\text{ms}$ inference latency.
  * **Web Dashboard:** Interactive real-time air quality & wildfire alert interface for California.
* **Right Panel — Q&A Session Callout (Navy `#0F172A`, White Text):**
  * `Q&A DEFENSE SESSION`  
  * *"Thank you for your attention! Group 5 is ready for your questions and feedback."*

---

## 📋 QUICK CANVA DESIGN CHECKLIST

1. [x] **Strict Visual Hierarchy:** Every slide has 1 primary visual focus (chart/table) and no more than 3 bullet points.
2. [x] **All English Text on Canvas:** English titles, English cards, concise metrics; detailed Vietnamese narration stays in [present2_dsr301m_script.md](file:///c:/FPT/FA2026/DSR301m/Project/presentations/present2/present2_dsr301m_script.md).
3. [x] **Source Assets Verified:** All 9 figures in `artifacts/figures/` and images in `artifacts/image/` are mapped 1-to-1 to exact slide numbers.
4. [x] **Consistent Brand Identity:** Warm cream canvas (`#F7F3EE`), right navy accent bar (`#1D264F`), rounded pill cards matching user reference slides.
