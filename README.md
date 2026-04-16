## Climate Trend Analyzer

### Overview
Climate Trend Analyzer is a portfolio-grade data science project that analyzes climate indicators (temperature, rainfall, CO₂, sea level) to uncover **long‑term trends**, **seasonal patterns**, **anomalies**, and **short‑term forecasts**.
It is designed for students to demonstrate real-world time-series analytics skills using **public datasets** or a **realistic virtual simulation** dataset.

### Problem Statement
Climate data is noisy, seasonal, and often incomplete. Stakeholders need:
- Clear long-term trends (e.g., warming rate in °C/decade)
- Seasonal behavior (monthly patterns across years)
- Anomaly detection (extreme heat / extreme rainfall months)
- Forecasts to support planning

This project builds a reproducible pipeline to generate those outputs and save them as charts + tables + a short markdown summary.

### Industry Relevance
Similar analytics are used in:
- Government climate monitoring and reporting
- Smart city resilience planning (heat/flood preparation)
- Environmental research and climate-tech analytics
- ESG and climate risk reporting (consulting/finance)

### Tech Stack
- Python 3.10+
- Pandas, NumPy
- Matplotlib, Seaborn, Plotly
- Statsmodels (seasonal decomposition, ARIMA)
- (Optional) Streamlit dashboard

### Architecture (High Level)
Raw data → Preprocessing → Trend analysis + Seasonality → Residual-based anomaly detection → Forecasting → Figures + Tables + Summary report

### Folder Structure
```
Climate-Trend-Analyzer/
├── app/                 # Streamlit dashboard
├── data/                # raw/ and processed/
├── docs/                # dataset sources + documentation
├── images/              # curated screenshots for README
├── notebooks/           # analysis notebooks (proof)
├── outputs/             # generated artifacts (figures/tables/summary)
├── reports/             # final report write-up
├── src/                 # modular pipeline code
├── tests/               # minimal tests for credibility
├── main.py              # pipeline entry point
├── requirements.txt
└── README.md
```

### Dataset Details
This repo supports two modes:
1) **Virtual simulation (default)**: realistic monthly climate time series with seasonality, trends, anomalies, and missing values.
2) **Public datasets (upgrade path)**: replace the simulation with a dataset loader (NASA/NOAA/OWID/Berkeley Earth/Kaggle).

See `docs/dataset_sources.md`.

### Installation

#### Windows (PowerShell)
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### Mac/Linux
```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### How to Run (Pipeline)
```bash
python main.py
```

### Outputs Created
- `data/processed/climate_raw_synthetic.csv`
- `data/processed/climate_processed.csv`
- `outputs/tables/trend_metrics_<region>.csv`
- `outputs/tables/anomalies_temp_<region>.csv`
- `outputs/tables/forecast_temp_<region>.csv`
- `outputs/figures/*.png`
- `outputs/summary/summary_<region>.md`

### Run the Dashboard (Optional)
```bash
streamlit run app/streamlit_app.py
```

### Proof Assets (What to capture)
Store curated screenshots in `images/` and reference them in README:
```markdown
![Temperature anomalies](images/07_temperature_anomalies.png)
```

Recommended filenames are in `docs/proof_assets_checklist.md`.

### Future Improvements
- Add real public dataset ingestion (NASA/NOAA/OWID/Berkeley Earth)
- Region-wise comparisons and KPI cards in Streamlit
- Isolation Forest anomalies, change-point detection
- SARIMA/SARIMAX forecasting with exogenous variables (CO₂)
- Geospatial mapping (GeoPandas) and choropleths

### Author
Your Name  
LinkedIn: <link>  
GitHub: <link>
