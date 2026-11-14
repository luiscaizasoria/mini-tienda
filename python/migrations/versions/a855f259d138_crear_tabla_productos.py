"""crear tabla productos

Revision ID: a855f259d138
Revises: bdc6e8430c58
Create Date: 2026-11-12 18:33:28.201264

"""
# Tipos para anotar los identificadores de revisión
from typing import Sequence, Union

# op ejecuta las operaciones sobre la base de datos
from alembic import op
# Tipos de columna de SQLAlchemy
import sqlalchemy as sa


# Identificadores de revisión que usa Alembic.
# Identificador de esta migración
revision: str = 'a855f259d138'
# Migración anterior (usuarios)
down_revision: Union[str, Sequence[str], None] = 'bdc6e8430c58'
# Etiquetas de ramas (no se usan)
branch_labels: Union[str, Sequence[str], None] = None
# Dependencias con otras migraciones (no se usan)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplica el cambio: crea la tabla productos."""
    op.create_table(
        'productos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=150), nullable=False),
        sa.Column('precio', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column('stock', sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Revierte el cambio: elimina la tabla productos."""
    op.drop_table('productos')
