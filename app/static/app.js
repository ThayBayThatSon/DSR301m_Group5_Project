// ============================================================================
// California Air Quality Observatory & Forecasting System
// Mission-Control Operations Frontend Logic
// (Live Operations layout · Analytics & Benchmarking layout · System Log drawer)
// ============================================================================

const APP_STATE = {
  theme: "dark",
  activeWindow: "win1",
  liveRegion: "FRES",
  liveSeq: 0,
  liveStationCache: {},
  prefetchedStations: false,
  meta: null,
  liveData: null,
  simulatedForecast: null,
  shapHorizon: "1h",
  trajViewMode: "rec",
  heatmapStation: "CURRENT",
  map: null,
  mapTileLayers: {},
  mapMarker: null,
  mapWindLine: null,
  mapWindHead: null,
  charts: {
    trajectory: null,
    shap: null,
    diurnalHeatmap: null,
    win2_FRES: null,
    win2_LA: null,
    win2_SJ: null,
  },
  whatIf: {
    timer: null,
    controller: null,
    seq: 0,
    actual: null, // slider-space values of the real observation
  },
  syslogOpen: false,
  win2: {
    scenario: "1h",
    activePresetId: "latest_today",
    startDate: "",
    endDate: "",
    sourceMode: "seamless",
    regionFilter: "ALL",
    residualMode: false,
    stationView: "ALL",
    activeGroup: "top",
    loadSeq: 0,
    selectedModels: new Set([
      "LSTM (PyTorch)",
      "Voting Ensemble",
      "LightGBM",
      "MLP (64, 32)",
    ]),
    dashboardData: null,
  },
};

const STATION_KEYS = ["FRES", "LA", "SJ"];
const HORIZON_KEYS = ["+1h", "+2h", "+3h", "+24h"];
const WHATIF_DEBOUNCE_MS = 140;

// ---------------------------------------------------------------------------
// Small DOM helpers
// ---------------------------------------------------------------------------
function byId(id) {
  return document.getElementById(id);
}

function setText(id, value) {
  const el = byId(id);
  if (el) el.textContent = value;
}

/** Toggle `is-active` on a group of segmented / toggle buttons. */
function setSegActive(ids, activeId) {
  ids.forEach((id) => {
    const el = byId(id);
    if (!el) return;
    const on = id === activeId;
    el.classList.toggle("is-active", on);
    el.setAttribute("aria-selected", on ? "true" : "false");
  });
}

function fmtNum(v, digits = 1) {
  const n = Number(v);
  return Number.isFinite(n) ? n.toFixed(digits) : "--";
}

function fmtSigned(v, digits = 1) {
  const n = Number(v);
  if (!Number.isFinite(n)) return "--";
  const s = n.toFixed(digits);
  return n > 0 ? `+${s}` : s;
}

function degToCompass(deg) {
  const dirs = ["N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE", "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"];
  const d = ((Number(deg) % 360) + 360) % 360;
  return dirs[Math.round(d / 22.5) % 16];
}

// Global busy indicator (thin progress bar under the header + dimmed targets)
let BUSY_COUNT = 0;
function beginBusy(targetIds = []) {
  BUSY_COUNT += 1;
  byId("global-progress")?.classList.add("is-on");
  targetIds.forEach((id) => byId(id)?.classList.add("is-busy"));
}
function endBusy(targetIds = []) {
  BUSY_COUNT = Math.max(0, BUSY_COUNT - 1);
  if (BUSY_COUNT === 0) byId("global-progress")?.classList.remove("is-on");
  targetIds.forEach((id) => byId(id)?.classList.remove("is-busy"));
}

// ---------------------------------------------------------------------------
// THEME MANAGEMENT (Light / Dark Mode with Persistence)
// ---------------------------------------------------------------------------
function initTheme() {
  const saved = localStorage.getItem("california_aqi_theme");
  const prefersDark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
  const initialTheme = saved || (prefersDark ? "dark" : "dark");
  applyTheme(initialTheme, false);
}

function toggleTheme() {
  const next = APP_STATE.theme === "dark" ? "light" : "dark";
  applyTheme(next, true);
}

function applyTheme(theme, notify = true) {
  APP_STATE.theme = theme;
  try {
    localStorage.setItem("california_aqi_theme", theme);
  } catch (_) {}

  const html = document.documentElement;
  html.classList.remove("dark", "light");
  html.classList.add(theme);

  const iconEl = byId("theme-icon");
  const labelEl = byId("theme-label");
  if (iconEl) iconEl.textContent = theme === "dark" ? "🌙" : "☀️";
  if (labelEl) labelEl.textContent = theme === "dark" ? "Dark Mode" : "Light Mode";

  // Re-render UI components that have theme-dependent colors
  if (APP_STATE.liveData) {
    renderCurrentObservation(APP_STATE.liveData.station_meta, APP_STATE.liveData.forecast);
    updateSatelliteMap(APP_STATE.liveData.station_meta, APP_STATE.liveData.forecast.current);
    renderHorizonCards();
    renderLiveTrajectoryChart(false);
    renderLiveShapChart(false);
  }
  if (APP_STATE.win2.dashboardData) {
    renderKpiCards(APP_STATE.win2.dashboardData);
    renderAllStationWindowCharts();
  }
}

function getChartThemeColors() {
  const isLight = APP_STATE.theme === "light";
  return {
    isLight,
    text: isLight ? "#475569" : "#64748b",
    axisLineColor: isLight ? "#cbd5e1" : "#1e293b",
    splitLineColor: isLight ? "#e2e8f0" : "#1e293b",
    splitLineType: isLight ? "dashed" : "solid",
    actualLineColor: isLight ? "#0f172a" : "#ffffff",
    actualItemColor: isLight ? "#0f172a" : "#ffffff",
    yAxisCategoryColor: isLight ? "#334155" : "#cbd5e1",
    legendText: isLight ? "#475569" : "#94a3b8",
    ghostOpacity: isLight ? 0.45 : 0.35,
    tooltip: {
      backgroundColor: isLight ? "#ffffff" : "#0f172a",
      borderColor: isLight ? "#cbd5e1" : "#334155",
      textStyle: {
        color: isLight ? "#0f172a" : "#f8fafc",
        fontSize: 11,
        fontFamily: "JetBrains Mono, monospace",
      },
      extraCssText: isLight ? "box-shadow: 0 4px 16px rgba(0,0,0,0.12);" : "box-shadow: 0 4px 16px rgba(0,0,0,0.4);",
      confine: true,
    },
  };
}

// EPA AQI Standard 6-Tier Styling Helper (Technical, Operational & Semantic)
function getAqiTheme(aqi) {
  const val = Number(aqi || 0);
  const isLight = APP_STATE.theme === "light";

  if (val <= 50) {
    return {
      tier: "good",
      tierClass: "aqi-tier-good",
      label: "Good (0–50)",
      short: "Good",
      hex: "#10b981",
      bgLight: "#ecfdf5",
      borderLight: "#a7f3d0",
      textLight: "#065f46",
      glow: "rgba(16, 185, 129, 0.16)",
      badgeClass: isLight
        ? "bg-emerald-50 text-emerald-800 border-emerald-300 shadow-sm"
        : "bg-emerald-950 text-emerald-300 border-emerald-800",
      circleClass: isLight
        ? "border-emerald-500 bg-emerald-50 text-emerald-700 shadow-sm"
        : "border-emerald-600 bg-emerald-950/40 text-emerald-400",
      advice:
        "Air quality is satisfactory, and air pollution poses little or no risk for outdoor activities.",
    };
  }
  if (val <= 100) {
    return {
      tier: "moderate",
      tierClass: "aqi-tier-moderate",
      label: "Moderate (51–100)",
      short: "Moderate",
      hex: "#eab308", // Official US EPA Yellow
      bgLight: "#fefce8",
      borderLight: "#fef08a",
      textLight: "#854d0e",
      glow: "rgba(234, 179, 8, 0.20)",
      badgeClass: isLight
        ? "bg-yellow-50 text-yellow-900 border-yellow-400 shadow-sm"
        : "bg-yellow-950/80 text-yellow-300 border-yellow-700",
      circleClass: isLight
        ? "border-yellow-500 bg-yellow-50 text-yellow-900 shadow-sm"
        : "border-yellow-500 bg-yellow-950/40 text-yellow-300",
      advice:
        "Air quality is acceptable. Unusually sensitive individuals should consider limiting prolonged outdoor exertion.",
    };
  }
  if (val <= 150) {
    return {
      tier: "sensitive",
      tierClass: "aqi-tier-sensitive",
      label: "Unhealthy for Sensitive (101–150)",
      short: "Sensitive",
      hex: "#f97316",
      bgLight: "#fff7ed",
      borderLight: "#fed7aa",
      textLight: "#9a3412",
      glow: "rgba(249, 115, 22, 0.16)",
      badgeClass: isLight
        ? "bg-orange-50 text-orange-800 border-orange-300 shadow-sm"
        : "bg-orange-950 text-orange-300 border-orange-800",
      circleClass: isLight
        ? "border-orange-500 bg-orange-50 text-orange-700 shadow-sm"
        : "border-orange-600 bg-orange-950/40 text-orange-400",
      advice:
        "Members of sensitive groups (respiratory, cardiac, elderly, children) should reduce prolonged outdoor exertion.",
    };
  }
  if (val <= 200) {
    return {
      tier: "unhealthy",
      tierClass: "aqi-tier-unhealthy",
      label: "Unhealthy (151–200)",
      short: "Unhealthy",
      hex: "#ef4444",
      bgLight: "#fef2f2",
      borderLight: "#fecdd3",
      textLight: "#9f1239",
      glow: "rgba(239, 68, 68, 0.16)",
      badgeClass: isLight
        ? "bg-rose-50 text-rose-800 border-rose-300 shadow-sm"
        : "bg-rose-950 text-rose-300 border-rose-800",
      circleClass: isLight
        ? "border-rose-500 bg-rose-50 text-rose-700 shadow-sm"
        : "border-rose-600 bg-rose-950/40 text-rose-400",
      advice:
        "Air quality alert: Some members of the general public may experience health effects; sensitive groups may experience more serious effects.",
    };
  }
  if (val <= 300) {
    return {
      tier: "very-unhealthy",
      tierClass: "aqi-tier-very-unhealthy",
      label: "Very Unhealthy (201–300)",
      short: "Very Unhealthy",
      hex: "#8b5cf6",
      bgLight: "#f5f3ff",
      borderLight: "#ddd6fe",
      textLight: "#5b21b6",
      glow: "rgba(139, 92, 246, 0.18)",
      badgeClass: isLight
        ? "bg-purple-50 text-purple-800 border-purple-300 shadow-sm"
        : "bg-purple-950 text-purple-300 border-purple-800",
      circleClass: isLight
        ? "border-purple-500 bg-purple-50 text-purple-700 shadow-sm"
        : "border-purple-600 bg-purple-950/40 text-purple-400",
      advice:
        "Health alert: Serious risk of health effects increased for everyone. Avoid prolonged outdoor exertion.",
    };
  }
  return {
    tier: "hazardous",
    tierClass: "aqi-tier-hazardous",
    label: "Hazardous (>300)",
    short: "Hazardous",
    hex: "#881337",
    bgLight: "#fff1f2",
    borderLight: "#fecdd3",
    textLight: "#4c0519",
    glow: "rgba(136, 19, 55, 0.22)",
    badgeClass: isLight
      ? "bg-rose-100 text-rose-900 border-rose-400 shadow-sm"
      : "bg-rose-950 text-rose-200 border-rose-800",
    circleClass: isLight
      ? "border-rose-700 bg-rose-100 text-rose-900 shadow-sm"
      : "border-rose-700 bg-rose-950 text-rose-200",
    advice:
      "Health warning of emergency conditions: The entire population is likely to be affected. Keep windows closed and run HEPA filtration.",
  };
}

// ============================================================================
// INITIALIZATION
// ============================================================================
document.addEventListener("DOMContentLoaded", async () => {
  initTheme();
  initLeafletMap();
  initEChartsInstances();
  initResizeObservers();
  initWhatIfSliderVisuals();
  initCollapsiblePanels();

  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && APP_STATE.syslogOpen) toggleSysLogDrawer(false);
    if ((e.key === "t" || e.key === "T") && !["INPUT", "SELECT", "TEXTAREA"].includes(e.target.tagName)) {
      toggleTheme();
    }
  });

  try {
    const metaResp = await fetch("/api/meta");
    APP_STATE.meta = await metaResp.json();
    updateQuotaHeader(APP_STATE.meta.quota);
    renderWildfirePresetButtons();
    renderModelChips();
  } catch (err) {
    console.error("Failed to load metadata:", err);
  }

  await loadLiveForecast("FRES", false);

  window.addEventListener("resize", () => {
    Object.values(APP_STATE.charts).forEach((ch) => {
      if (ch) ch.resize();
    });
    if (APP_STATE.map) APP_STATE.map.invalidateSize();
  });
});

/**
 * Charts & map live inside flex/grid cells whose size changes with layout
 * (window switch, station-view switch, drawer, viewport). ResizeObserver keeps
 * them crisp without manual setTimeout juggling.
 */
