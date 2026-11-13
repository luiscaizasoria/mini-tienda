"""Demo: consulta las tablas por la Data API de Supabase sin iniciar sesión.

Uso: python -m demos.supabase_auth.probar_data_api
"""

# create_client crea el cliente de Supabase
from supabase import create_client

# Configuración con la dirección y clave de Supabase
from app.core.config import settings

# Cliente anónimo: usa solo la clave pública, sin sesión
client = create_client(
    settings.supabase_url,
    settings.supabase_publishable_key,
)

# Prueba cada tabla del proyecto
for tabla in ["usuarios", "pedidos", "productos", "ventas", "categorias"]:
    try:
        # Pide 1 fila y el conteo de filas visibles
        r = client.table(tabla).select("*", count="exact").limit(1).execute()
        print(f"{tabla:10} SIN LOGIN -> filas visibles: {r.count}")
    # Si la política de seguridad bloquea el acceso, lo informa
    except Exception as e:
        print(f"{tabla:10} SIN LOGIN -> bloqueado ({type(e).__name__})")
