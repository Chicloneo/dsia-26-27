"""Programa principal: CSV -> validacion -> preprocess -> CSV de salida.

Se ejecuta asi (desde la raiz del proyecto):
    uv run python -m ventas_app.cli --input Datos/ventas.csv --output Datos/output/ventas_limpiasj.csv

Pasos del programa:
  1. read_claims : lee el CSV y valida cada fila con ClaimRequest
  2. load_model  : carga el modelo  
  3. escribe el CSV de salida 
"""

import argparse
import pandas as pd
from pydantic import ValidationError
from pathlib import Path

from ventas_app.contracts import Venta, Venta_expandida
from ventas_app.preprocess import es_valida, preprocess

# Columnas del CSV de salida, en este orden.
OUTPUT_COLUMNS = ["fecha","region","producto","unidades","precio_unitario", "importe","cliente_id"]


def read_sales(path:str) -> list[Venta_expandida]:
    """Leer el CSV y devolver la lista de ventas validas"""

    ruta = Path(path)
    
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el fichero de ventas: {ruta}")

    df = pd.read_csv(ruta, keep_default_na=False)

    # Validar cada fila con Venta. Si alguna fila no es valida,
    #   hay que parar con un ValueError cuyo mensaje diga en que LINEA del
    #   fichero esta el problema y cual es (la cabecera es la linea 1).
    ventas_validadas = []
    ventas_con_error = []
    for index, row in df.iterrows():
        try:
            venta_valida = Venta(**row.to_dict())
            ventas_validadas.append(preprocess(venta_valida))
        except:
            # Caso en que la fila no es válida
            ventas_con_error.append(row) #no sé si row o **row.to_dict()

    # Devolver la lista con todas las ventas validadas.
    return ventas_validadas, ventas_con_error


"""
    try:
        siniestros_validados = read_claims(path)
    except ValueError:
        return 2

    TypeError
"""
    

def main(argv=None):
    # Ya hecho: lee los argumentos --input, --output y --model.
    parser = argparse.ArgumentParser(description="Validacion de ventas")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv) 

    try:
        ventas_validadas, ventas_con_error = read_sales(args.input) # es una lista de ventas validadas
    except ValueError as e:
        print(f"Error: {e}")
        return 2

    df_valido = pd.DataFrame(
        [venta.model_dump() for venta in ventas_validadas]
    )
    df_valido.to_csv(args.output, index=False)

    df_error = pd.DataFrame(ventas_con_error)
    df_error.to_csv("Datos/output/ventas_con_error.csv", index=False)

    print(f"Hay {len(ventas_validadas)} ventas validas y {len(ventas_con_error)} ventas con error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