function initResizeObservers() {
  if (typeof ResizeObserver === "undefined") return;
  const pending = new Set();
  let raf = 0;
  const flush = () => {
    raf = 0;
    pending.forEach((fn) => fn());
    pending.clear();
  };
  const ro = new ResizeObserver((entries) => {
    entries.forEach((entry) => {
      const fn = entry.target.__onResize;
      if (fn) pending.add(fn);
    });
    if (!raf) raf = requestAnimationFrame(flush);
  });

  const chartDomMap = {
    trajectory: "live-trajectory-chart",
    shap: "live-shap-chart",
    win2_FRES: "win2-chart-FRES",
    win2_LA: "win2-chart-LA",
    win2_SJ: "win2-chart-SJ",
  };
  Object.entries(chartDomMap).forEach(([key, domId]) => {
    const dom = byId(domId);
    if (!dom) return;
    dom.__onResize = () => APP_STATE.charts[key] && APP_STATE.charts[key].resize();
    ro.observe(dom);
  });

  const mapDom = byId("satellite-map");
  if (mapDom) {
    mapDom.__onResize = () => APP_STATE.map && APP_STATE.map.invalidateSize();
    ro.observe(mapDom);
  }
}

// ============================================================================
// WINDOW NAVIGATION
// ============================================================================
function switchWindow(winId) {
  APP_STATE.activeWindow = winId;
  const sections = {
    win1: byId("window-1"),
    win2: byId("window-2"),
  };

  Object.keys(sections).forEach((k) => {
    sections[k].classList.toggle("hidden", k !== winId);
  });
  setSegActive(["tab-btn-win1", "tab-btn-win2"], `tab-btn-${winId}`);

  // Header station selector: show in Window 1, hide in Window 2
  const stSel = byId("header-station-selector");
  if (stSel) stSel.classList.toggle("hidden", winId !== "win1");

  window.scrollTo({ top: 0 });

  if (winId === "win1") {
    requestAnimationFrame(() => {
      if (APP_STATE.map) APP_STATE.map.invalidateSize();
      if (APP_STATE.charts.trajectory) APP_STATE.charts.trajectory.resize();
      if (APP_STATE.charts.shap) APP_STATE.charts.shap.resize();
    });
  } else if (winId === "win2") {
    renderWildfirePresetButtons();
    if (!APP_STATE.win2.dashboardData) {
      loadDashboardWindow();
    } else {
      requestAnimationFrame(() => {
        STATION_KEYS.forEach((rk) => {
          const ch = APP_STATE.charts[`win2_${rk}`];
          if (ch) ch.resize();
        });
      });
    }
  }
}

function updateQuotaHeader(quota) {
  if (!quota) return;
  const callsEl = byId("quota-calls-badge");
  const savedEl = byId("quota-saved-badge");
  if (callsEl) {
    const calls = quota.calls_today ?? quota.api_calls_today ?? 0;
    const limit = quota.daily_limit ? Number(quota.daily_limit).toLocaleString() : "10,000";
    callsEl.textContent = `${calls} / ${limit}`;
  }
  if (savedEl) {
    savedEl.textContent = `Optimized load: ${quota.saved_percent}% (${quota.cache_hits_today} cache hits)`;
  }
}

// ============================================================================
// LEAFLET SATELLITE MAP & WIND VECTOR
// ============================================================================
function initLeafletMap() {
  const mapEl = byId("satellite-map");
  if (!mapEl) return;

  APP_STATE.map = L.map("satellite-map", {
    zoomControl: true,
    attributionControl: true,
  }).setView([36.7854, -119.7732], 10);

  APP_STATE.mapTileLayers.satellite = L.tileLayer(
    "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
    {
      maxZoom: 18,
      attribution: "Tiles &copy; Esri — Source: Esri, Maxar, USDA, USGS",
    }
  );

  APP_STATE.mapTileLayers.topo = L.tileLayer(
    "https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png",
    {
      maxZoom: 17,
      attribution: "Map data: &copy; OpenStreetMap, SRTM | OpenTopoMap",
    }
  );

  APP_STATE.mapTileLayers.satellite.addTo(APP_STATE.map);
}

function setMapLayer(mode) {
  if (!APP_STATE.map) return;
  if (mode === "topo") {
    APP_STATE.map.removeLayer(APP_STATE.mapTileLayers.satellite);
    APP_STATE.mapTileLayers.topo.addTo(APP_STATE.map);
    setSegActive(["map-btn-sat", "map-btn-topo"], "map-btn-topo");
  } else {
    APP_STATE.map.removeLayer(APP_STATE.mapTileLayers.topo);
    APP_STATE.mapTileLayers.satellite.addTo(APP_STATE.map);
    setSegActive(["map-btn-sat", "map-btn-topo"], "map-btn-sat");
  }
}

function updateWindHud(currentObs) {
  if (!currentObs) return;
  const speed = Number(currentObs.wind_speed_10m || 0);
  const fromDeg = Number(currentObs.wind_direction_10m || 0);
  const arrow = byId("map-wind-arrow");
  // Arrow glyph points north; rotate to the direction the wind blows TOWARDS.
  if (arrow) arrow.style.transform = `rotate(${(fromDeg + 180) % 360}deg)`;
  setText("map-wind-text", `${fmtNum(speed, 1)} km/h · from ${degToCompass(fromDeg)} (${Math.round(fromDeg)}°)`);
}

function updateSatelliteMap(meta, currentObs) {
  if (!APP_STATE.map || !meta || !currentObs) return;
  const lat = meta.lat;
  const lon = meta.lon;
  const aqi = currentObs.aqi;
  const theme = getAqiTheme(aqi);

  APP_STATE.map.flyTo([lat, lon], 10, { duration: 0.9 });

  if (APP_STATE.mapMarker) APP_STATE.map.removeLayer(APP_STATE.mapMarker);
  if (APP_STATE.mapWindLine) APP_STATE.map.removeLayer(APP_STATE.mapWindLine);
  if (APP_STATE.mapWindHead) APP_STATE.map.removeLayer(APP_STATE.mapWindHead);

  const markerHtml = `
    <div class="aqi-map-pin" style="
      position: relative;
      width: 40px; height: 44px;
      display: flex; flex-direction: column; align-items: center; justify-content: flex-start;
      filter: drop-shadow(0 3px 6px rgba(0,0,0,0.45));
    ">
      <div style="
        width: 38px; height: 32px; border-radius: 6px;
        background: ${theme.hex}; color: ${theme.tier === "moderate" ? "#0f172a" : "#ffffff"};
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        font-family: 'JetBrains Mono', monospace; font-weight: 800; font-size: 13.5px;
        border: 2px solid #ffffff;
        box-shadow: inset 0 1px 2px rgba(255,255,255,0.4);
        line-height: 1;
      ">
        <span>${Math.round(aqi)}</span>
      </div>
      <div style="
        width: 0; height: 0;
        border-left: 6px solid transparent;
        border-right: 6px solid transparent;
        border-top: 8px solid ${theme.hex};
        margin-top: -1px;
      "></div>
    </div>
  `;

  const icon = L.divIcon({
    className: "custom-aqi-pin",
    html: markerHtml,
    iconSize: [40, 44],
    iconAnchor: [20, 40],
    popupAnchor: [0, -38],
  });

  const tc = getChartThemeColors();
  APP_STATE.mapMarker = L.marker([lat, lon], { icon })
    .addTo(APP_STATE.map)
    .bindPopup(
      `<div style="font-family: Inter, sans-serif; color: ${tc.isLight ? "#0f172a" : "#f8fafc"}; min-width: 200px; padding: 2px;">
        <div style="font-weight: 700; font-size: 13px; color: ${tc.isLight ? "#0f172a" : "#ffffff"};">${meta.name}</div>
        <div style="font-size: 11px; color: ${tc.text}; margin-bottom: 5px;">Basin: ${meta.basin} (${meta.elevation_m}m)</div>
        <div style="font-size: 12px; font-family: 'JetBrains Mono', monospace;">AQI: <strong>${aqi}</strong> [${theme.short}]</div>
        <div style="font-size: 11px; font-family: 'JetBrains Mono', monospace; color: ${tc.isLight ? "#334155" : "#cbd5e1"};">PM2.5: ${currentObs.pm25} µg/m³ · T: ${currentObs.temperature_2m}°C</div>
        <div style="font-size: 11px; font-family: 'JetBrains Mono', monospace; color: ${tc.isLight ? "#334155" : "#cbd5e1"};">Wind: ${currentObs.wind_speed_10m} km/h (${currentObs.wind_direction_10m}°)</div>
      </div>`
    );

  const windSpeed = Number(currentObs.wind_speed_10m || 5);
  const windFromDeg = Number(currentObs.wind_direction_10m || 0);
  const blowToRad = ((windFromDeg + 180) * Math.PI) / 180.0;
  const arrowLenDeg = Math.min(0.13, Math.max(0.04, windSpeed * 0.0035));
  const endLat = lat + arrowLenDeg * Math.cos(blowToRad);
  const endLon = lon + (arrowLenDeg * Math.sin(blowToRad)) / Math.cos((lat * Math.PI) / 180.0);

  APP_STATE.mapWindLine = L.polyline(
    [
      [lat, lon],
      [endLat, endLon],
    ],
    {
      color: "#38bdf8",
      weight: 2.5,
      dashArray: "5, 4",
      opacity: 0.9,
    }
  ).addTo(APP_STATE.map);

  APP_STATE.mapWindHead = L.circleMarker([endLat, endLon], {
    radius: 4,
    color: "#0284c7",
    fillColor: "#38bdf8",
    fillOpacity: 1,
  })
    .addTo(APP_STATE.map)
    .bindTooltip(`Wind Vector (${windSpeed} km/h)`, {
      direction: "top",
    });

  updateWindHud(currentObs);
}

// ============================================================================
// ECHARTS INITIALIZATION
// ============================================================================
function initEChartsInstances() {
  const trajDom = byId("live-trajectory-chart");
  const shapDom = byId("live-shap-chart");
  const hmDom = byId("historical-diurnal-heatmap-chart");
  if (trajDom) APP_STATE.charts.trajectory = echarts.init(trajDom);
  if (shapDom) APP_STATE.charts.shap = echarts.init(shapDom);
  if (hmDom) APP_STATE.charts.diurnalHeatmap = echarts.init(hmDom);

  STATION_KEYS.forEach((rk) => {
    const dom = byId(`win2-chart-${rk}`);
    if (dom) {
      const ch = echarts.init(dom);
      ch.group = "win2-sync-group";
      APP_STATE.charts[`win2_${rk}`] = ch;
    }
  });
  echarts.connect("win2-sync-group");
}

const DARK_TOOLTIP = {
  backgroundColor: "#0f172a",
  borderColor: "#334155",
  textStyle: { color: "#f8fafc", fontSize: 11, fontFamily: "JetBrains Mono, monospace" },
  confine: true,
};

// ============================================================================
// WINDOW 1: LIVE FORECAST, CACHE GUARD, TREESHAP & WHAT-IF
// ============================================================================
const LIVE_BUSY_TARGETS = ["live-obs-card", "forecast-card", "shap-card"];

function applyLiveForecastData(data) {
  APP_STATE.liveData = data;
  APP_STATE.simulatedForecast = null;
  updateQuotaHeader(data.quota);
  renderCacheBanner(data.cache_info);
  renderCurrentObservation(data.station_meta, data.forecast);
  updateSatelliteMap(data.station_meta, data.forecast.current);
  resetWhatIfSlidersToCurrent(data.forecast.current);
  renderHorizonCards();
  renderLiveTrajectoryChart(false);
  renderLiveShapChart(false);
  renderFetchHistoryTable(data.history_logs);
  loadHistoricalHeatmap(APP_STATE.heatmapStation === "ALL" ? "ALL" : data.region_key);
}

function selectLiveRegion(regionKey) {
  const toggle = byId("wi-wildfire-toggle");
  if (toggle && toggle.checked) {
    toggleWildfireSimulation(false);
  }
  APP_STATE.liveRegion = regionKey;
  setSegActive(STATION_KEYS.map((rk) => `st-btn-${rk}`), `st-btn-${regionKey}`);
  loadLiveForecast(regionKey, false);
}

function forceRefreshLive() {
  // Clear in-memory cache for current station on manual force refresh
  delete APP_STATE.liveStationCache[APP_STATE.liveRegion];
  loadLiveForecast(APP_STATE.liveRegion, true);
}

