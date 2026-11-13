"""Demo de paginación con un generador (paginación por llave).

Uso: python -m demos.base_de_datos.paginas_generador
"""

# event escucha lo que hace el motor; select construye consultas
from sqlalchemy import event, select

# Fábrica de sesiones y motor de base de datos
from app.db.database import SessionLocal, engine
# Modelo de la tabla ventas
from app.models import Venta

# Contador de consultas SQL enviadas a la base
consultas = {"n": 0}


@event.listens_for(engine, "before_cursor_execute")
def contar(conn, cursor, statement, parameters, context, executemany):
    """Suma 1 al contador cada vez que se envía una consulta."""
    consultas["n"] += 1


def paginas(session, tamano):
    """Generador: entrega una página de ventas por vez."""
    # Id de la última venta entregada
    ultimo_id = 0
    # Repite hasta que no queden más ventas
    while True:
        # Pide las siguientes ventas después del último id
        consulta = (
            select(Venta)
            .where(Venta.id > ultimo_id)
            .order_by(Venta.id)
            .limit(tamano)
        )
        # Ejecuta la consulta
        pagina = session.scalars(consulta).all()
        # Si no hay filas, termina el generador
        if not pagina:
            return
        # Entrega la página y se pausa hasta que pidan la siguiente
        yield pagina
        # Recuerda el id de la última fila para la próxima consulta
        ultimo_id = pagina[-1].id


# Abre una sesión y la cierra sola al terminar
with SessionLocal() as session:
    # Crear el generador no ejecuta ninguna consulta
    gen = paginas(session, 1000)
    print("Generador creado. Consultas ejecutadas:", consultas["n"])

    # Recorre las páginas numerándolas desde 1
    for i, pagina in enumerate(gen, start=1):
        print(
            f"Página {i}: {len(pagina)} filas, "
            f"ids {pagina[0].id} a {pagina[-1].id}"
            f" | consultas hasta ahora: {consultas['n']}"
        )
        # Se detiene en la página 3; las demás nunca se piden
        if i == 3:
            break

    print("Corté en la página 3. Consultas totales:", consultas["n"])
