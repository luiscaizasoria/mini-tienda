// Componente: título de una pantalla con una línea de ayuda.

// Estilos propios de este componente
import '../estilos/componentes/encabezado-pagina.css'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Crea el encabezado: un título y un texto que explica qué se puede probar
export function crearEncabezadoPagina(
  titulo: string,
  ayuda: string,
): HTMLElement {
  // Contenedor del encabezado
  const encabezado = crearElemento('header', 'encabezado-pagina')
  // Mete el título y la ayuda
  encabezado.append(
    crearElemento('h1', '', titulo),
    crearElemento('p', '', ayuda),
  )
  // Devuelve el encabezado terminado
  return encabezado
}