async function loadLiveForecast(regionKey, forceRefresh = false) {
  const seq = ++APP_STATE.liveSeq;
  cancelPendingWhatIf();

  // Instant render from client memory cache (0ms latency, zero lag)
  const cached = APP_STATE.liveStationCache[regionKey];
  if (!forceRefresh && cached) {
    applyLiveForecastData(cached);
    // If cache is younger than 5 minutes, station switch is instant without any network wait
    const now = Date.now();
    if (cached._cachedAt && now - cached._cachedAt < 300000) {
      return;
    }
  }

  const statusEl = byId("cache-status-text");
  if (statusEl) {
    statusEl.textContent = forceRefresh
      ? "Syncing live atmospheric observation data..."
      : "Loading station observations & running inference...";
  }
  const refreshBtn = byId("btn-force-refresh");
  if (refreshBtn) refreshBtn.disabled = true;

  // Only show grayed busy overlay if we don't already have data to show
  if (!cached || forceRefresh) {
    beginBusy(LIVE_BUSY_TARGETS);
  }

  try {
    const url = `/api/live-forecast?region=${encodeURIComponent(regionKey)}&force_refresh=${forceRefresh}`;
    const resp = await fetch(url);
    const data = await resp.json();
    if (seq !== APP_STATE.liveSeq) return; // a newer station request superseded this one

    data._cachedAt = Date.now();
    APP_STATE.liveStationCache[regionKey] = data;

    applyLiveForecastData(data);

    // After first station loads, prefetch remaining stations in idle time
    prefetchRemainingStations();
  } catch (err) {
    console.error("Error loading live forecast:", err);
    if (statusEl && seq === APP_STATE.liveSeq) {
      statusEl.textContent = "Server connection error while fetching data.";
    }
  } finally {
    endBusy(LIVE_BUSY_TARGETS);
    if (refreshBtn) refreshBtn.disabled = false;
  }
}

function prefetchRemainingStations() {
  if (APP_STATE.prefetchedStations) return;
  APP_STATE.prefetchedStations = true;
  const remaining = STATION_KEYS.filter((rk) => rk !== APP_STATE.liveRegion && !APP_STATE.liveStationCache[rk]);
  if (!remaining.length) return;

  setTimeout(async () => {
    for (const rk of remaining) {
      if (APP_STATE.liveStationCache[rk]) continue;
      try {
        const resp = await fetch(`/api/live-forecast?region=${encodeURIComponent(rk)}&force_refresh=false`);
        if (resp.ok) {
          const data = await resp.json();
          data._cachedAt = Date.now();
          APP_STATE.liveStationCache[rk] = data;
        }
      } catch (err) {
        console.warn("Background prefetch failed for", rk, err);
      }
    }
  }, 350);
}

function renderCacheBanner(cacheInfo) {
  const banner = byId("cache-status-banner");
  const textEl = byId("cache-status-text");
  if (!banner || !textEl || !cacheInfo) return;

  textEl.textContent = cacheInfo.message;
  textEl.title = cacheInfo.message;
  banner.classList.remove("is-warn", "is-fresh");
  const dot = banner.querySelector(".status-indicator");
  if (cacheInfo.status === "cooldown_blocked") {
    banner.classList.add("is-warn");
    if (dot) dot.className = "status-indicator bg-amber-400";
  } else if (cacheInfo.status === "fresh_api_call") {
    banner.classList.add("is-fresh");
    if (dot) dot.className = "status-indicator bg-sky-400";
  } else {
    if (dot) dot.className = "status-indicator bg-emerald-400";
  }
}

function renderCurrentObservation(meta, forecast) {
  const curr = forecast.current;
  const theme = getAqiTheme(curr.aqi);

  setText("live-basin-label", `${meta.basin} Basin`);
  setText("live-station-title", meta.name);
  setText("live-obs-time", `${curr.time} (PST)`);

  // Primary observation card dynamic severity tier
  const obsCard = byId("live-obs-card");
  if (obsCard) {
    obsCard.classList.remove(
      "aqi-tier-good",
      "aqi-tier-moderate",
      "aqi-tier-sensitive",
      "aqi-tier-unhealthy",
      "aqi-tier-very-unhealthy",
      "aqi-tier-hazardous"
    );
    obsCard.classList.add(theme.tierClass);
    obsCard.style.setProperty("--tier-color", theme.hex);
    obsCard.style.setProperty("--tier-bg-light", theme.bgLight);
    obsCard.style.setProperty("--tier-border-light", theme.borderLight);
    obsCard.style.setProperty("--tier-text-light", theme.textLight);
    obsCard.style.setProperty("--tier-glow", theme.glow);
  }

  const badge = byId("live-aqi-badge");
  badge.textContent = theme.label;
  badge.className = `shrink-0 px-2 py-0.5 rounded text-[10.5px] font-mono font-semibold uppercase tracking-wider border ${theme.badgeClass}`;

  const circle = byId("live-aqi-circle");
  circle.className = `aqi-tile ${theme.circleClass}`;
  setText("live-aqi-value", Math.round(curr.aqi));

  // Mini-stat alerts
  setText("live-pm25", curr.pm25);
  setText("live-pm10", curr.pm10);
  setText("live-vpd", curr.vpd_kpa);

  const pm25Val = Number(curr.pm25);
  const pm10Val = Number(curr.pm10);
  const vpdVal = Number(curr.vpd_kpa);

  const pm25Box = byId("stat-pm25");
  if (pm25Box) {
    pm25Box.className = `mini-stat ${pm25Val > 35 ? "mini-stat-warn" : ""}`;
  }
  const pm10Box = byId("stat-pm10");
  if (pm10Box) {
    pm10Box.className = `mini-stat ${pm10Val > 150 ? "mini-stat-warn" : ""}`;
  }
  const vpdBox = byId("stat-vpd");
  if (vpdBox) {
    vpdBox.className = `mini-stat ${vpdVal > 2.0 ? "mini-stat-alert" : ""}`;
  }

  const bestWin = forecast.best_outdoor_window;
  const bestTimeStr = bestWin.time ? bestWin.time.slice(11, 16) : bestWin.hour_label;
  const bestDateStr = bestWin.time ? bestWin.time.slice(5, 10).replace("-", "/") : "";
  setText(
    "best-outdoor-time",
    bestDateStr
      ? `${bestTimeStr} on ${bestDateStr} · AQI ${Math.round(bestWin.expected_aqi)}`
      : `${bestTimeStr} · AQI ${Math.round(bestWin.expected_aqi)}`
  );
  const bestTheme = getAqiTheme(bestWin.expected_aqi);
  const bestBadge = byId("best-outdoor-badge");
  if (bestBadge) {
    bestBadge.textContent = bestTheme.short;
    bestBadge.className = `px-1.5 py-0.5 rounded text-[10px] font-mono border ${bestTheme.badgeClass}`;
  }
  setText("live-health-advice", theme.advice);
  const adviceIcon = byId("health-advice-icon");
  if (adviceIcon) {
    adviceIcon.style.color = theme.hex;
  }

  setText("live-temp", curr.temperature_2m);
  setText("live-rh", curr.relative_humidity_2m);
  setText("live-wind", curr.wind_speed_10m);
  setText("live-wind-dir", curr.wind_direction_10m);
  setText("live-rain", curr.rain);
  setText("live-cloud", curr.cloud_cover);
  setText("live-pressure", curr.surface_pressure);

  setText("live-topo-desc", meta.topography_note);
  setText(
    "live-coords-text",
    `Coordinates: ${meta.lat.toFixed(4)}°N, ${meta.lon.toFixed(4)}°W · Elevation: ${meta.elevation_m}m`
  );

  // AQI Breakdown & Dominant Pollutant (Point B)
  const subPm25 = Number(curr.subindex_pm25 ?? curr.aqi ?? 0);
  const subPm10 = Number(curr.subindex_pm10 ?? 11);
  const subO3 = Number(curr.subindex_ozone ?? 38);
  const o3Conc = Number(curr.ozone ?? 74.5);

  const domLabel =
    curr.dominant_pollutant_label ||
    (subPm25 >= subO3 && subPm25 >= subPm10
      ? "PM2.5 (Fine Particulates)"
      : subO3 >= subPm10
      ? "Ground-Level Ozone (O₃)"
      : "PM10 (Coarse Particulates)");
  setText("dominant-pollutant-badge", domLabel);

  setText("val-subindex-pm25", Math.round(subPm25));
  setText("conc-pm25", curr.pm25);
  const thPm25 = getAqiTheme(subPm25);
  setText("tier-pm25", `${thPm25.short} (${Math.round(subPm25)})`);
  const barPm25 = byId("bar-subindex-pm25");
  if (barPm25) {
    barPm25.style.width = `${Math.min(100, Math.max(5, (subPm25 / 150) * 100))}%`;
    barPm25.style.backgroundColor = thPm25.hex;
  }
  const badgePm25 = byId("badge-pm25-sub");
  if (badgePm25) {
    badgePm25.className = `px-1.5 py-0.5 rounded text-[10px] border font-bold ${thPm25.badgeClass}`;
  }

  setText("val-subindex-pm10", Math.round(subPm10));
  setText("conc-pm10", curr.pm10);
  const thPm10 = getAqiTheme(subPm10);
  setText("tier-pm10", `${thPm10.short} (${Math.round(subPm10)})`);
  const barPm10 = byId("bar-subindex-pm10");
  if (barPm10) {
    barPm10.style.width = `${Math.min(100, Math.max(5, (subPm10 / 150) * 100))}%`;
    barPm10.style.backgroundColor = thPm10.hex;
  }
  const badgePm10 = byId("badge-pm10-sub");
  if (badgePm10) {
    badgePm10.className = `px-1.5 py-0.5 rounded text-[10px] border font-bold ${thPm10.badgeClass}`;
  }

  setText("val-subindex-o3", Math.round(subO3));
  setText("conc-o3", o3Conc);
  const thO3 = getAqiTheme(subO3);
  setText("tier-o3", `${thO3.short} (${Math.round(subO3)})`);
  const barO3 = byId("bar-subindex-o3");
  if (barO3) {
    barO3.style.width = `${Math.min(100, Math.max(5, (subO3 / 150) * 100))}%`;
    barO3.style.backgroundColor = thO3.hex;
  }
  const badgeO3 = byId("badge-o3-sub");
  if (badgeO3) {
    badgeO3.className = `px-1.5 py-0.5 rounded text-[10px] border font-bold ${thO3.badgeClass}`;
  }
}

/** Value of a horizon for the chosen card model (AUTO = recommended primary). */
function pickHorizonValue(fc, hk, selectModel) {
  const h = fc.horizons[hk];
  if (selectModel === "AUTO") return { val: h.primary_aqi, model: h.primary_model };
  return { val: h.models[selectModel] ?? h.primary_aqi, model: selectModel };
}

function renderHorizonCards() {
  if (!APP_STATE.liveData) return;
  const activeFc = APP_STATE.simulatedForecast || APP_STATE.liveData.forecast;
  const baseFc = APP_STATE.liveData.forecast;
  const selectModel = byId("horizon-model-select").value;
  const container = byId("horizon-cards-grid");
  if (!container) return;

  const currAqi = Number(baseFc.current.aqi);
  const isLight = APP_STATE.theme === "light";
  const horizonSubtitles = {
    "+1h": "Nowcasting t+1",
    "+2h": "Nowcasting t+2",
    "+3h": "Nowcasting t+3",
    "+24h": "Day-Ahead t+24",
  };

  container.innerHTML = HORIZON_KEYS
    .map((hk) => {
      const hObj = activeFc.horizons[hk];
      const { val, model: modelUsed } = pickHorizonValue(activeFc, hk, selectModel);
      const { val: baseVal } = pickHorizonValue(baseFc, hk, selectModel);

      const deltaCurr = Number(val) - currAqi;
      const deltaColor =
        deltaCurr > 1
          ? (isLight ? "text-rose-600 font-bold" : "text-rose-400 font-bold")
          : deltaCurr < -1
          ? (isLight ? "text-emerald-700 font-bold" : "text-emerald-400 font-bold")
          : (isLight ? "text-slate-500 font-medium" : "text-slate-400 font-medium");

      const simDelta = Number(val) - Number(baseVal);
      const hasSim = APP_STATE.simulatedForecast && Math.abs(simDelta) >= 0.1;
      const simCls = simDelta > 0.05 ? "hz-delta-up" : simDelta < -0.05 ? "hz-delta-down" : "hz-delta-flat";
      const theme = getAqiTheme(val);

      return `
        <div class="hz-card ${theme.tierClass} ${hasSim ? "is-sim" : ""}" style="--hz-accent:${theme.hex}; --hz-bg-tint:${theme.bgLight}; --hz-border:${theme.borderLight}; --hz-text:${theme.textLight}; --hz-glow:${theme.glow};">
          <div class="flex items-center justify-between gap-2">
            <span class="text-[11px] font-mono font-bold hz-time-title text-slate-100">${hk} <span class="text-slate-500 font-medium">· ${hObj.target_time.slice(11)}</span></span>
            <span class="px-1.5 rounded text-[9.5px] font-mono font-medium border ${theme.badgeClass}">${theme.short}</span>
          </div>
          <div class="flex items-baseline gap-1.5 mt-0.5">
            <span class="text-[22px] leading-tight font-mono font-bold hz-val text-slate-100">${fmtNum(val)}</span>
            <span class="text-[10.5px] font-mono ${deltaColor}" title="Delta vs current AQI">[${fmtSigned(deltaCurr)}]</span>
            ${hasSim ? `<span class="ml-auto hz-delta-chip ${simCls}" title="Delta from What-If simulation">What-If ${fmtSigned(simDelta)}</span>` : ""}
          </div>
          <div class="text-[10px] font-mono text-slate-500 truncate" title="${horizonSubtitles[hk]} · ${modelUsed}">
            ${horizonSubtitles[hk]} · <span class="text-slate-300 font-sans">${modelUsed}</span>
          </div>
          <div class="text-[10px] font-mono text-slate-500">
            LSTM <strong class="text-slate-300">${fmtNum(hObj.models["LSTM (PyTorch)"])}</strong> · Ens <strong class="text-slate-300">${fmtNum(hObj.models["Voting Ensemble"])}</strong>
          </div>
        </div>
      `;
    })
    .join("");

  renderWhatIfImpact();
}

