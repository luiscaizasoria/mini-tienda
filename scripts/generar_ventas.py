"""Genera 100.000 ventas sintéticas y las guarda en data/ventas.csv.

Uso: python -m scripts.generar_ventas
"""

# numpy genera números aleatorios de forma rápida
import numpy as np
# pandas arma y guarda la tabla de datos
import pandas as pd

# Precio de cada producto
PRECIOS = {
    "Agua 500 ml": 0.75,
    "Galletas": 1.50,
    "Jugo": 2.50,
    "Cereal": 3.80,
    "Leche": 1.10,
    "Pan": 0.30,
    "Detergente": 4.20,
    "Jabón": 0.90,
}
# Cantidad de ventas a generar
N = 100_000

# Generador aleatorio con semilla fija: siempre da los mismos datos
rng = np.random.default_rng(42)
# Elige un producto al azar para cada venta
producto = rng.choice(list(PRECIOS), N)

# Construye la tabla de ventas
df = pd.DataFrame({
    # Fecha al azar dentro de 2026, con precisión de minutos
    "fecha": pd.Timestamp("2026-01-01")
    + pd.to_timedelta(rng.integers(0, 365 * 24 * 60, N), unit="m"),
    # Cliente al azar entre 1 y 500
    "cliente_id": rng.integers(1, 501, N),
    # Producto vendido
    "producto": producto,
    # Unidades al azar entre 1 y 5
    "cantidad": rng.integers(1, 6, N),
    # Precio unitario buscado según el producto
    "precio_unitario": pd.Series(producto).map(PRECIOS),
})

# Guarda la tabla en un archivo CSV, sin la columna de índice
df.to_csv("data/ventas.csv", index=False)
# Informa cuántas filas se generaron
print(f"Generadas {len(df)} filas en data/ventas.csv")
# Muestra las primeras filas como ejemplo
print(df.head())
