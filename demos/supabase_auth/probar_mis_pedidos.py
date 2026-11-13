"""Demo: prueba las rutas /mis-pedidos con y sin token.

Uso: python -m demos.supabase_auth.probar_mis_pedidos
"""

# dotenv_values lee el .env (para TEST_EMAIL y TEST_PASSWORD)
from dotenv import dotenv_values
# TestClient llama a la API sin levantar un servidor
from fastapi.testclient import TestClient
# func y select permiten contar filas con SQL
from sqlalchemy import func, select
# create_client crea el cliente de Supabase
from supabase import create_client

# Configuración con la dirección y clave de Supabase
from app.core.config import settings
# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Aplicación FastAPI que se prueba
from app.main import app
# Modelo de la tabla pedidos
from app.models import Pedido

# Lee las credenciales de prueba del archivo .env
env = dotenv_values(".env")
# Crea el cliente de Supabase
supabase = create_client(
    settings.supabase_url,
    settings.supabase_publishable_key,
)
# Inicia sesión y guarda el token de acceso
token = supabase.auth.sign_in_with_password(
    {"email": env["TEST_EMAIL"], "password": env["TEST_PASSWORD"]}
).session.access_token
# Encabezado que se envía en las peticiones autenticadas
auth = {"Authorization": f"Bearer {token}"}

# Cliente que llama directamente a la API
api = TestClient(app)

# Sin token: debe dar 401
r = api.get("/mis-pedidos")
print("1. Sin token:", r.status_code)

# Crea un pedido a nombre del usuario de prueba
r = api.post("/mis-pedidos", json={"total": "12.50"}, headers=auth)
print("2. Crear pedido:", r.status_code, r.json())

# Lista solo los pedidos del usuario de prueba
r = api.get("/mis-pedidos", headers=auth)
print("3. Mis pedidos:", r.status_code, "->", len(r.json()), "pedido(s)")

# Cuenta todos los pedidos de la tabla, de todos los usuarios
with SessionLocal() as s:
    total = s.scalar(select(func.count()).select_from(Pedido))
print("4. Pedidos en toda la tabla:", total)
