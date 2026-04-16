import pandas as pd
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose


def compute_trend_metrics(df: pd.DataFrame, metrics: list[str]) -> pd.DataFrame:
    """
    Computes OLS slope (per decade) for each metric in a region-level dataframe.
    Returns slope_per_decade + p_value + r2.
    """
    d = df.copy().sort_values("date")
    t_years = (d["date"] - d["date"].min()).dt.days / 365.25
    X = sm.add_constant(t_years.values)

    rows: list[dict] = []
    for m in metrics:
        y = d[m].values
        model = sm.OLS(y, X, missing="drop").fit()
        slope_per_year = float(model.params[1])
        rows.append(
            {
                "metric": m,
                "slope_per_decade": slope_per_year * 10.0,
                "p_value": float(model.pvalues[1]),
                "r2": float(model.rsquared),
            }
        )

    return pd.DataFrame(rows)


def seasonal_decompose_series(series: pd.Series, period: int = 12) -> dict[str, pd.Series]:
    """
    Seasonal decomposition for a monthly series.
    Returns dict: observed/trend/seasonal/resid.
    """
    s = series.astype(float)
    result = seasonal_decompose(s, model="additive", period=period, extrapolate_trend="freq")
    return {
        "observed": result.observed,
        "trend": result.trend,
        "seasonal": result.seasonal,
        "resid": result.resid,
    }
