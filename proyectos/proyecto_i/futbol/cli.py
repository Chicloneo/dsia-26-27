"""
Ejemplo en terminal:

uv run cli.py --input datos/datos_transfermarkt/players.csv --output datos/outputs/futbolistas_clean.csv
Hay 38211 futbolistas válidos y 11938 futbolistas con error
"""

import argparse
import pandas as pd
from pydantic import ValidationError
from pathlib import Path

from contracts import Futbolista, Futbolista_salida
from preprocess import eliminar_columnas, preprocess


def read_footballers(path:str) -> list[Futbolista_salida]:
    """Leer el CSV y devolver la lista de futbolistas validos"""

    ruta = Path(path)
    
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el fichero: {ruta}")

    df = pd.read_csv(ruta, keep_default_na=False)

    futbolistas_validados = []
    futbolistas_con_error = []
    for index, row in df.iterrows():
        try:
            futbolista_valido = Futbolista(**row.to_dict())
            futbolistas_validados.append(preprocess(futbolista_valido))
        except:
            # Caso en que la fila no es válida
            futbolistas_con_error.append(row)

    # Devolver la lista con todos las futbolistas validados.
    return futbolistas_validados, futbolistas_con_error

    

def main(argv=None):
    # Ya hecho: lee los argumentos --input, --output y --model.
    parser = argparse.ArgumentParser(description="Validacion de futbolistas")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args(argv) 

    try:
        futbolistas_validados, futbolistas_con_error = read_footballers(args.input)
    except ValueError as e:
        print(f"Error: {e}")
        return 2

    df_valido = pd.DataFrame(
        [futbolista.model_dump() for futbolista in futbolistas_validados]
    )
    df_valido.to_csv(args.output, index=False)

    df_error = pd.DataFrame(futbolistas_con_error)
    df_error.to_csv("datos/outputs/futbolistas_con_error.csv", index=False)

    print(f"Hay {len(futbolistas_validados)} futbolistas válidos y {len(futbolistas_con_error)} futbolistas con error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
