"""Punto de entrada de la API: crea la aplicación y registra las rutas."""

# Clase principal de FastAPI
from fastapi import FastAPI

# Módulos que contienen los grupos de rutas (routers)
from app.api.routers import me, pedidos, productos

# Crea la aplicación; el título aparece en la documentación /docs
app = FastAPI(title="Mini tienda")
# Registra las rutas públicas de productos (/productos)
app.include_router(productos.router)
# Registra la ruta que muestra los datos del usuario (/me)
app.include_router(me.router)
# Registra las rutas privadas de pedidos (/mis-pedidos)
app.include_router(pedidos.router)
