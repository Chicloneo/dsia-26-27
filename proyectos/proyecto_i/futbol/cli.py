import argparse
import pandas as pd
from pydantic import ValidationError
from pathlib import Path

from futbol.contracts import Futbolista, Futbolista_salida
from futbol.preprocess import eliminar_columnas, preprocess


def read_footballers(path:str) -> list[Futbolista_salida]:
    """Leer el CSV y devolver la lista de futbolistas validos"""

    ruta = Path(path)
    
    if not ruta.exists():
        raise FileNotFoundError(f"No existe el fichero de ventas: {ruta}")

    df = pd.read_csv(ruta, keep_default_na=False)

    # Validar cada fila con Venta. Si alguna fila no es valida,
    #   hay que parar con un ValueError cuyo mensaje diga en que LINEA del
    #   fichero esta el problema y cual es (la cabecera es la linea 1).
    futbolistas_validados = []
    futbolistas_con_error = []
    for index, row in df.iterrows():
        try:
            futbolista_valido = Futbolista(**row.to_dict())
            futbolistas_validados.append(preprocess(futbolista_valido))
        except:
            # Caso en que la fila no es válida
            futbolistas_con_error.append(row)

    # Devolver la lista con todas las ventas validadas.
    return futbolistas_validados, futbolistas_con_error


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
        futbolistas_validados, futbolistas_con_error = read_footballers(args.input) # es una lista de ventas validadas
    except ValueError as e:
        print(f"Error: {e}")
        return 2

    df_valido = pd.DataFrame(
        [futbolista.model_dump() for futbolista in futbolistas_validados]
    )
    df_valido.to_csv(args.output, index=False)

    df_error = pd.DataFrame(futbolistas_con_error)
    df_error.to_csv("Datos/output/ventas_con_error.csv", index=False)

    print(f"Hay {len(futbolistas_validados)} ventas validas y {len(futbolistas_con_error)} ventas con error")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
