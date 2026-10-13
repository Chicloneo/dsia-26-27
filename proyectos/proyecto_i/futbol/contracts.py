from typing import Literal 
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator
import pandas as pd
import random


BIG_FIVE_LEAGUES = {
    "ES1": "La Liga",
    "GB1": "Premier League",
    "L1": "Bundesliga",
    "IT1": "Serie A",
    "FR1": "Ligue 1",
}


# ---------------------------------------------------------------------------
# modelo de ENTRADA (una fila de datos/datos_transfer,arkt/players.csv)
# ---------------------------------------------------------------------------
class Futbolista(BaseModel):
    """Ya hemos eliminado las urls"""

    player_id                           : int = Field(ge=0)

    last_season                         : int = Field(ge=1950, le=2026)

    current_club_id                     : int = Field(ge=0)

    player_code                         : str = Field(min_length=1)

    country_of_birth                    : str = Field(min_length=1)

    city_of_birth                       : str | None = Field(min_length=1)

    country_of_citizenship              : str | None = Field(min_length=1)

    date_of_birth                       : str | None = Field(min_length=1)

    sub_position                        : str = Field(min_length=1)

    position                            : str = Field(min_length=1)

    foot                                : str = Field(min_length=1)

    height_in_cm                        : float | None = Field(ge=100, le=250)

    contract_expiration_date            : str | None = Field(min_length=1)

    agent_name                          : str | None = Field(min_length=1)

    international_caps                  : int | None

    international_goals                 : int | None

    current_national_team_id            : int | None = Field(ge=0)

    current_club_domestic_competition_id: str | None = Field(min_length=1)

    current_club_name                   : str | None = Field(min_length=1)

    market_value_in_eur                 : int = Field(ge=0, le=300_000_000)

    highest_market_value_in_eur         : int = Field(ge=0, le=300_000_000)


    @field_validator("foot", mode="before") 
    @classmethod
    def choose_foot(cls, value):
        if value == "" or value == '' or pd.isna(value):
            opciones = ["right", "both", "left"]
            probabilidades = [0.6, 0.3, 0.1]
            return random.choices(opciones, weights=probabilidades, k=1)[0]
        return value

    @field_validator("height_in_cm", mode="before") 
    @classmethod
    def mean_heigth(cls, value):
        if value == "" or value == '' or pd.isna(value):
            return 176
        return value

    @field_validator("international_caps", "international_goals", mode="before") 
    @classmethod
    def international_caps_goals(cls, value):
        if value == "" or value == '' or pd.isna(value):
            return 0
        return value

    @field_validator("city_of_birth", "country_of_citizenship", "date_of_birth",\
                     "contract_expiration_date", "agent_name", "current_national_team_id", \
                    "current_club_domestic_competition_id", "current_club_name", mode="before") 
    @classmethod
    def citizenship(cls, value):
        if value == "" or value == '' or pd.isna(value):
            return None
        return value

    @field_validator("current_club_domestic_competition_id")
    @classmethod
    def map_big_five_league(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return BIG_FIVE_LEAGUES.get(value, value)
    

# ---------------------------------------------------------------------------
# modelo de SALIDA (lo que devuelve el programa)
# ---------------------------------------------------------------------------
class Futbolista_salida(BaseModel):
    """Fila de del csv futbolistas limpio"""

    last_season                         : int = Field(ge=1950, le=2026)

    player_code                         : str = Field(min_length=1)

    country_of_birth                    : str = Field(min_length=1)

    sub_position                        : str = Field(min_length=1)

    position                            : str = Field(min_length=1)

    international_goals                 : int | None

    current_club_domestic_competition_id: str | None = Field(min_length=1)

    current_club_name                   : str | None = Field(min_length=1)

    market_value_in_eur                 : int = Field(ge=0, le=300_000_000)

    highest_market_value_in_eur         : int = Field(ge=0, le=300_000_000)  

    @model_validator(mode="after")
    def verificar_market_value(self):

        if self.highest_market_value_in_eur < self.market_value_in_eur:
            raise ValueError("La valoración máxima no puede ser menor que la actual")
        return self