function setTrajViewMode(mode) {
  APP_STATE.trajViewMode = mode;
  setSegActive(["traj-mode-rec", "traj-mode-all", "traj-mode-ind"], `traj-mode-${mode}`);
  renderLiveTrajectoryChart(false);
}

function renderLiveTrajectoryChart(isUpdate = false) {
  const ch = APP_STATE.charts.trajectory;
  if (!ch || !APP_STATE.liveData) return;

  const tc = getChartThemeColors();
  const isLight = tc.isLight;
  const baseTraj = APP_STATE.liveData.forecast.trajectory_24h;
  const activeFc = APP_STATE.simulatedForecast || APP_STATE.liveData.forecast;
  const traj = activeFc.trajectory_24h;
  const currAqi = Number(activeFc.current?.aqi || APP_STATE.liveData.forecast.current.aqi || 50);
  const simActive = !!APP_STATE.simulatedForecast;
  const xLabels = traj.map((d) => `${d.step} (${d.hour_label})`);
  const viewMode = APP_STATE.trajViewMode || "rec";

  // Point C: Prominent Voting Ensemble & LSTM Nowcasting, muted benchmarks
  const modelConfigs = [
    {
      key: "Voting Ensemble",
      color: isLight ? "#059669" : "#34d399",
      width: 3.4,
      dash: "solid",
      symbolSize: 5,
      isPrimary: true,
    },
    {
      key: "LSTM (PyTorch)",
      color: isLight ? "#7c3aed" : "#a78bfa",
      width: 2.8,
      dash: "solid",
      symbolSize: 4.5,
      isPrimary: true,
    },
    {
      key: "LightGBM",
      color: isLight ? "#0284c7" : "#38bdf8",
      width: 1.5,
      dash: "solid",
      symbolSize: 3,
      isPrimary: false,
    },
    {
      key: "MLP (64, 32)",
      color: isLight ? "#db2777" : "#f472b6",
      width: 1.5,
      dash: "dashed",
      symbolSize: 3,
      isPrimary: false,
    },
    {
      key: "Ridge Regression",
      color: isLight ? "#d97706" : "#fb923c",
      width: 1.4,
      dash: "dotted",
      symbolSize: 3,
      isPrimary: false,
    },
  ];

  const series = [];

  // Point C: Prediction Uncertainty (Confidence Interval Band around Ensemble)
  // Transparent lower base
  series.push({
    name: "ci-lower-base",
    type: "line",
    stack: "prediction-ci",
    symbol: "none",
    silent: true,
    data: traj.map((d) => d.ci_lower ?? Math.max(0, d["Voting Ensemble"] - 4.2)),
    lineStyle: { opacity: 0 },
    itemStyle: { opacity: 0 },
    tooltip: { show: false },
    z: 1,
  });

  // Shaded band for uncertainty
  series.push({
    name: "90% Confidence Interval (CI)",
    type: "line",
    stack: "prediction-ci",
    symbol: "none",
    data: traj.map((d) => {
      const low = d.ci_lower ?? Math.max(0, d["Voting Ensemble"] - 4.2);
      const up = d.ci_upper ?? (d["Voting Ensemble"] + 4.2);
      return Math.max(0.1, up - low);
    }),
    lineStyle: { opacity: 0 },
    areaStyle: {
      color: isLight ? "rgba(16, 185, 129, 0.16)" : "rgba(52, 211, 153, 0.14)",
    },
    itemStyle: { color: isLight ? "#059669" : "#34d399" },
    silent: true,
    z: 1,
  });

  // Forecast model line curves
  modelConfigs.forEach((m) => {
    const isEnsemble = m.key === "Voting Ensemble";
    const lineObj = {
      name: m.key,
      type: "line",
      smooth: true,
      symbol: "circle",
      symbolSize: m.symbolSize,
      data: traj.map((d) => d[m.key]),
      lineStyle: {
        width: m.width,
        color: m.color,
        type: m.dash,
        opacity: m.isPrimary ? 1.0 : (viewMode === "all" ? 0.75 : 0.6),
      },
      itemStyle: { color: m.color },
      z: m.isPrimary ? 3 : 2,
    };

    // Point C: Add horizontal Current AQI baseline to Voting Ensemble
    if (isEnsemble) {
      lineObj.markLine = {
        symbol: ["none", "none"],
        silent: true,
        label: {
          show: true,
          position: "insideEndTop",
          formatter: `Current AQI: ${Math.round(currAqi)}`,
          fontSize: 10,
          fontFamily: "JetBrains Mono, monospace",
          color: isLight ? "#475569" : "#94a3b8",
        },
        lineStyle: {
          type: "dashed",
          width: 1.2,
          color: isLight ? "#94a3b8" : "#64748b",
        },
        data: [{ yAxis: currAqi }],
      };
    }

    series.push(lineObj);
  });

  // Ghost baselines (pre-What-If) so the simulated shift is visible in place.
  const ghosts = [
    { key: "LSTM (PyTorch)", name: "LSTM · Baseline", color: isLight ? "#7c3aed" : "#a78bfa" },
    { key: "Voting Ensemble", name: "Ensemble · Baseline", color: isLight ? "#059669" : "#34d399" },
  ];
  ghosts.forEach((g) => {
    series.push({
      name: g.name,
      type: "line",
      smooth: true,
      symbol: "none",
      silent: true,
      data: simActive ? baseTraj.map((d) => d[g.key]) : [],
      lineStyle: { width: 1.4, color: g.color, type: "dashed", opacity: tc.ghostOpacity },
      itemStyle: { color: g.color },
      z: 1,
    });
  });

  // Point C: Mode-dependent legend visibility
  const legendSelected = {};
  if (viewMode === "rec") {
    legendSelected["Voting Ensemble"] = true;
    legendSelected["LSTM (PyTorch)"] = true;
    legendSelected["90% Confidence Interval (CI)"] = true;
    legendSelected["LightGBM"] = false;
    legendSelected["MLP (64, 32)"] = false;
    legendSelected["Ridge Regression"] = false;
  } else if (viewMode === "all") {
    legendSelected["Voting Ensemble"] = true;
    legendSelected["LSTM (PyTorch)"] = true;
    legendSelected["90% Confidence Interval (CI)"] = true;
    legendSelected["LightGBM"] = true;
    legendSelected["MLP (64, 32)"] = true;
    legendSelected["Ridge Regression"] = true;
  }
  // In 'ind' mode, keep whatever user selected or all true

  const option = {
    backgroundColor: "transparent",
    animationDurationUpdate: 180,
    tooltip: {
      trigger: "axis",
      ...tc.tooltip,
      // Point C: Tooltip positioning locks to side of cursor so it never covers the chart line
      position: function (point, params, dom, rect, size) {
        const isRight = point[0] > size.viewSize[0] / 2;
        const x = isRight ? point[0] - size.contentSize[0] - 16 : point[0] + 16;
        const y = Math.max(
          8,
          Math.min(point[1] - size.contentSize[1] / 2, size.viewSize[1] - size.contentSize[1] - 8)
        );
        return [x, y];
      },
      formatter: (params) => {
        const idx = params[0].dataIndex;
        const row = traj[idx];
        let html = `<div style="font-weight:700; margin-bottom:4px; font-family: Inter, sans-serif; color:${tc.tooltip.textStyle.color};">${row.step} — ${row.time}</div>`;
        html += `<div style="font-size:11px; color:${tc.text}; margin-bottom:5px;">Temperature: ${row.temp_c}°C · Wind: ${row.wind_kmh} km/h · Humidity: ${row.rh_pct}%</div>`;
        if (row.ci_lower !== undefined && row.ci_upper !== undefined) {
          html += `<div style="font-size:10.5px; color:${tc.isLight ? "#059669" : "#34d399"}; font-family: 'JetBrains Mono', monospace; margin-bottom: 4px;">
            90% CI: [${row.ci_lower} — ${row.ci_upper}] AQI
          </div>`;
        }
        params.forEach((p) => {
          if (p.value === undefined || p.value === null || p.seriesName === "ci-lower-base") return;
          const isGhost = p.seriesName.includes("Baseline");
          const isCI = p.seriesName.includes("Confidence Interval");
          if (isCI) return;
          html += `<div style="display:flex; justify-content:space-between; gap:12px; font-size:11px; ${isGhost ? "opacity:.6;" : ""}">
            <span>${p.marker} ${p.seriesName}</span>
            <strong style="color:${tc.tooltip.textStyle.color}; font-family: 'JetBrains Mono', monospace;">${Number(p.value).toFixed(1)} AQI</strong>
          </div>`;
        });
        return html;
      },
    },
    legend: {
      top: 0,
      data: ["90% Confidence Interval (CI)", ...modelConfigs.map((m) => m.key)],
      itemWidth: 14,
      itemHeight: 8,
      selected: Object.keys(legendSelected).length > 0 ? legendSelected : undefined,
      selectedMode: "multiple", // Point C: Click legend to toggle any model on/off
      textStyle: { color: tc.legendText, fontSize: 10.5 },
    },
    grid: { left: 40, right: 14, top: 28, bottom: 24 },
    xAxis: {
      type: "category",
      data: xLabels,
      axisLabel: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace", hideOverlap: true },
      axisLine: { lineStyle: { color: tc.axisLineColor } },
    },
    yAxis: {
      type: "value",
      name: "AQI",
      scale: true,
      nameTextStyle: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace" },
      axisLabel: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace" },
      splitLine: { lineStyle: { color: tc.splitLineColor, type: tc.splitLineType || "solid" } },
    },
    series,
  };

  ch.setOption(option, { notMerge: !isUpdate, lazyUpdate: true });
}

// ============================================================================
// POINT D: HISTORICAL DIURNAL AQI HEATMAP (7 DAYS x 24 HOURS)
// ============================================================================
async function loadHistoricalHeatmap(stationKey) {
  const chDom = byId("historical-diurnal-heatmap-chart");
  if (!chDom) return;
  if (!APP_STATE.charts.diurnalHeatmap) {
    APP_STATE.charts.diurnalHeatmap = echarts.init(chDom);
  }
  const ch = APP_STATE.charts.diurnalHeatmap;

  try {
    const rk = stationKey === "ALL" ? "ALL" : (APP_STATE.liveRegion || "FRES");
    const resp = await fetch(`/api/historical-diurnal-heatmap?region=${encodeURIComponent(rk)}`);
    if (!resp.ok) throw new Error("HTTP error");
    const data = await resp.json();
    renderHistoricalHeatmap(data);
  } catch (err) {
    console.error("Error loading historical heatmap:", err);
  }
}

function changeHeatmapStation(mode) {
  APP_STATE.heatmapStation = mode;
  setSegActive(["hm-btn-current", "hm-btn-all"], mode === "ALL" ? "hm-btn-all" : "hm-btn-current");
  loadHistoricalHeatmap(mode === "ALL" ? "ALL" : APP_STATE.liveRegion);
}

