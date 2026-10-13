from contracts import Futbolista, Futbolista_salida
import pandas as pd
from pandas import DataFrame

def eliminar_columnas(df: DataFrame, lista_columnas: list[str]) -> DataFrame:
    df.drop(lista_columnas, axis=1)


def preprocess(futbolista:Futbolista) -> Futbolista_salida:

    return Futbolista_salida(
        last_season = futbolista.last_season,
        player_code = futbolista.player_code,
        country_of_birth = futbolista.country_of_birth,
        sub_position = futbolista.sub_position,
        position = futbolista.position,   
        international_goals = futbolista.international_goals,
        current_club_domestic_competition_id = futbolista.current_club_domestic_competition_id,
        current_club_name = futbolista.current_club_name,  
        market_value_in_eur = futbolista.market_value_in_eur,
        highest_market_value_in_eur = futbolista.highest_market_value_in_eur
    )