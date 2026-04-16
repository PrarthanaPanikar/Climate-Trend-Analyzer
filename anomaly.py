import numpy as np
import pandas as pd


def _robust_zscore(x: np.ndarray) -> np.ndarray:
    """
    Robust z-score using MAD (median absolute deviation).
    z = 0.6745 * (x - median) / MAD
    """
    x = np.asarray(x, dtype=float)
    med = np.nanmedian(x)
    mad = np.nanmedian(np.abs(x - med))
    if mad == 0 or np.isnan(mad):
        return (x - med) * 0.0
    return 0.6745 * (x - med) / mad


def detect_anomalies_from_residual(
    dates,
    observed,
    residual,
    metric_name: str,
    z_thresh: float = 3.5,
) -> pd.DataFrame:
    """
    Detect anomalies based on robust z-score of residuals after decomposition.
    Returns a table with anomaly dates and values.
    """
    rz = _robust_zscore(residual)
    mask = np.abs(rz) >= z_thresh

    out = pd.DataFrame(
        {
            "date": pd.to_datetime(dates),
            "metric": metric_name,
            "observed": observed,
            "residual": residual,
            "robust_z": rz,
            "is_anomaly": mask,
        }
    )

    out = out[out["is_anomaly"]].sort_values("date").reset_index(drop=True)
    return out
