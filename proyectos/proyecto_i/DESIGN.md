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