import os
import json
import asyncio
from contextlib import asynccontextmanager
from typing import Optional
from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from app.inference_engine import MultiModelInferenceEngine, STATION_META
from app.data_manager import AQIDataManager, WILDFIRE_PRESETS, MODEL_COLUMNS

engine = MultiModelInferenceEngine(artifacts_dir="artifacts")
data_mgr = AQIDataManager(data_dir="data")

worker_task = None


async def hourly_background_worker():
    """
    Background worker chạy liên tục trên Server 24/7:
    Mỗi 60 phút tự động kiểm tra và đồng bộ dữ liệu từ Open-Meteo cho 3 khu vực
    nếu bộ đệm đã hết hạn, giúp lịch sử thu thập không bao giờ bị đứt quãng.
    """
    await asyncio.sleep(3)
    while True:
        try:
            for rk in ["FRES", "LA", "SJ"]:
                res = data_mgr.fetch_live_or_cached_station_data(
                    region_key=rk, force_refresh=False, trigger_type="auto_worker_24_7"
                )
                if res["api_called"]:
                    fc = engine.forecast_next_24_hours(res["df"], STATION_META[rk]["openmeteo_id"])
                    data_mgr.save_live_fetch_log(
                        rk, STATION_META[rk]["openmeteo_id"], res.get("trigger_type", "auto_worker_24_7"), res["df"], fc
                    )
                await asyncio.sleep(1)
        except Exception as e:
            print(f"[BackgroundWorker] Warning: {e}")
        await asyncio.sleep(3600)


@asynccontextmanager
async def lifespan(app: FastAPI):
    global worker_task
    worker_task = asyncio.create_task(hourly_background_worker())
    yield
    if worker_task:
        worker_task.cancel()


app = FastAPI(
    title="California US AQI Live Forecaster & Model Benchmark Suite",
    description="24/7 Tailscale Server Edition — Spatio-Temporal LSTM, GBDT Ensemble, Live TreeSHAP & Dual-Source Explorer",
    version="2.0.0",
    lifespan=lifespan,
)

os.makedirs("app/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="app/static"), name="static")


class WhatIfRequest(BaseModel):
    region_key: str = "FRES"
    temperature_2m: Optional[float] = None
    relative_humidity_2m: Optional[float] = None
    wind_speed_10m: Optional[float] = None
    rain: Optional[float] = None
    wildfire_mode: Optional[bool] = False


@app.get("/")
async def serve_index():
    return FileResponse("app/static/index.html")


@app.get("/api/meta")
async def get_system_metadata():
    return {
        "stations": STATION_META,
        "wildfire_presets": WILDFIRE_PRESETS,
        "models": [
            {"col": col, "name": name, "family": fam, "color": color}
            for col, name, fam, color in MODEL_COLUMNS
        ],
        "quota": data_mgr.get_api_quota_stats(),
    }


_FORECAST_CACHE = {}


@app.get("/api/live-forecast")
async def get_live_forecast(
    region: str = Query("FRES", description="FRES | LA | SJ"),
    force_refresh: bool = Query(False, description="Force refresh with 5m cooldown guard"),
):
    rk = region.upper() if region.upper() in STATION_META else "FRES"
    meta = STATION_META[rk]
    fetch_res = data_mgr.fetch_live_or_cached_station_data(
        region_key=rk, force_refresh=force_refresh, trigger_type="user_request"
    )
    df_station = fetch_res["df"]

    # In-memory forecast cache avoids re-running 1.4s ML inference when station data is unchanged
    cache_key = (rk, fetch_res.get("last_fetched_at"))
    if not force_refresh and not fetch_res.get("api_called") and cache_key in _FORECAST_CACHE:
        fc_res = _FORECAST_CACHE[cache_key]
    else:
        fc_res = engine.forecast_next_24_hours(df_station, meta["openmeteo_id"])
        _FORECAST_CACHE[cache_key] = fc_res

    if fetch_res["api_called"]:
        data_mgr.save_live_fetch_log(
            rk, meta["openmeteo_id"], fetch_res.get("trigger_type", "user_request"), df_station, fc_res
        )

    return {
        "region_key": rk,
        "station_meta": meta,
        "cache_info": {
            "status": fetch_res["cache_status"],
            "api_called": fetch_res["api_called"],
            "age_seconds": fetch_res["age_seconds"],
            "ttl_remaining_seconds": fetch_res["ttl_remaining_seconds"],
            "cooldown_remaining_seconds": fetch_res["cooldown_remaining_seconds"],
            "last_fetched_at": fetch_res["last_fetched_at"],
            "message": fetch_res["message"],
        },
        "quota": data_mgr.get_api_quota_stats(),
        "forecast": fc_res,
        "history_logs": data_mgr.get_fetch_history(limit=25),
    }


@app.post("/api/what-if")
async def simulate_what_if(req: WhatIfRequest):
    rk = req.region_key.upper() if req.region_key.upper() in STATION_META else "FRES"
    meta = STATION_META[rk]
    fetch_res = data_mgr.fetch_live_or_cached_station_data(region_key=rk, force_refresh=False, trigger_type="what_if")
    overrides = {
        "temperature_2m": req.temperature_2m,
        "relative_humidity_2m": req.relative_humidity_2m,
        "wind_speed_10m": req.wind_speed_10m,
        "rain": req.rain,
    }
    fc_sim = engine.forecast_next_24_hours(
        fetch_res["df"],
        meta["openmeteo_id"],
        weather_overrides=overrides,
        wildfire_mode=bool(req.wildfire_mode),
    )
    return {
        "region_key": rk,
        "overrides": overrides,
        "wildfire_mode": bool(req.wildfire_mode),
        "simulated": fc_sim,
    }


@app.get("/api/history-logs")
async def get_api_logs(limit: int = 50):
    return {
        "quota": data_mgr.get_api_quota_stats(),
        "logs": data_mgr.get_fetch_history(limit=limit),
    }


@app.get("/api/historical-diurnal-heatmap")
async def get_historical_diurnal_heatmap(
    region: str = Query("FRES", description="FRES | LA | SJ | ALL"),
):
    rk = region.upper() if region.upper() in ["FRES", "LA", "SJ", "ALL"] else "FRES"
    return data_mgr.get_historical_diurnal_heatmap(rk)


@app.get("/api/dashboard-window")
async def get_dashboard_window(
    scenario: str = Query("1h", description="1h or 24h"),
    start_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="YYYY-MM-DD"),
    source_mode: str = Query("seamless", description="seamless | epa_only | openmeteo_only | both_compare"),
    region_filter: str = Query("ALL", description="ALL | FRES | LA | SJ"),
):
    sc = "24h" if scenario == "24h" else "1h"
    res = data_mgr.query_time_window_dashboard(
        scenario=sc,
        start_date=start_date,
        end_date=end_date,
        source_mode=source_mode,
        leaderboard_region=region_filter,
    )
    return res


@app.api_route("/api/reload-missing-dates", methods=["GET", "POST"])
async def reload_missing_dates():
    res = data_mgr.reload_precomputed_stores()
    return res

