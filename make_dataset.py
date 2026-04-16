import numpy as np
import pandas as pd


def generate_synthetic_climate_dataset(
    start: str = "1980-01-01",
    end: str = "2025-12-01",
    freq: str = "MS",
    regions: tuple[str, ...] = ("Region_A", "Region_B", "Region_C"),
    seed: int = 42,
) -> pd.DataFrame:
    """
    Virtual simulation dataset (monthly) that resembles real climate data:
    - temp_c: seasonal + long-term warming + noise + occasional heat spikes
    - rain_mm: seasonal + volatility + occasional extreme rainfall
    - co2_ppm: steady upward trend + small seasonal wiggle
    - sea_level_mm: upward trend + noise

    Also injects missing values to mimic real-world data quality issues.
    """
    rng = np.random.default_rng(seed)
    dates = pd.date_range(start=start, end=end, freq=freq)

    rows: list[dict] = []
    for r_i, region in enumerate(regions):
        # Region baselines (slightly different climates)
        temp_base = 14 + 2.0 * r_i
        rain_base = 80 + 15 * r_i
        co2_base = 338 + 0.5 * r_i
        sea_base = 0 + 10 * r_i

        # Long-term trends (force numpy arrays; avoids immutable Index operations)
        years = ((dates.year - dates.year.min()) + (dates.month - 1) / 12.0).to_numpy(dtype=float)
        warming_rate = 0.02 + 0.005 * r_i  # °C per year
        co2_rate = 1.8 + 0.1 * r_i  # ppm per year
        sea_rate = 3.2 + 0.2 * r_i  # mm per year

        # Seasonality (monthly)
        month = dates.month.to_numpy(dtype=int)
        temp_season = 6 * np.sin(2 * np.pi * (month - 1) / 12)
        rain_season = 30 * np.cos(2 * np.pi * (month - 1) / 12)

        # Noise
        temp_noise = rng.normal(0, 0.6, size=len(dates))
        rain_noise = rng.normal(0, 18, size=len(dates))
        co2_noise = rng.normal(0, 0.4, size=len(dates))
        sea_noise = rng.normal(0, 4.0, size=len(dates))

        temp = temp_base + warming_rate * years + temp_season + temp_noise
        rain = np.maximum(0, rain_base + 0.3 * years + rain_season + rain_noise)
        co2 = (
            co2_base
            + co2_rate * years
            + 1.2 * np.sin(2 * np.pi * (month - 1) / 12)
            + co2_noise
        )
        sea = sea_base + sea_rate * years + sea_noise

        # Inject anomalies: heat spikes + extreme rainfall
        heat_idx = rng.choice(len(dates), size=10, replace=False)
        rain_idx = rng.choice(len(dates), size=10, replace=False)
        temp[heat_idx] += rng.uniform(2.5, 5.0, size=len(heat_idx))
        rain[rain_idx] += rng.uniform(60, 140, size=len(rain_idx))

        # Inject missing values
        miss_idx = rng.choice(len(dates), size=12, replace=False)
        temp[miss_idx[:4]] = np.nan
        rain[miss_idx[4:8]] = np.nan
        co2[miss_idx[8:10]] = np.nan
        sea[miss_idx[10:12]] = np.nan

        for d, t, rn, c, s in zip(dates, temp, rain, co2, sea):
            rows.append(
                {
                    "date": d,
                    "region": region,
                    "temp_c": t,
                    "rain_mm": rn,
                    "co2_ppm": c,
                    "sea_level_mm": s,
                }
            )

    return pd.DataFrame(rows)
