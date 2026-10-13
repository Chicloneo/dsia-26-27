from typing import Literal 
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
import pandas as pd


# ---------------------------------------------------------------------------
# modelo de ENTRADA (una fila de Datos/ventas.csv)
# ---------------------------------------------------------------------------
class Venta(BaseModel):
    """Ya hemos eliminado las urls"""
    'player_id',
    'first_name',
    'last_name',
    'name',
    'last_season',
    'current_club_id',
    'player_code',
    'country_of_birth',
    'city_of_birth',
    'country_of_citizenship',
    'date_of_birth',
    'sub_position',
    'position',
    'foot',
    'height_in_cm',
    'contract_expiration_date',
    'agent_name',
    'international_caps',
    'international_goals',
    'current_national_team_id',
    'current_club_domestic_competition_id',
    'current_club_name',
    'market_value_in_eur',
    'highest_market_value_in_eur'

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