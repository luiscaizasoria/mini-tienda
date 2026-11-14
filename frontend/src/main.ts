// Arranque de la aplicación: arma el diseño general y activa el enrutador.

// Valores de diseño (colores, espacios) y estilos globales
import './estilos/variables.css'
import './estilos/base.css'
// Menú de navegación
import { crearMenuNavegacion } from './componentes/menu-navegacion.ts'
// Enrutador que cambia de pantalla según la dirección
import { iniciarEnrutador } from './router/enrutador.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from './utilidades/dom.ts'

// Busca en la página el contenedor con id "app" (definido en index.html)
const app = document.querySelector<HTMLDivElement>('#app')

// Si no existe, detiene la ejecución con un mensaje claro
if (app === null) {
  throw new Error('No se encontró el elemento #app en index.html')
}

// Cabecera fija en todas las pantallas
const cabecera = crearElemento('header', 'cabecera')
// Nombre de la tienda: al pulsarlo se vuelve al inicio
const marca = crearElemento('a', 'cabecera__marca', 'Mini tienda')
// Dirección del inicio
marca.href = '#/'
// Mete la marca y el menú en la cabecera
cabecera.append(marca, crearMenuNavegacion())

// Zona central donde el enrutador dibuja cada pantalla
const contenido = crearElemento('main')

// Arma el diseño general: cabecera arriba, contenido debajo
app.replaceChildren(cabecera, contenido)

// Activa el enrutador: muestra la pantalla que corresponde a la dirección
iniciarEnrutador(contenido)
