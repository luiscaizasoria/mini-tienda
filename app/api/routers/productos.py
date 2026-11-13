"""Rutas del catálogo de productos."""

# APIRouter agrupa rutas; HTTPException y status devuelven errores
from fastapi import APIRouter, Depends, HTTPException, status
# select construye consultas SQL
from sqlalchemy import select
# Session es la conexión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Dependencia que entrega la sesión de base de datos
from app.api.dependencies import get_db
# Modelo de la tabla productos
from app.models import Producto
# Esquemas de entrada y salida de un producto
from app.schemas.producto import ProductoCreate, ProductoRead

# Todas las rutas empiezan con /productos
router = APIRouter(prefix="/productos", tags=["productos"])


@router.get("", response_model=list[ProductoRead])
def listar(db: Session = Depends(get_db)):
    """Lista todos los productos ordenados por id."""
    # Consulta todos los productos ordenados por id
    consulta = select(Producto).order_by(Producto.id)
    # Ejecuta la consulta y devuelve todos los resultados
    return db.scalars(consulta).all()


@router.get("/{producto_id}", response_model=ProductoRead)
def obtener(producto_id: int, db: Session = Depends(get_db)):
    """Devuelve un producto por su id, o 404 si no existe."""
    # Busca el producto por su llave primaria
    producto = db.get(Producto, producto_id)
    # Si no existe
    if producto is None:
        # Responde 404 Not Found
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            "Producto no encontrado",
        )
    # Devuelve el producto encontrado
    return producto


@router.post(
    "",
    response_model=ProductoRead,
    status_code=status.HTTP_201_CREATED,
)
def crear(datos: ProductoCreate, db: Session = Depends(get_db)):
    """Crea un producto nuevo con los datos recibidos."""
    # Convierte los datos validados en un objeto de la tabla
    producto = Producto(**datos.model_dump())
    # Lo marca para guardarlo
    db.add(producto)
    # Confirma el guardado en la base de datos
    db.commit()
    # Recarga el objeto para obtener el id generado
    db.refresh(producto)
    # Devuelve el producto creado
    return producto
