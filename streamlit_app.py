from pathlib import Path

import pandas as pd
import streamlit as st

from src.config import DEFAULT_DATA_OUT, FIGURES_DIR
from src.viz.plots import plot_metric_timeseries


st.set_page_config(page_title="Climate Trend Analyzer", layout="wide")
st.title("Climate Trend Analyzer (Student Portfolio Project)")

data_path = Path(DEFAULT_DATA_OUT)
if not data_path.exists():
    st.warning("Processed dataset not found. Run: `python main.py` first.")
    st.stop()

df = pd.read_csv(data_path)
df["date"] = pd.to_datetime(df["date"])

region = st.sidebar.selectbox("Select Region", sorted(df["region"].unique()))
metric = st.sidebar.selectbox("Select Metric", ["temp_c", "rain_mm", "co2_ppm", "sea_level_mm"])

region_df = df[df["region"] == region].sort_values("date")

st.subheader(f"{metric} over time — {region}")
st.line_chart(region_df.set_index("date")[metric])

st.subheader("Quick stats")
c1, c2, c3 = st.columns(3)
c1.metric("Start", f"{region_df[metric].iloc[0]:.2f}")
c2.metric("Latest", f"{region_df[metric].iloc[-1]:.2f}")
c3.metric("Mean", f"{region_df[metric].mean():.2f}")

if st.button("Save chart to outputs/figures"):
    out_path = FIGURES_DIR / f"streamlit_saved_{metric}_{region}.png"
    plot_metric_timeseries(region_df, metric, out_path)
    st.success(f"Saved: {out_path.as_posix()}")
