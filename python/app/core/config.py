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


# Instancia única que usa el resto del código
settings = Settings()
