# Mini tienda: estructura y tecnologías

Documento de referencia de los dos proyectos que forman la mini tienda:
el **backend** (`python/`) y el **frontend** (`frontend/`).

- Repositorio: https://github.com/luiscaizasoria/mini-tienda
- Historia detallada del trabajo, etapa por etapa: [BITACORA.md](BITACORA.md)

---

## 1. Vista general

```
┌───────────────────────────┐  HTTP / JSON  ┌───────────────────────────┐        ┌──────────────────────┐
│  FRONTEND  (frontend/)    │──────────────▶│  BACKEND  (python/)       │───────▶│  BASE DE DATOS       │
│  TypeScript + Vite        │◀──────────────│  FastAPI + SQLAlchemy     │◀───────│  PostgreSQL          │
│  Navegador · puerto 5173  │               │  Puerto 8000              │        │  (Supabase)          │
└───────────────────────────┘               └───────────────────────────┘        └──────────────────────┘
        Dibuja pantallas                      Valida datos, aplica reglas          Guarda las tablas
        y pide datos                          y consulta la base                   y la autenticación
```

| Proyecto | Carpeta     | Responsabilidad                                                  |
|----------|-------------|------------------------------------------------------------------|
| Backend  | `python/`   | API REST, base de datos, migraciones, análisis de datos y tests. |
| Frontend | `frontend/` | Interfaz de usuario que consume la API.                          |

Cada proyecto tiene sus propias dependencias y se ejecuta por separado.

---

## 2. Tecnologías

### 2.1 Backend (`python/`)

| Tecnología       | Versión   | Para qué se usa                                         |
|------------------|-----------|---------------------------------------------------------|
| Python           | 3.13      | Lenguaje.                                               |
| FastAPI          | 0.162.5   | Framework de la API; genera la documentación en `/docs`.|
| Uvicorn          | 0.54.0    | Servidor que ejecuta la aplicación.                     |
| SQLAlchemy       | 2.1.8     | ORM: tablas como clases de Python.                      |
| Alembic          | 1.20.1    | Migraciones: historial versionado de cambios de la BD.  |
| Pydantic         | 2.14.3    | Validación de datos de entrada y salida.                |
| pydantic-settings| 2.16.2    | Lee la configuración desde variables de entorno (`.env`).|
| psycopg          | 3.3.9     | Controlador de PostgreSQL.                              |
| PyJWT + cryptography | 2.15.1 / 50.0.2 | Verifica los tokens JWT firmados por Supabase.  |
| supabase         | 2.34.1    | Cliente de Supabase (usado en los demos de login/RLS).  |
| pandas, numpy    | 3.1.1 / 2.5.4 | Análisis de las 100.000 ventas.                     |
| pytest, httpx    | 9.2.0 / 0.28.1 | Pruebas automáticas.                               |
| **PostgreSQL en Supabase** | -  | Base de datos y servicio de autenticación.       |

Estándar de código: **PEP 8** (verificado con `pycodestyle`, líneas de máximo
79 caracteres) y comentarios en español.

### 2.2 Frontend (`frontend/`)

| Tecnología  | Versión | Para qué se usa                                          |
|-------------|---------|----------------------------------------------------------|
| Node.js     | 24      | Ejecuta las herramientas de desarrollo (no corre en producción). |
| npm         | 11      | Gestor de paquetes.                                      |
| TypeScript  | 7.0     | Lenguaje con tipos; se revisa al compilar (`tsc`).       |
| Vite        | 8.3     | Servidor de desarrollo con recarga automática y empaquetador. |
| HTML + CSS  | -       | Estructura y estilos, **sin frameworks** (ni React ni Angular). |

Solo hay **dos dependencias** de desarrollo: `typescript` y `vite`.
La interfaz se construye con el DOM del navegador directamente.

---

## 3. Estructura del backend

```
python/
├── app/                          La API
│   ├── main.py                   Crea la app, activa CORS y registra las rutas
│   ├── api/
│   │   ├── dependencies.py       Sesión de BD y usuario autenticado
│   │   └── routers/              Un archivo por recurso
│   │       ├── productos.py      GET /productos, GET /productos/{id}, POST /productos
│   │       ├── categorias.py     GET /categorias, POST /categorias
│   │       ├── ventas.py         GET /ventas (paginado), GET /ventas/resumen
│   │       ├── pedidos.py        GET y POST /mis-pedidos (requiere token)
│   │       └── me.py             GET /me (requiere token)
│   ├── core/
│   │   ├── config.py             Variables de entorno (Settings)
│   │   └── security.py           Verificación del JWT de Supabase
│   ├── db/database.py            Motor y fábrica de sesiones
│   ├── models/                   Tablas (SQLAlchemy): usuario, pedido, producto, venta, categoria
│   └── schemas/                  Validación entrada/salida (Pydantic)
├── migrations/                   Alembic: env.py y 5 migraciones encadenadas
├── scripts/                      Generar, cargar y analizar ventas; sembrar datos
├── demos/                        Ejercicios de práctica
│   ├── python_basico/            Comprensiones, decoradores, generadores
│   ├── base_de_datos/            ORM, problema N+1, paginación, reflexión, Pydantic
│   └── supabase_auth/            Login, JWT, RLS, pruebas contra la API
├── tests/                        pytest con SQLite en memoria (11 tests)
├── alembic.ini · requirements.txt · .env.example · README.md
└── .env                          Credenciales reales (no se sube a Git)
```

