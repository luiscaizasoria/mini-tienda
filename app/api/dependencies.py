"""Dependencias de FastAPI: sesión de base de datos y usuario autenticado."""

# Para convertir el texto del token (sub) en un UUID
import uuid
# Tipo del generador que entrega la sesión de base de datos
from collections.abc import Iterator

# Librería para manejar tokens JWT y sus errores
import jwt
# Depends inyecta dependencias; HTTPException y status devuelven errores
from fastapi import Depends, HTTPException, status
# Lee el encabezado "Authorization: Bearer <token>"
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
# select construye consultas SQL
from sqlalchemy import select
# Session es la conexión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Función que valida la firma y los datos del token
from app.core.security import verificar_token
# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Modelo de la tabla usuarios
from app.models import Usuario

# Esquema Bearer; auto_error=False permite devolver nuestro propio 401
bearer = HTTPBearer(auto_error=False)


def get_db() -> Iterator[Session]:
    """Entrega una sesión de base de datos y la cierra al terminar."""
    # Abre una sesión y la cierra sola al salir del bloque
    with SessionLocal() as session:
        # Entrega la sesión a la ruta que la pidió
        yield session


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer),
) -> dict:
    """Valida el token del encabezado y devuelve sus datos (claims)."""
    # Si el cliente no envió el encabezado Authorization
    if credentials is None:
        # Responde 401 indicando que falta el token
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Falta el token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Intenta verificar el token
    try:
        # Devuelve los datos del token si es válido
        return verificar_token(credentials.credentials)
    # Si el token es falso, está manipulado o venció
    except jwt.PyJWTError:
        # Responde 401 indicando que el token no sirve
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            "Token inválido o vencido",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_usuario_actual(
    claims: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> Usuario:
    """Enlaza al usuario de Supabase (sub) con su fila local en usuarios."""
    # Identificador del usuario en Supabase, convertido a UUID
    auth_id = uuid.UUID(claims["sub"])
    # Busca en la tabla usuarios la fila con ese auth_id
    consulta = select(Usuario).where(Usuario.auth_id == auth_id)
    # Toma la primera coincidencia, o None si no existe
    usuario = db.scalars(consulta).first()
    # Si es la primera vez que el usuario entra a la API
    if usuario is None:
        # Usa su correo, o uno ficticio si el token no lo trae
        email = claims.get("email") or f"{auth_id}@sin-correo.local"
        # Crea el usuario; el nombre es la parte del correo antes de @
        usuario = Usuario(
            auth_id=auth_id,
            nombre=email.split("@")[0],
            email=email,
        )
        # Lo marca para guardarlo
        db.add(usuario)
        # Confirma el guardado en la base de datos
        db.commit()
        # Recarga el objeto para obtener el id generado
        db.refresh(usuario)
    # Devuelve la fila local del usuario
    return usuario
