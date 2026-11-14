"""agregar auth_id a usuarios

Revision ID: a90ee1ff0156
Revises: bf8f044b69bf
Create Date: 2026-11-13 16:30:47.464498

"""
# Tipos para anotar los identificadores de revisión
from typing import Sequence, Union

# op ejecuta las operaciones sobre la base de datos
from alembic import op
# Tipos de columna de SQLAlchemy
import sqlalchemy as sa


# Identificadores de revisión que usa Alembic.
# Identificador de esta migración
revision: str = 'a90ee1ff0156'
# Migración anterior (ventas)
down_revision: Union[str, Sequence[str], None] = 'bf8f044b69bf'
# Etiquetas de ramas (no se usan)
branch_labels: Union[str, Sequence[str], None] = None
# Dependencias con otras migraciones (no se usan)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplica el cambio: añade auth_id (único) a usuarios."""
    # Añade la columna que enlaza con Supabase Auth
    op.add_column('usuarios', sa.Column('auth_id', sa.Uuid(), nullable=True))
    # Evita que dos usuarios compartan el mismo auth_id
    op.create_unique_constraint('uq_usuarios_auth_id', 'usuarios', ['auth_id'])


def downgrade() -> None:
    """Revierte el cambio: quita auth_id de usuarios."""
    # Elimina primero la restricción de unicidad
    op.drop_constraint('uq_usuarios_auth_id', 'usuarios', type_='unique')
    # Luego elimina la columna
    op.drop_column('usuarios', 'auth_id')
