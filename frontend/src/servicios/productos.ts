// Operaciones de la API relacionadas con productos.

// Tipo que describe un producto
import type { Producto } from '../tipos/producto.ts'
// Función base que hace la petición HTTP
import { pedirJson } from './cliente-api.ts'

// Pide a la API la lista de todos los productos
export function obtenerProductos(): Promise<Producto[]> {
  // GET /productos
  return pedirJson<Producto[]>('/productos')
}
