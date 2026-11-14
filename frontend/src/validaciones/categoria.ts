// Reglas para validar una categoría antes de enviarla a la API.
// Reflejan las de CategoriaCreate en python/app/schemas/categoria.py.

// Tipo de los datos a validar
import type { NuevaCategoria } from '../tipos/categoria.ts'

// Revisa una categoría y devuelve la lista de problemas (vacía si está bien)
export function validarCategoria(datos: NuevaCategoria): string[] {
  // Aquí se acumulan los mensajes de error
  const errores: string[] = []

  // El nombre debe tener entre 2 y 100 caracteres
  if (datos.nombre.length < 2 || datos.nombre.length > 100) {
    errores.push('El nombre debe tener entre 2 y 100 caracteres.')
  }

  // Devuelve todos los problemas encontrados
  return errores
}
