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
| 8 | Formulario de productos | Crear productos desde la interfaz, con validación en el navegador y `POST` a la API. |
| 9 | Navegación y pantallas por tabla | Página de inicio, menú, enrutador y una pantalla de prueba por tabla; la API suma `/categorias` y `/ventas`. |

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
    │   ├── router/          Enrutador: qué pantalla se muestra según la dirección
    │   ├── paginas/         Pantallas
    │   ├── componentes/     Piezas reutilizables
    │   ├── servicios/       Llamadas a la API
    │   ├── tipos/           Forma de los datos
    │   ├── validaciones/    Reglas de validación de formularios
    │   ├── utilidades/      Ayudas pequeñas (crear elementos HTML)
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
| `api/routers/categorias.py` | Categorías: `GET /categorias` y `POST /categorias`. | **Nuevo (etapa 9).** |
| `api/routers/ventas.py` | Ventas en solo lectura: `GET /ventas?limite=&desplazamiento=` (paginado, límite 1–100) y `GET /ventas/resumen` (conteo e ingresos calculados por la base). | **Nuevo (etapa 9).** |
| `schemas/categoria.py`, `schemas/venta.py` | Validación y forma de salida de categorías y ventas (`PaginaVentas`, `ResumenVentas`). | **Nuevos (etapa 9).** |
| `__init__.py` (varios) | Marcar las carpetas como paquetes de Python. | Antes vacíos, ahora con una línea de descripción. |

### 3.3 Backend: resto de `python/`

