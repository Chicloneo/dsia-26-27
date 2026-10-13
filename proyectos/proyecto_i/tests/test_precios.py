import pytest

# Necesito importar alguna función de ventas_app que mire algo sobre los precios

class PrecioInvalido(Exception):
    """El precio no es positivo"""

@pytest.mark.parametrize("precio", [0, -1])
def test_precio_no_positivo_es_error(precio, ventas_mini_factory):
    with pytest.raises(PrecioInvalido):
        precio > 0