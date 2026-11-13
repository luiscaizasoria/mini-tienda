"""Configuración de Alembic: cómo se conecta y qué tablas conoce."""

# Configura el sistema de mensajes (logs) a partir de alembic.ini
from logging.config import fileConfig

# Contexto de Alembic, usado para ejecutar las migraciones
from alembic import context
# engine_from_config crea el motor; pool controla las conexiones
from sqlalchemy import engine_from_config, pool

# Configuración con la dirección de la base de datos
from app.core.config import settings
# Base con el registro de todas las tablas del proyecto
from app.models import Base

# Objeto de configuración de Alembic (lee alembic.ini)
config = context.config
# Usa la dirección de base de datos del archivo .env
config.set_main_option("sqlalchemy.url", settings.database_url)
# Activa los mensajes (logs) si hay archivo de configuración
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Tablas que Alembic compara para generar migraciones automáticas
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Genera el SQL de las migraciones sin conectarse a la base."""
    # Dirección de la base de datos
    url = config.get_main_option("sqlalchemy.url")
    # Configura Alembic solo con la dirección (sin conexión real)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    # Abre una transacción
    with context.begin_transaction():
        # Ejecuta las migraciones pendientes
        context.run_migrations()


def run_migrations_online() -> None:
    """Aplica las migraciones conectándose a la base de datos."""
    # Crea el motor; NullPool no deja conexiones abiertas
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    # Abre una conexión
    with connectable.connect() as connection:
        # Configura Alembic con esa conexión
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        # Abre una transacción
        with context.begin_transaction():
            # Ejecuta las migraciones pendientes
            context.run_migrations()


# Elige el modo según cómo se ejecutó Alembic
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
