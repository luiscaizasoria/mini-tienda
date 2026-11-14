// Componente: menú de navegación con un enlace por pantalla.

// Estilos propios de este componente
import '../estilos/componentes/menu-navegacion.css'
// Lista de pantallas (única fuente de títulos y descripciones)
import { ENLACES } from '../router/enlaces.ts'
// Ruta que está activa en este momento
import { rutaActual } from '../router/ruta-actual.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Crea el menú y lo mantiene sincronizado con la dirección de la página
export function crearMenuNavegacion(): HTMLElement {
  // Elemento <nav>: lo identifica como navegación para lectores de pantalla
  const menu = crearElemento('nav', 'menu-navegacion')
  // Lista de enlaces
  const lista = crearElemento('ul')

  // Guarda cada enlace junto con su ruta para marcar el activo
  const enlaces: { ruta: string; elemento: HTMLAnchorElement }[] = []

  // Crea un enlace por pantalla
  for (const enlace of ENLACES) {
    // Elemento de la lista
    const item = crearElemento('li')
    // El "#" hace que la navegación no recargue la página
    const a = crearElemento('a', '', enlace.titulo)
    // Dirección del enlace, por ejemplo "#/productos"
    a.href = `#${enlace.ruta}`
    // Mete el enlace en su elemento y este en la lista
    item.append(a)
    lista.append(item)
    // Recuerda el enlace para poder marcarlo después
    enlaces.push({ ruta: enlace.ruta, elemento: a })
  }

  // Marca como activo el enlace que corresponde a la ruta actual
  const marcarActivo = (): void => {
    // Ruta que se está mostrando
    const actual = rutaActual()
    // Revisa cada enlace
    for (const { ruta, elemento } of enlaces) {
      // aria-current="page" informa a lectores de pantalla y da estilo
      if (ruta === actual) {
        elemento.setAttribute('aria-current', 'page')
      } else {
        elemento.removeAttribute('aria-current')
      }
    }
  }

  // Se actualiza cada vez que cambia la dirección (#/...)
  window.addEventListener('hashchange', marcarActivo)
  // Y una vez al crear el menú
  marcarActivo()

  // Mete la lista en el menú y lo devuelve
  menu.append(lista)
  return menu
}
