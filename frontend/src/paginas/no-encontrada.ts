// Pantalla: la dirección no corresponde a ninguna pantalla.

// Estilos compartidos por las pantallas
import '../estilos/paginas/pagina.css'
// Título de pantalla con ayuda
import { crearEncabezadoPagina } from '../componentes/encabezado-pagina.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Construye la pantalla de "no encontrada"
export function crearPaginaNoEncontrada(): HTMLElement {
  // Contenedor principal de la pantalla
  const pagina = crearElemento('section', 'pagina')
  // Enlace para volver al inicio
  const volver = crearElemento('a', '', 'Volver al inicio')
  // Dirección del enlace
  volver.href = '#/'
  // Arma la pantalla
  pagina.append(
    crearEncabezadoPagina('Página no encontrada', 'Esa dirección no existe.'),
    volver,
  )
  // Devuelve la pantalla terminada
  return pagina
}
