import pandas as pd


def preprocess_climate_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and prepares the climate dataset for analysis:
    - ensures datetime
    - sorts by region/date
    - imputes missing values per region via time interpolation
    - adds year/month columns
    - clips obvious impossible values (basic sanity)
    """
    out = df.copy()

    out["date"] = pd.to_datetime(out["date"])
    out = out.sort_values(["region", "date"]).reset_index(drop=True)

    # Basic sanity: rainfall cannot be negative
    if "rain_mm" in out.columns:
        out.loc[out["rain_mm"] < 0, "rain_mm"] = 0

    metrics = [c for c in ["temp_c", "rain_mm", "co2_ppm", "sea_level_mm"] if c in out.columns]

    filled_parts: list[pd.DataFrame] = []
    for region, part in out.groupby("region", sort=False):
        part = part.set_index("date")
        part[metrics] = part[metrics].interpolate(method="time").ffill().bfill()
        part = part.reset_index()
        filled_parts.append(part)

    out = pd.concat(filled_parts, ignore_index=True)
    out["year"] = out["date"].dt.year
    out["month"] = out["date"].dt.month

    return out
