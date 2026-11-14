// Pantalla: inicio. Explica qué hace el proyecto y cómo probarlo.

// Estilos de esta pantalla
import '../estilos/paginas/inicio.css'
// Estilos compartidos por las pantallas
import '../estilos/paginas/pagina.css'
// Título de pantalla con ayuda
import { crearEncabezadoPagina } from '../componentes/encabezado-pagina.ts'
// Lista de pantallas con sus descripciones
import { ENLACES } from '../router/enlaces.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Crea un elemento de lista con una parte en negrita y el resto en texto
function crearItem(negrita: string, texto: string): HTMLLIElement {
  // Elemento de la lista
  const item = crearElemento('li')
  // Primera parte en negrita, luego el texto normal
  item.append(crearElemento('strong', '', negrita), ` ${texto}`)
  // Devuelve el elemento terminado
  return item
}

// Bloque "¿Cómo funciona?": las tres piezas del proyecto
function crearBloqueFuncionamiento(): HTMLElement {
  // Sección con su título
  const bloque = crearElemento('section', 'inicio__bloque')
  bloque.append(crearElemento('h2', '', '¿Cómo funciona?'))
  // Lista numerada con las tres piezas
  const lista = crearElemento('ol')
  lista.append(
    crearItem(
      'Interfaz (esta página).',
      'Hecha con TypeScript y Vite. Corre en tu navegador, pide datos ' +
        'y los muestra.',
    ),
    crearItem(
      'API (Python, FastAPI).',
      'Recibe las peticiones de la interfaz, valida los datos y consulta ' +
        'la base de datos.',
    ),
    crearItem(
      'Base de datos (PostgreSQL en Supabase).',
      'Guarda las tablas: productos, categorías, ventas, usuarios y pedidos.',
    ),
  )
  // Mete la lista en el bloque
  bloque.append(lista)
  // Devuelve el bloque terminado
  return bloque
}

// Bloque "Tablas para probar": una tarjeta por pantalla con su enlace
function crearBloqueTablas(): HTMLElement {
  // Sección con su título
  const bloque = crearElemento('section', 'inicio__bloque')
  bloque.append(crearElemento('h2', '', 'Tablas para probar'))
  // Cuadrícula de tarjetas
  const cuadricula = crearElemento('div', 'inicio__tablas')

  // Una tarjeta por pantalla, sin contar el propio inicio
  for (const enlace of ENLACES.filter((e) => e.ruta !== '/')) {
    // La tarjeta completa es un enlace a la pantalla
    const tarjeta = crearElemento('a', 'inicio__tarjeta')
    // Dirección de la pantalla, por ejemplo "#/productos"
    tarjeta.href = `#${enlace.ruta}`
    // Nombre y descripción de la tabla
    tarjeta.append(
      crearElemento('h3', '', enlace.titulo),
      crearElemento('p', '', enlace.descripcion),
    )
    // Si necesita login, lo indica con una etiqueta
    if (enlace.requiereLogin) {
      tarjeta.append(crearElemento('span', 'inicio__etiqueta', 'Requiere login'))
    }
    // Añade la tarjeta a la cuadrícula
    cuadricula.append(tarjeta)
  }

  // Mete la cuadrícula en el bloque
  bloque.append(cuadricula)
  // Devuelve el bloque terminado
  return bloque
}

// Bloque "Qué probar": sugerencias para cada pantalla
function crearBloqueGuia(): HTMLElement {
  // Sección con su título
  const bloque = crearElemento('section', 'inicio__bloque')
  bloque.append(crearElemento('h2', '', 'Qué probar'))
  // Lista con una sugerencia por pantalla
  const lista = crearElemento('ul')
  lista.append(
    crearItem(
      'Productos y Categorías:',
      'crea un registro con el formulario y mira cómo aparece en la lista.',
    ),
    crearItem(
      'Ventas:',
      'recorre las 100.000 ventas con los botones Anterior y Siguiente.',
    ),
    crearItem(
      'Usuarios y Pedidos:',
      'estarán disponibles cuando exista el login.',
    ),
  )
  // Mete la lista en el bloque
  bloque.append(lista)
  // Devuelve el bloque terminado
  return bloque
}

// Construye la pantalla de inicio completa
export function crearPaginaInicio(): HTMLElement {
  // Contenedor principal de la pantalla
  const pagina = crearElemento('section', 'pagina')
  // Arma la pantalla con su encabezado y los tres bloques
  pagina.append(
    crearEncabezadoPagina(
      'Mini tienda',
      'Proyecto de aprendizaje: una tienda pequeña con una API en Python ' +
        'y una interfaz en TypeScript. Sirve para ver cómo se conectan las ' +
        'piezas de una aplicación completa y para probar cada tabla.',
    ),
    crearBloqueFuncionamiento(),
    crearBloqueTablas(),
    crearBloqueGuia(),
  )
  // Devuelve la pantalla terminada
  return pagina
}
