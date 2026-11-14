// Componente: formulario para crear una categoría.

// Estilos compartidos por todos los formularios
import '../estilos/componentes/formulario.css'
// Servicio que envía la categoría a la API
import { crearCategoria } from '../servicios/categorias.ts'
// Tipo que describe los datos de una categoría nueva
import type { NuevaCategoria } from '../tipos/categoria.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'
// Reglas de validación
import { validarCategoria } from '../validaciones/categoria.ts'
// Campo de formulario con su etiqueta
import { crearCampo } from './campo-formulario.ts'

// Crea el formulario. "alCrear" se ejecuta cuando la categoría ya se guardó.
export function crearFormularioCategoria(
  alCrear: () => void,
): HTMLFormElement {
  // Elemento <form> que agrupa los campos
  const formulario = crearElemento('form', 'formulario')
  // Desactiva la validación del navegador: usamos la nuestra
  formulario.noValidate = true

  // Título del formulario
  const titulo = crearElemento('h2', '', 'Nueva categoría')
  // Único campo: el nombre
  const campoNombre = crearCampo('Nombre', 'nombre', { type: 'text' })
  // Zona donde se muestran los errores
  const mensaje = crearElemento('p', 'formulario__mensaje')
  // role="alert" hace que los lectores de pantalla lo anuncien
  mensaje.setAttribute('role', 'alert')
  // Botón que envía el formulario
  const boton = crearElemento('button', '', 'Guardar categoría')
  // type="submit" lo conecta con el evento submit del formulario
  boton.type = 'submit'

  // Mete todas las piezas dentro del formulario
  formulario.append(titulo, campoNombre, mensaje, boton)

  // Muestra un mensaje de error en rojo
  const mostrarError = (texto: string): void => {
    mensaje.className = 'formulario__mensaje formulario__mensaje--error'
    mensaje.textContent = texto
  }

  // Se ejecuta al enviar el formulario (botón o tecla Enter)
  formulario.addEventListener('submit', async (evento) => {
    // Evita que el navegador recargue la página
    evento.preventDefault()

    // Arma la categoría con el nombre escrito
    const datos: NuevaCategoria = {
      nombre: String(new FormData(formulario).get('nombre')).trim(),
    }

    // Revisa las reglas antes de molestar a la API
    const errores = validarCategoria(datos)
    // Si hay errores, los muestra y no envía nada
    if (errores.length > 0) {
      mostrarError(errores.join(' '))
      return
    }

    // Bloquea el botón para evitar envíos dobles mientras se espera
    boton.disabled = true
    // Limpia el mensaje anterior
    mensaje.textContent = ''

    // Intenta guardar la categoría
    try {
      // Envía la categoría a la API y espera su respuesta
      await crearCategoria(datos)
      // Vacía el formulario para poder crear otra
      formulario.reset()
      // Avisa a la pantalla para que actualice la lista
      alCrear()
    } catch (error) {
      // Si falla (API apagada, datos rechazados...) lo informa y lo registra
      mostrarError('No se pudo guardar la categoría.')
      console.error(error)
    } finally {
      // Pase lo que pase, vuelve a habilitar el botón
      boton.disabled = false
    }
  })

  // Devuelve el formulario terminado
  return formulario
}
