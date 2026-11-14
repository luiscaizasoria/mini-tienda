"""Clase base declarativa compartida por todos los modelos."""

# DeclarativeBase es la base de los modelos ORM de SQLAlchemy 2
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Base común; guarda el registro (metadata) de todas las tablas."""
