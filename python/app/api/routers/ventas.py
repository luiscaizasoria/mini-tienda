"""Rutas de las ventas: solo lectura, paginadas para tablas grandes."""

# APIRouter agrupa rutas; Depends inyecta; Query valida parámetros de URL
from fastapi import APIRouter, Depends, Query
# func permite usar funciones de SQL (count, sum); select arma consultas
from sqlalchemy import func, select
# Session es la conexión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Dependencia que entrega la sesión de base de datos
from app.api.dependencies import get_db
# Modelo de la tabla ventas
from app.models import Venta
# Esquemas de salida de las ventas
from app.schemas.venta import PaginaVentas, ResumenVentas

# Todas las rutas empiezan con /ventas
router = APIRouter(prefix="/ventas", tags=["ventas"])


@router.get("", response_model=PaginaVentas)
def listar(
    # Cuántas ventas devolver: entre 1 y 100, por defecto 20
    limite: int = Query(20, ge=1, le=100),
    # Cuántas ventas saltar desde el inicio, por defecto 0
    desplazamiento: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    """Devuelve una página de ventas y el total de ventas existentes."""
    # Cuenta todas las ventas de la tabla
    total = db.scalar(select(func.count()).select_from(Venta))
    # Consulta una página: ordena por id, salta y limita
    consulta = (
        select(Venta)
        .order_by(Venta.id)
        .offset(desplazamiento)
        .limit(limite)
    )
    # Ejecuta la consulta
    items = db.scalars(consulta).all()
    # Devuelve el total y las ventas de esta página
    return {"total": total, "items": items}


@router.get("/resumen", response_model=ResumenVentas)
def resumir(db: Session = Depends(get_db)):
    """Calcula en la base de datos el número de ventas y los ingresos."""
    # La base suma cantidad * precio de todas las ventas (0 si no hay)
    consulta = select(
        func.count(Venta.id),
        func.coalesce(func.sum(Venta.cantidad * Venta.precio_unitario), 0),
    )
    # Ejecuta la consulta y toma su única fila
    cantidad, ingresos = db.execute(consulta).one()
    # Devuelve los totales
    return {"cantidad_ventas": cantidad, "ingresos": ingresos}
