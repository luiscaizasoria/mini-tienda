"""Modelo de la tabla categorias."""

# String define columnas de texto con longitud máxima
from sqlalchemy import String
# Mapped y mapped_column declaran columnas con tipos de Python
from sqlalchemy.orm import Mapped, mapped_column

# Clase base de los modelos
from app.models.base import Base


class Categoria(Base):
    """Categoría a la que puede pertenecer un producto."""

    # Nombre de la tabla en la base de datos
    __tablename__ = "categorias"

    # Identificador único autoincremental
    id: Mapped[int] = mapped_column(primary_key=True)
    # Nombre de la categoría (máximo 100 caracteres)
    nombre: Mapped[str] = mapped_column(String(100))