### Capas del backend

```
 Petición HTTP
      │
      ▼
 routers/      Reciben la petición y devuelven la respuesta
      │ usan
      ▼
 schemas/      Validan lo que entra y dan forma a lo que sale
      │
      ▼
 models/       Representan las tablas
      │
      ▼
 db/           Conexión a PostgreSQL
```

### Modelo de datos

| Tabla        | Columnas principales                                              | Notas |
|--------------|-------------------------------------------------------------------|-------|
| `usuarios`   | id, auth_id (UUID de Supabase), nombre, email, creado_en          | Se crea la fila automáticamente la primera vez que entra un usuario con token. |
| `pedidos`    | id, usuario_id (→ usuarios), total, creado_en                     | Cada usuario solo ve los suyos. |
| `productos`  | id, nombre, precio, stock                                         | |
| `categorias` | id, nombre                                                        | La tabla existe en Supabase, pero **no tiene migración** de Alembic. |
| `ventas`     | id, fecha, cliente_id, producto, cantidad, precio_unitario        | 100.000 filas de datos sintéticos; sin llaves foráneas. |

### Rutas de la API

| Método | Ruta               | Acceso  | Descripción                                          |
|--------|--------------------|---------|------------------------------------------------------|
| GET    | `/productos`       | Público | Lista los productos.                                 |
| GET    | `/productos/{id}`  | Público | Devuelve un producto (404 si no existe).             |
| POST   | `/productos`       | Público | Crea un producto.                                    |
| GET    | `/categorias`      | Público | Lista las categorías.                                |
| POST   | `/categorias`      | Público | Crea una categoría.                                  |
| GET    | `/ventas`          | Público | Página de ventas (`limite` 1–100, `desplazamiento`). |
| GET    | `/ventas/resumen`  | Público | Número de ventas e ingresos totales.                 |
| GET    | `/me`              | Token   | Datos del usuario del token.                         |
| GET    | `/mis-pedidos`     | Token   | Pedidos del usuario.                                 |
| POST   | `/mis-pedidos`     | Token   | Crea un pedido para el usuario.                      |

La tabla `usuarios` **no se expone** en ninguna ruta pública porque contiene
datos personales.

### Autenticación

1. El usuario inicia sesión en **Supabase Auth**, que emite un token JWT firmado (ES256).
2. El cliente envía el token en `Authorization: Bearer <token>`.
3. `core/security.py` descarga las claves públicas de Supabase y valida firma, caducidad, audiencia y emisor.
4. `api/dependencies.py` enlaza el `sub` del token con `usuarios.auth_id`.

---

## 4. Estructura del frontend

```
frontend/
├── index.html                    Página única con <div id="app"> vacío
├── package.json · tsconfig.json
├── .env.development              Variables de desarrollo (sin secretos)
├── .env.example                  Plantilla para otros ambientes
├── README.md                     Estándar del frontend
└── src/
    ├── main.ts                   Arranque: cabecera, menú y enrutador
    ├── config/                   entorno.ts (única lectura de variables) y env.d.ts
    ├── router/
    │   ├── enlaces.ts            Lista de pantallas (fuente única para menú e inicio)
    │   ├── rutas.ts              Ruta → función que construye la pantalla
    │   ├── enrutador.ts          Cambia de pantalla según #/ruta
    │   └── ruta-actual.ts        Lee la ruta de la dirección
    ├── paginas/                  Pantallas: inicio, productos, categorias, ventas,
    │                             requiere-login, no-encontrada
    ├── componentes/              Piezas reutilizables: menú, tabla, paginador,
    │                             formularios, tarjeta, encabezado, campo
    ├── servicios/                Llamadas a la API: cliente-api, productos,
    │                             categorias, ventas
    ├── tipos/                    Interfaces de TypeScript: producto, categoria, venta
    ├── validaciones/             Reglas de validación de formularios
    ├── utilidades/               dom.ts (crear elementos HTML)
    └── estilos/                  Todo el CSS
        ├── variables.css         Colores, espacios, tamaños
        ├── base.css              Reglas globales y cabecera
        ├── paginas/              Un .css por pantalla
        └── componentes/          Un .css por componente
```

