"""Demo: prueba la ruta /me sin token, con token falso y con token real.

Uso: python -m demos.supabase_auth.probar_api_auth
"""

# dotenv_values lee el .env (para TEST_EMAIL y TEST_PASSWORD)
from dotenv import dotenv_values
# TestClient llama a la API sin levantar un servidor
from fastapi.testclient import TestClient
# create_client crea el cliente de Supabase
from supabase import create_client

# Configuración con la dirección y clave de Supabase
from app.core.config import settings
# Aplicación FastAPI que se prueba
from app.main import app

# Lee las credenciales de prueba del archivo .env
env = dotenv_values(".env")
# Crea el cliente de Supabase
client_supabase = create_client(
    settings.supabase_url,
    settings.supabase_publishable_key,
)
# Inicia sesión y guarda el token de acceso
token = client_supabase.auth.sign_in_with_password(
    {"email": env["TEST_EMAIL"], "password": env["TEST_PASSWORD"]}
).session.access_token

# Cliente que llama directamente a la API
api = TestClient(app)

# Sin encabezado Authorization: debe dar 401
r = api.get("/me")
print("1. Sin token:        ", r.status_code, r.json())

# Con un token inventado: debe dar 401
r = api.get("/me", headers={"Authorization": "Bearer abc.def.ghi"})
print("2. Token falso:      ", r.status_code, r.json())

# Con el token real: debe dar 200 y los datos del usuario
r = api.get("/me", headers={"Authorization": f"Bearer {token}"})
print("3. Token real:       ", r.status_code, r.json())
