"""Demo del problema N+1 y cómo evitarlo con carga anticipada.

Uso: python -m demos.base_de_datos.n_mas_uno
"""

# event escucha lo que hace el motor; select construye consultas
from sqlalchemy import event, select
# Estrategias para cargar relaciones de forma anticipada
from sqlalchemy.orm import joinedload, selectinload

# Fábrica de sesiones y motor de base de datos
from app.db.database import SessionLocal, engine
# Modelo de la tabla usuarios
from app.models import Usuario

# Contador de consultas SQL enviadas a la base
contador = {"n": 0}


@event.listens_for(engine, "before_cursor_execute")
def contar(conn, cursor, statement, parameters, context, executemany):
    """Suma 1 al contador cada vez que se envía una consulta."""
    contador["n"] += 1


def medir(titulo, consulta):
    """Ejecuta una consulta e informa cuántas consultas SQL hizo."""
    # Reinicia el contador
    contador["n"] = 0
    # Abre una sesión y la cierra sola al terminar
    with SessionLocal() as session:
        # Ejecuta la consulta; unique() quita duplicados del join
        usuarios = session.scalars(consulta).unique().all()
        # Cuenta los pedidos de todos los usuarios (carga las relaciones)
        total = sum(len(u.pedidos) for u in usuarios)
    print(
        f"{titulo}: {contador['n']} consultas "
        f"({len(usuarios)} usuarios, {total} pedidos)"
    )


# Carga perezosa: una consulta por cada usuario (el problema N+1)
medir("Carga perezosa (N+1)", select(Usuario))
# Dos consultas en total: usuarios y luego todos sus pedidos
medir(
    "selectinload",
    select(Usuario).options(selectinload(Usuario.pedidos)),
)
# Una sola consulta con JOIN
medir("joinedload", select(Usuario).options(joinedload(Usuario.pedidos)))
