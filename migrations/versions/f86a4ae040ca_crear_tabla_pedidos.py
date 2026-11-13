"""crear tabla pedidos

Revision ID: f86a4ae040ca
Revises: a855f259d138
Create Date: 2026-11-12 19:37:24.076982

"""
# Tipos para anotar los identificadores de revisión
from typing import Sequence, Union

# op ejecuta las operaciones sobre la base de datos
from alembic import op
# Tipos de columna de SQLAlchemy
import sqlalchemy as sa


# Identificadores de revisión que usa Alembic.
# Identificador de esta migración
revision: str = 'f86a4ae040ca'
# Migración anterior (productos)
down_revision: Union[str, Sequence[str], None] = 'a855f259d138'
# Etiquetas de ramas (no se usan)
branch_labels: Union[str, Sequence[str], None] = None
# Dependencias con otras migraciones (no se usan)
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Aplica el cambio: crea la tabla pedidos."""
    op.create_table(
        'pedidos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('usuario_id', sa.Integer(), nullable=False),
        sa.Column('total', sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column(
            'creado_en',
            sa.DateTime(),
            server_default=sa.text('now()'),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['usuario_id'], ['usuarios.id']),
        sa.PrimaryKeyConstraint('id'),
    )


def downgrade() -> None:
    """Revierte el cambio: elimina la tabla pedidos."""
    op.drop_table('pedidos')
