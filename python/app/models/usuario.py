"""Modelo de la tabla usuarios."""

# uuid tipa el identificador que viene de Supabase
import uuid
# datetime tipa la columna de fecha
from datetime import datetime
# TYPE_CHECKING evita importaciones circulares en tiempo de ejecución
from typing import TYPE_CHECKING

# String define texto; Uuid define UUID; func llama a funciones SQL
from sqlalchemy import String, Uuid, func
# Mapped, mapped_column y relationship declaran columnas y relaciones
from sqlalchemy.orm import Mapped, mapped_column, relationship

# Clase base de los modelos
from app.models.base import Base

# Solo se importa para los editores y verificadores de tipos
if TYPE_CHECKING:
    from app.models.pedido import Pedido


class Usuario(Base):
    """Usuario de la tienda, enlazado con su cuenta de Supabase."""

    # Nombre de la tabla en la base de datos
    __tablename__ = "usuarios"

    # Identificador único autoincremental
    id: Mapped[int] = mapped_column(primary_key=True)
    # Identificador del usuario en Supabase Auth (único, puede ser nulo)
    auth_id: Mapped[uuid.UUID | None] = mapped_column(Uuid, unique=True)
    # Nombre del usuario (máximo 100 caracteres)
    nombre: Mapped[str] = mapped_column(String(100))
    # Correo electrónico (único, máximo 255 caracteres)
    email: Mapped[str] = mapped_column(String(255), unique=True)
    # Fecha de creación; la base de datos pone now() automáticamente
    creado_en: Mapped[datetime] = mapped_column(server_default=func.now())

    # Lista de pedidos del usuario
    pedidos: Mapped[list["Pedido"]] = relationship(back_populates="usuario")
