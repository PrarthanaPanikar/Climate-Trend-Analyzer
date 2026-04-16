from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJECT_ROOT / "data"
OUTPUTS_DIR = PROJECT_ROOT / "outputs"

DEFAULT_DATA_OUT = DATA_DIR / "processed" / "climate_processed.csv"

FIGURES_DIR = OUTPUTS_DIR / "figures"
TABLES_DIR = OUTPUTS_DIR / "tables"
SUMMARY_DIR = OUTPUTS_DIR / "summary"
