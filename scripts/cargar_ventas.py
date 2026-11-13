"""Compara tres formas de cargar ventas en PostgreSQL.

Uso: python -m scripts.cargar_ventas
"""

# time mide cuánto tarda cada método
import time

# pandas lee el CSV
import pandas as pd
# insert construye INSERT; text ejecuta SQL escrito a mano
from sqlalchemy import insert, text

# Motor de conexión a la base de datos
from app.db.database import engine
# Modelo de la tabla ventas
from app.models import Venta

# Objeto tabla del modelo, necesario para construir los INSERT
tabla = Venta.__table__
# Columnas que se cargan (id se genera solo)
COLUMNAS = ["fecha", "cliente_id", "producto", "cantidad", "precio_unitario"]

# Lee el CSV interpretando "fecha" como fecha y hora
df = pd.read_csv("data/ventas.csv", parse_dates=["fecha"])


def limpiar():
    """Vacía la tabla ventas y reinicia el contador de ids."""
    # Abre una transacción que se confirma al terminar
    with engine.begin() as conn:
        # Borra todas las filas y reinicia los ids
        conn.execute(text("TRUNCATE TABLE ventas RESTART IDENTITY"))


def contar():
    """Devuelve cuántas filas hay en la tabla ventas."""
    # Abre una conexión de solo lectura
    with engine.connect() as conn:
        # Cuenta las filas y devuelve el número
        return conn.execute(text("SELECT count(*) FROM ventas")).scalar()


def informar(titulo, filas, inicio):
    """Imprime el tiempo y la velocidad de un método de carga."""
    # Segundos transcurridos desde el inicio
    segundos = time.perf_counter() - inicio
    # Muestra filas, tiempo, velocidad y total real en la tabla
    print(
        f"{titulo}: {filas} filas en {segundos:.2f} s "
        f"({filas / segundos:,.0f} filas/s) | en tabla: {contar()}"
    )


# 1. Una fila por vez, con commit en cada una
limpiar()
# Marca el instante de inicio
inicio = time.perf_counter()
# Recorre las primeras 100 filas como diccionarios
for fila in df.head(100).to_dict("records"):
    # Abre una transacción nueva por cada fila (lo más lento)
    with engine.begin() as conn:
        # Inserta la fila
        conn.execute(insert(tabla), fila)
informar("1. fila por fila   ", 100, inicio)

# 2. Por lotes: una sola transacción, parámetros en bloque
limpiar()
# Marca el instante de inicio
inicio = time.perf_counter()
# Una sola transacción para todas las filas
with engine.begin() as conn:
    # Inserta 5.000 filas en una sola llamada
    conn.execute(insert(tabla), df.head(5_000).to_dict("records"))
informar("2. por lotes       ", 5_000, inicio)

# 3. COPY: el protocolo de carga masiva de PostgreSQL
limpiar()
# Marca el instante de inicio
inicio = time.perf_counter()
# Conexión de bajo nivel, necesaria para usar COPY
raw = engine.raw_connection()
try:
    # Cursor de la conexión
    with raw.cursor() as cur:
        # Abre el canal COPY hacia la tabla
        with cur.copy(
            f"COPY ventas ({', '.join(COLUMNAS)}) FROM STDIN"
        ) as copy:
            # Envía las filas una por una por el canal
            for fila in df[COLUMNAS].itertuples(index=False, name=None):
                copy.write_row(fila)
    # Confirma la carga completa
    raw.commit()
finally:
    # Cierra la conexión aunque haya ocurrido un error
    raw.close()
informar("3. COPY            ", len(df), inicio)
