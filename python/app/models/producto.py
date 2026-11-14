"""Modelo de la tabla productos."""

# Decimal guarda dinero sin errores de redondeo
from decimal import Decimal

# Numeric define decimales; String define texto con longitud máxima
from sqlalchemy import Numeric, String
# Mapped y mapped_column declaran columnas con tipos de Python
from sqlalchemy.orm import Mapped, mapped_column

# Clase base de los modelos
from app.models.base import Base


class Producto(Base):
    """Producto que se vende en la tienda."""

    # Nombre de la tabla en la base de datos
    __tablename__ = "productos"

    # Identificador único autoincremental
    id: Mapped[int] = mapped_column(primary_key=True)
    # Nombre del producto (máximo 150 caracteres)
    nombre: Mapped[str] = mapped_column(String(150))
    # Precio: hasta 10 dígitos, 2 decimales
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    # Unidades disponibles; por defecto 0
    stock: Mapped[int] = mapped_column(default=0)
