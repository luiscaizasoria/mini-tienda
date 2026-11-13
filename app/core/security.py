"""Verificación de los tokens JWT que emite Supabase Auth."""

# Librería para decodificar y validar tokens JWT
import jwt

# Configuración con la dirección de Supabase
from app.core.config import settings

# Emisor esperado: debe coincidir con el campo "iss" del token
ISSUER = f"{settings.supabase_url}/auth/v1"
# Cliente que descarga las claves públicas de Supabase (JWKS)
_jwks_client = jwt.PyJWKClient(f"{ISSUER}/.well-known/jwks.json")


def verificar_token(token: str) -> dict:
    """Valida firma, caducidad, audiencia y emisor.

    Lanza PyJWTError si el token no es válido.
    """
    # Obtiene la clave pública que firmó este token
    clave = _jwks_client.get_signing_key_from_jwt(token)
    # Decodifica el token y comprueba que todo sea correcto
    return jwt.decode(
        token,
        clave.key,
        # Único algoritmo de firma permitido
        algorithms=["ES256"],
        # El token debe ser para usuarios autenticados
        audience="authenticated",
        # El token debe venir de nuestro proyecto de Supabase
        issuer=ISSUER,
    )
