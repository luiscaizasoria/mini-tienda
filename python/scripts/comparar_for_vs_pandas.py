"""Compara la velocidad de un bucle for frente a pandas vectorizado.

Uso: python -m scripts.comparar_for_vs_pandas
"""

# time mide cuánto tarda cada método
import time

# pandas lee el CSV y hace los cálculos vectorizados
import pandas as pd

# Lee todas las ventas del CSV
df = pd.read_csv("data/ventas.csv")


def medir(titulo, funcion):
    """Ejecuta una función e imprime su tiempo y su resultado."""
    # Marca el instante de inicio
    inicio = time.perf_counter()
    # Ejecuta la función a medir
    resultado = funcion()
    # Imprime el tiempo transcurrido y el total calculado
    print(
        f"{titulo}: {time.perf_counter() - inicio:.4f} s "
        f"-> total {resultado:.2f}"
    )


def con_iterrows():
    """Suma cantidad * precio fila por fila con iterrows (lento)."""
    # Acumulador del total
    total = 0.0
    # Recorre cada fila como una Serie de pandas
    for _, fila in df.iterrows():
        # Suma el total de esta venta
        total += fila["cantidad"] * fila["precio_unitario"]
    # Devuelve el total acumulado
    return total


def con_for_zip():
    """Suma cantidad * precio recorriendo dos columnas con zip."""
    # Acumulador del total
    total = 0.0
    # Recorre las dos columnas en paralelo
    for cantidad, precio in zip(df["cantidad"], df["precio_unitario"]):
        # Suma el total de esta venta
        total += cantidad * precio
    # Devuelve el total acumulado
    return total


def vectorizado():
    """Suma cantidad * precio con operaciones de columna completa."""
    # Multiplica las columnas y suma todo de una vez
    return (df["cantidad"] * df["precio_unitario"]).sum()


# Ejecuta y mide los tres métodos
medir("1. for con iterrows ", con_iterrows)
medir("2. for con zip      ", con_for_zip)
medir("3. pandas vectorizado", vectorizado)
