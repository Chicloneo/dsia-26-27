from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError

from ventas_app.cli import read_sales
from ventas_app.contracts import Venta, Venta_expandida
from ventas_app.preprocess import preprocess


@pytest.fixture
def ventas_mini():
    return pd.DataFrame({
        "fecha": ["2026-01-01", "2026-01-02", "2026-01-03"],
        "region": ["Norte", "Sur", "Norte"],
        "producto": ["A", "B", "A"],
        "unidades": [2, None, 5],
        "precio_unitario": [10.0, 20.0, -1.0],
        "cliente_id": ["C1", "C2", "C1"],
    })


def _venta(precio_unitario=10.0, region="Norte"):
    return Venta(
        fecha="2026-01-01",
        region=region,
        producto="A",
        unidades=2,
        precio_unitario=precio_unitario,
        cliente_id="C1",
    )


def test_ventas_mini_tiene_una_valida_y_dos_invalidas(ventas_mini, tmp_path):
    csv_path = tmp_path / "ventas_mini.csv"
    ventas_mini.to_csv(csv_path, index=False)

    validas, invalidas = read_sales(str(csv_path))

    assert len(validas) == 1
    assert len(invalidas) == 2


def test_preprocess_devuelve_venta_expandida_para_venta_valida():
    resultado = preprocess(_venta())

    assert isinstance(resultado, Venta_expandida)


def test_preprocess_calcula_importe():
    resultado = preprocess(_venta())

    assert resultado.importe == 20.0


def test_preprocess_devuelve_none_si_falta_region():
    resultado = preprocess(_venta(region=None))

    assert resultado is None


def test_read_sales_lanza_error_si_path_no_existe(tmp_path):
    missing_path = tmp_path / "no_existe.csv"

    with pytest.raises(FileNotFoundError, match="No existe el fichero de ventas"):
        read_sales(str(missing_path))


@pytest.mark.parametrize(
    ("precio", "es_valido"),
    [(0, False), (-1, False), (1, True)],
)
def test_precio_unitario_solo_acepta_valores_positivos(precio, es_valido):
    if es_valido:
        venta = _venta(precio_unitario=precio)
        assert preprocess(venta) is not None
    else:
        with pytest.raises(ValidationError):
            _venta(precio_unitario=precio)


@pytest.mark.integration
def test_csv_curso_tiene_140_validas_y_10_invalidas():
    csv_path = Path(__file__).resolve().parents[1] / "Datos" / "ventas.csv"

    validas, invalidas = read_sales(str(csv_path))

    assert len(validas) == 140
    assert len(invalidas) == 10


def test_read_sales_sin_filas_devuelve_dos_listas_vacias(tmp_path):
    csv_path = tmp_path / "ventas_vacio.csv"
    csv_path.write_text(
        "fecha,region,producto,unidades,precio_unitario,cliente_id\n",
        encoding="utf-8",
    )

    validas, invalidas = read_sales(str(csv_path))

    assert validas == []
    assert invalidas == []
