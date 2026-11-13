"""Calcula estadísticas de las ventas del CSV con pandas.

Uso: python -m scripts.estadisticas_ventas
"""

# time mide la duración total del análisis
import time

# pandas lee el CSV y agrupa los datos
import pandas as pd

# Marca el instante de inicio
inicio = time.perf_counter()

# Lee el CSV interpretando "fecha" como fecha y hora
df = pd.read_csv("data/ventas.csv", parse_dates=["fecha"])
# Nueva columna con el total de cada venta
df["total"] = df["cantidad"] * df["precio_unitario"]

# Muestra la cantidad de filas
print("Filas:", len(df))
# Muestra el ingreso total redondeado a 2 decimales
print("Ingreso total:", round(df["total"].sum(), 2))
print()

print("Ventas por mes")
# Suma los totales agrupando por mes
por_mes = df.groupby(df["fecha"].dt.to_period("M"))["total"].sum().round(2)
print(por_mes)
print()

print("Productos por ingresos")
# Unidades e ingresos por producto, del que más ingresa al que menos
por_producto = (
    df.groupby("producto")
    .agg(unidades=("cantidad", "sum"), ingresos=("total", "sum"))
    .sort_values("ingresos", ascending=False)
    .round(2)
)
print(por_producto)
print()

print("Top 5 clientes por gasto")
# Compras y gasto por cliente; se queda con los 5 que más gastan
por_cliente = (
    df.groupby("cliente_id")
    .agg(compras=("total", "count"), gasto=("total", "sum"))
    .sort_values("gasto", ascending=False)
    .head(5)
    .round(2)
)
print(por_cliente)
print()

# Muestra cuánto tardó todo el análisis
print(f"Tiempo: {time.perf_counter() - inicio:.2f} s")
