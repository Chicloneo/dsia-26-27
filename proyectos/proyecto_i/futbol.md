# Proyecto de fútbol
---
Santiago Lillo Macías - DSIA, MUIAAp 2026
---

El proyecto procesa filas de futbolistas del conjunto de datos de Transfermarkt: valida los datos, normaliza algunos valores y separa las filas válidas de las que contienen errores.

## Datos

Los CSV proceden del conjunto [Football Data from Transfermarkt](https://www.kaggle.com/datasets/davidcariboo/player-scores). El fichero de jugadores utilizado está en `futbol/datos/datos_transfermarkt/players.csv`.

## Estructura

- `futbol/contracts.py`: contratos Pydantic de entrada y salida; valida rangos, reemplaza algunos valores vacíos y convierte los códigos de las cinco grandes ligas en sus nombres.

- `futbol/preprocess.py`: construye el modelo de salida con las columnas seleccionadas.

- `futbol/cli.py`: lee el CSV, valida cada fila y escribe los futbolistas limpios y los errores.

- `tests/test_futbolistas.py`: pruebas unitarias y una prueba de integración de la CLI con un CSV temporal.

- `futbol/datos/`: datos de entrada y resultados generados.

## Comandos

El repositorio raíz es `dsia-26-27`; desde allí, entra en la carpeta `futbol` y ejecuta el programa:

```bash
cd proyectos/proyecto_i/futbol
uv run --project ../.. --no-sync python cli.py \
  --input datos/datos_transfermarkt/players.csv \
  --output datos/outputs/futbolistas_clean.csv
```

Para ejecutar solo las pruebas de fútbol:

```bash
cd proyectos/proyecto_i
uv run --project ../.. --no-sync python -m pytest -q tests/test_futbolistas.py
```

Para excluir la prueba de integración o ejecutar solo esa prueba:

```bash
uv run --project ../.. --no-sync python -m pytest -q tests/test_futbolistas.py -m "not integration"
uv run --project ../.. --no-sync python -m pytest -q tests/test_futbolistas.py -m integration
```

Para medir la cobertura de fútbol:

```bash
uv run --project ../.. --no-sync python -m pytest -q tests/test_futbolistas.py \
  --cov=futbol --cov-report=term-missing --cov-fail-under=60
```

## Resultado real de las pruebas y cobertura

Salida obtenida al ejecutar el comando de cobertura de fútbol:

```text
...................                                                      [100%]
================================ tests coverage ================================
_______________ coverage: platform darwin, python 3.14.7-final-0 _______________

Name                   Stmts   Miss  Cover   Missing
----------------------------------------------------
futbol/__init__.py         0      0   100%
futbol/cli.py             38      1    97%   68
futbol/contracts.py       72      0   100%
futbol/preprocess.py       7      1    86%   6
----------------------------------------------------
TOTAL                    117      2    98%
Required test coverage of 60% reached. Total coverage: 98.29%
19 passed in 0.31s
```

El CI también ejecuta las pruebas de ventas: **33 tests** y **98,40 %** de cobertura agregada en la última ejecución verificada.


## Validación y valores vacíos con Pydantic

- Los tipos `str | None` o `int | None` permiten que el valor sea `None`, pero **no hacen que el campo pueda omitirse**. Sin un valor por defecto, Pydantic sigue exigiendo que la columna esté presente.

- El CSV se lee con `keep_default_na=False`, así que las celdas vacías llegan como `""`. Los validadores `mode="before"` sustituyen algunas antes de la validación de tipos:

  - `foot`: elige al azar `right`, `both` o `left` con probabilidades 60 %, 30 % y 10 % (probabilidades estimadas de ser diestro, ambidiestro o zurdo de pie).

  - `height_in_cm`: usa `176` (media de hombres de 18 a 40 años).

  - `international_caps` e `international_goals`: usan `0` si no hay datos disponibles.

  - Ciudad, ciudadanía, fecha de nacimiento, fecha de fin de contrato, agente, selección nacional, competición y club: usan `None`.

- La competición se convierte del código de las cinco grandes ligas a su nombre; los demás códigos se conservan. Por ejemplo, `ES1` -> `La Liga`
