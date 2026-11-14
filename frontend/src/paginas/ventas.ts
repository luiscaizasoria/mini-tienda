// Pantalla: ventas. Tabla de solo lectura con resumen y paginación.

// Estilos de esta pantalla
import '../estilos/paginas/ventas.css'
// Estilos compartidos por las pantallas
import '../estilos/paginas/pagina.css'
// Título de pantalla con ayuda
import { crearEncabezadoPagina } from '../componentes/encabezado-pagina.ts'
// Botones Anterior / Siguiente
import { crearPaginador } from '../componentes/paginador.ts'
// Tabla genérica
import { crearTabla } from '../componentes/tabla-datos.ts'
// Servicios que piden las ventas y su resumen a la API
import { obtenerResumenVentas, obtenerVentas } from '../servicios/ventas.ts'
// Ayuda para crear elementos HTML
import { crearElemento } from '../utilidades/dom.ts'

// Cuántas ventas se muestran por página
const VENTAS_POR_PAGINA = 20

// Construye la pantalla completa y la devuelve lista para insertar en la página
export function crearPaginaVentas(): HTMLElement {
  // Contenedor principal de la pantalla
  const pagina = crearElemento('section', 'pagina')
  // Texto con el resumen de ventas e ingresos
  const resumen = crearElemento('p', 'pagina-ventas__resumen')
  // Contenedor donde irá la tabla
  const tabla = crearElemento('div')
  // Paginador: al pulsar un botón carga la página pedida
  const paginador = crearPaginador((desplazamiento) => {
    void cargarPagina(desplazamiento)
  })

  // Pide una página de ventas y actualiza tabla y paginador
  async function cargarPagina(desplazamiento: number): Promise<void> {
    // Mensaje mientras se espera la respuesta de la API
    tabla.textContent = 'Cargando ventas...'

    // Intenta obtener la página pedida
    try {
      // Espera la página de ventas
      const datos = await obtenerVentas(VENTAS_POR_PAGINA, desplazamiento)

      // Reemplaza el mensaje por la tabla
      tabla.replaceChildren(
        crearTabla(
          [
            { titulo: 'ID', valor: (v) => String(v.id) },
            {
              titulo: 'Fecha',
              valor: (v) => new Date(v.fecha).toLocaleString('es-EC'),
            },
            { titulo: 'Cliente', valor: (v) => String(v.cliente_id) },
            { titulo: 'Producto', valor: (v) => v.producto },
            { titulo: 'Cantidad', valor: (v) => String(v.cantidad) },
            { titulo: 'Precio', valor: (v) => `$${v.precio_unitario}` },
          ],
          datos.items,
        ),
      )
      // Actualiza el texto "1–20 de 100.000" y los botones
      paginador.actualizar(desplazamiento, VENTAS_POR_PAGINA, datos.total)
    } catch (error) {
      // Si algo falla (API apagada, CORS...) lo muestra y lo registra
      tabla.textContent = 'No se pudieron cargar las ventas.'
      console.error(error)
    }
  }

  // Pide el resumen (se calcula una sola vez, en la base de datos)
  async function cargarResumen(): Promise<void> {
    // Mensaje mientras se espera la respuesta de la API
    resumen.textContent = 'Calculando resumen...'

    // Intenta obtener el resumen
    try {
      // Espera los totales
      const datos = await obtenerResumenVentas()
      // Formatea los números con separador de miles
      const cantidad = datos.cantidad_ventas.toLocaleString('es-EC')
      const ingresos = Number(datos.ingresos).toLocaleString('es-EC', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      })
      // Muestra el resumen
      resumen.textContent = `${cantidad} ventas · Ingresos totales: $${ingresos}`
    } catch (error) {
      // Si algo falla lo muestra y lo registra
      resumen.textContent = 'No se pudo calcular el resumen.'
      console.error(error)
    }
  }

  // Arma la pantalla: encabezado, resumen, tabla y paginador
  pagina.append(
    crearEncabezadoPagina(
      'Ventas',
      'Solo lectura. Llama a GET /ventas (paginado) y GET /ventas/resumen.',
    ),
    resumen,
    tabla,
    paginador.elemento,
  )

  // Carga el resumen y la primera página sin bloquear
  void cargarResumen()
  void cargarPagina(0)

  // Devuelve la pantalla terminada
  return pagina
}
