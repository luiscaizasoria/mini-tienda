"""Demo: compara lo que ve la Data API (con RLS) y la conexión directa.

RLS (Row Level Security) limita las filas visibles según el usuario.

Uso: python -m demos.supabase_auth.probar_rls
"""

# dotenv_values lee el .env (para TEST_EMAIL y TEST_PASSWORD)
from dotenv import dotenv_values
# func y select permiten contar filas con SQL
from sqlalchemy import func, select
# create_client crea el cliente de Supabase
from supabase import create_client

# Configuración con la dirección y clave de Supabase
from app.core.config import settings
# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Modelos de las tablas pedidos y usuarios
from app.models import Pedido, Usuario

# Lee las credenciales de prueba del archivo .env
env = dotenv_values(".env")
# Crea el cliente de Supabase
client = create_client(
    settings.supabase_url,
    settings.supabase_publishable_key,
)


def contar(titulo):
    """Muestra cuántas filas ve la Data API en cada tabla."""
    # Revisa las dos tablas protegidas
    for tabla in ("usuarios", "pedidos"):
        # Pide el conteo exacto de filas visibles
        r = client.table(tabla).select("*", count="exact").execute()
        print(f"{titulo}: {tabla:9} -> {r.count} fila(s)")


# Sin sesión: RLS debería ocultar las filas
contar("SIN LOGIN (Data API)")
# Inicia sesión con el usuario de prueba
client.auth.sign_in_with_password(
    {"email": env["TEST_EMAIL"], "password": env["TEST_PASSWORD"]}
)
# Con sesión: solo se ven las filas del propio usuario
contar("CON LOGIN (Data API)")

# Conexión directa con DATABASE_URL: no aplica RLS, ve todo
with SessionLocal() as s:
    print(
        "REAL (DATABASE_URL)   : usuarios ->",
        s.scalar(select(func.count()).select_from(Usuario)),
    )
    print(
        "REAL (DATABASE_URL)   : pedidos  ->",
        s.scalar(select(func.count()).select_from(Pedido)),
    )