function renderHistoricalHeatmap(hm) {
  const ch = APP_STATE.charts.diurnalHeatmap;
  if (!ch || !hm || !hm.data) return;

  const tc = getChartThemeColors();

  setText("hm-kpi-peak-time", `${hm.peak.day} at ${hm.peak.hour}`);
  setText("hm-kpi-peak-val", `${hm.peak.aqi} AQI`);
  setText("hm-kpi-clean-time", `${hm.cleanest.day} at ${hm.cleanest.hour}`);
  setText("hm-kpi-clean-val", `${hm.cleanest.aqi} AQI`);
  setText("heatmap-summary-peak", `Peak: ${hm.peak.day} ${hm.peak.hour} (${hm.peak.aqi} AQI)`);
  setText("heatmap-summary-clean", `Cleanest: ${hm.cleanest.day} ${hm.cleanest.hour} (${hm.cleanest.aqi} AQI)`);

  const option = {
    backgroundColor: "transparent",
    tooltip: {
      position: "top",
      ...tc.tooltip,
      formatter: (params) => {
        const h = hm.hours[params.value[0]];
        const d = hm.days[params.value[1]];
        const val = params.value[2];
        const theme = getAqiTheme(val);
        return `
          <div style="font-family: Inter, sans-serif; font-size: 11px;">
            <div style="font-weight: 700; color: ${tc.tooltip.textStyle.color}; margin-bottom: 3px;">${d} — ${h}</div>
            <div style="font-family: 'JetBrains Mono', monospace; font-size: 12px; margin-bottom: 3px;">
              Average AQI: <strong style="color: ${theme.hex}; font-size: 13px;">${val.toFixed(1)}</strong>
            </div>
            <div style="font-size: 10.5px; color: ${tc.text};">Category: <span style="color: ${theme.hex}; font-weight: 600;">${theme.label}</span></div>
          </div>
        `;
      },
    },
    grid: { left: 62, right: 24, top: 12, bottom: 44 },
    xAxis: {
      type: "category",
      data: hm.hours,
      splitArea: { show: true },
      axisLabel: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace" },
      axisLine: { lineStyle: { color: tc.axisLineColor } },
    },
    yAxis: {
      type: "category",
      data: hm.days,
      splitArea: { show: true },
      axisLabel: { color: tc.text, fontSize: 10.5, fontFamily: "Inter, sans-serif", fontWeight: 600 },
      axisLine: { lineStyle: { color: tc.axisLineColor } },
    },
    visualMap: {
      min: Math.floor(hm.min_aqi / 10) * 10,
      max: Math.ceil(hm.max_aqi / 10) * 10,
      calculable: true,
      orient: "horizontal",
      left: "center",
      bottom: 2,
      itemWidth: 11,
      itemHeight: 110,
      textStyle: { color: tc.legendText, fontSize: 9.5, fontFamily: "JetBrains Mono, monospace" },
      inRange: {
        color: [
          "#10b981", // Good Green
          "#eab308", // Moderate Yellow
          "#f97316", // Sensitive Orange
          "#ef4444", // Unhealthy Red
          "#8b5cf6", // Very Unhealthy Purple
        ],
      },
    },
    series: [
      {
        name: "Historical AQI Diurnal",
        type: "heatmap",
        data: hm.data,
        emphasis: {
          itemStyle: {
            shadowBlur: 8,
            shadowColor: "rgba(0, 0, 0, 0.5)",
            borderColor: "#ffffff",
            borderWidth: 1.5,
          },
        },
      },
    ],
  };

  ch.setOption(option, true);
}

// ============================================================================
// LIVE TREESHAP WATERFALL / HORIZONTAL BAR EXPLAINABILITY
// ============================================================================
function switchShapHorizon(h) {
  APP_STATE.shapHorizon = h;
  setSegActive(["shap-btn-1h", "shap-btn-24h"], `shap-btn-${h}`);
  renderLiveShapChart(false);
}

function renderLiveShapChart(isUpdate = false) {
  const ch = APP_STATE.charts.shap;
  if (!ch || !APP_STATE.liveData) return;

  const tc = getChartThemeColors();
  const activeFc = APP_STATE.simulatedForecast || APP_STATE.liveData.forecast;
  const shapObj =
    APP_STATE.shapHorizon === "24h" ? activeFc.shap_24h : activeFc.shap_1h;
  if (!shapObj) return;

  setText("shap-base-val", shapObj.base_value.toFixed(2));
  setText("shap-pred-val", shapObj.predicted_value.toFixed(2));
  updateShapSummaryPill(shapObj);

  // Decomposition strip: total push-up vs pull-down across top attributes
  let up = 0;
  let down = 0;
  shapObj.top_features.forEach((f) => {
    if (f.shap >= 0) up += f.shap;
    else down += f.shap;
  });
  const total = up + Math.abs(down) || 1;
  setText("shap-decomp-up-label", `▲ +${up.toFixed(2)}`);
  setText("shap-decomp-down-label", `▼ −${Math.abs(down).toFixed(2)}`);
  const downEl = byId("shap-decomp-down");
  const upEl = byId("shap-decomp-up");
  if (downEl) downEl.style.width = `${(Math.abs(down) / total) * 100}%`;
  if (upEl) upEl.style.width = `${(up / total) * 100}%`;

  const items = [...shapObj.top_features].reverse();
  const yLabels = items.map((d) => `${d.label} (${d.value})`);
  const xValues = items.map((d) => ({
    value: d.shap,
    itemStyle: {
      color: d.shap >= 0 ? "#f43f5e" : "#10b981",
      borderRadius: d.shap >= 0 ? [0, 2, 2, 0] : [2, 0, 0, 2],
    },
  }));

  const option = {
    backgroundColor: "transparent",
    animationDurationUpdate: 180,
    tooltip: {
      trigger: "axis",
      axisPointer: { type: "shadow" },
      ...tc.tooltip,
      formatter: (params) => {
        const idx = params[0].dataIndex;
        const it = items[idx];
        const sign = it.shap >= 0 ? `+${it.shap}` : `${it.shap}`;
        const desc =
          it.shap >= 0
            ? "Increases air pollution"
            : "Decreases air pollution";
        return `
          <div style="font-weight:700; margin-bottom:3px; font-family: Inter, sans-serif; color:${tc.tooltip.textStyle.color};">${it.label}</div>
          <div style="font-size:11px; color:${tc.text};">Observed value: <strong style="color:${tc.tooltip.textStyle.color};">${it.value}</strong></div>
          <div style="font-size:11px; color:${tc.text};">Impact on AQI: <strong style="color:${it.shap >= 0 ? "#fb7185" : "#34d399"};">${sign} AQI</strong> (${desc})</div>
        `;
      },
    },
    grid: { left: 4, right: 36, top: 4, bottom: 20, containLabel: true },
    xAxis: {
      type: "value",
      name: "Impact (AQI)",
      nameLocation: "middle",
      nameGap: 18,
      nameTextStyle: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace" },
      axisLabel: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace" },
      splitLine: { lineStyle: { color: tc.splitLineColor, type: tc.splitLineType || "solid" } },
    },
    yAxis: {
      type: "category",
      data: yLabels,
      axisLabel: { color: tc.yAxisCategoryColor, fontSize: 10, width: 175, overflow: "truncate" },
      axisLine: { lineStyle: { color: tc.axisLineColor } },
    },
    series: [
      {
        type: "bar",
        data: xValues,
        barMaxWidth: 14,
        label: {
          show: true,
          position: "right",
          color: tc.yAxisCategoryColor,
          fontSize: 10,
          fontFamily: "JetBrains Mono, monospace",
          formatter: (p) => (p.value > 0 ? `+${p.value}` : `${p.value}`),
        },
      },
    ],
  };

  ch.setOption(option, { notMerge: !isUpdate, lazyUpdate: true });
}

// ============================================================================
// WHAT-IF WEATHER SIMULATOR
// ============================================================================
const WI_FIELDS = [
  { key: "wind", obsKey: "wind_speed_10m", round: true },
  { key: "temp", obsKey: "temperature_2m", round: false },
  { key: "rh", obsKey: "relative_humidity_2m", round: true },
  { key: "rain", obsKey: "rain", round: false },
];

function sliderPct(slider) {
  const min = Number(slider.min);
  const max = Number(slider.max);
  const v = Number(slider.value);
  return Math.max(0, Math.min(100, ((v - min) / (max - min)) * 100));
}

/** Paint the filled track of every slider. */
function initWhatIfSliderVisuals() {
  WI_FIELDS.forEach((f) => {
    const s = byId(`wi-slider-${f.key}`);
    if (s) s.style.setProperty("--fill", `${sliderPct(s)}%`);
  });
}

function placeActualMark(fieldKey, actualValue) {
  const s = byId(`wi-slider-${fieldKey}`);
  const mark = byId(`wi-mark-${fieldKey}`);
  if (!s || !mark) return;
  const min = Number(s.min);
  const max = Number(s.max);
  const pct = Math.max(0, Math.min(100, ((actualValue - min) / (max - min)) * 100));
  // Align to the 14px thumb centre.
  mark.style.left = `calc(${pct}% + ${(7 - pct * 0.14).toFixed(2)}px)`;
}

function resetWhatIfSlidersToCurrent(curr) {
  if (!curr) return;
  const actual = {};
  WI_FIELDS.forEach((f) => {
    const raw = Number(curr[f.obsKey]);
    const v = f.round ? Math.round(raw) : raw;
    const s = byId(`wi-slider-${f.key}`);
    if (s) s.value = v;
    actual[f.key] = Number(s ? s.value : v); // clamp/step-normalised by the input
    placeActualMark(f.key, actual[f.key]);
  });
  APP_STATE.whatIf.actual = actual;
  onWhatIfSlide(false);
  setWhatIfChip("actual");

  const deltaBadge = byId("wi-delta-badge");
  if (deltaBadge) {
    deltaBadge.textContent = "Observed baseline";
    deltaBadge.className = "text-[10.5px] font-mono font-semibold text-slate-400";
  }
}

function isWhatIfModified() {
  const actual = APP_STATE.whatIf.actual;
  if (!actual) return false;
  return WI_FIELDS.some((f) => {
    const s = byId(`wi-slider-${f.key}`);
    return s && Math.abs(Number(s.value) - actual[f.key]) > 1e-9;
  });
}

function setWhatIfChip(state, latencyMs) {
  const chip = byId("wi-status-chip");
  if (!chip) return;
  chip.classList.remove("is-pending", "is-sim");
  if (state === "pending") {
    chip.classList.add("is-pending");
    chip.textContent = "Inferring…";
  } else if (state === "sim") {
    chip.classList.add("is-sim");
    chip.textContent = latencyMs != null ? `Simulated · ${Math.round(latencyMs)}ms` : "Simulated";
  } else {
    chip.textContent = "Observed";
  }
}

/**
 * Instant (<16ms) visual feedback on every slider movement: value labels,
 * filled track, deltas vs actual. When triggered by user input, schedules a
 * debounced inference call so the forecast updates while dragging.
 */
function onWhatIfSlide(fromInput = false) {
  const actual = APP_STATE.whatIf.actual;
  WI_FIELDS.forEach((f) => {
    const s = byId(`wi-slider-${f.key}`);
    if (!s) return;
    const v = Number(s.value);
    s.style.setProperty("--fill", `${sliderPct(s)}%`);
    const valEl = byId(`wi-val-${f.key}`);
    const diffEl = byId(`wi-diff-${f.key}`);
    if (valEl) valEl.textContent = s.value;
    const diff = actual ? v - actual[f.key] : 0;
    const modified = Math.abs(diff) > 1e-9;
    if (valEl) valEl.classList.toggle("is-modified", modified);
    if (diffEl) {
      diffEl.textContent = modified ? `(${fmtSigned(diff, f.round ? 0 : 1)})` : "";
      diffEl.classList.toggle("is-modified", modified);
    }
  });

  if (fromInput) {
    setWhatIfChip("pending");
    clearTimeout(APP_STATE.whatIf.timer);
    APP_STATE.whatIf.timer = setTimeout(runWhatIfSimulation, WHATIF_DEBOUNCE_MS);
  }
}

function cancelPendingWhatIf() {
  clearTimeout(APP_STATE.whatIf.timer);
  APP_STATE.whatIf.timer = null;
  if (APP_STATE.whatIf.controller) {
    APP_STATE.whatIf.controller.abort();
    APP_STATE.whatIf.controller = null;
  }
  APP_STATE.whatIf.seq += 1;
}

function rerenderSimulationViews() {
  renderHorizonCards();
  renderLiveTrajectoryChart(true);
  renderLiveShapChart(true);
}

async function runWhatIfSimulation() {
  if (!APP_STATE.liveData) return;
  clearTimeout(APP_STATE.whatIf.timer);
  APP_STATE.whatIf.timer = null;
  onWhatIfSlide(false);

  // Sliders back at the observed state -> show the real forecast, no request needed.
  if (!isWhatIfModified()) {
    cancelPendingWhatIf();
    APP_STATE.simulatedForecast = null;
    setWhatIfChip("actual");
    const deltaBadge = byId("wi-delta-badge");
    if (deltaBadge) {
      deltaBadge.textContent = "Observed baseline";
      deltaBadge.className = "text-[10.5px] font-mono font-semibold text-slate-400";
    }
    rerenderSimulationViews();
    return;
  }

  const payload = {
    region_key: APP_STATE.liveRegion,
    wind_speed_10m: parseFloat(byId("wi-slider-wind").value),
    temperature_2m: parseFloat(byId("wi-slider-temp").value),
    relative_humidity_2m: parseFloat(byId("wi-slider-rh").value),
    rain: parseFloat(byId("wi-slider-rain").value),
  };

  // Cancel any in-flight request; only the latest slider state matters.
  if (APP_STATE.whatIf.controller) APP_STATE.whatIf.controller.abort();
  const controller = new AbortController();
  APP_STATE.whatIf.controller = controller;
  const seq = ++APP_STATE.whatIf.seq;
  const liveSeqAtStart = APP_STATE.liveSeq;
  const t0 = performance.now();
  setWhatIfChip("pending");

  try {
    const resp = await fetch("/api/what-if", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      signal: controller.signal,
    });
    const res = await resp.json();
    if (seq !== APP_STATE.whatIf.seq || liveSeqAtStart !== APP_STATE.liveSeq) return;

    APP_STATE.simulatedForecast = res.simulated;
    APP_STATE.whatIf.controller = null;

    const base24 = APP_STATE.liveData.forecast.horizons["+24h"].primary_aqi;
    const sim24 = res.simulated.horizons["+24h"].primary_aqi;
    const diff24 = sim24 - base24;

    const deltaBadge = byId("wi-delta-badge");
    if (deltaBadge) {
      deltaBadge.textContent = `24h Impact: ${fmtSigned(diff24)} AQI`;
      const isLight = APP_STATE.theme === "light";
      const color = diff24 > 0.05
        ? (isLight ? "text-rose-600 font-bold" : "text-rose-400 font-bold")
        : diff24 < -0.05
        ? (isLight ? "text-emerald-700 font-bold" : "text-emerald-400 font-bold")
        : (isLight ? "text-slate-600" : "text-slate-300");
      deltaBadge.className = `text-[10.5px] font-mono font-semibold ${color}`;
    }

    setWhatIfChip("sim", performance.now() - t0);
    rerenderSimulationViews();
  } catch (err) {
    if (err.name === "AbortError") return;
    console.error("What-If simulation error:", err);
    setWhatIfChip("actual");
  }
}

