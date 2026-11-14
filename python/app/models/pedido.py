"""Modelo de la tabla pedidos."""

# datetime tipa la columna de fecha
from datetime import datetime
# Decimal guarda dinero sin errores de redondeo
from decimal import Decimal
# TYPE_CHECKING evita importaciones circulares en tiempo de ejecución
from typing import TYPE_CHECKING

# ForeignKey enlaza tablas; Numeric define decimales; func llama a SQL
from sqlalchemy import ForeignKey, Numeric, func
# Mapped, mapped_column y relationship declaran columnas y relaciones
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Clase base de los modelos
from app.models.base import Base

# Solo se importa para los editores y verificadores de tipos
if TYPE_CHECKING:
    from app.models.usuario import Usuario


class Pedido(Base):
    """Pedido realizado por un usuario."""

    # Nombre de la tabla en la base de datos
    __tablename__ = "pedidos"

    # Identificador único autoincremental
    id: Mapped[int] = mapped_column(primary_key=True)
    # Usuario dueño del pedido (llave foránea a usuarios.id)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
    # Total del pedido: hasta 10 dígitos, 2 decimales; por defecto 0
    total: Mapped[Decimal] = mapped_column(Numeric(10, 2), default=0)
    # Fecha de creación; la base de datos pone now() automáticamente
    creado_en: Mapped[datetime] = mapped_column(server_default=func.now())

    # Acceso directo al usuario dueño desde el pedido
    usuario: Mapped["Usuario"] = relationship(back_populates="pedidos")
