"""Fixtures compartidas por todas las pruebas."""

# pytest provee el decorador de fixtures
import pytest
# TestClient simula un cliente HTTP sin levantar un servidor
from fastapi.testclient import TestClient
# create_engine crea el motor de conexión a la base de datos
from sqlalchemy import create_engine
# sessionmaker fabrica sesiones de trabajo
from sqlalchemy.orm import sessionmaker
# StaticPool mantiene una sola conexión (necesario para SQLite en memoria)
from sqlalchemy.pool import StaticPool

# Dependencia original que las pruebas van a reemplazar
from app.api.dependencies import get_db
# Aplicación FastAPI que se prueba
from app.main import app
# Base con el registro de todas las tablas
from app.models import Base


@pytest.fixture
def motor():
    """Motor de una base de datos temporal en memoria, con las tablas."""
    # Base de datos SQLite en memoria: no toca Supabase
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Crea todas las tablas en la base temporal
    Base.metadata.create_all(engine)
    # Entrega el motor a quien lo pida
    yield engine
    # Cierra la base temporal al terminar la prueba
    engine.dispose()


@pytest.fixture
def sesion_bd(motor):
    """Sesión para preparar datos directamente en la base temporal."""
    # Abre una sesión y la cierra sola al terminar
    with sessionmaker(bind=motor)() as session:
        # Entrega la sesión a la prueba
        yield session


@pytest.fixture
def client(motor):
    """Cliente HTTP conectado a la base de datos temporal."""
    # Fábrica de sesiones para la base temporal
    testing_session = sessionmaker(bind=motor)

    def override_get_db():
        """Entrega sesiones de la base temporal en lugar de la real."""
        # Abre una sesión y la cierra sola al terminar
        with testing_session() as session:
            # Entrega la sesión a la ruta
            yield session

    # Le dice a FastAPI que use la base temporal
    app.dependency_overrides[get_db] = override_get_db
    # Abre el cliente de pruebas
    with TestClient(app) as test_client:
        # Entrega el cliente a la prueba
        yield test_client
    # Restaura las dependencias originales
    app.dependency_overrides.clear()
