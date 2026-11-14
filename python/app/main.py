"""Punto de entrada de la API: crea la aplicación y registra las rutas."""

# Clase principal de FastAPI
from fastapi import FastAPI
# Middleware que decide qué páginas web pueden llamar a la API (CORS)
from fastapi.middleware.cors import CORSMiddleware

# Módulos que contienen los grupos de rutas (routers)
from app.api.routers import me, pedidos, productos
# Configuración leída desde variables de entorno
from app.core.config import settings

# Crea la aplicación; el título aparece en la documentación /docs
app = FastAPI(title="Mini tienda")
# Activa CORS: sin esto el navegador bloquea las respuestas de la API
app.add_middleware(
    CORSMiddleware,
    # Solo estas páginas pueden leer las respuestas (viene de la config)
    allow_origins=settings.cors_origins,
    # Métodos HTTP permitidos
    allow_methods=["GET", "POST"],
    # Encabezados permitidos (Authorization llevará el token más adelante)
    allow_headers=["Authorization", "Content-Type"],
)
# Registra las rutas públicas de productos (/productos)
app.include_router(productos.router)
# Registra la ruta que muestra los datos del usuario (/me)
app.include_router(me.router)
# Registra las rutas privadas de pedidos (/mis-pedidos)
app.include_router(pedidos.router)