### Pantallas

| Ruta          | Pantalla    | Qué permite probar                                         |
|---------------|-------------|------------------------------------------------------------|
| `#/`          | Inicio      | Explicación del proyecto y acceso a cada tabla.            |
| `#/productos` | Productos   | Listar y crear productos.                                  |
| `#/categorias`| Categorías  | Listar y crear categorías.                                 |
| `#/ventas`    | Ventas      | Resumen y recorrido paginado de las 100.000 ventas.        |
| `#/usuarios`  | Usuarios    | Aviso: requiere login (pendiente).                         |
| `#/pedidos`   | Pedidos     | Aviso: requiere login (pendiente).                         |

### Capas del frontend

```
 pantalla (paginas/)
     │ usa
     ├──▶ componentes/   piezas de interfaz
     ├──▶ servicios/     comunicación con la API ──▶ cliente-api.ts ──▶ fetch
     ├──▶ validaciones/  reglas antes de enviar
     └──▶ tipos/         forma de los datos

 config/entorno.ts  ◀── .env.<modo>   (única lectura de variables de entorno)
```

### Reglas del estándar

1. Nombres de archivo en minúsculas con guiones (`tarjeta-producto.ts`).
2. Una dependencia por capa: solo `cliente-api.ts` usa `fetch`.
3. Sin valores fijos en el código: todo sale de `config/entorno.ts`.
4. Colores y espacios con las variables de `variables.css`.
5. Datos de la API en pantalla con `textContent`, nunca `innerHTML`.
6. Un CSS por pantalla o componente, en `estilos/`, espejo de la estructura de `src/`.
7. Cada línea o bloque de código lleva su comentario en español.

---

## 5. Configuración por ambiente

| Proyecto | Archivo               | Variable            | Para qué sirve                                   |
|----------|-----------------------|---------------------|--------------------------------------------------|
| Backend  | `python/.env`         | `DATABASE_URL`      | Conexión a PostgreSQL.                           |
| Backend  | `python/.env`         | `SUPABASE_URL`, `SUPABASE_PUBLISHABLE_KEY` | Proyecto de Supabase.     |
| Backend  | `python/.env`         | `CORS_ORIGINS`      | Páginas autorizadas a llamar a la API (opcional).|
| Frontend | `frontend/.env.<modo>`| `VITE_API_URL`      | Dirección de la API.                             |

- **Frontend:** `npm run dev` lee `.env.development`; `npm run build` lee `.env.production`; `npm run build -- --mode staging` lee `.env.staging`.
- Todo lo que empieza con `VITE_` queda **visible en el navegador**: nunca van claves secretas ahí.
- `python/.env` **nunca se sube a Git**; las plantillas son los archivos `.env.example`.

---

## 6. Cómo ejecutarlo

Se necesitan dos terminales:

```powershell
# Terminal 1: backend (http://127.0.0.1:8000/docs)
cd python
python -m venv .venv                   # solo la primera vez
.venv\Scripts\Activate.ps1
pip install -r requirements.txt        # solo la primera vez
copy .env.example .env                 # y editar los valores
alembic upgrade head                   # crear las tablas
uvicorn app.main:app --reload

# Terminal 2: frontend (http://localhost:5173)
cd frontend
npm install                            # solo la primera vez
npm run dev
```

Pruebas del backend: `cd python` y `pytest` (11 tests, sin tocar Supabase).

Scripts y demos, desde `python/`:

```powershell
python -m scripts.generar_ventas          # crea data/ventas.csv
python -m scripts.estadisticas_ventas
python -m demos.python_basico.decoradores
```

---

## 7. Calidad y seguridad

| Aspecto            | Estado                                                             |
|--------------------|--------------------------------------------------------------------|
| Estilo Python      | PEP 8 sin avisos.                                                  |
| Tests              | 11 tests del backend. Sin tests automáticos en el frontend.        |
| Tipos              | TypeScript se revisa al compilar (`npm run build`).                |
| Validación         | En el navegador (comodidad) y en la API con Pydantic (la que protege). |
| Secretos           | `.env` fuera de Git; el frontend solo recibe valores públicos.     |
| CORS               | Lista cerrada de orígenes, configurable por ambiente.              |
| Inyección de HTML  | Evitada: los datos se insertan con `textContent`.                  |

### Pendientes conocidos

- `POST /productos` y `POST /categorias` son públicos; deben exigir sesión.
- Login con Supabase en el frontend y activación de Usuarios y Pedidos.
- La tabla `categorias` no tiene migración de Alembic.
- Faltan tests de `/mis-pedidos`, de autenticación y del frontend.
