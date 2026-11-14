"""Demo de generadores con el CSV de ventas.

Uso: python -m demos.python_basico.generadores
"""

# csv lee el archivo fila por fila
import csv
# sys.getsizeof mide la memoria que ocupa un objeto
import sys
# islice toma solo las primeras filas de un generador
from itertools import islice

# Ubicación del archivo de ventas
RUTA = "data/ventas.csv"


def leer_ventas(ruta):
    """Generador: entrega una fila a la vez."""
    # Abre el archivo y lo cierra solo al terminar
    with open(ruta, newline="", encoding="utf-8") as f:
        # Lee cada fila como un diccionario
        for fila in csv.DictReader(f):
            # Entrega la fila y se pausa hasta que pidan la siguiente
            yield fila


def solo_producto(ventas, producto):
    """Generador: deja pasar solo las ventas de un producto."""
    # Recorre las ventas que llegan
    for v in ventas:
        # Si es el producto buscado
        if v["producto"] == producto:
            # Entrega la venta
            yield v


def con_total(ventas):
    """Generador: añade a cada venta su total."""
    # Recorre las ventas que llegan
    for v in ventas:
        # Calcula cantidad * precio unitario
        v["total"] = int(v["cantidad"]) * float(v["precio_unitario"])
        # Entrega la venta ya con su total
        yield v


# 1. Crear el generador no ejecuta nada; cada next() entrega una fila
gen = leer_ventas(RUTA)
print("1. Tipo:", type(gen).__name__)
print("   Fila 1:", next(gen))
print("   Fila 2:", next(gen))

# 2. Un pipeline de generadores: lee, filtra y calcula solo lo que se pide
pipeline = con_total(solo_producto(leer_ventas(RUTA), "Pan"))
print("2. Primeras 3 ventas de Pan:")
# Toma solo 3 resultados; el resto del archivo no se procesa
for v in islice(pipeline, 3):
    print("  ", v["fecha"], v["cantidad"], v["total"])

# 3. Memoria: lista frente a generador
# Carga todas las filas en memoria a la vez
todas = list(leer_ventas(RUTA))
print(
    "3. Lista de", len(todas), "filas:",
    sys.getsizeof(todas), "bytes (solo la lista)",
)
print("   Generador:", sys.getsizeof(leer_ventas(RUTA)), "bytes")

# 4. Expresión generadora: suma sin crear lista intermedia
total = sum(
    int(v["cantidad"]) * float(v["precio_unitario"])
    for v in leer_ventas(RUTA)
)
print("4. Ingreso total:", round(total, 2))

# 5. Un generador se consume una sola vez
g = leer_ventas(RUTA)
# Cuenta las filas recorriendo el generador completo
print("5. Primera pasada:", sum(1 for _ in g), "filas")
# El generador ya se agotó, así que no queda nada por contar
print("   Segunda pasada:", sum(1 for _ in g), "filas")
