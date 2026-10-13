`ventas_app`
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