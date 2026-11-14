"""Modelo de la tabla ventas (datos históricos para análisis)."""

# datetime tipa la columna de fecha
from datetime import datetime
# Decimal guarda dinero sin errores de redondeo
from decimal import Decimal

# BigInteger admite ids grandes; Numeric decimales; String texto
from sqlalchemy import BigInteger, Numeric, String
# Mapped y mapped_column declaran columnas con tipos de Python
from sqlalchemy.orm import Mapped, mapped_column

# Clase base de los modelos
from app.models.base import Base


class Venta(Base):
    """Una línea de venta; no está enlazada a otras tablas."""

    # Nombre de la tabla en la base de datos
    __tablename__ = "ventas"

    # Identificador grande, pensado para muchas filas
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    # Fecha y hora de la venta
    fecha: Mapped[datetime]
    # Número del cliente (no es llave foránea)
    cliente_id: Mapped[int]
    # Nombre del producto vendido (máximo 150 caracteres)
    producto: Mapped[str] = mapped_column(String(150))
    # Unidades vendidas
    cantidad: Mapped[int]
    # Precio de cada unidad: hasta 10 dígitos, 2 decimales
    precio_unitario: Mapped[Decimal] = mapped_column(Numeric(10, 2))