async function toggleWildfireSimulation(isFireActive) {
  const toggle = byId("wi-wildfire-toggle");
  if (toggle) toggle.checked = isFireActive;
  const banner = byId("wildfire-alert-banner");
  const box = byId("what-if-status-box");
  const fireLabel = byId("wi-fire-label");

  if (isFireActive) {
    if (banner) banner.classList.remove("hidden");
    if (box) box.classList.add("wildfire-active-border");
    if (fireLabel) fireLabel.className = "text-[10px] font-bold text-rose-400";

    // Set wildfire parameters: 34°C, 14% RH, 38 km/h wind, 0 mm rain
    const sWind = byId("wi-slider-wind");
    const sTemp = byId("wi-slider-temp");
    const sRh = byId("wi-slider-rh");
    const sRain = byId("wi-slider-rain");

    if (sWind) { sWind.value = 38; sWind.disabled = true; }
    if (sTemp) { sTemp.value = 34; sTemp.disabled = true; }
    if (sRh) { sRh.value = 14; sRh.disabled = true; }
    if (sRain) { sRain.value = 0; sRain.disabled = true; }

    onWhatIfSlide(false);

    // Call API with wildfire_mode: true
    cancelPendingWhatIf();
    const controller = new AbortController();
    APP_STATE.whatIf.controller = controller;
    const seq = ++APP_STATE.whatIf.seq;
    const liveSeqAtStart = APP_STATE.liveSeq;
    setWhatIfChip("pending");

    const payload = {
      region_key: APP_STATE.liveRegion,
      wind_speed_10m: 38.0,
      temperature_2m: 34.0,
      relative_humidity_2m: 14.0,
      rain: 0.0,
      wildfire_mode: true,
    };

    try {
      const resp = await fetch("/api/what-if", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
        signal: controller.signal,
      });
      const res = await resp.json();
      if (seq !== APP_STATE.whatIf.seq || liveSeqAtStart !== APP_STATE.liveSeq) return;

      APP_STATE.simulatedForecast = res.simulated;
      APP_STATE.whatIf.controller = null;

      const chip = byId("wi-status-chip");
      if (chip) {
        chip.className = "wi-chip is-sim !bg-rose-950 !text-rose-300 !border-rose-600";
        chip.textContent = "🔥 Wildfire";
      }

      const deltaBadge = byId("wi-delta-badge");
      if (deltaBadge) {
        deltaBadge.textContent = "⚠️ Wildfire smoke: AQI > 300 (Hazardous)";
        deltaBadge.className = "text-[10.5px] font-mono font-bold text-rose-400";
      }

      rerenderSimulationViews();
    } catch (err) {
      if (err.name === "AbortError") return;
      console.error("Wildfire simulation error:", err);
    }
  } else {
    // Turn off wildfire simulation
    if (banner) banner.classList.add("hidden");
    if (box) box.classList.remove("wildfire-active-border");
    if (fireLabel) fireLabel.className = "text-[10px] font-semibold text-slate-400";

    // Re-enable sliders
    ["wind", "temp", "rh", "rain"].forEach((k) => {
      const s = byId(`wi-slider-${k}`);
      if (s) s.disabled = false;
    });

    // Reset back to live station data
    resetWhatIf();
  }
}

function resetWhatIf() {
  if (!APP_STATE.liveData) return;
  const toggle = byId("wi-wildfire-toggle");
  if (toggle && toggle.checked) {
    toggle.checked = false;
    const banner = byId("wildfire-alert-banner");
    if (banner) banner.classList.add("hidden");
    const box = byId("what-if-status-box");
    if (box) box.classList.remove("wildfire-active-border");
    const fireLabel = byId("wi-fire-label");
    if (fireLabel) fireLabel.className = "text-[10px] font-semibold text-slate-400";
    ["wind", "temp", "rh", "rain"].forEach((k) => {
      const s = byId(`wi-slider-${k}`);
      if (s) s.disabled = false;
    });
  }
  cancelPendingWhatIf();
  APP_STATE.simulatedForecast = null;
  resetWhatIfSlidersToCurrent(APP_STATE.liveData.forecast.current);
  updateWhatIfSummaryPill();
  rerenderSimulationViews();
}

/** In-place impact readout under the What-If sliders (+1h..+24h). */
function renderWhatIfImpact() {
  updateWhatIfSummaryPill();
  const grid = byId("wi-impact-grid");
  if (!grid || !APP_STATE.liveData) return;
  const baseFc = APP_STATE.liveData.forecast;
  const simFc = APP_STATE.simulatedForecast;
  const selectModel = byId("horizon-model-select").value;
  const isLight = APP_STATE.theme === "light";

  const box = byId("what-if-status-box");
  if (box) {
    if (simFc && isWhatIfModified()) {
      box.classList.add("is-simulating");
    } else {
      box.classList.remove("is-simulating");
    }
  }

  grid.innerHTML = HORIZON_KEYS.map((hk) => {
    const base = Number(pickHorizonValue(baseFc, hk, selectModel).val);
    const sim = simFc ? Number(pickHorizonValue(simFc, hk, selectModel).val) : base;
    const d = sim - base;
    const dCls = !simFc
      ? (isLight ? "text-slate-400" : "text-slate-600")
      : d > 0.05
      ? (isLight ? "text-rose-600 font-bold" : "text-rose-400 font-bold")
      : d < -0.05
      ? (isLight ? "text-emerald-700 font-bold" : "text-emerald-400 font-bold")
      : (isLight ? "text-slate-600" : "text-slate-400");
    const theme = getAqiTheme(sim);
    return `
      <div class="wi-impact ${theme.tierClass}" style="--impact-accent:${theme.hex}; --impact-bg:${theme.bgLight}; --impact-border:${theme.borderLight}; border-left: 3px solid ${theme.hex};">
        <div class="lbl">${hk}</div>
        <div class="flex items-baseline justify-between gap-1">
          <span class="val font-mono">${fmtNum(sim)}</span>
          <span class="dlt ${dCls}">${simFc ? fmtSigned(d) : "±0.0"}</span>
        </div>
      </div>`;
  }).join("");
}

function formatTriggerType(trigger) {
  const map = {
    auto_worker_24_7: "Automatic (Hourly)",
    manual_force: "Manual Refresh",
    user_request: "Direct Query",
    what_if: "What-If Simulation",
    cache_hit: "Cache Hit",
    offline_fallback: "Fallback Store",
  };
  return map[trigger] || trigger;
}

function formatRegionName(regionKey) {
  const map = {
    FRES: "Fresno",
    LA: "Los Angeles",
    SJ: "San Jose",
  };
  return map[regionKey] || regionKey;
}

function formatActiveSources(sources) {
  if (!sources || sources.length === 0) return "Unknown";
  const names = sources.map((s) => {
    if (s === "FRES" || s === "LA") return "EPA Ground Station";
    if (s.includes("OPENMETEO")) return "Atmospheric Model";
    return s;
  });
  return [...new Set(names)].join(" + ");
}

// ============================================================================
// SMART COLLAPSIBLE PANELS (Progressive Disclosure & Decluttering Architecture)
// ============================================================================
const COLLAPSIBLE_STORAGE_KEY = "ca_aqi_collapsible_panels_v1";

const DEFAULT_PANEL_STATES = {
  "what-if": false, // Collapsed by default (interactive sandbox)
  "shap": false,    // Collapsed by default (advanced explainability chart)
};

function getCollapsibleStates() {
  try {
    const raw = localStorage.getItem(COLLAPSIBLE_STORAGE_KEY);
    return raw ? { ...DEFAULT_PANEL_STATES, ...JSON.parse(raw) } : { ...DEFAULT_PANEL_STATES };
  } catch {
    return { ...DEFAULT_PANEL_STATES };
  }
}

function setCollapsibleState(panelId, isOpen) {
  const states = getCollapsibleStates();
  states[panelId] = isOpen;
  try {
    localStorage.setItem(COLLAPSIBLE_STORAGE_KEY, JSON.stringify(states));
  } catch (err) {
    console.warn("Failed to persist collapsible panel state:", err);
  }
}

function toggleCollapsiblePanel(panelId, force) {
  const panel = document.querySelector(`[data-panel-id="${panelId}"]`);
  if (!panel) return;

  const isCurrentlyOpen = panel.classList.contains("is-open");
  const nextOpen = typeof force === "boolean" ? force : !isCurrentlyOpen;

  panel.classList.toggle("is-open", nextOpen);
  panel.querySelector(".collapsible-head")?.setAttribute("aria-expanded", nextOpen ? "true" : "false");
  setCollapsibleState(panelId, nextOpen);

  // Trigger chart/map resize smoothly once transition is settling
  setTimeout(() => {
    if (panelId === "shap" && APP_STATE.charts.shap) {
      APP_STATE.charts.shap.resize();
    }
    if (panelId === "diurnal-heatmap" && APP_STATE.charts.diurnalHeatmap) {
      APP_STATE.charts.diurnalHeatmap.resize();
    }
    if (APP_STATE.charts.trajectory) {
      APP_STATE.charts.trajectory.resize();
    }
    if (APP_STATE.map) {
      APP_STATE.map.invalidateSize();
    }
  }, 260);
}

function initCollapsiblePanels() {
  const states = getCollapsibleStates();
  document.querySelectorAll("[data-panel-id]").forEach((panel) => {
    const id = panel.getAttribute("data-panel-id");
    const defaultOpen = id === "diurnal-heatmap";
    const isOpen = states[id] !== undefined ? states[id] : defaultOpen;
    panel.classList.toggle("is-open", isOpen);
    panel.querySelector(".collapsible-head")?.setAttribute("aria-expanded", isOpen ? "true" : "false");
  });
}

function updateWhatIfSummaryPill() {
  const pill = byId("what-if-summary-pill");
  if (!pill) return;
  const isMod = typeof isWhatIfModified === "function" ? isWhatIfModified() : false;
  const stateEl = byId("what-if-summary-state");
  const metricsEl = byId("what-if-summary-metrics");

  const w = byId("wi-slider-wind")?.value ?? "10";
  const t = byId("wi-slider-temp")?.value ?? "20";
  const rh = byId("wi-slider-rh")?.value ?? "50";
  const rain = byId("wi-slider-rain")?.value ?? "0";

  if (isMod) {
    if (stateEl) {
      stateEl.textContent = "Simulation";
      stateEl.className = "text-amber-400 font-semibold";
    }
    if (metricsEl) {
      metricsEl.textContent = `Wind ${w}k · ${t}°C · ${rh}% · ${rain}mm (Simulated)`;
    }
  } else {
    if (stateEl) {
      stateEl.textContent = "Observed";
      stateEl.className = "text-emerald-400 font-semibold";
    }
    if (metricsEl) {
      metricsEl.textContent = `Wind ${w}km/h · ${t}°C · ${rh}% · 0 variance`;
    }
  }
}

function updateShapSummaryPill(shapObj) {
  const textEl = byId("shap-summary-text");
  if (!textEl || !shapObj) return;

  const top = shapObj.top_features && shapObj.top_features[0];
  if (top) {
    const sign = top.shap >= 0 ? `+${top.shap.toFixed(1)}` : `${top.shap.toFixed(1)}`;
    const col = top.shap >= 0 ? "text-rose-400" : "text-emerald-400";
    textEl.innerHTML = `Base: <strong class="text-slate-100">${shapObj.base_value.toFixed(1)}</strong> │ Dominant Factor: <strong class="${col}">${top.label} (${sign})</strong>`;
  }
}

// ============================================================================
// SYSTEM LOG DRAWER — SYNCHRONIZATION LOGS
// ============================================================================
function toggleSysLogDrawer(force) {
  const open = typeof force === "boolean" ? force : !APP_STATE.syslogOpen;
  APP_STATE.syslogOpen = open;
  byId("syslog-drawer")?.classList.toggle("is-open", open);
  byId("syslog-toggle")?.setAttribute("aria-expanded", open ? "true" : "false");
  setText("syslog-toggle-label", open ? "Collapse" : "Open logs");
}

