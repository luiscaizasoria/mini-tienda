// Componente: botones Anterior / Siguiente para recorrer páginas de datos.

// Estilos propios de este componente
import '../estilos/componentes/paginador.css'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Lo que devuelve crearPaginador: el elemento y una función para actualizarlo
export interface Paginador {
  // Elemento HTML que se inserta en la pantalla
  elemento: HTMLElement
  // Actualiza el texto y activa o desactiva los botones
  actualizar: (desplazamiento: number, limite: number, total: number) => void
}

// Crea el paginador. "alCambiar" recibe el nuevo desplazamiento al pulsar.
export function crearPaginador(
  alCambiar: (desplazamiento: number) => void,
): Paginador {
  // Contenedor de los controles
  const elemento = crearElemento('div', 'paginador')
  // Botón para ir a la página anterior
  const anterior = crearElemento('button', '', '← Anterior')
  // Texto con el rango visible
  const texto = crearElemento('span')
  // Botón para ir a la página siguiente
  const siguiente = crearElemento('button', '', 'Siguiente →')
  // Mete las tres piezas en el contenedor
  elemento.append(anterior, texto, siguiente)

  // Posición actual, guardada para calcular el siguiente salto
  let desplazamientoActual = 0
  // Tamaño de página actual
  let limiteActual = 1

  // Al pulsar "Anterior", retrocede una página sin bajar de 0
  anterior.addEventListener('click', () => {
    alCambiar(Math.max(0, desplazamientoActual - limiteActual))
  })
  // Al pulsar "Siguiente", avanza una página
  siguiente.addEventListener('click', () => {
    alCambiar(desplazamientoActual + limiteActual)
  })

  // Función que la pantalla llama cada vez que llegan datos nuevos
  const actualizar = (
    desplazamiento: number,
    limite: number,
    total: number,
  ): void => {
    // Guarda la posición para los próximos clics
    desplazamientoActual = desplazamiento
    limiteActual = limite
    // Último elemento visible, sin pasar del total
    const hasta = Math.min(desplazamiento + limite, total)
    // Muestra, por ejemplo, "1–20 de 100.000"
    texto.textContent = `${total === 0 ? 0 : desplazamiento + 1}–${hasta} de ${total.toLocaleString('es-EC')}`
    // No se puede retroceder desde la primera página
    anterior.disabled = desplazamiento === 0
    // No se puede avanzar desde la última página
    siguiente.disabled = hasta >= total
  }

  // Devuelve el elemento y la función de actualización
  return { elemento, actualizar }
}
