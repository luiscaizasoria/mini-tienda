"""Configuración de la aplicación, leída desde variables de entorno."""

# BaseSettings lee variables de entorno; SettingsConfigDict la configura
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Valores de configuración que la aplicación necesita para arrancar."""

    # Lee el archivo .env e ignora las variables que no se declaran aquí
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Dirección de conexión a la base de datos PostgreSQL
    database_url: str
    # Dirección del proyecto en Supabase
    supabase_url: str
    # Clave pública (publishable) de Supabase
    supabase_publishable_key: str
    # Páginas web autorizadas a llamar a la API desde un navegador (CORS).
    # Por defecto, el servidor de desarrollo del frontend. En otros
    # ambientes se cambia con CORS_ORIGINS='["https://mi-tienda.com"]'
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ]


# Instancia única que usa el resto del código
settings = Settings()
