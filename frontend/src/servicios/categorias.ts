// Operaciones de la API relacionadas con categorías.

// Tipos que describen una categoría y los datos para crearla
import type { Categoria, NuevaCategoria } from '../tipos/categoria.ts'
// Funciones base que hacen la petición HTTP
import { enviarJson, pedirJson } from './cliente-api.ts'

// Pide a la API la lista de todas las categorías
export function obtenerCategorias(): Promise<Categoria[]> {
  // GET /categorias
  return pedirJson<Categoria[]>('/categorias')
}

// Crea una categoría nueva y devuelve la categoría guardada (con su id)
export function crearCategoria(datos: NuevaCategoria): Promise<Categoria> {
  // POST /categorias
  return enviarJson<Categoria>('/categorias', datos)
}
