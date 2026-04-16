import pandas as pd
from statsmodels.tsa.arima.model import ARIMA


def forecast_arima(series: pd.Series, steps: int = 24) -> pd.DataFrame:
    """
    Simple ARIMA forecast for a univariate monthly series.
    Returns forecast mean and confidence intervals.
    """
    s = series.dropna().asfreq("MS")

    # Baseline order (good enough for student portfolio).
    model = ARIMA(s, order=(1, 1, 1))
    fit = model.fit()

    fc = fit.get_forecast(steps=steps)
    mean = fc.predicted_mean
    ci = fc.conf_int()

    return pd.DataFrame(
        {
            "date": mean.index,
            "forecast": mean.values,
            "lower": ci.iloc[:, 0].values,
            "upper": ci.iloc[:, 1].values,
        }
    )
