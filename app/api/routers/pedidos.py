"""Rutas privadas: cada usuario ve y crea solo sus propios pedidos."""

# APIRouter agrupa rutas; Depends inyecta; status da los códigos HTTP
from fastapi import APIRouter, Depends, status
# select construye consultas SQL
from sqlalchemy import select
# Session es la conexión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Sesión de base de datos y usuario ya autenticado
from app.api.dependencies import get_db, get_usuario_actual
# Modelos de las tablas pedidos y usuarios
from app.models import Pedido, Usuario
# Esquemas de entrada y salida de un pedido
from app.schemas.pedido import PedidoCreate, PedidoRead

# Todas las rutas empiezan con /mis-pedidos
router = APIRouter(prefix="/mis-pedidos", tags=["pedidos"])


@router.get("", response_model=list[PedidoRead])
def listar(
    usuario: Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_db),
):
    """Lista los pedidos del usuario que hizo la petición."""
    # Consulta: pedidos de este usuario, ordenados por id
    consulta = (
        select(Pedido)
        .where(Pedido.usuario_id == usuario.id)
        .order_by(Pedido.id)
    )
    # Ejecuta la consulta y devuelve todos los resultados
    return db.scalars(consulta).all()


@router.post(
    "",
    response_model=PedidoRead,
    status_code=status.HTTP_201_CREATED,
)
def crear(
    datos: PedidoCreate,
    usuario: Usuario = Depends(get_usuario_actual),
    db: Session = Depends(get_db),
):
    """Crea un pedido a nombre del usuario autenticado."""
    # Construye el pedido con el total recibido
    pedido = Pedido(usuario_id=usuario.id, total=datos.total)
    # Lo marca para guardarlo
    db.add(pedido)
    # Confirma el guardado en la base de datos
    db.commit()
    # Recarga el objeto para obtener id y fecha generados
    db.refresh(pedido)
    # Devuelve el pedido creado
    return pedido
