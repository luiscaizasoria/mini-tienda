// Componente: tarjeta que muestra un producto.

// Estilos propios de este componente
import '../estilos/componentes/tarjeta-producto.css'
// Tipo que describe un producto
import type { Producto } from '../tipos/producto.ts'

// Crea la tarjeta HTML de un solo producto
export function crearTarjetaProducto(producto: Producto): HTMLElement {
  // Crea un elemento <article> vacío
  const tarjeta = document.createElement('article')
  // Le asigna la clase CSS "tarjeta-producto"
  tarjeta.className = 'tarjeta-producto'

  // Crea el título con el nombre
  const nombre = document.createElement('h2')
  // textContent inserta texto plano: evita que se ejecute HTML malicioso
  nombre.textContent = producto.nombre

  // Crea el párrafo del precio
  const precio = document.createElement('p')
  // Muestra el precio con el símbolo de dólar
  precio.textContent = `$${producto.precio}`

  // Crea el párrafo del stock
  const stock = document.createElement('p')
  // Si no quedan unidades lo avisa, si no muestra cuántas hay
  stock.textContent =
    producto.stock > 0 ? `Disponibles: ${producto.stock}` : 'Agotado'

  // Mete nombre, precio y stock dentro de la tarjeta
  tarjeta.append(nombre, precio, stock)
  // Devuelve la tarjeta terminada
  return tarjeta
}
