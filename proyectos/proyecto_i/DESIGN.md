`ventas_app/`
---

`contracts.py` tiene dos contratos:

- `Venta` para el contrato de entrada (una fila del csv inicial)

- `Venta_extendida` para el contrato de salida. Si es válida, le añadimos el importe total. 

---

`preprocess.py` es un contrato de datos (salida) / preprocesado:

- `es_valida` verifica que no hay ningún `pd.isna()`.

- Devuelve una fila de tipo `Venta_extendida` si es valida.

---

`cli.py`

Recibe un csv de entrada y devuelve un csv con las filas válidas y otro con las inválidas, según los argumentos que le pasemos por la terminal.

---

`tests/test_ventas.py`

Contiene 10 tests de distinta naturaleza. Verifican que:

- En un df hay una fila válida y dos inválidas
- La función `preprocess` devuelve un objeto de clase `Venta_expandida`.
- Calcula el importe correcto para una venta válida
- Devuelve `None` en el caso que hemos indicado
- Lanza error si no existe el path
- Valida precios dentro de los rangos del contrato
- Valida el csv `ventas.csv` correctamente (140/10) <-- este test es de integración porque comprueba todo el flujo datos
- Devuelve listas vacías si el csv es vacío

---

`pytest` en CI

```bash
pytest -q --cov=ventas_app --cov-report=term-missing --cov-fail-under=60 
```

```bash
..........                                                                             [100%]
======================================= tests coverage =======================================
______________________ coverage: platform darwin, python 3.14.7-final-0 ______________________

Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
ventas_app/__init__.py         2      1    50%   2
ventas_app/cli.py             40     16    60%   63-81, 85
ventas_app/contracts.py       22      1    95%   77
ventas_app/preprocess.py       9      0   100%
--------------------------------------------------------
TOTAL                         73     18    75%
Required test coverage of 60% reached. Total coverage: 75.34%
10 passed in 0.33s
```

Añadimos 3 tests para subir el porcentaje de coverage

```bash
.............                                                                                                                     [100%]
============================================================ tests coverage =============================================================
___________________________________________ coverage: platform darwin, python 3.14.7-final-0 ____________________________________________

Name                       Stmts   Miss  Cover   Missing
--------------------------------------------------------
ventas_app/__init__.py         0      0   100%
ventas_app/cli.py             40      1    98%   87
ventas_app/contracts.py       22      0   100%
ventas_app/preprocess.py       9      0   100%
--------------------------------------------------------
TOTAL                         71      1    99%
Required test coverage of 60% reached. Total coverage: 98.59%
13 passed in 0.39s

```