function renderSysLogStatus(logs) {
  if (!logs) return;
  const apiCount = logs.filter((r) => r.api_called === 1).length;
  setText("syslog-count", logs.length);
  setText("syslog-api", apiCount);
  setText("syslog-cache", logs.length - apiCount);

  const last = logs[0];
  if (last) {
    setText(
      "syslog-last",
      `${last.fetched_at} · ${formatRegionName(last.region_key)} · ${formatTriggerType(last.trigger_type)}`
    );
  }
  const dot = byId("syslog-dot");
  if (dot) {
    dot.className = `status-indicator ${last && last.api_called === 1 ? "bg-sky-400" : "bg-emerald-400"}`;
    void dot.offsetWidth; // restart flash animation
    dot.classList.add("syslog-dot-flash");
  }
}

function renderFetchHistoryTable(logs) {
  const tbody = byId("fetch-history-tbody");
  if (!tbody || !logs) return;
  renderSysLogStatus(logs);

  tbody.innerHTML = logs
    .map((r) => {
      const apiBadge =
        r.api_called === 1
          ? `<span class="px-1.5 py-0.5 rounded text-[10px] bg-blue-950 text-blue-300 border border-blue-800">Direct API</span>`
          : `<span class="px-1.5 py-0.5 rounded text-[10px] bg-slate-800 text-slate-400 border border-slate-700">Cached Read</span>`;

      return `
        <tr>
          <td class="text-slate-500">${String(r.id).padStart(3, "0")}</td>
          <td class="text-slate-200">${r.fetched_at}</td>
          <td class="font-sans font-medium text-slate-200">${formatRegionName(r.region_key)}</td>
          <td class="text-slate-400 font-sans">${formatTriggerType(r.trigger_type)}</td>
          <td class="font-sans">${apiBadge}</td>
          <td class="text-right font-bold text-slate-100">${Number(r.current_aqi).toFixed(1)}</td>
          <td class="text-right text-slate-300">${Number(r.pm25).toFixed(1)}</td>
          <td class="text-slate-300">${Number(r.temp_c).toFixed(1)}°C / ${Number(r.wind_kmh).toFixed(1)} km/h</td>
          <td class="text-right font-semibold text-purple-300">${Number(r.pred_1h_aqi).toFixed(1)}</td>
          <td class="text-right font-semibold text-emerald-300">${Number(r.pred_24h_aqi).toFixed(1)}</td>
        </tr>
      `;
    })
    .join("");
}

function exportHistoryCSV() {
  if (!APP_STATE.liveData || !APP_STATE.liveData.history_logs) return;
  const rows = APP_STATE.liveData.history_logs;
  const headers = [
    "id",
    "fetched_at",
    "region_key",
    "station_id",
    "trigger_type",
    "api_called",
    "current_aqi",
    "pm25",
    "temp_c",
    "wind_kmh",
    "pred_1h_aqi",
    "pred_24h_aqi",
  ];
  const csvLines = [
    headers.join(","),
    ...rows.map((r) => headers.map((h) => JSON.stringify(r[h] ?? "")).join(",")),
  ];
  downloadCSVBlob(csvLines.join("\n"), "california_aqi_system_history.csv");
}

// ============================================================================
// WINDOW 2: TIME-WINDOW EXPLORER & DYNAMIC LEADERBOARD
// ============================================================================
const WIN2_BUSY_TARGETS = ["kpi-row", "station-charts-card", "benchmark-row"];

function renderWildfirePresetButtons() {
  const container = byId("wildfire-presets-container");
  if (!container || !APP_STATE.meta || !APP_STATE.meta.wildfire_presets) return;

  container.innerHTML = APP_STATE.meta.wildfire_presets
    .map((p) => {
      const isAct = p.id === APP_STATE.win2.activePresetId;
      const badgeHtml = p.badge
        ? `<span class="ml-1.5 px-1.5 py-0.5 rounded text-[9.5px] font-mono ${
            isAct
              ? "bg-blue-600 text-white"
              : "bg-slate-800 text-slate-400 border border-slate-700"
          }">${p.badge}</span>`
        : "";
      return `<button id="preset-btn-${p.id}" onclick="selectWildfirePreset('${p.id}')" class="chip ${
        isAct ? "is-active" : ""
      }" title="${(p.description || "").replace(/"/g, "&quot;")}">${p.title}${badgeHtml}</button>`;
    })
    .join("");
}

function selectWildfirePreset(presetId) {
  if (!APP_STATE.meta) return;
  const preset = APP_STATE.meta.wildfire_presets.find((p) => p.id === presetId);
  if (!preset) return;

  APP_STATE.win2.activePresetId = presetId;
  renderWildfirePresetButtons();

  const descEl = byId("win2-preset-desc");
  if (descEl) {
    descEl.textContent = preset.description;
    descEl.title = preset.description;
  }

  byId("win2-start-date").value = preset.start_date || "";
  byId("win2-end-date").value = preset.end_date || "";
  byId("win2-source-mode").value = preset.source_mode || preset.recommended_source_mode || "seamless";
  const regSel = byId("lb-region-filter");
  if (regSel) regSel.value = "ALL";

  loadDashboardWindow();
}

function applyCustomDateWindow() {
  APP_STATE.win2.activePresetId = "";
  renderWildfirePresetButtons();
  loadDashboardWindow();
}

async function reloadMissingDates() {
  const btn = byId("btn-reload-missing-dates");
  if (btn) btn.classList.add("animate-spin");
  try {
    const res = await fetch("/api/reload-missing-dates", { method: "POST" });
    const json = await res.json();
    console.log("Sync missing dates:", json);
    await loadDashboardWindow();
    alert(`[Data Sync]\n${json.message}\nTotal warehouse forecast records: ${json.total_records_1h ? json.total_records_1h.toLocaleString() : "--"} rows.`);
  } catch (err) {
    console.error("Error reloading missing dates:", err);
    alert("Could not reload missing dates. Please check network connection.");
  } finally {
    if (btn) btn.classList.remove("animate-spin");
  }
}

function setDashboardScenario(sc) {
  APP_STATE.win2.scenario = sc;
  setSegActive(["sc-btn-1h", "sc-btn-24h"], `sc-btn-${sc}`);
  loadDashboardWindow();
}

function renderModelChips() {
  const container = byId("model-chips-container");
  if (!container || !APP_STATE.meta) return;

  container.innerHTML = APP_STATE.meta.models
    .map((m) => {
      const active = APP_STATE.win2.selectedModels.has(m.name);
      return `
        <button onclick="toggleSingleModel('${m.name}')" class="chip font-mono ${active ? "model-chip-active" : "model-chip-off"}" aria-pressed="${active}">
          <span class="w-2 h-2 rounded-full inline-block" style="background:${m.color};"></span>
          <span>${m.name}</span>
        </button>
      `;
    })
    .join("");
}

function setGroupButtons(groupType) {
  APP_STATE.win2.activeGroup = groupType;
  ["top", "dl", "all"].forEach((g) => {
    byId(`grp-btn-${g}`)?.classList.toggle("is-active", g === groupType);
  });
}

function toggleSingleModel(modelName) {
  if (APP_STATE.win2.selectedModels.has(modelName)) {
    if (APP_STATE.win2.selectedModels.size > 1) {
      APP_STATE.win2.selectedModels.delete(modelName);
    }
  } else {
    APP_STATE.win2.selectedModels.add(modelName);
  }
  setGroupButtons(null);
  renderModelChips();
  renderAllStationWindowCharts();
}

function setModelGroup(groupType) {
  if (!APP_STATE.meta) return;
  if (groupType === "top") {
    APP_STATE.win2.selectedModels = new Set([
      "LSTM (PyTorch)",
      "Voting Ensemble",
      "LightGBM",
      "MLP (64, 32)",
    ]);
  } else if (groupType === "dl") {
    APP_STATE.win2.selectedModels = new Set([
      "LSTM (PyTorch)",
      "MLP (64, 32)",
    ]);
  } else if (groupType === "all") {
    APP_STATE.win2.selectedModels = new Set(
      APP_STATE.meta.models.map((m) => m.name)
    );
  }
  setGroupButtons(groupType);
  renderModelChips();
  renderAllStationWindowCharts();
}

function toggleResidualMode() {
  APP_STATE.win2.residualMode = !APP_STATE.win2.residualMode;
  const btn = byId("btn-toggle-residual");
  if (btn) {
    btn.classList.toggle("is-active", APP_STATE.win2.residualMode);
    btn.textContent = APP_STATE.win2.residualMode ? "View Actual Observations" : "View Forecast Residuals";
  }
  renderAllStationWindowCharts();
}

/** Station view: "ALL" = 3-column grid, or a single station in detail mode. */
function setStationView(view) {
  APP_STATE.win2.stationView = view;
  setSegActive(["sv-btn-ALL", ...STATION_KEYS.map((rk) => `sv-btn-${rk}`)], `sv-btn-${view}`);
  const grid = byId("station-grid");
  if (grid) grid.classList.toggle("is-detail", view !== "ALL");
  STATION_KEYS.forEach((rk) => {
    byId(`station-panel-${rk}`)?.classList.toggle("is-hidden", view !== "ALL" && view !== rk);
  });
  renderAllStationWindowCharts();
}

function toggleStationFocus(rk) {
  setStationView(APP_STATE.win2.stationView === rk ? "ALL" : rk);
}

async function loadDashboardWindow() {
  const sc = APP_STATE.win2.scenario;
  const startDate = byId("win2-start-date").value;
  const endDate = byId("win2-end-date").value;
  const sourceMode = byId("win2-source-mode").value;
  const regionFilter = byId("lb-region-filter").value;

  const params = new URLSearchParams({
    scenario: sc,
    source_mode: sourceMode,
    region_filter: regionFilter,
  });
  if (startDate) params.set("start_date", startDate);
  if (endDate) params.set("end_date", endDate);

  const seq = ++APP_STATE.win2.loadSeq;
  beginBusy(WIN2_BUSY_TARGETS);
  try {
    const resp = await fetch(`/api/dashboard-window?${params.toString()}`);
    const data = await resp.json();
    if (seq !== APP_STATE.win2.loadSeq) return;
    APP_STATE.win2.dashboardData = data;

    byId("win2-start-date").value = data.start_date;
    byId("win2-end-date").value = data.end_date;
    if (data.max_available_date) {
      const sEl = byId("win2-start-date");
      const eEl = byId("win2-end-date");
      if (sEl) sEl.max = data.max_available_date;
      if (eEl) eEl.max = data.max_available_date;
    }

    const alertEl = byId("dual-source-alert");
    if (alertEl) alertEl.classList.toggle("hidden", !data.has_dual_source_overlap);

    renderKpiCards(data);
    renderAllStationWindowCharts();
    renderHeadToHeadBattle(data.head_to_head);
    renderDynamicLeaderboard(data);
  } catch (err) {
    console.error("Failed to load dashboard window:", err);
  } finally {
    endBusy(WIN2_BUSY_TARGETS);
  }
}

function renderKpiCards(data) {
  const lb = data.leaderboard || [];
  const top = lb[0];
  const second = lb[1];
  const scLabel = data.scenario === "24h" ? "24h Day-Ahead" : "1h Nowcasting";
  const regionSel = byId("lb-region-filter");
  const regionLabel = regionSel ? regionSel.options[regionSel.selectedIndex].text : "";

  // [Leading model]
  if (top) {
    setText("kpi-leader-name", top.model);
    const dot = byId("kpi-leader-dot");
    if (dot) dot.style.background = top.color || "#64748b";
    byId("kpi-card-leader")?.style.setProperty("--kpi-accent", top.color || "#7c3aed");
    setText("kpi-leader-sub", `${top.family} · ${scLabel} · ${regionLabel}`);
  } else {
    setText("kpi-leader-name", "--");
    setText("kpi-leader-sub", "No data in selected window");
  }

  // [Best MAE]
  if (top) {
    setText("kpi-mae-val", top.MAE.toFixed(2));
    const gap = second ? ` · +${(second.MAE - top.MAE).toFixed(2)} vs #2` : "";
    setText("kpi-mae-sub", `RMSE ${top.RMSE.toFixed(2)} · R² ${top.R2.toFixed(3)}${gap}`);
  } else {
    setText("kpi-mae-val", "--");
    setText("kpi-mae-sub", "--");
  }

  // [Total observed hours]
  const total = Number(data.total_window_records || 0);
  setText("kpi-hours-val", total.toLocaleString());
  let days = "";
  if (data.start_date && data.end_date) {
    const n = Math.round((new Date(data.end_date) - new Date(data.start_date)) / 86400000) + 1;
    if (Number.isFinite(n) && n > 0) days = ` · ${n} days`;
  }
  setText("kpi-hours-sub", `${data.start_date} → ${data.end_date}${days}`);

  // [Hours AQI > 150]
  const extreme = Number(data.extreme_hours_150 || 0);
  setText("kpi-extreme-val", extreme.toLocaleString());
  const pct = total > 0 ? ((extreme / total) * 100).toFixed(1) : "0.0";
  setText(
    "kpi-extreme-sub",
    extreme > 0 ? `${pct}% of observation hours · smoke / inversion alert` : "No extreme pollution hours recorded"
  );
  const isLight = APP_STATE.theme === "light";
  const exCard = byId("kpi-card-extreme");
  if (exCard) {
    if (extreme > 0) {
      exCard.style.setProperty("--kpi-accent", "#f43f5e");
      exCard.classList.remove("is-safe");
    } else {
      exCard.style.setProperty("--kpi-accent", "#10b981");
      exCard.classList.add("is-safe");
    }
  }
  const exVal = byId("kpi-extreme-val");
  if (exVal) {
    exVal.className = extreme > 0
      ? (isLight ? "text-rose-600 font-bold" : "text-rose-300 font-bold")
      : (isLight ? "text-emerald-700 font-bold" : "text-emerald-300 font-bold");
  }
}

