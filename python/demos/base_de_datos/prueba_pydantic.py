"""Demo de validación con Pydantic y conversión desde el ORM.

Uso: python -m demos.base_de_datos.prueba_pydantic
"""

# ValidationError se lanza cuando los datos no cumplen el esquema
from pydantic import ValidationError
# select construye consultas SQL
from sqlalchemy import select

# Fábrica de sesiones de base de datos
from app.db.database import SessionLocal
# Modelo de la tabla productos
from app.models import Producto
# Esquemas de entrada y salida de un producto
from app.schemas.producto import ProductoCreate, ProductoRead

# 1. Entrada válida: Pydantic convierte "2.50" a Decimal y "10" a int
ok = ProductoCreate(nombre="Jugo", precio="2.50", stock="10")
print("Válido:", ok)

# 2. Entrada inválida: precio negativo y nombre corto
try:
    ProductoCreate(nombre="A", precio=-1)
# Captura el error de validación y lo recorre
except ValidationError as e:
    # Muestra cada campo inválido y su motivo
    for error in e.errors():
        print("Error en", error["loc"], "->", error["msg"])

# 3. Del modelo ORM al esquema de salida
with SessionLocal() as session:
    # Toma el primer producto de la tabla
    producto = session.scalars(select(Producto)).first()
    # Convierte el objeto ORM en el esquema y luego en diccionario
    print("Salida:", ProductoRead.model_validate(producto).model_dump())
