from pathlib import Path

import pandas as pd
import pytest
from pydantic import ValidationError

from ventas_app.cli import main, read_sales
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


def test_venta_convierte_cadenas_vacias_en_none():
    venta = Venta(
        fecha="",
        region="",
        producto="A",
        unidades=1,
        precio_unitario=10.0,
        cliente_id="",
    )

    assert venta.fecha is None
    assert venta.region is None
    assert venta.cliente_id is None


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


def test_venta_expandida_rechaza_importe_menor_que_precio_unitario():
    with pytest.raises(
        ValidationError,
        match="El importe no puede ser menor que el precio unitario",
    ):
        Venta_expandida(
            fecha="2026-01-01",
            region="Norte",
            producto="A",
            unidades=1,
            precio_unitario=10.0,
            importe=9.0,
            cliente_id="C1",
        )


def test_main_escribe_ventas_validas_y_con_error(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "Datos" / "output").mkdir(parents=True)
    csv_path = tmp_path / "ventas.csv"
    pd.DataFrame(
        [
            {
                "fecha": "2026-01-01",
                "region": "Norte",
                "producto": "A",
                "unidades": 2,
                "precio_unitario": 10.0,
                "cliente_id": "C1",
            },
            {
                "fecha": "2026-01-02",
                "region": "Sur",
                "producto": "B",
                "unidades": 0,
                "precio_unitario": 20.0,
                "cliente_id": "C2",
            },
        ]
    ).to_csv(csv_path, index=False)
    output_path = tmp_path / "ventas_limpias.csv"

    resultado = main(["--input", str(csv_path), "--output", str(output_path)])

    assert resultado == 0
    assert pd.read_csv(output_path)["importe"].tolist() == [20.0]
    errores = pd.read_csv("Datos/output/ventas_con_error.csv")
    assert len(errores) == 1
    assert "Hay 1 ventas validas y 1 ventas con error" in capsys.readouterr().out


def test_main_devuelve_2_si_read_sales_lanza_value_error(monkeypatch, capsys):
    def read_sales_con_error(_path):
        raise ValueError("CSV inválido")

    monkeypatch.setattr("ventas_app.cli.read_sales", read_sales_con_error)

    resultado = main(["--input", "ventas.csv", "--output", "salida.csv"])

    assert resultado == 2
    assert "Error: CSV inválido" in capsys.readouterr().out
