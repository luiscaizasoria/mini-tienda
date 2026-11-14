"""crear tabla usuarios

Revision ID: bdc6e8430c58
Revises:
Create Date: 2026-11-12 18:14:00.908480

"""
# Tipos para anotar los identificadores de revisión
from typing import Sequence, Union

# op ejecuta las operaciones sobre la base de datos
from alembic import op
# Tipos de columna de SQLAlchemy
import sqlalchemy as sa


# Identificadores de revisión que usa Alembic.
# Identificador de esta migración
revision: str = 'bdc6e8430c58'
# Migración anterior (None: es la primera)
down_revision: Union[str, Sequence[str], None] = None
# Etiquetas de ramas (no se usan)
branch_labels: Union[str, Sequence[str], None] = None
# Dependencias con otras migraciones (no se usan)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplica el cambio: crea la tabla usuarios."""
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column(
            'creado_en',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
    )


def downgrade() -> None:
    """Revierte el cambio: elimina la tabla usuarios."""
    op.drop_table('usuarios')
