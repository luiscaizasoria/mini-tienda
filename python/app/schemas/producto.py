"""Esquemas de entrada y salida para los productos."""

# Decimal representa dinero sin errores de redondeo
from decimal import Decimal

# BaseModel es la base; ConfigDict configura; Field añade validaciones
from pydantic import BaseModel, ConfigDict, Field


class ProductoCreate(BaseModel):
    """Datos que el cliente envía para crear un producto."""

    # Nombre de 2 a 150 caracteres
    nombre: str = Field(min_length=2, max_length=150)
    # Precio mayor que 0, con máximo 10 dígitos y 2 decimales
    precio: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    # Stock mayor o igual a 0; por defecto 0
    stock: int = Field(default=0, ge=0)


class ProductoRead(BaseModel):
    """Datos de un producto que la API devuelve al cliente."""

    # Permite construir el esquema directamente desde un modelo ORM
    model_config = ConfigDict(from_attributes=True)

    # Identificador del producto
    id: int
    # Nombre del producto
    nombre: str
    # Precio del producto
    precio: Decimal
    # Unidades disponibles
    stock: int
