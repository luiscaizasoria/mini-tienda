"""Esquemas de entrada y salida para las categorías."""

# BaseModel es la base; ConfigDict configura; Field añade validaciones
from pydantic import BaseModel, ConfigDict, Field


class CategoriaCreate(BaseModel):
    """Datos que el cliente envía para crear una categoría."""

    # Nombre de 2 a 100 caracteres
    nombre: str = Field(min_length=2, max_length=100)


class CategoriaRead(BaseModel):
    """Datos de una categoría que la API devuelve al cliente."""

    # Permite construir el esquema directamente desde un modelo ORM
    model_config = ConfigDict(from_attributes=True)

    # Identificador de la categoría
    id: int
    # Nombre de la categoría
    nombre: str
