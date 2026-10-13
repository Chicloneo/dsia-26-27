`loader.py` tiene dos funcionalidades:

- La función load recibe el path del csv de entrada y devuelve un dataframe

- Si no existe el path, devuelve un error personalizado `DataLoadError`. 

---

`validator.py` es un contrato de datos (salida) / preprocesado:

- `validar_ventas` recibe un DataFrame y devuelve df_valido, df_error

    - df_valido es un DataFrame con filas validadas según nuestro criterio

    - df_error es un DataFrame con el resto de filas

- `limpiar_ventas` recibe un path del csv de entrada y un path del csv de salida. Escribe un csv de salida según la ruta, y adicionalmente un json con metadatos del csv (calidad, cuántas filas válidas, etc.)