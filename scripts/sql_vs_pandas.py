"""Compara el mismo cálculo hecho con SQL y con pandas.

Uso: python -m scripts.sql_vs_pandas
"""

# pandas lee el CSV y también consultas SQL
import pandas as pd

# Motor de conexión a la base de datos
from app.db.database import engine

# Consulta: los 5 clientes que más gastan
SQL = """
select cliente_id,
       count(*) as compras,
       round(sum(cantidad * precio_unitario), 2) as gasto
from ventas
group by cliente_id
order by gasto desc
limit 5
"""

# 1. SQL: la base calcula y solo viajan 5 filas
con_sql = pd.read_sql(SQL, engine)
# Convierte el gasto a número decimal normal para poder compararlo
con_sql["gasto"] = con_sql["gasto"].astype(float)

# 2. pandas: se leen las 100.000 filas del CSV y se calcula en memoria
df = pd.read_csv("data/ventas.csv")
# Nueva columna con el total de cada venta
df["total"] = df["cantidad"] * df["precio_unitario"]
# Compras y gasto por cliente; se queda con los 5 que más gastan
con_pandas = (
    df.groupby("cliente_id")
    .agg(compras=("total", "count"), gasto=("total", "sum"))
    .sort_values("gasto", ascending=False)
    .head(5)
    .round(2)
    .reset_index()
)

print("Con SQL (read_sql):")
print(con_sql)
print()
print("Con pandas (CSV):")
print(con_pandas)
print()

# ¿Los dos métodos eligieron a los mismos clientes en el mismo orden?
mismos_clientes = (
    con_sql["cliente_id"].tolist() == con_pandas["cliente_id"].tolist()
)
# ¿Los gastos coinciden con menos de un centavo de diferencia?
mismo_gasto = ((con_sql["gasto"] - con_pandas["gasto"]).abs() < 0.01).all()
# Muestra True solo si ambas comprobaciones se cumplen
print("Coinciden:", mismos_clientes and mismo_gasto)
