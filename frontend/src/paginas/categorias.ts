// Pantalla: categorías. Lista las categorías y permite crear nuevas.

// Estilos compartidos por las pantallas
import '../estilos/paginas/pagina.css'
// Título de pantalla con ayuda
import { crearEncabezadoPagina } from '../componentes/encabezado-pagina.ts'
// Componente del formulario de creación
import { crearFormularioCategoria } from '../componentes/formulario-categoria.ts'
// Tabla genérica
import { crearTabla } from '../componentes/tabla-datos.ts'
// Servicio que pide las categorías a la API
import { obtenerCategorias } from '../servicios/categorias.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Construye la pantalla completa y la devuelve lista para insertar en la página
export function crearPaginaCategorias(): HTMLElement {
  // Contenedor principal de la pantalla
  const pagina = crearElemento('section', 'pagina')
  // Contenedor donde irá la tabla
  const lista = crearElemento('div')

  // Formulario: al guardar una categoría, vuelve a cargar la tabla
  const formulario = crearFormularioCategoria(() => {
    void cargarCategorias(lista)
  })

  // Arma la pantalla: encabezado, formulario y tabla
  pagina.append(
    crearEncabezadoPagina(
      'Categorías',
      'Llama a GET /categorias para listar y a POST /categorias para crear.',
    ),
    formulario,
    lista,
  )

  // Carga las categorías sin bloquear
  void cargarCategorias(lista)

  // Devuelve la pantalla terminada
  return pagina
}

// Pide las categorías y las dibuja en una tabla dentro del contenedor
async function cargarCategorias(lista: HTMLElement): Promise<void> {
  // Mensaje mientras se espera la respuesta de la API
  lista.textContent = 'Cargando categorías...'

  // Intenta obtener las categorías
  try {
    // Espera la lista de categorías
    const categorias = await obtenerCategorias()

    // Si no hay ninguna, lo informa y termina
    if (categorias.length === 0) {
      lista.textContent = 'Todavía no hay categorías.'
      return
    }

    // Reemplaza el mensaje por la tabla
    lista.replaceChildren(
      crearTabla(
        [
          { titulo: 'ID', valor: (c) => String(c.id) },
          { titulo: 'Nombre', valor: (c) => c.nombre },
        ],
        categorias,
      ),
    )
  } catch (error) {
    // Si algo falla (API apagada, CORS...) lo muestra y lo registra
    lista.textContent = 'No se pudieron cargar las categorías.'
    console.error(error)
  }
}
