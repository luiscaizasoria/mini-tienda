// Pantalla: productos. Lista el catálogo y permite crear productos nuevos.

// Estilos de esta pantalla
import '../estilos/paginas/productos.css'
// Estilos compartidos por las pantallas
import '../estilos/paginas/pagina.css'
// Título de pantalla con ayuda
import { crearEncabezadoPagina } from '../componentes/encabezado-pagina.ts'
// Componente del formulario de creación
import { crearFormularioProducto } from '../componentes/formulario-producto.ts'
// Componente que dibuja un producto
import { crearTarjetaProducto } from '../componentes/tarjeta-producto.ts'
// Servicio que pide los productos a la API
import { obtenerProductos } from '../servicios/productos.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Construye la pantalla completa y la devuelve lista para insertar en la página
export function crearPaginaProductos(): HTMLElement {
  // Contenedor principal de la pantalla
  const pagina = crearElemento('section', 'pagina')
  // Cuadrícula donde irán las tarjetas
  const lista = crearElemento('div', 'pagina-productos__lista')

  // Formulario: al guardar un producto, vuelve a cargar la lista
  const formulario = crearFormularioProducto(() => {
    void cargarProductos(lista)
  })

  // Arma la pantalla: encabezado, formulario y lista
  pagina.append(
    crearEncabezadoPagina(
      'Productos',
      'Llama a GET /productos para listar y a POST /productos para crear.',
    ),
    formulario,
    lista,
  )

  // Carga los productos sin bloquear: la pantalla se muestra de inmediato
  void cargarProductos(lista)

  // Devuelve la pantalla terminada
  return pagina
}

// Pide los productos y los dibuja dentro de la lista recibida
async function cargarProductos(lista: HTMLElement): Promise<void> {
  // Mensaje mientras se espera la respuesta de la API
  lista.textContent = 'Cargando productos...'

  // Intenta obtener los productos
  try {
    // Espera la lista de productos
    const productos = await obtenerProductos()

    // Si la tienda no tiene productos, lo informa y termina
    if (productos.length === 0) {
      lista.textContent = 'Todavía no hay productos.'
      return
    }

    // Borra el mensaje "Cargando..."
    lista.replaceChildren()
    // Crea una tarjeta por producto y las añade a la lista
    lista.append(...productos.map(crearTarjetaProducto))
  } catch (error) {
    // Si algo falla (API apagada, CORS...) lo muestra y lo registra
    lista.textContent = 'No se pudo cargar el catálogo.'
    console.error(error)
  }
}
