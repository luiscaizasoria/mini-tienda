"""Demo de reflexión: leer una tabla existente sin declarar su modelo.

Uso: python -m demos.base_de_datos.prueba_reflexion
"""

# MetaData guarda tablas; Table las representa; select arma consultas
from sqlalchemy import MetaData, Table, select

# Motor de conexión a la base de datos
from app.db.database import engine

# Contenedor vacío donde se registrará la tabla
metadata = MetaData()
# Lee la estructura real de "categorias" directamente desde la base
categorias = Table("categorias", metadata, autoload_with=engine)

# Muestra los nombres de las columnas descubiertas
print("Columnas:", [c.name for c in categorias.columns])

# Abre una conexión y la cierra sola al terminar
with engine.connect() as conn:
    # Recorre todas las filas de la tabla
    for fila in conn.execute(select(categorias)):
        print(fila.id, fila.nombre)
