from ventas_app.contracts import Venta, Venta_expandida
import pandas as pd

def es_valida(venta:Venta) -> bool:

    # Si la fila tiene un valor None la consideramos como inválida 

    if pd.isna(venta.fecha) or pd.isna(venta.region) or pd.isna(venta.producto) or \
        pd.isna(venta.unidades) or pd.isna(venta.precio_unitario) or pd.isna(venta.cliente_id):
        return False
    
    return True


def preprocess(venta:Venta) -> Venta_expandida:
    """
    Recibe una venta y añade una columna con el importe total
    """

    if es_valida(venta):
        return Venta_expandida(
            fecha           = venta.fecha,
            region          = venta.region,
            producto        = venta.producto,
            unidades        = venta.unidades,
            precio_unitario =  venta.precio_unitario,
            importe         = venta.unidades * venta.precio_unitario,
            cliente_id      = venta.cliente_id
        )