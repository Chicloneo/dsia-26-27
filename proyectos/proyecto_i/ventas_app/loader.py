from pathlib import Path
import pandas as pd
from pandas import DataFrame


class DataLoadError(Exception):
    """Error al cargar datos de origen."""

def load(path:str) -> DataFrame:
    ruta = Path(path)

    if not ruta.exists():
        raise DataLoadError(f"Error al cargar datos: El path '{ruta}' no existe.")

    return pd.read_csv(ruta)
