"""Esquemas de entrada y salida para los pedidos."""

# datetime tipa la fecha de creación
from datetime import datetime
# Decimal representa dinero sin errores de redondeo
from decimal import Decimal

# BaseModel es la base; ConfigDict configura; Field añade validaciones
from pydantic import BaseModel, ConfigDict, Field


class PedidoCreate(BaseModel):
    """Datos que el cliente envía para crear un pedido."""

    # Total mayor que 0, con máximo 10 dígitos y 2 decimales
    total: Decimal = Field(gt=0, max_digits=10, decimal_places=2)


class PedidoRead(BaseModel):
    """Datos de un pedido que la API devuelve al cliente."""

    # Permite construir el esquema directamente desde un modelo ORM
    model_config = ConfigDict(from_attributes=True)

    # Identificador del pedido
    id: int
    # Total del pedido
    total: Decimal
    # Fecha y hora de creación
    creado_en: datetime
