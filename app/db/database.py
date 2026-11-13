"""Motor de conexión y fábrica de sesiones de SQLAlchemy."""

# create_engine crea el motor de conexión a la base de datos
from sqlalchemy import create_engine
# sessionmaker fabrica sesiones de trabajo
from sqlalchemy.orm import sessionmaker

# Configuración con la dirección de la base de datos
from app.core.config import settings

# Motor de conexión; pool_pre_ping prueba la conexión antes de usarla
engine = create_engine(settings.database_url, pool_pre_ping=True)
# Fábrica de sesiones ligadas al motor
SessionLocal = sessionmaker(bind=engine)
