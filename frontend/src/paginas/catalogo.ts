// Pantalla: catálogo de productos.

// Estilos propios de esta pantalla
import '../estilos/paginas/catalogo.css'
// Componente que dibuja un producto
import { crearTarjetaProducto } from '../componentes/tarjeta-producto.ts'
// Servicio que pide los productos a la API
import { obtenerProductos } from '../servicios/productos.ts'

// Construye la pantalla completa y la devuelve lista para insertar en la página
export function crearPaginaCatalogo(): HTMLElement {
  // Contenedor principal de la pantalla
  const pagina = document.createElement('section')
  // Clase CSS de la pantalla
  pagina.className = 'pagina-catalogo'

  // Título de la pantalla
  const titulo = document.createElement('h1')
  // Texto del título
  titulo.textContent = 'Mini tienda'

  // Cuadrícula donde irán las tarjetas
  const lista = document.createElement('div')
  // Clase CSS de la cuadrícula
  lista.className = 'pagina-catalogo__lista'

  // Mete el título y la lista dentro de la pantalla
  pagina.append(titulo, lista)

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
