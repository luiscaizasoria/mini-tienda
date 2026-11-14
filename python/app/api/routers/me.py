"""Ruta que muestra los datos del usuario autenticado."""

# APIRouter agrupa rutas; Depends inyecta dependencias
from fastapi import APIRouter, Depends

# Dependencia que valida el token y devuelve sus datos
from app.api.dependencies import get_current_user

# Grupo de rutas; "auth" es la etiqueta en la documentación
router = APIRouter(tags=["auth"])


@router.get("/me")
def me(user: dict = Depends(get_current_user)):
    """Devuelve el id, correo y rol que vienen dentro del token."""
    # Arma la respuesta solo con los campos que interesan
    return {
        "id": user["sub"],
        "email": user.get("email"),
        "role": user.get("role"),
    }
