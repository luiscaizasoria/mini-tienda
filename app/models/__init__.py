"""Modelos ORM: cada clase representa una tabla de la base de datos."""

# Clase base de la que heredan todos los modelos
from app.models.base import Base
# Tabla categorias
from app.models.categoria import Categoria
# Tabla pedidos
from app.models.pedido import Pedido
# Tabla productos
from app.models.producto import Producto
# Tabla usuarios
from app.models.usuario import Usuario
# Tabla ventas
from app.models.venta import Venta

# Nombres que se exportan al hacer "from app.models import ..."
__all__ = ["Base", "Categoria", "Pedido", "Producto", "Usuario", "Venta"]
