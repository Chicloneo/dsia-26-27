from dataclasses import dataclass
import pandas as pd
from pathlib import Path
import json

from limpieza_dataset import validar_ventas, limpiar_ventas

class ValidationError(Exception):
    """Datos que no cumplen reglas de negocio."""

@dataclass(frozen=True)
class SalesRecord:
    region: str
    producto: str
    unidades: float
    precio_unitario: float
    importe: float

    @property
    def importe(self) -> float:
        return self.unidades * self.precio_unitario

    def cumplir_condicion(self):

        condicion_unidades = (self.unidades > 0) & (self.unidades% 1 == 0)  # enteros positivos
        condicion_precio_unitario = self.precio_unitario > 0 

        return condicion_unidades & condicion_precio_unitario