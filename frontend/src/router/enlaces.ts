// Lista de pantallas de la aplicación. Es la ÚNICA fuente de títulos y
// descripciones: el menú y la página de inicio leen de aquí.
// Para añadir una pantalla: agrégala aquí y en rutas.ts.

// Datos de una pantalla que aparece en el menú
export interface Enlace {
  // Dirección dentro de la aplicación, por ejemplo "/productos"
  ruta: string
  // Texto del menú
  titulo: string
  // Qué se puede probar en esa pantalla
  descripcion: string
  // true si la pantalla necesita iniciar sesión (todavía no disponible)
  requiereLogin: boolean
}

// Pantallas en el orden en que aparecen en el menú
export const ENLACES: Enlace[] = [
  {
    ruta: '/',
    titulo: 'Inicio',
    descripcion: 'Explica qué hace el proyecto y cómo se conectan sus partes.',
    requiereLogin: false,
  },
  {
    ruta: '/productos',
    titulo: 'Productos',
    descripcion:
      'Catálogo de la tienda. Lista los productos y permite crear nuevos.',
    requiereLogin: false,
  },
  {
    ruta: '/categorias',
    titulo: 'Categorías',
    descripcion:
      'Clasificación de productos. Lista las categorías y permite crear nuevas.',
    requiereLogin: false,
  },
  {
    ruta: '/ventas',
    titulo: 'Ventas',
    descripcion:
      'Historial de 100.000 ventas. Solo lectura, con resumen y paginación.',
    requiereLogin: false,
  },
  {
    ruta: '/usuarios',
    titulo: 'Usuarios',
    descripcion: 'Personas registradas en la tienda. Son datos privados.',
    requiereLogin: true,
  },
  {
    ruta: '/pedidos',
    titulo: 'Pedidos',
    descripcion: 'Pedidos de cada usuario. Cada persona solo ve los suyos.',
    requiereLogin: true,
  },
]

// Busca los datos de una pantalla por su ruta; falla si no existe
export function buscarEnlace(ruta: string): Enlace {
  // Busca el primer enlace con esa ruta
  const enlace = ENLACES.find((e) => e.ruta === ruta)
  // Si no existe, es un error de programación: se detiene con un aviso claro
  if (enlace === undefined) {
    throw new Error(`No hay ninguna pantalla registrada para ${ruta}`)
  }
  // Devuelve el enlace encontrado
  return enlace
}
