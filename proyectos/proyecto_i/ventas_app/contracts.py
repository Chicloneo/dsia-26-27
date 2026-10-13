# UBICACION FINAL (ejercicio 1): src/claims_triage/contracts.py
"""Contratos de datos: describen que datos son validos.

Aqui hay DOS modelos de Pydantic:
  - ClaimRequest    -> una fila del CSV de entrada (EJERCICIO 2)
  - ClaimPrediction -> el resultado que devuelve el programa (EJERCICIO 4)

Un modelo de Pydantic es una clase con campos y tipos. Al crear un objeto,
Pydantic comprueba los datos y lanza ValidationError si algo no cuadra.
"""

from typing import Literal 
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
import pandas as pd


# ---------------------------------------------------------------------------
# modelo de ENTRADA (una fila de Datos/ventas.csv)
# ---------------------------------------------------------------------------
class Venta(BaseModel):
    """Una fila del CSV de siniestros.

    El lector de CSV entrega TODOS los valores como texto ("29", "3.5"...).
    Pydantic debe convertirlos al tipo correcto y rechazar los que no cuadren.
    """

    # No se admiten columnas que no esten declaradas en este modelo.
    model_config = ConfigDict(extra="forbid")

    fecha: str | None
    
    region: str | None
    
    producto: str | None
    
    unidades: int = Field(ge=1)             #unidades y precio_unitario no puede venir vacío

    precio_unitario: float = Field(gt=0)
    
    cliente_id: str | None

    @field_validator("fecha", "region", "producto", "cliente_id", mode="before") 
    # mode="before": recibe el valor ANTES de que Pydantic lo convierta
    @classmethod
    def empty_is_none(cls, value):
        if value == "" or value == '' or pd.isna(value):
            return None       # qué devolver cuando esta vacio
        return value          # en cualquier otro caso, el valor tal cual


# ---------------------------------------------------------------------------
# modelo de SALIDA (lo que devuelve el programa)
# ---------------------------------------------------------------------------
class Venta_expandida(BaseModel):
    """Fila de del csv ventas limpio"""

    model_config = ConfigDict(extra="forbid")
    
    fecha: str | None
    
    region: str | None
    
    producto: str | None
    
    unidades: int = Field(ge=1)             #unidades y precio_unitario no puede venir vacío

    precio_unitario: float = Field(gt=0)

    importe: float 
    
    cliente_id: str | None  

    @model_validator(mode="after")
    def verificar_importe(self):

        if self.importe < self.precio_unitario:
            raise ValueError("El importe no puede ser menor que el precio unitario")
        return self