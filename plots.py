from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_metric_timeseries(df: pd.DataFrame, metric: str, out_path: Path) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(df["date"], df[metric], linewidth=1)
    plt.title(f"{metric} over time")
    plt.xlabel("Date")
    plt.ylabel(metric)
    plt.grid(True, alpha=0.3)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()

def plot_dashboard_overview(region_df: pd.DataFrame, out_path: Path, region: str) -> None:
    """
    Saves a single "dashboard-style" image (KPIs + multiple charts) suitable for GitHub proof.
    This is a static figure (not a Streamlit screenshot), but looks like a dashboard summary.
    """
    d = region_df.sort_values("date").copy()

    # KPIs
    kpis = {
        "Temp latest (°C)": float(d["temp_c"].iloc[-1]),
        "Rain latest (mm)": float(d["rain_mm"].iloc[-1]),
        "CO₂ latest (ppm)": float(d["co2_ppm"].iloc[-1]),
        "Sea lvl latest (mm)": float(d["sea_level_mm"].iloc[-1]),
    }

    fig = plt.figure(figsize=(16, 9))
    gs = fig.add_gridspec(3, 4, height_ratios=[0.9, 2.2, 2.2], hspace=0.4, wspace=0.35)

    # Header/KPI row
    ax0 = fig.add_subplot(gs[0, :])
    ax0.axis("off")
    ax0.text(0.01, 0.75, "Climate Trend Analyzer — Dashboard Snapshot", fontsize=18, fontweight="bold")
    ax0.text(0.01, 0.35, f"Region: {region} | Period: {d['date'].min().date()} → {d['date'].max().date()}", fontsize=11)

    kpi_text = "   ".join([f"{k}: {v:.2f}" for k, v in kpis.items()])
    ax0.text(0.01, 0.05, kpi_text, fontsize=12)

    # Temp chart
    ax1 = fig.add_subplot(gs[1, 0:2])
    ax1.plot(d["date"], d["temp_c"], linewidth=1.2)
    ax1.set_title("Temperature (°C)")
    ax1.grid(True, alpha=0.25)

    # Rain chart
    ax2 = fig.add_subplot(gs[1, 2:4])
    ax2.plot(d["date"], d["rain_mm"], linewidth=1.2, color="#2c7fb8")
    ax2.set_title("Rainfall (mm)")
    ax2.grid(True, alpha=0.25)

    # CO2 chart
    ax3 = fig.add_subplot(gs[2, 0:2])
    ax3.plot(d["date"], d["co2_ppm"], linewidth=1.2, color="#d95f0e")
    ax3.set_title("CO₂ (ppm)")
    ax3.grid(True, alpha=0.25)

    # Sea level chart
    ax4 = fig.add_subplot(gs[2, 2:4])
    ax4.plot(d["date"], d["sea_level_mm"], linewidth=1.2, color="#756bb1")
    ax4.set_title("Sea level (mm)")
    ax4.grid(True, alpha=0.25)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close(fig)


def plot_seasonality_heatmap(df: pd.DataFrame, metric: str, out_path: Path) -> None:
    d = df.copy()
    d["year"] = d["date"].dt.year
    d["month"] = d["date"].dt.month
    pivot = d.pivot_table(index="month", columns="year", values=metric, aggfunc="mean")

    plt.figure(figsize=(16, 6))
    sns.heatmap(pivot, cmap="coolwarm", linewidths=0.1)
    plt.title(f"Seasonality heatmap: {metric}")
    plt.xlabel("Year")
    plt.ylabel("Month")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def plot_anomalies(
    dates,
    values,
    anomaly_dates,
    anomaly_values,
    out_path: Path,
    title: str,
    y_label: str,
) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(dates, values, label="Observed", linewidth=1)
    plt.scatter(anomaly_dates, anomaly_values, color="red", label="Anomaly", s=30)
    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(y_label)
    plt.grid(True, alpha=0.3)
    plt.legend()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()


def plot_forecast(
    history: pd.Series,
    forecast_df: pd.DataFrame,
    out_path: Path,
    title: str,
    y_label: str,
) -> None:
    plt.figure(figsize=(12, 5))
    plt.plot(history.index, history.values, label="History", linewidth=1)

    fc_dates = pd.to_datetime(forecast_df["date"])
    plt.plot(fc_dates, forecast_df["forecast"], label="Forecast", linewidth=2)
    plt.fill_between(fc_dates, forecast_df["lower"], forecast_df["upper"], alpha=0.2, label="95% CI")

    plt.title(title)
    plt.xlabel("Date")
    plt.ylabel(y_label)
    plt.grid(True, alpha=0.3)
    plt.legend()
    out_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(out_path, dpi=160)
    plt.close()
