from pathlib import Path
import pandas as pd
import json


ruta_ventas = Path('./Datos/ventas.csv')

df = pd.read_csv(ruta_ventas)

df.replace(["na", "nan"], "", inplace=True)


def validar_ventas(frame: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    unidades numérica y > 0
    precio_unitario numérico y > 0
    columnas derivadas: importe = unidades * precio_unitario solo en válidos (añado una nueva columna) 
    Devuelve (validos, errores).
    """

    #forzamos que la columna sea numérica
    unidades_num = pd.to_numeric(frame["unidades"], errors="coerce")
    precio_num = pd.to_numeric(frame["precio_unitario"], errors="coerce")

    condicion_unidades = (unidades_num > 0) & (unidades_num % 1 == 0)  # enteros positivos
    condicion_precio_unitario = precio_num > 0  # enteros o floats positivos
    condicion = condicion_unidades & condicion_precio_unitario

    df_valido = frame[condicion].copy()
    df_error = frame[~condicion].copy()

    #el df original sigue teniendo strings como na o nan
    df_valido["importe"] = (
        pd.to_numeric(df_valido["unidades"])
        * pd.to_numeric(df_valido["precio_unitario"])
    )

    return df_valido, df_error


validos, errores = validar_ventas(df)
validos.to_csv("./Datos/ventas_limpias.csv")

metricas = {
    "filas_totales": len(df),
    "filas_validas": len(validos),
    "filas_invalidas": len(errores),
    "importe_total": float(validos.groupby("producto")["importe"].sum().sum()),
}

ruta_json = Path("./Datos/calidad_datos.json")
with open(ruta_json, "w", encoding="utf-8") as archivo:
    json.dump(metricas, archivo, ensure_ascii=False, indent=4)