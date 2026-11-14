// Tabla que relaciona cada ruta con la función que construye su pantalla.

// Pantallas de la aplicación
import { crearPaginaCategorias } from '../paginas/categorias.ts'
import { crearPaginaInicio } from '../paginas/inicio.ts'
import { crearPaginaProductos } from '../paginas/productos.ts'
import { crearPaginaRequiereLogin } from '../paginas/requiere-login.ts'
import { crearPaginaVentas } from '../paginas/ventas.ts'

// Cada ruta apunta a una función que crea y devuelve la pantalla
export const rutas: Record<string, () => HTMLElement> = {
  '/': crearPaginaInicio,
  '/productos': crearPaginaProductos,
  '/categorias': crearPaginaCategorias,
  '/ventas': crearPaginaVentas,
  // Usuarios y pedidos comparten la pantalla de "requiere login"
  '/usuarios': () => crearPaginaRequiereLogin('/usuarios'),
  '/pedidos': () => crearPaginaRequiereLogin('/pedidos'),
}
