"""Esquemas de salida para las ventas (solo lectura)."""

# datetime tipa la fecha de la venta
from datetime import datetime
# Decimal representa dinero sin errores de redondeo
from decimal import Decimal

# BaseModel es la base; ConfigDict configura
from pydantic import BaseModel, ConfigDict


class VentaRead(BaseModel):
    """Una venta tal como la API la devuelve al cliente."""

    # Permite construir el esquema directamente desde un modelo ORM
    model_config = ConfigDict(from_attributes=True)

    # Identificador de la venta
    id: int
    # Fecha y hora de la venta
    fecha: datetime
    # Número del cliente
    cliente_id: int
    # Nombre del producto vendido
    producto: str
    # Unidades vendidas
    cantidad: int
    # Precio de cada unidad
    precio_unitario: Decimal


class PaginaVentas(BaseModel):
    """Una página de ventas junto con el total de ventas existentes."""

    # Cantidad total de ventas en la tabla (no solo las de esta página)
    total: int
    # Ventas de esta página
    items: list[VentaRead]


class ResumenVentas(BaseModel):
    """Totales calculados por la base de datos sobre todas las ventas."""

    # Número de ventas registradas
    cantidad_ventas: int
    # Suma de cantidad * precio unitario de todas las ventas
    ingresos: Decimal