| Archivo o carpeta | Objetivo | Qué se hizo |
|---|---|---|
| `migrations/env.py` y `versions/*.py` | Alembic: crear y versionar las tablas. | Reescritos con PEP 8 y comentarios. Los identificadores de revisión **no cambiaron**, así que la cadena sigue intacta. |
| `tests/` | Probar la API con SQLite en memoria, sin tocar Supabase. | Reescritos. En la etapa 9 se añadieron `test_categorias.py` y `test_ventas.py`, y `conftest.py` ganó las fixtures `motor` y `sesion_bd` para preparar datos. **11 tests pasan.** |
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
| `src/main.ts` | Arranque. | Arma el diseño general (cabecera con marca y menú, y una zona central) y activa el enrutador. Sin lógica propia. |
| `src/router/enlaces.ts` | **Única fuente de las pantallas.** | Lista de `{ruta, titulo, descripcion, requiereLogin}`. El menú y la página de inicio leen de aquí. |
| `src/router/rutas.ts` | Relacionar cada ruta con la función que construye su pantalla. | Una tabla `ruta -> función`. |
| `src/router/enrutador.ts` | Cambiar de pantalla sin recargar la página. | Escucha el evento `hashchange` (la parte `#/...` de la dirección) y dibuja la pantalla; si la ruta no existe muestra "no encontrada". Usa `#` para funcionar en cualquier hosting estático sin configurar el servidor. |
| `src/router/ruta-actual.ts` | Leer la ruta de la dirección. | `"#/productos"` pasa a `"/productos"`. |
| `src/utilidades/dom.ts` | Crear elementos HTML sin repetir código. | `crearElemento(etiqueta, clase, texto)`; el texto se inserta como texto plano. |
| `src/config/env.d.ts` | Decirle a TypeScript qué variables de entorno existen. | Declara `VITE_API_URL`. |
| `src/config/entorno.ts` | **Única puerta a la configuración.** | Lee `VITE_API_URL`, falla con un mensaje claro si falta y exporta `entorno.apiUrl`. |
| `src/tipos/producto.ts` | Describir los datos de producto. | `Producto` (lo que devuelve la API) y `NuevoProducto` (lo que se envía para crear). El precio es `string` porque Pydantic usa texto para los `Decimal`. |
| `src/validaciones/producto.ts` | Reglas de validación del producto. | `validarProducto()` devuelve la lista de errores: nombre 2–150 caracteres, precio > 0 con hasta 2 decimales, stock entero ≥ 0. Refleja `ProductoCreate` del backend. Es una función pura, sin DOM. |
| `src/servicios/cliente-api.ts` | Cliente HTTP base. | `pedirJson<T>()` hace `fetch` y revisa errores HTTP; `enviarJson<T>()` hace `POST` con JSON. |
| `src/servicios/productos.ts` | Operaciones de productos. | `obtenerProductos()` (`GET /productos`) y `crearProducto()` (`POST /productos`). |
| `src/componentes/tarjeta-producto.ts` | Pieza reutilizable. | Crea la tarjeta de un producto. |
| `src/componentes/formulario-producto.ts` | Formulario de creación. | Lee los campos con `FormData`, cambia la coma por punto en el precio, valida, bloquea el botón mientras envía y avisa a la pantalla al terminar. |
| `src/paginas/inicio.ts` | **Página de inicio.** | Explica qué es el proyecto, cómo se conectan interfaz, API y base de datos, y ofrece una tarjeta de acceso a cada tabla. |
| `src/paginas/productos.ts` | Pantalla de productos (antes `catalogo.ts`). | Formulario y tarjetas; al guardar vuelve a cargar la lista. Muestra "Cargando...", lista vacía y error. |
| `src/paginas/categorias.ts` | Pantalla de categorías. | Formulario y tabla; llama a `GET` y `POST /categorias`. |
| `src/paginas/ventas.ts` | Pantalla de ventas. | Resumen, tabla de 20 filas y paginador; llama a `GET /ventas` y `GET /ventas/resumen`. |
| `src/paginas/requiere-login.ts` | Pantalla de `/usuarios` y `/pedidos`. | Aviso de que son datos privados que se activarán con el login. |
| `src/paginas/no-encontrada.ts` | Pantalla para rutas inexistentes. | Mensaje y enlace al inicio. |
| `src/componentes/menu-navegacion.ts` | Menú. | Un enlace por pantalla; marca la actual con `aria-current="page"`. |
| `src/componentes/encabezado-pagina.ts` | Título + línea de ayuda. | Lo usan todas las pantallas. |
| `src/componentes/tabla-datos.ts` | Tabla genérica. | `crearTabla<T>(columnas, filas)`: sirve para cualquier tipo de dato. |
| `src/componentes/paginador.ts` | Botones Anterior / Siguiente. | Muestra "1–20 de 100.000" y desactiva los extremos. |
| `src/componentes/campo-formulario.ts` | Campo con etiqueta. | Extraído de `formulario-producto.ts` para reutilizarlo. |
| `src/componentes/formulario-categoria.ts` | Formulario de categorías. | Con la misma estructura que el de productos. |
| `src/servicios/categorias.ts`, `servicios/ventas.ts` | Llamadas a la API. | `obtenerCategorias`, `crearCategoria`, `obtenerVentas`, `obtenerResumenVentas`. |
| `src/tipos/categoria.ts`, `tipos/venta.ts`, `validaciones/categoria.ts` | Tipos y reglas de las nuevas tablas. | Reflejan los esquemas de Python. |
| `src/estilos/variables.css` | Valores de diseño. | Colores, espacios, radios, sombra y ancho máximo. |
| `src/estilos/base.css` | Estilos globales. | Fuente, fondo y contenedor central. |
| `src/estilos/paginas/*.css` | CSS por pantalla. | `inicio`, `productos`, `ventas` y `pagina.css` (común a todas). |
| `src/estilos/componentes/tarjeta-producto.css` | CSS del componente. | Caja, nombre, precio y stock. |
| `src/estilos/componentes/formulario.css` | CSS de todos los formularios. | Antes `formulario-producto.css`; ahora lo comparten productos y categorías. |
| `src/estilos/componentes/*.css` (resto) | CSS por componente. | Menú, tabla, paginador y encabezado. |
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
│      └─ paginas/productos.ts   │ fetch  │      └─ SQLAlchemy ──────┼─────▶│ productos  │
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
2. `main.ts` importa los estilos globales y arma la cabecera y activa el enrutador (`router/enrutador.ts`), que según la dirección `#/...` elige la pantalla; en `#/productos` es `crearPaginaProductos()`.
3. Al cargarse, `config/entorno.ts` lee `VITE_API_URL` del archivo `.env` del modo actual (en desarrollo, `.env.development`).
4. `paginas/productos.ts` muestra "Cargando productos..." y llama a `obtenerProductos()`.
5. `servicios/productos.ts` delega en `pedirJson()` de `cliente-api.ts`, que hace `fetch` a `<VITE_API_URL>/productos`.
6. El navegador nota que la página (puerto 5173) y la API (puerto 8000) son **orígenes distintos**. Por eso la API responde con la cabecera CORS `Access-Control-Allow-Origin: http://localhost:5173`. Sin ella, el navegador bloquearía la respuesta.
7. En la API, `routers/productos.py` recibe la petición. `dependencies.get_db` le entrega una sesión de base de datos.
8. SQLAlchemy ejecuta `SELECT` sobre la tabla `productos` (clase `Producto` en `models/`).
9. El esquema `ProductoRead` convierte cada fila en JSON, por ejemplo `{"id":1,"nombre":"Agua 500 ml","precio":"0.75","stock":100}`.
10. De vuelta en el navegador, `pedirJson()` convierte el JSON en un arreglo de `Producto`.
11. `productos.ts` crea una tarjeta por producto con `componentes/tarjeta-producto.ts` y reemplaza el "Cargando...".

**El recorrido al navegar entre pantallas (etapa 9):**

1. `main.ts` dibuja la cabecera (marca + menú) y una zona central vacía, y llama a `iniciarEnrutador()`.
2. El enrutador lee la dirección con `rutaActual()` (`#/ventas` pasa a `/ventas`), busca esa ruta en `rutas.ts` y dibuja la pantalla en la zona central.
3. Al pulsar un enlace del menú cambia solo el `#...` de la dirección: el navegador **no recarga la página** y dispara el evento `hashchange`.
4. El enrutador responde a ese evento cambiando la pantalla; el menú responde al mismo evento moviendo la marca de "activo".
5. Para añadir una pantalla nueva solo se toca `router/enlaces.ts` (menú e inicio la muestran solos) y `router/rutas.ts`.

