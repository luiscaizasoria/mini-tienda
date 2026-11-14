"""Demo de actualizar, crear y borrar filas con el ORM.

Uso: python -m demos.base_de_datos.modificar_orm
"""

# select construye consultas SQL
from sqlalchemy import select

# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Modelo de la tabla productos
from app.models import Producto

# Abre una sesión y la cierra sola al terminar
with SessionLocal() as session:
    # Actualizar: cargas el objeto y cambias el atributo
    galletas = session.scalars(
        select(Producto).where(Producto.nombre == "Galletas")
    ).one()
    # Nuevo precio
    galletas.precio = 1.50
    # Resta 5 unidades al stock
    galletas.stock -= 5

    # Crea un producto temporal para borrarlo después
    temporal = Producto(nombre="Temporal", precio=9.99, stock=1)
    # Lo marca para guardarlo
    session.add(temporal)
    # Envía los cambios a la base sin confirmarlos, para obtener el id
    session.flush()
    print("Temporal creado con id:", temporal.id)

    # Lo marca para borrarlo
    session.delete(temporal)

    # Confirma todos los cambios
    session.commit()
    print("Listo")

# Nueva sesión para comprobar el resultado
with SessionLocal() as session:
    # Recorre todos los productos ordenados por id
    for p in session.scalars(select(Producto).order_by(Producto.id)):
        print(p.id, p.nombre, p.precio, p.stock)
