"""Genera modelos ORM a partir de las tablas existentes (sqlacodegen).

Guarda el resultado en modelos_generados.py, que está en .gitignore.

Uso: python -m demos.base_de_datos.generar_modelos
"""

# subprocess ejecuta sqlacodegen como un programa externo
import subprocess
# sys.executable es el Python del entorno virtual actual
import sys

# Configuración con la dirección de la base de datos
from app.core.config import settings

# Ejecuta sqlacodegen y captura su salida
resultado = subprocess.run(
    [sys.executable, "-m", "sqlacodegen", settings.database_url],
    capture_output=True,
    text=True,
)

# Si sqlacodegen falló, muestra el error
if resultado.returncode != 0:
    print(resultado.stderr)
else:
    # Guarda los modelos generados en un archivo
    with open("modelos_generados.py", "w", encoding="utf-8") as f:
        f.write(resultado.stdout)
    print("Listo: modelos_generados.py")
