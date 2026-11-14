# Mini tienda: frontend (TypeScript + Vite)

Interfaz en TypeScript puro, sin frameworks. Corre en el navegador y consume
la API de [../python](../python/README.md).

## Estructura

```
frontend/
├── index.html               Página única; carga src/main.ts
├── .env.development         Variables del ambiente de desarrollo
├── .env.example             Plantilla para crear otros ambientes
└── src/
    ├── main.ts              Arranque: solo conecta piezas
    ├── config/              Configuración (lee las variables de entorno)
    ├── paginas/             Pantallas completas
    ├── componentes/         Piezas reutilizables (tarjeta, botón, formulario)
    ├── servicios/           Comunicación con la API
    ├── tipos/               Interfaces de TypeScript (forma de los datos)
    └── estilos/             Todo el CSS
        ├── variables.css    Colores, espacios, tamaños
        ├── base.css         Reglas globales
        ├── paginas/         Un .css por pantalla
        └── componentes/     Un .css por componente
```

## ¿Dónde pongo...?

| Quiero añadir...                  | Va en...                                  |
|-----------------------------------|-------------------------------------------|
| Una pantalla nueva                | `paginas/nombre.ts` + `estilos/paginas/nombre.css` |
| Una pieza que se repite           | `componentes/nombre.ts` + `estilos/componentes/nombre.css` |
| Una llamada nueva a la API        | `servicios/recurso.ts`                    |
| La forma de un dato de la API     | `tipos/recurso.ts`                        |
| Un color o espacio                | `estilos/variables.css`                   |
| Una variable de configuración     | `.env.*` + `config/env.d.ts` + `config/entorno.ts` |

## Reglas

1. **Nombres de archivo en minúsculas con guiones**: `tarjeta-producto.ts`.
2. **Una dependencia por capa**: las pantallas usan componentes y servicios;
   los servicios usan `cliente-api.ts`; nadie más habla con `fetch`.
3. **Nada de valores fijos en el código**: direcciones y opciones salen de
   `config/entorno.ts`. Ese archivo es el único que lee `import.meta.env`.
4. **Colores y espacios**: se usan las variables de `variables.css`, nunca
   valores escritos a mano.
5. **Datos de la API en pantalla**: se insertan con `textContent`, nunca con
   `innerHTML`, para evitar inyección de HTML.
6. **Comentarios**: cada línea o bloque lleva su explicación en español.

## Ambientes (desarrollo, staging, producción)

Vite elige el archivo `.env` según el **modo**:

| Comando                              | Archivo que lee      |
|--------------------------------------|----------------------|
| `npm run dev`                        | `.env.development`   |
| `npm run build`                      | `.env.production`    |
| `npm run build -- --mode staging`    | `.env.staging`       |

Para un ambiente nuevo: copia `.env.example` con el nombre del modo y cambia
`VITE_API_URL`. Si falta una variable, la aplicación se detiene al arrancar
con un mensaje que lo explica.

Los archivos `*.local` (por ejemplo `.env.production.local`) son personales y
Git los ignora. **Todo lo que empieza con `VITE_` queda visible en el
navegador: nunca pongas contraseñas ni claves secretas.**

En el backend, la API debe autorizar la dirección del frontend publicado con
la variable `CORS_ORIGINS` (ver `python/.env.example`).

## Comandos

```powershell
npm install        # instala dependencias (primera vez)
npm run dev        # servidor de desarrollo en http://localhost:5173
npm run build      # revisa los tipos y genera la carpeta dist/
```
