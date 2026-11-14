// Pantalla: tablas con datos privados que necesitan iniciar sesión.

// Estilos compartidos por las pantallas
import '../estilos/paginas/pagina.css'
// Título de pantalla con ayuda
import { crearEncabezadoPagina } from '../componentes/encabezado-pagina.ts'
// Datos de la pantalla (título y descripción)
import { buscarEnlace } from '../router/enlaces.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Construye la pantalla para la ruta indicada (/usuarios o /pedidos)
export function crearPaginaRequiereLogin(ruta: string): HTMLElement {
  // Título y descripción de esta tabla
  const enlace = buscarEnlace(ruta)
  // Contenedor principal de la pantalla
  const pagina = crearElemento('section', 'pagina')
  // Caja con la explicación
  const aviso = crearElemento('div', 'aviso')
  // Texto del aviso
  aviso.append(
    crearElemento('strong', '', 'Requiere iniciar sesión. '),
    crearElemento(
      'span',
      '',
      'Esta tabla contiene datos privados de cada persona, por eso la API ' +
        'no los muestra sin identificarse. Se activará cuando agreguemos ' +
        'el login con Supabase.',
    ),
  )
  // Arma la pantalla
  pagina.append(
    crearEncabezadoPagina(enlace.titulo, enlace.descripcion),
    aviso,
  )
  // Devuelve la pantalla terminada
  return pagina
}
