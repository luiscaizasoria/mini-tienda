// Operaciones de la API relacionadas con ventas (solo lectura).

// Tipos que describen la página de ventas y el resumen
import type { PaginaVentas, ResumenVentas } from '../tipos/venta.ts'
// Función base que hace la petición HTTP
import { pedirJson } from './cliente-api.ts'

// Pide una página de ventas: cuántas traer y cuántas saltar
export function obtenerVentas(
  limite: number,
  desplazamiento: number,
): Promise<PaginaVentas> {
  // GET /ventas?limite=..&desplazamiento=..
  return pedirJson<PaginaVentas>(
    `/ventas?limite=${limite}&desplazamiento=${desplazamiento}`,
  )
}

// Pide el resumen calculado por la base de datos
export function obtenerResumenVentas(): Promise<ResumenVentas> {
  // GET /ventas/resumen
  return pedirJson<ResumenVentas>('/ventas/resumen')
}
