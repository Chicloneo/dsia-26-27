import argparse
#from X import limpiar_ventas

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