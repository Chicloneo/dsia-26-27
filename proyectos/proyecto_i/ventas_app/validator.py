from dataclasses import dataclass


class ValidationError(Exception):
    """Datos que no cumplen reglas de negocio."""

@dataclass(frozen=True)
class SalesRecord:
    region: str
    product: str
    units: float
    unit_price: float

    @property
    def amount(self) -> float:
        return self.units * self.unit_price

    def cumplir_condicion(self):

        condicion_unidades = (self.units > 0) & (self.units% 1 == 0)  # enteros positivos
        condicion_precio_unitario = self.unit_price > 0 

        return condicion_unidades & condicion_precio_unitario
    