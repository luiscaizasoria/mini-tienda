// Componente: tabla genérica que sirve para cualquier tipo de dato.

// Estilos propios de este componente
import '../estilos/componentes/tabla-datos.css'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Describe una columna: su título y cómo obtener el texto de cada fila.
// <T> es el tipo de las filas (Venta, Categoria...).
export interface Columna<T> {
  // Texto del encabezado de la columna
  titulo: string
  // Función que, dada una fila, devuelve el texto de esta columna
  valor: (fila: T) => string
}

// Crea una tabla con las columnas y filas indicadas
export function crearTabla<T>(
  columnas: Columna<T>[],
  filas: T[],
): HTMLElement {
  // Contenedor con barra de desplazamiento si la tabla es muy ancha
  const contenedor = crearElemento('div', 'tabla-datos')
  // La tabla en sí
  const tabla = crearElemento('table')

  // Encabezado: una fila con el título de cada columna
  const encabezado = crearElemento('thead')
  // Fila del encabezado
  const filaEncabezado = crearElemento('tr')
  // Una celda de encabezado por columna
  for (const columna of columnas) {
    filaEncabezado.append(crearElemento('th', '', columna.titulo))
  }
  // Mete la fila en el encabezado
  encabezado.append(filaEncabezado)

  // Cuerpo: una fila por dato
  const cuerpo = crearElemento('tbody')
  // Recorre cada dato
  for (const fila of filas) {
    // Fila de la tabla
    const tr = crearElemento('tr')
    // Una celda por columna; textContent evita ejecutar HTML malicioso
    for (const columna of columnas) {
      tr.append(crearElemento('td', '', columna.valor(fila)))
    }
    // Mete la fila en el cuerpo
    cuerpo.append(tr)
  }

  // Arma la tabla y la mete en el contenedor
  tabla.append(encabezado, cuerpo)
  contenedor.append(tabla)
  // Devuelve el contenedor terminado
  return contenedor
}
