"""Demo de consultas básicas con el ORM.

Uso: python -m demos.base_de_datos.consultas_orm
"""

# select construye consultas SQL
from sqlalchemy import select

# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Modelo de la tabla productos
from app.models import Producto

# Abre una sesión y la cierra sola al terminar
with SessionLocal() as session:
    # 1. Todos los productos
    todos = session.scalars(select(Producto)).all()
    # Muestra los datos de cada producto
    for p in todos:
        print(p.id, p.nombre, p.precio, p.stock)

    # 2. Con filtro y orden
    consulta = (
        select(Producto)
        .where(Producto.precio > 1)
        .order_by(Producto.nombre)
    )
    # Ejecuta la consulta
    caros = session.scalars(consulta).all()
    print("Precio mayor a 1:", [p.nombre for p in caros])

    # 3. Uno solo por id
    uno = session.get(Producto, 1)
    print("Por id:", uno.nombre)
