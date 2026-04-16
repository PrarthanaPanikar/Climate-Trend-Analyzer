from pathlib import Path

import pandas as pd

from src.config import DEFAULT_DATA_OUT, FIGURES_DIR, SUMMARY_DIR, TABLES_DIR
from src.data.make_dataset import generate_synthetic_climate_dataset
from src.data.preprocess import preprocess_climate_data
from src.analysis.anomaly import detect_anomalies_from_residual
from src.analysis.forecast import forecast_arima
from src.analysis.trends import compute_trend_metrics, seasonal_decompose_series
from src.utils.io import ensure_dirs, save_markdown
from src.viz.plots import (
    plot_anomalies,
    plot_dashboard_overview,
    plot_forecast,
    plot_metric_timeseries,
    plot_seasonality_heatmap,
)


def run_pipeline(region: str = "Region_A") -> None:
    ensure_dirs(
        [
            DEFAULT_DATA_OUT.parent,
            FIGURES_DIR,
            TABLES_DIR,
            SUMMARY_DIR,
            Path("data/raw"),
        ]
    )

    # 1) Virtual simulation dataset (realistic synthetic monthly climate series)
    raw_df = generate_synthetic_climate_dataset(seed=42)
    raw_path = DEFAULT_DATA_OUT.parent / "climate_raw_synthetic.csv"
    raw_df.to_csv(raw_path, index=False)

    # 2) Preprocess
    df = preprocess_climate_data(raw_df)
    df.to_csv(DEFAULT_DATA_OUT, index=False)

    # 3) Focus on one region for decomposition/forecast visuals
    region_df = df[df["region"] == region].copy()
    region_df = region_df.sort_values("date")

    summary_lines: list[str] = []
    summary_lines.append(f"## Climate Trend Analyzer Summary ({region})\n")
    summary_lines.append("Generated from the virtual simulation dataset.\n")

    # 4) Trend metrics (per decade)
    trend_metrics = compute_trend_metrics(
        region_df, metrics=["temp_c", "rain_mm", "co2_ppm", "sea_level_mm"]
    )
    metrics_path = TABLES_DIR / f"trend_metrics_{region}.csv"
    trend_metrics.to_csv(metrics_path, index=False)

    summary_lines.append("### Trend metrics (per decade)\n")
    summary_lines.append(trend_metrics.to_markdown(index=False))
    summary_lines.append("")

    # 5) Seasonal decomposition + anomaly detection for temperature
    temp_series = region_df.set_index("date")["temp_c"].asfreq("MS")
    decomp = seasonal_decompose_series(temp_series, period=12)

    anomalies = detect_anomalies_from_residual(
        dates=temp_series.index,
        observed=temp_series.values,
        residual=decomp["resid"].values,
        metric_name="temp_c",
        z_thresh=3.5,
    )
    anomalies_path = TABLES_DIR / f"anomalies_temp_{region}.csv"
    anomalies.to_csv(anomalies_path, index=False)

    summary_lines.append("### Detected anomalies (temperature)\n")
    summary_lines.append(f"- Saved to: `{anomalies_path.as_posix()}`\n")
    summary_lines.append(f"- Total anomalies: **{len(anomalies)}**\n")

    # 6) Forecast (ARIMA) for temperature
    forecast_df = forecast_arima(temp_series.dropna(), steps=24)
    forecast_path = TABLES_DIR / f"forecast_temp_{region}.csv"
    forecast_df.to_csv(forecast_path, index=False)

    summary_lines.append("### Forecast (temperature)\n")
    summary_lines.append(f"- Saved to: `{forecast_path.as_posix()}`\n")

    # 7) Visuals
    plot_metric_timeseries(region_df, "temp_c", FIGURES_DIR / f"temp_timeseries_{region}.png")
    plot_metric_timeseries(region_df, "rain_mm", FIGURES_DIR / f"rain_timeseries_{region}.png")
    plot_metric_timeseries(region_df, "co2_ppm", FIGURES_DIR / f"co2_timeseries_{region}.png")
    plot_metric_timeseries(
        region_df, "sea_level_mm", FIGURES_DIR / f"sea_level_timeseries_{region}.png"
    )

    plot_seasonality_heatmap(
        region_df, "temp_c", FIGURES_DIR / f"temp_seasonality_heatmap_{region}.png"
    )

    if len(anomalies) > 0:
        plot_anomalies(
            dates=temp_series.index,
            values=temp_series.values,
            anomaly_dates=pd.to_datetime(anomalies["date"]),
            anomaly_values=anomalies["observed"].values,
            out_path=FIGURES_DIR / f"temp_anomalies_{region}.png",
            title=f"Temperature anomalies ({region})",
            y_label="Temperature (°C)",
        )

    plot_forecast(
        history=temp_series,
        forecast_df=forecast_df,
        out_path=FIGURES_DIR / f"temp_forecast_{region}.png",
        title=f"Temperature forecast ({region})",
        y_label="Temperature (°C)",
    )

    # 8) Dashboard-style snapshot image (for GitHub proof)
    plot_dashboard_overview(
        region_df=region_df,
        out_path=FIGURES_DIR / f"dashboard_snapshot_{region}.png",
        region=region,
    )

    # 9) Save summary markdown
    summary_path = SUMMARY_DIR / f"summary_{region}.md"
    save_markdown(summary_path, "\n".join(summary_lines))


if __name__ == "__main__":
    run_pipeline(region="Region_A")
