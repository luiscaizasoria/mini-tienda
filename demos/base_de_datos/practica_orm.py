"""Demo de la diferencia entre flush y commit.

Uso: python -m demos.base_de_datos.practica_orm
"""

# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Modelo de la tabla productos
from app.models import Producto

# Abre una sesión y la cierra sola al terminar
with SessionLocal() as session:
    # Crea dos productos en memoria
    p1 = Producto(nombre="Agua 500 ml", precio=0.75, stock=100)
    p2 = Producto(nombre="Galletas", precio=1.20, stock=50)

    # Los marca para guardarlos
    session.add_all([p1, p2])
    # Todavía no hay id: nada se envió a la base
    print("Antes del commit, id de p1:", p1.id)

    # Envía los cambios a la base sin confirmarlos
    session.flush()
    # Ahora la base ya generó el id
    print("Después del flush, id de p1:", p1.id)

    # Confirma los cambios de forma definitiva
    session.commit()
    print("Guardado")