function renderAllStationWindowCharts() {
  const data = APP_STATE.win2.dashboardData;
  if (!data || !data.stations) return;

  const tc = getChartThemeColors();
  const view = APP_STATE.win2.stationView;
  const isDetail = view !== "ALL";

  const colorMap = {};
  if (APP_STATE.meta && APP_STATE.meta.models) {
    APP_STATE.meta.models.forEach((m) => {
      colorMap[m.name] = m.color;
    });
  }

  STATION_KEYS.forEach((rk) => {
    const stObj = data.stations[rk];
    const ch = APP_STATE.charts[`win2_${rk}`];
    const metaEl = byId(`chart-meta-${rk}`);
    const badgesEl = byId(`chart-badges-${rk}`);
    if (!ch || !stObj) return;
    if (isDetail && rk !== view) return; // hidden panel: skip work, re-rendered on return
    ch.resize();

    if (stObj.empty || !stObj.timestamps || stObj.timestamps.length === 0) {
      if (rk === "SJ") {
        metaEl.textContent = "Open-Meteo coverage starts 2023. Historical 2018–2022 monitored via Fresno & LA.";
        badgesEl.innerHTML = `<span class="px-1.5 py-0.5 rounded bg-amber-950/60 border border-amber-800 text-amber-300 text-[10px] font-mono">Active 2023–2026</span>`;
      } else {
        metaEl.textContent = "No records match the filter criteria.";
        badgesEl.innerHTML = `<span class="px-1.5 py-0.5 rounded bg-slate-900 border border-slate-800 text-slate-500">0 records</span>`;
      }
      ch.clear();
      ch.setOption({
        graphic: {
          type: "text",
          left: "center",
          top: "middle",
          style: {
            text: rk === "SJ"
              ? "San Jose (Bay Area) joined dataset in 2023 via Open-Meteo atmospheric analysis.\nThis historical event was recorded by Fresno & Los Angeles EPA ground stations."
              : "No records found for this station in the selected time window.",
            textAlign: "center",
            fill: tc.subText,
            fontSize: 12,
            lineHeight: 18,
            fontFamily: "Inter, sans-serif"
          }
        }
      });
      return;
    }

    const meanAqi = Number(stObj.mean_aqi || 0);
    const maxAqi = Number(stObj.max_aqi || 0);
    const meanTheme = getAqiTheme(meanAqi);
    const maxTheme = getAqiTheme(maxAqi);
    const isLight = APP_STATE.theme === "light";

    const panelEl = byId(`station-panel-${rk}`);
    if (panelEl) {
      panelEl.style.setProperty("--station-accent", meanTheme.hex);
      panelEl.style.setProperty("--station-bg-tint", meanTheme.bgLight);
      panelEl.style.setProperty("--station-border-tint", meanTheme.borderLight);
    }

    metaEl.textContent = `${formatActiveSources(stObj.active_sources)} · ${stObj.record_count.toLocaleString()} hours`;
    metaEl.title = `Sources: ${formatActiveSources(stObj.active_sources)} · Observations: ${stObj.record_count.toLocaleString()} hours`;
    badgesEl.innerHTML = `
      <span class="px-2 py-0.5 rounded text-[10px] font-mono font-medium border"
        style="background: ${isLight ? meanTheme.bgLight : 'rgba(15, 23, 42, 0.8)'}; border-color: ${isLight ? meanTheme.borderLight : '#334155'}; color: ${isLight ? meanTheme.textLight : '#cbd5e1'};"
        title="Average AQI in selected time window">
        Avg <strong style="color: ${isLight ? meanTheme.textLight : meanTheme.hex}">${stObj.mean_aqi}</strong> [${meanTheme.short}]
      </span>
      <span class="px-2 py-0.5 rounded text-[10px] font-mono font-medium border"
        style="background: ${isLight ? maxTheme.bgLight : 'rgba(15, 23, 42, 0.8)'}; border-color: ${isLight ? maxTheme.borderLight : '#334155'}; color: ${isLight ? maxTheme.textLight : '#cbd5e1'};"
        title="Peak AQI recorded">
        Max <strong style="color: ${isLight ? maxTheme.textLight : maxTheme.hex}">${stObj.max_aqi}</strong>
      </span>
    `;

    const series = [];

    if (!APP_STATE.win2.residualMode) {
      series.push({
        name: "Observed (Actual AQI)",
        type: "line",
        data: stObj.actual,
        symbol: "none",
        lineStyle: { color: tc.actualLineColor, width: isDetail ? 2.5 : 2 },
        itemStyle: { color: tc.actualItemColor },
        z: 10,
      });

      if (stObj.dual_openmeteo_actual) {
        series.push({
          name: "Observed (Atmospheric Model)",
          type: "line",
          data: stObj.dual_openmeteo_actual,
          symbol: "none",
          lineStyle: { color: "#38bdf8", width: 1.8, type: "dashed" },
          itemStyle: { color: "#38bdf8" },
          z: 9,
        });
      }
    }

    APP_STATE.win2.selectedModels.forEach((mName) => {
      const mVals = stObj.models[mName];
      if (!mVals) return;

      const plotData = APP_STATE.win2.residualMode
        ? mVals.map((v, i) => Number(Math.abs(stObj.actual[i] - v).toFixed(2)))
        : mVals;

      const isPrimary =
        mName === "LSTM (PyTorch)" || mName === "Voting Ensemble";
      series.push({
        name: mName,
        type: "line",
        data: plotData,
        symbol: "none",
        smooth: true,
        lineStyle: {
          color: colorMap[mName] || "#94a3b8",
          width: isPrimary ? 2.2 : 1.4,
          type: mName === "MLP (64, 32)" ? "dashed" : "solid",
        },
        itemStyle: { color: colorMap[mName] || "#94a3b8" },
      });
    });

    const option = {
      backgroundColor: "transparent",
      animation: false,
      tooltip: {
        trigger: "axis",
        ...tc.tooltip,
      },
      legend: {
        show: isDetail,
        top: 0,
        itemWidth: 14,
        itemHeight: 8,
        textStyle: { color: tc.legendText, fontSize: 11 },
      },
      grid: isDetail
        ? { left: 45, right: 20, top: 30, bottom: 48 }
        : { left: 38, right: 10, top: 14, bottom: 42 },
      dataZoom: [
        { type: "inside", start: 0, end: 100 },
        {
          type: "slider",
          height: isDetail ? 16 : 14,
          bottom: 6,
          borderColor: tc.axisLineColor,
          textStyle: { color: tc.text, fontSize: 9 },
          showDetail: isDetail,
        },
      ],
      xAxis: {
        type: "category",
        data: stObj.timestamps,
        axisLabel: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace", hideOverlap: true },
        axisLine: { lineStyle: { color: tc.axisLineColor } },
      },
      yAxis: {
        type: "value",
        name: APP_STATE.win2.residualMode ? "Absolute Residual" : "AQI",
        nameTextStyle: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace" },
        axisLabel: { color: tc.text, fontSize: 10, fontFamily: "JetBrains Mono, monospace" },
        splitLine: { lineStyle: { color: tc.splitLineColor } },
      },
      series,
    };

    ch.setOption(option, true);
  });
}

function renderHeadToHeadBattle(b) {
  if (!b || !b.total_hours) {
    byId("battle-win-bar").style.width = "50%";
    setText("battle-win-rate", "--%");
    setText("battle-hours-count", "0 hours");
    setText("battle-lstm-mae", "-- AQI");
    setText("battle-mlp-mae", "-- AQI");
    setText("battle-summary-box", "Insufficient data in selected window to compare models.");
    return;
  }
  byId("battle-win-bar").style.width = `${b.lstm_win_rate_pct}%`;
  setText("battle-win-rate", `${b.lstm_win_rate_pct}%`);
  setText(
    "battle-hours-count",
    `${b.lstm_wins_count.toLocaleString()} / ${b.total_hours.toLocaleString()} hours`
  );
  setText("battle-lstm-mae", `${b.lstm_mae.toFixed(2)} AQI`);
  setText("battle-mlp-mae", `${b.mlp_mae.toFixed(2)} AQI`);

  const summaryEl = byId("battle-summary-box");
  if (b.mae_saved >= 0) {
    summaryEl.innerHTML = `Across the selected window, <strong>Spatio-Temporal LSTM</strong> achieved lower prediction error by <strong>-${b.mae_saved.toFixed(2)} MAE</strong> (a <strong>${b.improvement_pct}%</strong> reduction) compared to Feedforward <strong>MLP (64, 32)</strong>.`;
  } else {
    summaryEl.innerHTML = `Across this short-term window, both Deep Learning models performed comparably (difference of ${Math.abs(b.mae_saved).toFixed(2)} MAE).`;
  }
}

function renderDynamicLeaderboard(data) {
  const tbody = byId("dynamic-leaderboard-tbody");
  const subEl = byId("lb-window-subtitle");
  if (!tbody || !data) return;

  if (subEl) {
    subEl.textContent = `Window: ${data.start_date} → ${data.end_date} · Total ${data.total_window_records.toLocaleString()} observations · Extreme pollution hours (AQI > 150): ${data.extreme_hours_150} hours`;
    subEl.title = subEl.textContent;
  }

  if (!data.leaderboard || data.leaderboard.length === 0) {
    tbody.innerHTML = `<tr><td colspan="9" class="text-center text-slate-500 py-6 font-sans">No evaluation records available for the selected window.</td></tr>`;
    return;
  }

  const maxMae = Math.max(...data.leaderboard.map((r) => r.MAE)) || 1;

  tbody.innerHTML = data.leaderboard
    .map((r) => {
      const rankBadge =
        r.rank === 1
          ? `<span class="px-1.5 py-0.5 rounded bg-emerald-950 text-emerald-300 border border-emerald-800 font-bold">#01</span>`
          : r.rank === 2
          ? `<span class="px-1.5 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-700">#02</span>`
          : r.rank === 3
          ? `<span class="px-1.5 py-0.5 rounded bg-slate-900 text-slate-300 border border-slate-700">#03</span>`
          : `<span class="text-slate-500 pl-1 font-mono">#${String(r.rank).padStart(2, "0")}</span>`;

      const isHighlight =
        r.model === "LSTM (PyTorch)" || r.model === "Voting Ensemble";
      const rowCls = isHighlight ? "bg-slate-900/70" : "";
      const barPct = Math.max(4, (r.MAE / maxMae) * 100);

      return `
        <tr class="${rowCls}">
          <td>${rankBadge}</td>
          <td class="font-semibold text-slate-100 font-sans">
            <span class="inline-flex items-center gap-2">
              <span class="w-2 h-2 rounded-full inline-block" style="background:${r.color};"></span>
              <span>${r.model}</span>
            </span>
          </td>
          <td class="text-slate-400 font-sans">${r.family}</td>
          <td class="text-right">
            <span class="inline-flex items-center justify-end gap-2">
              <span class="w-12 h-1 bg-slate-800 rounded overflow-hidden"><span class="block h-full rounded ${r.rank === 1 ? "bg-emerald-400" : "bg-slate-500"}" style="width:${barPct}%"></span></span>
              <strong class="${r.rank === 1 ? "text-emerald-300" : "text-slate-100"}">${r.MAE.toFixed(2)}</strong>
            </span>
          </td>
          <td class="text-right text-slate-300">${r.RMSE.toFixed(2)}</td>
          <td class="text-right text-slate-300">${r.R2.toFixed(4)}</td>
          <td class="text-right text-slate-400">${r.sMAPE.toFixed(2)}%</td>
          <td class="text-right text-slate-300">${r.F1_150 !== null ? r.F1_150.toFixed(4) : '<span class="text-slate-600 font-sans">N/A</span>'}</td>
          <td class="text-right text-slate-400">${r.max_error.toFixed(1)}</td>
        </tr>
      `;
    })
    .join("");
}

function exportWindowLeaderboardCSV() {
  const data = APP_STATE.win2.dashboardData;
  if (!data || !data.leaderboard) return;
  const headers = [
    "rank",
    "model",
    "family",
    "MAE",
    "RMSE",
    "R2",
    "sMAPE",
    "F1_150",
    "max_error",
  ];
  const lines = [
    headers.join(","),
    ...data.leaderboard.map((r) =>
      headers.map((h) => JSON.stringify(r[h] ?? "")).join(",")
    ),
  ];
  downloadCSVBlob(
    lines.join("\n"),
    `leaderboard_${data.scenario}_${data.start_date}_to_${data.end_date}.csv`
  );
}

function downloadCSVBlob(csvContent, filename) {
  const blob = new Blob(["\uFEFF" + csvContent], {
    type: "text/csv;charset=utf-8;",
  });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}
