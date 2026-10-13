"""
Escribimos aquí la función limpiar_ventas que definimos en el notebook ejercicios/ejercicio_1_notebook.ipynb
Como ya la hemos probado en el notebook, sabemos que funciona
"""

import pandas as pd
from pathlib import Path
import json

def validar_ventas(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    unidades numérica y > 0
    precio_unitario numérico y > 0
    columnas derivadas: importe = unidades * precio_unitario solo en válidos (añado una nueva columna) 
    Devuelve (validos, errores).
    """

    #forzamos que la columna sea numérica
    unidades_num = pd.to_numeric(df["unidades"], errors="coerce")
    precio_num = pd.to_numeric(df["precio_unitario"], errors="coerce")

    condicion_unidades = (unidades_num > 0) & (unidades_num % 1 == 0)  # enteros positivos
    condicion_precio_unitario = precio_num > 0  # enteros o floats positivos
    condicion = condicion_unidades & condicion_precio_unitario

    df_valido = df[condicion].copy()
    df_error = df[~condicion].copy()

    #el df original sigue teniendo strings como na o nan
    df_valido["importe"] = (
        pd.to_numeric(df_valido["unidades"])
        * pd.to_numeric(df_valido["precio_unitario"])
    )
    
    print(f"{len(df_valido)} filas válidas y {len(df_error)} filas erróneas")

    return df_valido, df_error


def limpiar_ventas(path_dataset, path_salida):

    ruta_dataset_entrada = Path(path_dataset)
    df = pd.read_csv(ruta_dataset_entrada)

    df_valido, df_error = validar_ventas(df)

    ruta_csv_salida = Path(path_salida)
    df_valido.to_csv(ruta_csv_salida)

    ruta_json_salida = Path("Datos/calidad_datos.json")

    metricas = {
        "filas_totales": len(df),
        "filas_validas": len(df_valido),
        "filas_invalidas": len(df_valido),
        "importe_total": float(df_valido.groupby("producto")["importe"].sum().sum()),
    }

    with open(ruta_json_salida, "w", encoding="utf-8") as archivo:
        json.dump(metricas, archivo, ensure_ascii=False, indent=4)