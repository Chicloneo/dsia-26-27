import sys
from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError


FUTBOL_DIR = Path(__file__).resolve().parents[1] / "futbol"
sys.path.insert(0, str(FUTBOL_DIR))

import cli
from contracts import Futbolista, Futbolista_salida
from preprocess import preprocess


def _fila_futbolista(**overrides):
    fila = {
        "player_id": 1,
        "last_season": 2024,
        "current_club_id": 10,
        "player_code": "jugador-uno",
        "country_of_birth": "España",
        "city_of_birth": "Madrid",
        "country_of_citizenship": "España",
        "date_of_birth": "2000-01-01",
        "sub_position": "Delantero centro",
        "position": "Attack",
        "foot": "right",
        "height_in_cm": 180,
        "contract_expiration_date": "2026-06-30",
        "agent_name": "Agencia",
        "international_caps": 5,
        "international_goals": 2,
        "current_national_team_id": 20,
        "current_club_domestic_competition_id": "ES1",
        "current_club_name": "Club Uno",
        "market_value_in_eur": 1_000_000,
        "highest_market_value_in_eur": 2_000_000,
    }
    fila.update(overrides)
    return fila


def test_futbolista_traduce_los_codigos_de_las_cinco_ligas():
    casos = {
        "ES1": "La Liga",
        "GB1": "Premier League",
        "L1": "Bundesliga",
        "IT1": "Serie A",
        "FR1": "Ligue 1",
    }

    for codigo, liga in casos.items():
        futbolista = Futbolista(
            **_fila_futbolista(current_club_domestic_competition_id=codigo)
        )
        assert futbolista.current_club_domestic_competition_id == liga


def test_futbolista_conserva_codigo_de_liga_no_mapeado():
    futbolista = Futbolista(
        **_fila_futbolista(current_club_domestic_competition_id="NL1")
    )

    assert futbolista.current_club_domestic_competition_id == "NL1"


def test_futbolista_reemplaza_datos_vacios_y_elige_pie(monkeypatch):
    monkeypatch.setattr("contracts.random.choices", lambda *args, **kwargs: ["left"])
    futbolista = Futbolista(
        **_fila_futbolista(
            city_of_birth="",
            country_of_citizenship="",
            date_of_birth="",
            foot="",
            height_in_cm="",
            contract_expiration_date="",
            agent_name="",
            international_caps="",
            international_goals="",
            current_national_team_id="",
            current_club_domestic_competition_id="",
            current_club_name="",
        )
    )

    assert futbolista.foot == "left"
    assert futbolista.height_in_cm == 176
    assert futbolista.international_caps == 0
    assert futbolista.international_goals == 0
    assert futbolista.city_of_birth is None
    assert futbolista.country_of_citizenship is None
    assert futbolista.date_of_birth is None
    assert futbolista.contract_expiration_date is None
    assert futbolista.agent_name is None
    assert futbolista.current_national_team_id is None
    assert futbolista.current_club_domestic_competition_id is None
    assert futbolista.current_club_name is None


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("player_id", -1),
        ("last_season", 1949),
        ("current_club_id", -1),
        ("player_code", ""),
        ("height_in_cm", 99),
        ("current_national_team_id", -1),
        ("market_value_in_eur", -1),
        ("highest_market_value_in_eur", 300_000_001),
    ],
)
def test_futbolista_rechaza_valores_fuera_de_rango(field, value):
    with pytest.raises(ValidationError):
        Futbolista(**_fila_futbolista(**{field: value}))


def test_preprocess_construye_futbolista_de_salida():
    futbolista = Futbolista(**_fila_futbolista())

    resultado = preprocess(futbolista)

    assert isinstance(resultado, Futbolista_salida)
    assert resultado.current_club_domestic_competition_id == "La Liga"
    assert resultado.international_goals == 2


def test_futbolista_salida_rechaza_valoracion_maxima_menor():
    with pytest.raises(ValidationError, match="La valoración máxima"):
        Futbolista_salida(
            last_season=2024,
            player_code="jugador-uno",
            country_of_birth="España",
            sub_position="Delantero centro",
            position="Attack",
            international_goals=2,
            current_club_domestic_competition_id="La Liga",
            current_club_name="Club Uno",
            market_value_in_eur=2_000_000,
            highest_market_value_in_eur=1_000_000,
        )


def test_read_footballers_procesa_fila_valida_y_separa_invalida(tmp_path):
    csv_path = tmp_path / "jugadores.csv"
    filas = [
        _fila_futbolista(),
        _fila_futbolista(player_id=-1, player_code="jugador-dos"),
    ]
    pd.DataFrame(filas).to_csv(csv_path, index=False)

    validos, invalidos = cli.read_footballers(csv_path)

    assert len(validos) == 1
    assert validos[0].player_code == "jugador-uno"
    assert len(invalidos) == 1
    assert invalidos[0]["player_code"] == "jugador-dos"


def test_read_footballers_rechaza_ruta_inexistente(tmp_path):
    with pytest.raises(FileNotFoundError, match="No existe el fichero"):
        cli.read_footballers(tmp_path / "inexistente.csv")


def test_read_footballers_con_csv_sin_filas_devuelve_listas_vacias(tmp_path):
    csv_path = tmp_path / "jugadores_vacio.csv"
    csv_path.write_text("player_id,player_code\n", encoding="utf-8")

    validos, invalidos = cli.read_footballers(csv_path)

    assert validos == []
    assert invalidos == []


@pytest.mark.integration
def test_main_escribe_jugadores_validos_y_filas_con_error(
    tmp_path, monkeypatch, capsys
):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "datos" / "outputs").mkdir(parents=True)
    csv_path = tmp_path / "jugadores.csv"
    pd.DataFrame(
        [
            _fila_futbolista(),
            _fila_futbolista(player_id=-1, player_code="jugador-invalido"),
        ]
    ).to_csv(csv_path, index=False)
    output_path = tmp_path / "salida.csv"

    resultado = cli.main(
        ["--input", str(csv_path), "--output", str(output_path)]
    )

    assert resultado == 0
    assert pd.read_csv(output_path)["player_code"].tolist() == ["jugador-uno"]
    assert len(pd.read_csv("datos/outputs/futbolistas_con_error.csv")) == 1
    assert "Hay 1 futbolistas válidos y 1 futbolistas con error" in capsys.readouterr().out


def test_main_devuelve_codigo_2_si_falla_la_lectura(monkeypatch, capsys):
    def read_con_error(_path):
        raise ValueError("CSV inválido")

    monkeypatch.setattr(cli, "read_footballers", read_con_error)

    resultado = cli.main(["--input", "jugadores.csv", "--output", "salida.csv"])

    assert resultado == 2
    assert "Error: CSV inválido" in capsys.readouterr().out