**El recorrido de la pantalla de ventas (etapa 9):** al abrirla pide `GET /ventas/resumen` (la base cuenta y suma las 100.000 filas y viaja una sola línea) y `GET /ventas?limite=20&desplazamiento=0` (viajan 20 filas, no 100.000). Cada clic en Siguiente o Anterior pide otra página con otro `desplazamiento`.

**El recorrido al crear un producto (etapa 8):**

1. El usuario escribe nombre, precio y stock, y pulsa "Guardar producto" (o Enter).
2. `formulario-producto.ts` captura el evento `submit` y llama a `preventDefault()` para que el navegador no recargue la página.
3. Lee los campos con `FormData` y arma un `NuevoProducto` (cambia `2,50` por `2.50`).
4. `validaciones/producto.ts` revisa las reglas. Si hay errores, se muestran en rojo y **no se envía nada**.
5. Si todo está bien, se bloquea el botón y `servicios/productos.ts` hace `POST /productos` mediante `enviarJson()`.
6. Antes del `POST`, el navegador envía una petición previa (`OPTIONS`, el *preflight* de CORS) porque el contenido es JSON. La API responde que `POST` y `Content-Type` están permitidos.
7. En la API, `ProductoCreate` valida de nuevo (la validación del navegador no es una defensa, solo una comodidad), `routers/productos.py` guarda la fila y responde 201 con el producto.
8. El formulario se vacía, avisa a `paginas/productos.ts` y esta recarga la lista, donde aparece el producto nuevo.

**Decisiones de diseño a recordar:**
- **Validar en dos lugares:** el navegador da avisos rápidos; la API es la que realmente protege los datos.
- **Precio como texto:** se envía `"2.50"` y no el número `2.5`, para no perder decimales por redondeo de punto flotante.
- **`noValidate` en el formulario:** se desactiva la validación del navegador para que los mensajes sean todos en español y con el mismo estilo.
- **`textContent` en lugar de `innerHTML`** al pintar datos de la API. Así, un producto con HTML malicioso en el nombre se muestra como texto y no se ejecuta.
- **Una responsabilidad por carpeta:** `tipos/` (datos), `servicios/` (red), `componentes/` y `paginas/` (pantalla), `estilos/` (CSS). Cada archivo cambia por una sola razón.
- **Una dependencia por capa:** las pantallas usan componentes y servicios; los servicios usan `cliente-api.ts`; nadie más habla con `fetch`.
- **Sin valores fijos:** la URL de la API vive en `.env.*` y solo `config/entorno.ts` la lee. Cambiar de ambiente no toca el código.
- **Ambientes por modo de Vite:** `npm run dev` lee `.env.development`; `npm run build -- --mode staging` lee `.env.staging`. Se comprobó que cada build incrusta su propia URL.
- **CORS configurable:** solo los orígenes de `cors_origins` pueden leer la API desde un navegador. Para otro ambiente se define `CORS_ORIGINS` en el `.env` de Python, sin editar código.
- **`usuarios` no se expone:** contiene correos de personas. Las pantallas de usuarios y pedidos avisan que requieren login, y la API no tiene ninguna ruta pública que devuelva usuarios.
- **Ventas paginadas con tope de 100:** pedir 100.000 filas de una vez sería lento e innecesario; la API rechaza `limite` mayor que 100 con 422. El desplazamiento (`offset`) es simple pero se vuelve lento en páginas muy profundas; la alternativa es la paginación por llave que ya se practicó en `demos/base_de_datos/paginas_generador.py`.
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

- **Datos de prueba:** la tabla `productos` tiene dos filas "Jugo" (ids 4 y 5) y un "Arroz" creado desde el formulario.
- **`POST /categorias` también es público**, igual que `POST /productos`.
- **`POST /productos` es público:** cualquiera puede crear productos, y ahora el formulario lo usa tal cual. Conviene protegerlo con el token de Supabase cuando llegue el login; entonces el formulario solo debería mostrarse a usuarios con sesión.
- **`Categoria` sin migración:** la tabla existe en Supabase y ahora tiene API, pero Alembic no tiene una migración que la cree. En una base nueva no se crearía con `alembic upgrade head`.
- **Faltan tests** de `/mis-pedidos` y de autenticación. En el frontend no hay pruebas automáticas; solo se ha comprobado con capturas de un navegador real.

## 7. Próximos pasos del frontend

1. ~~Formulario para crear productos, con validación.~~ Hecho en la etapa 8.
2. Login con Supabase y rutas protegidas. El enrutador ya existe; falta que `rutas.ts` decida según la sesión y activar las pantallas de usuarios y pedidos.
3. Pedidos del usuario (`/mis-pedidos`).
4. Cuando se necesite la clave de Supabase en el frontend, añadir `VITE_SUPABASE_URL` y `VITE_SUPABASE_PUBLISHABLE_KEY` (solo la clave *publishable*, nunca una secreta).
