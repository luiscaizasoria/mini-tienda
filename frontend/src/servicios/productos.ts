// Operaciones de la API relacionadas con productos.

// Tipos que describen un producto y los datos para crearlo
import type { NuevoProducto, Producto } from '../tipos/producto.ts'
// Funciones base que hacen la petición HTTP
import { enviarJson, pedirJson } from './cliente-api.ts'

// Pide a la API la lista de todos los productos
export function obtenerProductos(): Promise<Producto[]> {
  // GET /productos
  return pedirJson<Producto[]>('/productos')
}

// Crea un producto nuevo y devuelve el producto guardado (ya con su id)
export function crearProducto(datos: NuevoProducto): Promise<Producto> {
  // POST /productos
  return enviarJson<Producto>('/productos', datos)
}
