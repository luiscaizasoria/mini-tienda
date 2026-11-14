# Bitácora del proyecto Mini tienda

Registro de lo que se hizo, archivo por archivo, y de cómo encaja todo.

---

## 1. Resumen de las etapas

| # | Etapa | Resultado |
|---|-------|-----------|
| 1 | Entender el proyecto | Backend en Python (FastAPI + SQLAlchemy + Supabase) y scripts de práctica. |
| 2 | Reorganizar el código | PEP 8, comentarios línea a línea, demos agrupados, caché y archivos inútiles borrados. |
| 3 | Subir a GitHub | Repositorio público `luiscaizasoria/mini-tienda`. |
| 4 | Separar en dos proyectos | `python/` (backend) y `frontend/` (interfaz). |
| 5 | Crear el frontend | Vite + TypeScript puro, sin frameworks. |
| 6 | Primer catálogo | La interfaz pide los productos a la API y los dibuja. |
| 7 | Estándar del frontend | Estructura por capas, estilos organizados y configuración por ambiente (sin valores fijos en el código). |

---

## 2. Mapa del proyecto

```
mini-tienda/
├── BITACORA.md          Este documento
├── README.md            Presentación corta del proyecto
├── .gitignore           Qué NO se sube a Git
├── python/              BACKEND (puerto 8000)
│   ├── app/             La API
│   ├── migrations/      Historial de cambios de la base de datos
│   ├── scripts/         Carga y análisis de datos
│   ├── demos/           Ejercicios de práctica
│   ├── tests/           Pruebas automáticas
│   ├── alembic.ini, requirements.txt, .env, .env.example, README.md
└── frontend/            INTERFAZ (puerto 5173)
    ├── index.html
    ├── .env.development, .env.example    Configuración por ambiente
    ├── README.md        Estándar del frontend: dónde va cada cosa
    ├── src/
    │   ├── main.ts          Arranque
    │   ├── config/          Variables de entorno
    │   ├── paginas/         Pantallas
    │   ├── componentes/     Piezas reutilizables
    │   ├── servicios/       Llamadas a la API
    │   ├── tipos/           Forma de los datos
    │   └── estilos/         Todo el CSS
    └── package.json, tsconfig.json
```

---

## 3. Qué hace cada archivo

### 3.1 Raíz

| Archivo | Objetivo | Qué se hizo |
|---|---|---|
| `.gitignore` | Evitar que se suban secretos y basura. | Estaba roto (dos reglas pegadas en una línea). Se reescribió: ignora `.venv/`, `.env`, cachés, `data/`, `.vscode/`, `node_modules/` y `dist/`. |
| `README.md` | Explicar la división en dos partes. | Nuevo. |
| `BITACORA.md` | Este registro. | Nuevo. |

### 3.2 Backend: `python/app/` (la API)

| Archivo | Objetivo | Qué se hizo |
|---|---|---|
| `main.py` | Crear la aplicación y registrar las rutas. | Comentado. En la etapa 6 se añadió **CORS** para que el navegador acepte las respuestas del frontend. En la etapa 7 la lista de orígenes dejó de estar fija y se lee de la configuración. |
| `core/config.py` | Leer la configuración del archivo `.env`. | Comentado y ajustado a PEP 8. En la etapa 7 se añadió `cors_origins` (por defecto `localhost:5173`, se cambia con `CORS_ORIGINS`). |
| `core/security.py` | Verificar los tokens JWT de Supabase (firma, caducidad, emisor). | Comentado. |
| `db/database.py` | Crear la conexión a PostgreSQL y las sesiones. | Comentado. |
| `models/*.py` | Una clase por tabla: `Usuario`, `Pedido`, `Producto`, `Venta`, `Categoria`. | Comentados, con una explicación por columna. |
| `schemas/*.py` | Validar lo que entra y sale de la API (Pydantic). | Comentados. |
| `api/dependencies.py` | Entregar la sesión de BD y el usuario autenticado a las rutas. | Comentado. |
| `api/routers/productos.py` | Rutas públicas del catálogo: `GET /productos`, `GET /productos/{id}`, `POST /productos`. | Comentado. |
| `api/routers/pedidos.py` | Rutas privadas: pedidos del usuario con sesión. | Comentado. |
| `api/routers/me.py` | Devuelve los datos del usuario del token. | Comentado. |
| `__init__.py` (varios) | Marcar las carpetas como paquetes de Python. | Antes vacíos, ahora con una línea de descripción. |

### 3.3 Backend: resto de `python/`

