"""
Test para probar en CLI:
uv run 03_oop_clean_code_solid.py --input Datos/ventas.csv --output Datos/datos_limpios.csv
"""

import argparse
from limpieza_dataset import limpiar_ventas

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required = True,
        help = "Introduce la ruta al csv"
    )

    parser.add_argument(
        "--output",
        required = True,
        help = "Introduce la ruta donde quieres guardar el csv final"
    )

    args = parser.parse_args()

    limpiar_ventas(path_dataset = args.input, path_salida = args.output)

if __name__ == "__main__":
    main()