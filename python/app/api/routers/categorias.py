"""Rutas de las categorías."""

# APIRouter agrupa rutas; Depends inyecta; status da los códigos HTTP
from fastapi import APIRouter, Depends, status
# select construye consultas SQL
from sqlalchemy import select
# Session es la conexión de trabajo con la base de datos
from sqlalchemy.orm import Session

# Dependencia que entrega la sesión de base de datos
from app.api.dependencies import get_db
# Modelo de la tabla categorias
from app.models import Categoria
# Esquemas de entrada y salida de una categoría
from app.schemas.categoria import CategoriaCreate, CategoriaRead

# Todas las rutas empiezan con /categorias
router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.get("", response_model=list[CategoriaRead])
def listar(db: Session = Depends(get_db)):
    """Lista todas las categorías ordenadas por id."""
    # Consulta todas las categorías ordenadas por id
    consulta = select(Categoria).order_by(Categoria.id)
    # Ejecuta la consulta y devuelve todos los resultados
    return db.scalars(consulta).all()


@router.post(
    "",
    response_model=CategoriaRead,
    status_code=status.HTTP_201_CREATED,
)
def crear(datos: CategoriaCreate, db: Session = Depends(get_db)):
    """Crea una categoría nueva con los datos recibidos."""
    # Convierte los datos validados en un objeto de la tabla
    categoria = Categoria(**datos.model_dump())
    # Lo marca para guardarlo
    db.add(categoria)
    # Confirma el guardado en la base de datos
    db.commit()
    # Recarga el objeto para obtener el id generado
    db.refresh(categoria)
    # Devuelve la categoría creada
    return categoria