| Archivo o carpeta | Objetivo | Qué se hizo |
|---|---|---|
| `migrations/env.py` y `versions/*.py` | Alembic: crear y versionar las tablas. | Reescritos con PEP 8 y comentarios. Los identificadores de revisión **no cambiaron**, así que la cadena sigue intacta. |
| `tests/` | Probar la API con SQLite en memoria, sin tocar Supabase. | Reescritos; los 4 tests pasan. |
| `scripts/` | Generar, cargar y analizar 100.000 ventas. | Comentados y con PEP 8. |
| `demos/` | Ejercicios: decoradores, generadores, ORM, JWT, RLS. | Agrupados en `python_basico/`, `base_de_datos/` y `supabase_auth/`. |
| `requirements.txt` | Dependencias exactas. | Faltaban `PyJWT`, `cryptography` y `supabase`. Además fijaba `websockets 17.4`, incompatible con `supabase`. Se regeneró con `pip freeze` desde el entorno que funcionaba. |
| `.env.example` | Plantilla de variables de entorno. | Ahora lista todas las variables, sin valores reales. |
| `.env` | Credenciales reales. | Solo se movió de lugar. **Nunca se sube a Git.** |
| `README.md` | Cómo arrancar el backend. | Actualizado: los comandos se ejecutan desde `python/`. |

**Se eliminó:** todos los `__pycache__` y `.pytest_cache`, las carpetas vacías `repositories/` y `services/`, y `demos/modelos_generados.py` (salida autogenerada y desactualizada).

### 3.4 Frontend: `frontend/`

| Archivo | Objetivo | Qué hace |
|---|---|---|
| `index.html` | La única página de la aplicación. | Tiene un `<div id="app">` vacío y carga `src/main.ts`. |
| `src/main.ts` | Arranque. | Importa los estilos globales y monta la pantalla del catálogo. No tiene lógica propia. |
| `src/config/env.d.ts` | Decirle a TypeScript qué variables de entorno existen. | Declara `VITE_API_URL`. |
| `src/config/entorno.ts` | **Única puerta a la configuración.** | Lee `VITE_API_URL`, falla con un mensaje claro si falta y exporta `entorno.apiUrl`. |
| `src/tipos/producto.ts` | Describir un producto de la API. | `interface Producto`. El precio es `string` porque Pydantic envía los `Decimal` como texto. |
| `src/servicios/cliente-api.ts` | Cliente HTTP base. | `pedirJson<T>()` une la URL base con la ruta, hace `fetch` y revisa errores HTTP. |
| `src/servicios/productos.ts` | Operaciones de productos. | `obtenerProductos()` llama a `GET /productos`. |
| `src/componentes/tarjeta-producto.ts` | Pieza reutilizable. | Crea la tarjeta de un producto. |
| `src/paginas/catalogo.ts` | Pantalla del catálogo. | Arma el título y la lista, muestra "Cargando...", lista vacía y error. |
| `src/estilos/variables.css` | Valores de diseño. | Colores, espacios, radios, sombra y ancho máximo. |
| `src/estilos/base.css` | Estilos globales. | Fuente, fondo y contenedor central. |
| `src/estilos/paginas/catalogo.css` | CSS de la pantalla. | Cuadrícula de tarjetas. |
| `src/estilos/componentes/tarjeta-producto.css` | CSS del componente. | Caja, nombre, precio y stock. |
| `.env.development` | Variables del ambiente de desarrollo. | `VITE_API_URL=http://127.0.0.1:8000`. Sin secretos, por eso se sube a Git. |
| `.env.example` | Plantilla para otros ambientes. | Explica los modos de Vite y cómo crear `.env.production` o `.env.staging`. |
| `README.md` | Estándar del frontend. | Estructura, tabla "¿Dónde pongo...?", reglas y manejo de ambientes. |
| `tsconfig.json` | Reglas de TypeScript. | Generado por Vite; no se modificó. |
| `package.json` | Dependencias y comandos. | Solo dos dependencias: `typescript` y `vite`. |

> En la etapa 6 existían `tipos.ts`, `api.ts`, `catalogo.ts` y `style.css` planos dentro de `src/`. En la etapa 7 se repartieron en las carpetas de arriba y se borraron.

---

## 4. Cómo funciona todo en conjunto

```
 Navegador (http://localhost:5173)          API (http://127.0.0.1:8000)         Supabase
┌────────────────────────────────┐        ┌──────────────────────────┐      ┌────────────┐
│ index.html                     │        │ FastAPI  (app/main.py)   │      │ PostgreSQL │
│  └─ main.ts                    │        │  └─ routers/productos.py │      │ tabla      │
│      └─ paginas/catalogo.ts    │ fetch  │      └─ SQLAlchemy ──────┼─────▶│ productos  │
│          ├─ servicios/         │───────▶│         (models/)        │      └────────────┘
│          │   productos.ts      │◀───────┤  responde JSON           │
│          │   └ cliente-api.ts  │  JSON  │  (schemas/ lo valida)    │
│          └─ componentes/       │        └──────────────────────────┘
│              tarjeta-producto  │
│                                │   La URL de la API sale de
│  config/entorno.ts ◀── .env.*  │   VITE_API_URL (según el ambiente)
└────────────────────────────────┘
```

