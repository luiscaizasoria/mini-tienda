"""Demo: inicia sesión en Supabase y muestra el contenido del token JWT.

Uso: python -m demos.supabase_auth.login_supabase
"""

# base64 decodifica las partes del token
import base64
# json convierte el texto decodificado en diccionario
import json

# dotenv_values lee el .env (para TEST_EMAIL y TEST_PASSWORD)
from dotenv import dotenv_values
# create_client crea el cliente de Supabase
from supabase import create_client

# Configuración con la dirección y clave de Supabase
from app.core.config import settings

# Lee las credenciales de prueba del archivo .env
env = dotenv_values(".env")
# Crea el cliente de Supabase
client = create_client(
    settings.supabase_url,
    settings.supabase_publishable_key,
)

# Inicia sesión con el usuario de prueba
resp = client.auth.sign_in_with_password(
    {"email": env["TEST_EMAIL"], "password": env["TEST_PASSWORD"]}
)
# Token de acceso (JWT) que devuelve Supabase
token = resp.session.access_token


def decodificar(parte: str) -> dict:
    """Decodifica una parte del token (base64url) a diccionario."""
    # Añade el relleno "=" que base64 necesita para tener longitud válida
    parte += "=" * (-len(parte) % 4)
    # Decodifica los bytes y los interpreta como JSON
    return json.loads(base64.urlsafe_b64decode(parte))


# Un JWT tiene tres partes separadas por puntos
encabezado, carga, _firma = token.split(".")
# Datos (claims) que lleva el token
claims = decodificar(carga)

print("Sesión iniciada:", resp.user.email)
print("Token empieza con:", token[:20], "...")
print("Encabezado:", decodificar(encabezado))
# Muestra los claims más importantes
for clave in ("sub", "role", "aud", "iss", "exp"):
    print(f"{clave}:", claims.get(clave))
