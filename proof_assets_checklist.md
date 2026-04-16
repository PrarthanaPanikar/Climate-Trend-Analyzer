## Proof assets checklist (what to capture for GitHub + interviews)

### Recommended screenshots (save in `images/`)
- `01_dataset_preview.png` (df.head() + df.info())
- `02_missing_before.png` (missing values table before preprocessing)
- `03_missing_after.png` (missing values table after preprocessing)
- `04_temperature_trend.png` (time-series temperature plot)
- `05_rainfall_trend.png` (time-series rainfall plot)
- `06_seasonality_heatmap.png` (monthly heatmap)
- `07_temperature_anomalies.png` (anomaly plot with red markers)
- `08_yearly_comparison.png` (optional: yearly mean bar chart)
- `09_temperature_forecast.png` (forecast with confidence interval)
- `10_streamlit_dashboard.png` (dashboard screenshot)
- `11_github_repo.png` (repo front page)
- `12_readme_preview.png` (README rendered view)

### Recommended short demo video (30–60s)
- Run `python main.py` and show created files in `outputs/`
- Run `streamlit run app/streamlit_app.py` and switch region/metric

### Where to reference in README
Use markdown:
```markdown
![Temperature anomalies](images/07_temperature_anomalies.png)
```
