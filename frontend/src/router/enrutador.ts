// Enrutador: muestra la pantalla que corresponde a la dirección (#/ruta).
// Usa el "#" de la dirección, así funciona en cualquier hosting estático
// sin configurar el servidor.

// Pantalla que se muestra si la ruta no existe
import { crearPaginaNoEncontrada } from '../paginas/no-encontrada.ts'
// Tabla de rutas y sus pantallas
import { rutas } from './rutas.ts'
// Ruta que está activa en este momento
import { rutaActual } from './ruta-actual.ts'

// Arranca el enrutador dentro del contenedor indicado
export function iniciarEnrutador(contenedor: HTMLElement): void {
  // Dibuja la pantalla que corresponde a la dirección actual
  const mostrar = (): void => {
    // Busca la función de esa ruta; si no existe, usa la de "no encontrada"
    const crearPagina = rutas[rutaActual()] ?? crearPaginaNoEncontrada
    // Reemplaza el contenido anterior por la pantalla nueva
    contenedor.replaceChildren(crearPagina())
    // Lleva la vista al inicio al cambiar de pantalla
    window.scrollTo(0, 0)
  }

  // Cada vez que cambia el "#" de la dirección, se cambia de pantalla
  window.addEventListener('hashchange', mostrar)
  // Muestra la pantalla inicial al cargar la página
  mostrar()
}
