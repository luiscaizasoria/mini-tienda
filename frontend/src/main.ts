// Arranque de la aplicación: solo conecta las piezas, no contiene lógica.

// Valores de diseño (colores, espacios) y estilos globales
import './estilos/variables.css'
import './estilos/base.css'
// Pantalla que se muestra al entrar
import { crearPaginaCatalogo } from './paginas/catalogo.ts'

// Busca en la página el contenedor con id "app" (definido en index.html)
const app = document.querySelector<HTMLDivElement>('#app')

// Si no existe, detiene la ejecución con un mensaje claro
if (app === null) {
  throw new Error('No se encontró el elemento #app en index.html')
}

// Muestra la pantalla del catálogo dentro del contenedor
app.replaceChildren(crearPaginaCatalogo())
