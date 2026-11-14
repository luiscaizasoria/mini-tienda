// Componente: formulario para crear un producto.

// Estilos compartidos por todos los formularios
import '../estilos/componentes/formulario.css'
// Servicio que envía el producto a la API
import { crearProducto } from '../servicios/productos.ts'
// Tipo que describe los datos de un producto nuevo
import type { NuevoProducto } from '../tipos/producto.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'
// Reglas de validación
import { validarProducto } from '../validaciones/producto.ts'
// Campo de formulario con su etiqueta
import { crearCampo } from './campo-formulario.ts'

// Crea el formulario. "alCrear" se ejecuta cuando el producto ya se guardó.
export function crearFormularioProducto(
  alCrear: () => void,
): HTMLFormElement {
  // Elemento <form> que agrupa los campos
  const formulario = crearElemento('form', 'formulario')
  // Desactiva la validación del navegador: usamos la nuestra
  formulario.noValidate = true

  // Título del formulario
  const titulo = crearElemento('h2', '', 'Nuevo producto')

  // Campos del formulario
  const campoNombre = crearCampo('Nombre', 'nombre', {
    type: 'text',
    required: 'true',
  })
  const campoPrecio = crearCampo('Precio ($)', 'precio', {
    type: 'text',
    inputmode: 'decimal',
    placeholder: '2.50',
  })
  const campoStock = crearCampo('Stock', 'stock', {
    type: 'number',
    min: '0',
    step: '1',
    value: '0',
  })

  // Zona donde se muestran los errores
  const mensaje = crearElemento('p', 'formulario__mensaje')
  // role="alert" hace que los lectores de pantalla lo anuncien
  mensaje.setAttribute('role', 'alert')

  // Botón que envía el formulario
  const boton = crearElemento('button', '', 'Guardar producto')
  // type="submit" lo conecta con el evento submit del formulario
  boton.type = 'submit'

  // Mete todas las piezas dentro del formulario
  formulario.append(
    titulo,
    campoNombre,
    campoPrecio,
    campoStock,
    mensaje,
    boton,
  )

  // Muestra un mensaje de error en rojo
  const mostrarError = (texto: string): void => {
    mensaje.className = 'formulario__mensaje formulario__mensaje--error'
    mensaje.textContent = texto
  }

  // Se ejecuta al enviar el formulario (botón o tecla Enter)
  formulario.addEventListener('submit', async (evento) => {
    // Evita que el navegador recargue la página
    evento.preventDefault()

    // Lee los valores escritos en los campos
    const valores = new FormData(formulario)
    // Arma el producto; cambia la coma por punto ("2,50" -> "2.50")
    const datos: NuevoProducto = {
      nombre: String(valores.get('nombre')).trim(),
      precio: String(valores.get('precio')).trim().replace(',', '.'),
      stock: Number(valores.get('stock')),
    }

    // Revisa las reglas antes de molestar a la API
    const errores = validarProducto(datos)
    // Si hay errores, los muestra y no envía nada
    if (errores.length > 0) {
      mostrarError(errores.join(' '))
      return
    }

    // Bloquea el botón para evitar envíos dobles mientras se espera
    boton.disabled = true
    // Limpia el mensaje anterior
    mensaje.textContent = ''

    // Intenta guardar el producto
    try {
      // Envía el producto a la API y espera su respuesta
      await crearProducto(datos)
      // Vacía el formulario para poder crear otro
      formulario.reset()
      // Avisa a la pantalla para que actualice la lista
      alCrear()
    } catch (error) {
      // Si falla (API apagada, datos rechazados...) lo informa y lo registra
      mostrarError('No se pudo guardar el producto.')
      console.error(error)
    } finally {
      // Pase lo que pase, vuelve a habilitar el botón
      boton.disabled = false
    }
  })

  // Devuelve el formulario terminado
  return formulario
}