**El recorrido de una visita, paso a paso:**

1. El navegador abre `localhost:5173`. **Vite** entrega `index.html`, que carga `main.ts`.
2. `main.ts` importa los estilos globales y monta la pantalla `crearPaginaCatalogo()`.
3. Al cargarse, `config/entorno.ts` lee `VITE_API_URL` del archivo `.env` del modo actual (en desarrollo, `.env.development`).
4. `paginas/catalogo.ts` muestra "Cargando productos..." y llama a `obtenerProductos()`.
5. `servicios/productos.ts` delega en `pedirJson()` de `cliente-api.ts`, que hace `fetch` a `<VITE_API_URL>/productos`.
6. El navegador nota que la página (puerto 5173) y la API (puerto 8000) son **orígenes distintos**. Por eso la API responde con la cabecera CORS `Access-Control-Allow-Origin: http://localhost:5173`. Sin ella, el navegador bloquearía la respuesta.
7. En la API, `routers/productos.py` recibe la petición. `dependencies.get_db` le entrega una sesión de base de datos.
8. SQLAlchemy ejecuta `SELECT` sobre la tabla `productos` (clase `Producto` en `models/`).
9. El esquema `ProductoRead` convierte cada fila en JSON, por ejemplo `{"id":1,"nombre":"Agua 500 ml","precio":"0.75","stock":100}`.
10. De vuelta en el navegador, `pedirJson()` convierte el JSON en un arreglo de `Producto`.
11. `catalogo.ts` crea una tarjeta por producto con `componentes/tarjeta-producto.ts` y reemplaza el "Cargando...".

**Decisiones de diseño a recordar:**
- **`textContent` en lugar de `innerHTML`** al pintar datos de la API. Así, un producto con HTML malicioso en el nombre se muestra como texto y no se ejecuta.
- **Una responsabilidad por carpeta:** `tipos/` (datos), `servicios/` (red), `componentes/` y `paginas/` (pantalla), `estilos/` (CSS). Cada archivo cambia por una sola razón.
- **Una dependencia por capa:** las pantallas usan componentes y servicios; los servicios usan `cliente-api.ts`; nadie más habla con `fetch`.
- **Sin valores fijos:** la URL de la API vive en `.env.*` y solo `config/entorno.ts` la lee. Cambiar de ambiente no toca el código.
- **Ambientes por modo de Vite:** `npm run dev` lee `.env.development`; `npm run build -- --mode staging` lee `.env.staging`. Se comprobó que cada build incrusta su propia URL.
- **CORS configurable:** solo los orígenes de `cors_origins` pueden leer la API desde un navegador. Para otro ambiente se define `CORS_ORIGINS` en el `.env` de Python, sin editar código.
- **Las variables `VITE_*` son públicas:** quedan dentro del JavaScript que descarga el navegador. Nunca van contraseñas ahí.
- **Pruebas sin Supabase:** los tests usan SQLite en memoria, así que se pueden correr sin conexión ni credenciales.

---

## 5. Cómo ejecutarlo

Se necesitan **dos terminales**:

```powershell
# Terminal 1: API
cd python
.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload          # http://127.0.0.1:8000/docs

# Terminal 2: interfaz
cd frontend
npm install                            # solo la primera vez
npm run dev                            # http://localhost:5173
```

Pruebas del backend: `cd python` y luego `pytest`.

**Para otro ambiente (staging o producción):**
1. Frontend: copia `frontend/.env.example` como `.env.staging` (o `.env.production`) y pon la URL de la API de ese ambiente. Compila con `npm run build -- --mode staging`.
2. Backend: en `python/.env` define `CORS_ORIGINS=["https://direccion-del-frontend"]`.

---

## 6. Observaciones y pendientes

- **Datos duplicados:** la tabla `productos` tiene dos filas "Jugo" (ids 4 y 5), probablemente de pruebas anteriores.
- **`POST /productos` es público:** cualquiera puede crear productos. Conviene protegerlo con el token de Supabase.
- **`Categoria` sin migración:** existe el modelo, pero Alembic no tiene una migración que cree la tabla.
- **Faltan tests** de `/mis-pedidos` y de autenticación.

## 7. Próximos pasos del frontend

1. Formulario para crear productos, con validación.
2. Login con Supabase y rutas protegidas. Aquí hará falta un enrutador sencillo para cambiar de pantalla; por ahora `main.ts` monta una sola.
3. Pedidos del usuario (`/mis-pedidos`).
4. Cuando se necesite la clave de Supabase en el frontend, añadir `VITE_SUPABASE_URL` y `VITE_SUPABASE_PUBLISHABLE_KEY` (solo la clave *publishable*, nunca una secreta).
