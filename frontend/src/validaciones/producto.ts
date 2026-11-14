// Reglas para validar un producto antes de enviarlo a la API.
// Reflejan las de ProductoCreate en python/app/schemas/producto.py.
// La API vuelve a validar: esto solo evita viajes inútiles y da avisos rápidos.

// Tipo de los datos a validar
import type { NuevoProducto } from '../tipos/producto.ts'

// Precio válido: hasta 8 enteros y 2 decimales (máximo 10 dígitos en total)
const FORMATO_PRECIO = /^\d{1,8}(\.\d{1,2})?$/

// Revisa un producto y devuelve la lista de problemas (vacía si todo está bien)
export function validarProducto(datos: NuevoProducto): string[] {
  // Aquí se acumulan los mensajes de error
  const errores: string[] = []

  // El nombre debe tener entre 2 y 150 caracteres
  if (datos.nombre.length < 2 || datos.nombre.length > 150) {
    errores.push('El nombre debe tener entre 2 y 150 caracteres.')
  }

  // El precio debe tener formato numérico con máximo 2 decimales
  if (!FORMATO_PRECIO.test(datos.precio)) {
    errores.push('El precio debe ser un número con hasta 2 decimales.')
  } else if (Number(datos.precio) <= 0) {
    // Y además debe ser mayor que cero
    errores.push('El precio debe ser mayor que 0.')
  }

  // El stock debe ser un número entero de 0 en adelante
  if (!Number.isInteger(datos.stock) || datos.stock < 0) {
    errores.push('El stock debe ser un número entero de 0 o más.')
  }

  // Devuelve todos los problemas encontrados
  return errores
}
