# Mini tienda: backend (Python)

API de una tienda pequeña hecha con **FastAPI**, **SQLAlchemy 2** y
**PostgreSQL en Supabase**. Incluye autenticación con tokens JWT de Supabase,
migraciones con Alembic, pruebas con pytest y scripts de análisis con pandas.

Todos los comandos de este documento se ejecutan **dentro de la carpeta
`python/`**.

## Estructura

```
python/
├── app/                     Código de la API
│   ├── main.py              Crea la app y registra las rutas
│   ├── api/
│   │   ├── dependencies.py  Sesión de BD y usuario autenticado
│   │   └── routers/         Rutas: productos, me, pedidos
│   ├── core/
│   │   ├── config.py        Variables de entorno (.env)
│   │   └── security.py      Verificación del token JWT
│   ├── db/database.py       Motor y sesiones de SQLAlchemy
│   ├── models/              Tablas (ORM)
│   └── schemas/             Validación de entrada y salida (Pydantic)
├── migrations/              Migraciones de Alembic
├── scripts/                 Carga y análisis de datos de ventas
├── demos/                   Ejercicios de práctica
│   ├── python_basico/       Comprensiones, decoradores, generadores
│   ├── base_de_datos/       ORM, N+1, paginación, reflexión, Pydantic
│   └── supabase_auth/       Login, JWT, RLS, pruebas contra la API
└── tests/                   Pruebas automáticas (SQLite en memoria)
```

## Puesta en marcha

```powershell
# 0. Entrar a la carpeta del backend
cd python

# 1. Crear y activar el entorno virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Configurar variables de entorno
copy .env.example .env      # y editar los valores

# 4. Crear las tablas en la base de datos
alembic upgrade head

# 5. Levantar la API (documentación en http://127.0.0.1:8000/docs)
uvicorn app.main:app --reload
```

## Rutas

| Método | Ruta               | Acceso  | Descripción                  |
|--------|--------------------|---------|------------------------------|
| GET    | `/productos`       | Público | Lista los productos          |
| GET    | `/productos/{id}`  | Público | Devuelve un producto         |
| POST   | `/productos`       | Público | Crea un producto             |
| GET    | `/me`              | Token   | Datos del usuario del token  |
| GET    | `/mis-pedidos`     | Token   | Pedidos del usuario          |
| POST   | `/mis-pedidos`     | Token   | Crea un pedido               |
| GET    | `/categorias`      | Público | Lista las categorías         |
| POST   | `/categorias`      | Público | Crea una categoría           |
| GET    | `/ventas`          | Público | Página de ventas (`limite` 1–100, `desplazamiento`) |
| GET    | `/ventas/resumen`  | Público | Número de ventas e ingresos totales |

## Pruebas

```powershell
pytest
```

Las pruebas usan SQLite en memoria, así que no tocan Supabase.

## Scripts y demos

Se ejecutan como módulos desde la raíz del proyecto:

```powershell
python -m scripts.generar_ventas          # crea data/ventas.csv
python -m scripts.estadisticas_ventas
python -m demos.python_basico.decoradores
python -m demos.base_de_datos.n_mas_uno
```

`data/ventas.csv` no se sube al repositorio: se genera con
`scripts.generar_ventas`.
