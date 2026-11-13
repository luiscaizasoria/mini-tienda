"""crear tabla ventas

Revision ID: bf8f044b69bf
Revises: f86a4ae040ca
Create Date: 2026-11-12 20:36:41.627648

"""
# Tipos para anotar los identificadores de revisión
from typing import Sequence, Union

# op ejecuta las operaciones sobre la base de datos
from alembic import op
# Tipos de columna de SQLAlchemy
import sqlalchemy as sa


# Identificadores de revisión que usa Alembic.
# Identificador de esta migración
revision: str = 'bf8f044b69bf'
# Migración anterior (pedidos)
down_revision: Union[str, Sequence[str], None] = 'f86a4ae040ca'
# Etiquetas de ramas (no se usan)
branch_labels: Union[str, Sequence[str], None] = None
# Dependencias con otras migraciones (no se usan)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplica el cambio: crea la tabla ventas."""
    op.create_table(
        'ventas',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('fecha', sa.DateTime(), nullable=False),
        sa.Column('cliente_id', sa.Integer(), nullable=False),
        sa.Column('producto', sa.String(length=150), nullable=False),
        sa.Column('cantidad', sa.Integer(), nullable=False),
        sa.Column(
            'precio_unitario',
            sa.Numeric(precision=10, scale=2),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Revierte el cambio: elimina la tabla ventas."""
    op.drop_table('ventas')
