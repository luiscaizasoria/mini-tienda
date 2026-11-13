"""Demo: verifica un token real y comprueba que uno manipulado se rechaza.

Uso: python -m demos.supabase_auth.verificar_jwt
"""

# Librería para validar tokens JWT
import jwt
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

# Dirección donde Supabase publica sus claves públicas
jwks_url = f"{settings.supabase_url}/auth/v1/.well-known/jwks.json"
# Cliente que descarga esas claves
jwks_client = jwt.PyJWKClient(jwks_url)


def verificar(t):
    """Valida la firma y la audiencia de un token."""
    # Obtiene la clave pública que firmó el token
    clave = jwks_client.get_signing_key_from_jwt(t)
    # Decodifica y comprueba el token
    return jwt.decode(
        t,
        clave.key,
        algorithms=["ES256"],
        audience="authenticated",
    )


print("1. Token real:")
# Verifica el token sin tocarlo
claims = verificar(token)
print("   válido, usuario:", claims["sub"])

print("2. Token manipulado:")
# Cambia los últimos 4 caracteres de la firma
manipulado = token[:-4] + ("AAAA" if not token.endswith("AAAA") else "BBBB")
try:
    # Si la verificación pasa, hay un problema de seguridad
    verificar(manipulado)
    print("   ¡aceptado! (no debería)")
# Lo esperado: la firma no coincide y se rechaza
except jwt.PyJWTError as e:
    print("   rechazado:", type(e).__name__)
